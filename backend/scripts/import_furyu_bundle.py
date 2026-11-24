#!/usr/bin/env python3
"""Offline FuRyu JSONL/media importer. Default: read-only database preview."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import io
import json
import os
from pathlib import Path
import re
import tempfile
import unicodedata
import zipfile
from app.core.paths import import_bundle_path

TABLES = ('figures', 'figure_variants', 'release_prices', 'source_documents', 'product_images')
IMAGE_NAME = re.compile(r'^[0-9a-f]{64}\.(?:jpg|jpeg|png|webp|gif|avif)$')


def norm(value):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', value or '')).casefold()


def parse_time(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00')) if value else datetime.now(timezone.utc)


def read_rows(raw):
    return [json.loads(line) for line in raw.decode('utf-8-sig').splitlines() if line.strip()]


def load_bundle(root):
    """Read extracted parts, original ZIPs, or the nested DB ZIP; never extract archive paths."""
    datasets = []
    images = {}
    errors = []
    duplicate_images = 0

    def register(name, read, origin):
        nonlocal duplicate_images
        basename = name.rsplit('/', 1)[-1]
        if not IMAGE_NAME.fullmatch(basename):
            return
        try:
            payload = read()
            digest = hashlib.sha256(payload).hexdigest()
            if digest != basename.split('.')[0]:
                errors.append({'file': origin, 'error': 'IMAGE_HASH_MISMATCH'})
                return
            if basename in images:
                duplicate_images += 1
            else:
                images[basename] = (origin, read)
        except Exception as exc:
            errors.append({'file': origin, 'error': str(exc)})

    archives = []  # Keep archive handles alive for lazy image reads.

    def scan_zip(z, label):
        archives.append(z)
        names = {i.filename.rsplit('/', 1)[-1]: i for i in z.infolist() if not i.is_dir()}
        if all(t + '.jsonl' in names for t in TABLES):
            datasets.append({t: read_rows(z.read(names[t + '.jsonl'])) for t in TABLES})
        for item in z.infolist():
            if item.is_dir():
                continue
            if item.filename.lower().endswith('.zip'):
                scan_zip(zipfile.ZipFile(io.BytesIO(z.read(item))), label + ':' + item.filename)
            else:
                register(item.filename, lambda z=z, item=item: z.read(item), label + ':' + item.filename)

    for p in sorted(root.rglob('*')):
        if p.is_symlink() or not p.is_file():
            continue
        if p.suffix.lower() == '.zip':
            scan_zip(zipfile.ZipFile(p), str(p))
        elif IMAGE_NAME.fullmatch(p.name):
            register(p.name, p.read_bytes, str(p))
        elif p.name == 'figures.jsonl' and all((p.parent / (t + '.jsonl')).is_file() for t in TABLES):
            datasets.append({t: read_rows((p.parent / (t + '.jsonl')).read_bytes()) for t in TABLES})
    if not datasets:
        raise ValueError('DB JSONL not found: include part1/DB_原本 or DB_원본/furyu_historical_db_increment.zip')
    fingerprints = {hashlib.sha256(json.dumps(d, sort_keys=True, ensure_ascii=False).encode()).hexdigest() for d in datasets}
    if len(fingerprints) != 1:
        raise ValueError('Multiple different DB bundles found; keep only one authoritative DB version')
    return datasets[0], images, errors, duplicate_images, archives


def validate(data, images, errors, duplicates):
    urls = [r['official_url'] for r in data['figures']]
    keys = [(r['figure_official_url'], r['variant_key']) for r in data['figure_variants']]
    if len(set(urls)) != len(urls) or len(set(keys)) != len(keys):
        errors.append({'error': 'DUPLICATE_PRODUCT_OR_VARIANT_KEY'})
    urlset, keyset = set(urls), set(keys)
    for r in data['figures']:
        if r.get('manufacturer_name') != 'FuRyu' or not r.get('name_original') or not r['official_url'].startswith(('http://', 'https://')):
            errors.append({'url': r.get('official_url'), 'error': 'INVALID_FURYU_PRODUCT'})
        parse_time(r.get('collected_at'))
    for r in data['figure_variants']:
        if r['figure_official_url'] not in urlset:
            errors.append({'error': 'ORPHAN_VARIANT', 'row': r})
    for t in TABLES[2:]:
        for r in data[t]:
            if (r['figure_official_url'], r['variant_key']) not in keyset:
                errors.append({'error': 'ORPHAN_CHILD', 'table': t})
            parse_time(r.get('checked_at') or r.get('collected_at'))
    for r in data['release_prices']:
        amount = Decimal(str(r['price_amount']))
        if not amount.is_finite() or amount < 0 or len(r['currency']) != 3:
            errors.append({'error': 'INVALID_PRICE', 'row': r})
    expected = set()
    for r in data['product_images']:
        name = r['image_url'].rsplit('/', 1)[-1]
        if r['image_url'] != '/api/media/' + name or not IMAGE_NAME.fullmatch(name):
            errors.append({'error': 'INVALID_IMAGE_PATH', 'path': r['image_url']})
        expected.add(name)
    return {
        'rows': {t: len(data[t]) for t in TABLES},
        'quality': dict(Counter(r.get('quality') for r in data['figures'])),
        'image_files_found': len(images), 'image_files_expected': len(expected),
        'image_files_missing': len(expected - images.keys()),
        'missing_image_names': sorted(expected - images.keys()),
        'duplicate_image_files': duplicates, 'errors': errors,
    }


def import_db(data, images, media_dir, commit, report):
    from app.services.import_pipeline import commit_import
    from sqlalchemy import select, text
    from app.core.database import SessionLocal
    from app.models.entities import Manufacturer, ProductLine, Figure, FigureVariant, ReleasePrice, SourceDocument, ProductImage

    counts = Counter()
    reviews = []
    planned_copy = set()
    touched = {}
    virtual = -1
    with SessionLocal() as db:
        db.autoflush = False
        if db.get_bind().dialect.name == 'postgresql':
            if commit:
                locked = db.scalar(text('SELECT pg_try_advisory_xact_lock(1163219511)'))
                if not locked:
                    raise RuntimeError('Another FuRyu import is already running')
                # Coordinate with all ordinary writers too; timeout instead of waiting indefinitely.
                db.execute(text("SET LOCAL lock_timeout = '10s'"))
                db.execute(text('LOCK TABLE manufacturers, product_lines, figures, figure_variants, release_prices, source_documents, product_images IN SHARE ROW EXCLUSIVE MODE'))
            else:
                db.execute(text('SET TRANSACTION READ ONLY'))

        def add(obj):
            nonlocal virtual
            if commit:
                db.add(obj)
                db.flush()
            else:
                obj.id = virtual
                virtual -= 1
            return obj

        maker = db.scalar(select(Manufacturer).where(Manufacturer.name == 'FuRyu'))
        if maker is None:
            raise ValueError('Existing manufacturer FuRyu not found; no manufacturer was created')
        all_figures = list(db.scalars(select(Figure)))
        all_variants = list(db.scalars(select(FigureVariant)))
        by_url = {f.official_url: f for f in all_figures}
        by_id = {f.id: f for f in all_figures}
        names, codes = defaultdict(set), defaultdict(set)
        for f in all_figures:
            if f.manufacturer_id == maker.id:
                names[norm(f.name_original)].add(f.id)
        variants = {(v.figure_id, v.variant_key): v for v in all_variants}
        per_figure = defaultdict(list)
        for v in all_variants:
            per_figure[v.figure_id].append(v)
            if v.figure_id in by_id and by_id[v.figure_id].manufacturer_id == maker.id:
                for field in ('sku', 'jan_code'):
                    if getattr(v, field):
                        codes[(field, norm(getattr(v, field)))].add(v.figure_id)
        lines = {p.name: p for p in db.scalars(select(ProductLine).where(ProductLine.manufacturer_id == maker.id))}
        prices = {(p.variant_id, p.source_url, p.price_kind): p for p in db.scalars(select(ReleasePrice).join(FigureVariant).join(Figure).where(Figure.manufacturer_id == maker.id))}
        docs = {(p.variant_id, p.url): p for p in db.scalars(select(SourceDocument).join(FigureVariant).join(Figure).where(Figure.manufacturer_id == maker.id))}
        image_keys = {(p.variant_id, p.image_url) for p in db.scalars(select(ProductImage).join(FigureVariant).join(Figure).where(Figure.manufacturer_id == maker.id))}
        grouped = {t: defaultdict(list) for t in TABLES[1:]}
        for t in TABLES[1:]:
            for r in data[t]:
                grouped[t][r['figure_official_url']].append(r)

        def review(url, reason, **extra):
            reviews.append(dict(url=url, reason=reason, **extra))
            counts['review'] += 1

        for row in data['figures']:
            url = row['official_url']
            fig = by_url.get(url)
            incoming_variants = grouped['figure_variants'][url]
            if fig is not None and fig.manufacturer_id != maker.id:
                review(url, 'URL_BELONGS_TO_OTHER_MANUFACTURER')
                continue
            if fig is None:
                candidates = set(names.get(norm(row['name_original']), set()))
                for vrow in incoming_variants:
                    for field in ('sku', 'jan_code'):
                        if vrow.get(field):
                            candidates.update(codes.get((field, norm(vrow[field])), set()))
                if candidates:
                    review(url, 'OTHER_URL_NAME_SKU_OR_JAN_MATCH', candidate_ids=sorted(candidates))
                    continue
            # New variant keys on an existing product can duplicate existing purchase-linked variants.
            if fig is not None and per_figure[fig.id] and any((fig.id, r['variant_key']) not in variants for r in incoming_variants):
                review(url, 'VARIANT_KEY_DIFFERS_FROM_EXISTING', figure_id=fig.id)
                continue
            line_name = row.get('product_line_name')
            line = lines.get(line_name)
            if line_name and line is None:
                line = add(ProductLine(manufacturer_id=maker.id, name=line_name))
                lines[line_name] = line
                counts['product_lines_added'] += 1
            if fig is None:
                fields = {k: row.get(k) for k in ('name_original', 'name_ko', 'franchise', 'character', 'type', 'scale', 'height_mm', 'material', 'quality')}
                fig = add(Figure(manufacturer_id=maker.id, product_line_id=line.id if line else None, official_url=url, collected_at=parse_time(row.get('collected_at')), **fields))
                by_url[url] = fig
                names[norm(fig.name_original)].add(fig.id)
                counts['created'] += 1
            else:
                counts['existing'] += 1
                # Preserve all nonempty existing metadata, especially Korean names.
                for field in ('name_ko', 'franchise', 'character', 'scale', 'height_mm', 'material'):
                    if getattr(fig, field) in (None, '') and row.get(field) not in (None, ''):
                        if commit:
                            setattr(fig, field, row[field])
                        counts['metadata_fields_filled'] += 1
                if fig.product_line_id is None and line:
                    if commit:
                        fig.product_line_id = line.id
                    counts['metadata_fields_filled'] += 1
            mapped = {}
            for r in incoming_variants:
                key = (fig.id, r['variant_key'])
                variant = variants.get(key)
                if variant is None:
                    fields = {k: r.get(k) for k in ('variant_key', 'sku', 'jan_code', 'edition', 'reissue_no', 'release_date', 'release_precision')}
                    variant = add(FigureVariant(figure_id=fig.id, **fields))
                    variants[key] = variant
                    per_figure[fig.id].append(variant)
                    counts['variants_added'] += 1
                    for field in ('sku', 'jan_code'):
                        if r.get(field):
                            codes[(field, norm(r[field]))].add(fig.id)
                mapped[r['variant_key']] = variant.id
            for r in grouped['release_prices'][url]:
                vid = mapped[r['variant_key']]
                key = (vid, r['source_url'], r['price_kind'])
                if key in prices:
                    counts['prices_existing'] += 1
                    continue
                prices[key] = add(ReleasePrice(variant_id=vid, price_amount=Decimal(str(r['price_amount'])), currency=r['currency'], price_kind=r['price_kind'], tax_included=r.get('tax_included'), source_url=r['source_url'], checked_at=parse_time(r.get('checked_at'))))
                counts['prices_added'] += 1
            for r in grouped['source_documents'][url]:
                vid = mapped[r['variant_key']]
                key = (vid, r['url'])
                if key in docs:
                    counts['documents_existing'] += 1
                    continue
                body = r.get('body') or ''
                fields = dict(title=r.get('title') or row['name_original'], url=r['url'],
                              source_type=r.get('source_type') or 'historical_metadata',
                              language=r.get('language') or 'ja', body=body,
                              usage_status=r.get('usage_status') or 'factual_metadata_only',
                              content_hash=r.get('content_hash') or hashlib.sha256(body.encode()).hexdigest())
                docs[key] = add(SourceDocument(variant_id=vid, collected_at=parse_time(r.get('collected_at')), **fields))
                counts['documents_added'] += 1
            for r in grouped['product_images'][url]:
                vid = mapped[r['variant_key']]
                key = (vid, r['image_url'])
                name = r['image_url'].rsplit('/', 1)[-1]
                target = media_dir / name
                if name not in images:
                    if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != name.split('.')[0]:
                        counts['image_links_missing_file'] += 1
                        continue
                if name in images and not target.exists() and name not in planned_copy:
                    counts['image_files_to_copy'] += 1
                    planned_copy.add(name)
                if commit and name in images:
                    if target.is_symlink():
                        raise ValueError('Refusing symlink media target: ' + str(target))
                    if target.exists():
                        if hashlib.sha256(target.read_bytes()).hexdigest() != name.split('.')[0]:
                            raise ValueError('Existing media hash mismatch: ' + name)
                    else:
                        media_dir.mkdir(parents=True, exist_ok=True)
                        fd, temp = tempfile.mkstemp(prefix='.furyu-', dir=media_dir)
                        try:
                            with os.fdopen(fd, 'wb') as out:
                                out.write(images[name][1]())
                            os.chmod(temp, 0o644)
                            os.replace(temp, target)
                        finally:
                            if os.path.exists(temp):
                                os.unlink(temp)
                        counts['image_files_copied'] += 1
                if key in image_keys:
                    counts['images_existing'] += 1
                    continue
                fields = {k: r.get(k) for k in ('image_url', 'source_url', 'usage_status', 'license_evidence')}
                add(ProductImage(variant_id=vid, checked_at=parse_time(r.get('checked_at')), **fields))
                image_keys.add(key)
                counts['images_added'] += 1
            touched[fig.id] = fig
        # Reports are written outside the input tree. Prove writable BEFORE commit.
        report['summary'] = dict(selected=len(data['figures']), created=0, existing=0, review=0, failed=0, **{k: v for k, v in counts.items() if k not in ('created', 'existing', 'review')})
        report['summary'].update({k: counts[k] for k in ('created', 'existing', 'review')})
        report['reviews'] = reviews
        if commit:
            report['summary'].update(commit_import(db, touched.values()))
            report['db_committed'] = True
        else:
            db.rollback()
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=import_bundle_path('furyu'))
    parser.add_argument('--media-dir', type=Path, default=Path('/app/media'))
    parser.add_argument('--validate-only', action='store_true')
    parser.add_argument('--commit', action='store_true')
    parser.add_argument('--allow-missing-images', action='store_true', help='Import metadata; skip image links whose files are unavailable')
    parser.add_argument('--report', type=Path, help='Writable JSON report path outside input folder; defaults to a unique temp file')
    args = parser.parse_args()
    if args.validate_only and args.commit:
        parser.error('--validate-only cannot be combined with --commit')
    mode = 'VALIDATE' if args.validate_only else 'COMMIT' if args.commit else 'PREVIEW'
    path = args.report
    if path is None:
        fd, name = tempfile.mkstemp(prefix='furyu_import_', suffix='.json')
        os.close(fd)
        path = Path(name)
    report = {'mode': mode, 'db_committed': False}
    try:
        # Fail before touching the DB if the report cannot be written.
        path.write_text('{}', encoding='utf-8')
        data, images, errors, duplicates, archives = load_bundle(args.root)
        report['validation'] = validate(data, images, errors, duplicates)
        if errors:
            raise ValueError('Bundle validation failed; see report errors')
        if not args.validate_only:
            if args.commit and report['validation']['image_files_missing'] and not args.allow_missing_images:
                raise ValueError('Some DB-referenced image files are absent. Preview first; use --allow-missing-images only to skip unavailable image links')
            import_db(data, images, args.media_dir, args.commit, report)
            report['db_committed'] = args.commit
        report['mode'] = mode
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        summary = dict(report.get('summary', {}), mode=mode, db_committed=report['db_committed'], image_files_found=len(images), image_files_missing=report['validation']['image_files_missing'], report=str(path))
        print(json.dumps(summary, ensure_ascii=False), flush=True)
    except Exception as exc:
        report['error'] = type(exc).__name__ + ': ' + str(exc)
        try:
            path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        except Exception:
            pass
        print(json.dumps({'mode': mode, 'failed': 1, 'db_committed': report['db_committed'], 'error': report['error'], 'report': str(path)}, ensure_ascii=False), flush=True)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
