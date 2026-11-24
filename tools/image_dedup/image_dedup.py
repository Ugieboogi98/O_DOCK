"""Offline gallery deduplication. Audit first; reversible row status changes only."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import html
import io
import json
from pathlib import Path
import base64
import sys
from urllib.parse import unquote, urlsplit

from PIL import Image, ImageChops, ImageOps, ImageStat
from sqlalchemy import select

VISIBLE = ('authorized', 'personal_local')
HIDDEN = 'duplicate_hidden'
VERSION = 1


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    temporary.replace(path)


def local_path(url, media):
    parts = urlsplit(url)
    if parts.scheme or parts.netloc or not parts.path.startswith('/api/media/'):
        raise ValueError('REMOTE_OR_UNSUPPORTED_URL')
    root = Path(media).resolve()
    path = (root / unquote(parts.path[len('/api/media/'):])).resolve()
    if not path.is_relative_to(root) or path == root:
        raise ValueError('PATH_OUTSIDE_MEDIA')
    return path


def inspect_image(path):
    # Bound compressed and decoded sizes; unreadable/animated files are never deduplicated.
    if path.stat().st_size > 30_000_000:
        raise ValueError('FILE_TOO_LARGE')
    raw = path.read_bytes()
    with Image.open(io.BytesIO(raw)) as original:
        if getattr(original, 'n_frames', 1) != 1:
            raise ValueError('ANIMATED_IMAGE')
        if original.width * original.height > 40_000_000:
            raise ValueError('PIXELS_TOO_LARGE')
        rgba = ImageOps.exif_transpose(original).convert('RGBA')
        rgb = Image.new('RGB', rgba.size, 'white')
        rgb.paste(rgba, mask=rgba.getchannel('A'))
        # Preserve alpha in exact-pixel comparison; white composite is for similarity only.
        pixel_hash = hashlib.sha256(str(rgba.size).encode() + rgba.tobytes()).hexdigest()
        small = rgb.resize((96, 96), Image.Resampling.LANCZOS)
        gray = small.convert('L').resize((9, 8), Image.Resampling.LANCZOS).tobytes()
        bits = sum((gray[y*9+x] > gray[y*9+x+1]) << (y*8+x) for y in range(8) for x in range(8))
        thumb = rgb.copy(); thumb.thumbnail((220, 220))
        stream = io.BytesIO(); thumb.save(stream, 'JPEG', quality=75)
        return dict(sha256=hashlib.sha256(raw).hexdigest(), pixels=pixel_hash,
                    width=rgba.width, height=rgba.height, byte_size=len(raw), dhash=bits,
                    small=small, thumb='data:image/jpeg;base64,'+base64.b64encode(stream.getvalue()).decode())


def similar(a, b):
    if abs((a['width']/a['height'])/(b['width']/b['height']) - 1) > .01:
        return False, {}
    distance = (a['dhash'] ^ b['dhash']).bit_count()
    if distance > 3:
        return False, {}
    diff = ImageChops.difference(a['small'], b['small'])
    mae = sum(ImageStat.Stat(diff).mean) / 3
    # Block guard prevents small local details being diluted by a white background.
    worst = max(sum(ImageStat.Stat(diff.crop((x,y,x+12,y+12))).mean)/3
                for y in range(0,96,12) for x in range(0,96,12))
    return mae <= 3 and worst <= 12, dict(dhash_distance=distance, rgb_mae=round(mae,3), worst_block_mae=round(worst,3))


def snapshot(row):
    return {key: getattr(row, key) for key in ('id','variant_id','image_url','source_url','usage_status')}


def audit(db, media, output, figure_ids=None):
    from app.models.entities import ProductImage, FigureVariant, Figure
    query = (select(ProductImage, FigureVariant.figure_id, Figure.name_original)
             .join(FigureVariant, ProductImage.variant_id == FigureVariant.id)
             .join(Figure, Figure.id == FigureVariant.figure_id)
             .where(ProductImage.usage_status.in_(VISIBLE)).order_by(ProductImage.variant_id, ProductImage.id))
    if figure_ids:
        query = query.where(Figure.id.in_(figure_ids))
    groups = defaultdict(list)
    for row, fid, name in db.execute(query):
        groups[row.variant_id].append((row, fid, name))
    report = dict(version=VERSION, mode='AUDIT', generated_at=datetime.now(timezone.utc).isoformat(),
                  scope='same_variant_only', candidates=[], skipped=[], checked_images=0)
    cards = []
    for number, items in enumerate(groups.values(), 1):
        if len(items) < 2:
            continue
        decoded = []
        for row, fid, name in items:
            try:
                info = inspect_image(local_path(row.image_url, media))
                decoded.append((row, fid, name, info)); report['checked_images'] += 1
            except Exception as exc:
                report['skipped'].append(dict(image_id=row.id, reason=type(exc).__name__+':'+str(exc)[:100]))
        # Higher resolution wins within the same permission tier; never substitute an
        # authorized row with one allowed only for local personal use.
        decoded.sort(key=lambda item: (item[0].usage_status == 'authorized', item[3]['width']*item[3]['height'], item[3]['byte_size'], -item[0].id), reverse=True)
        keepers = []
        for row, fid, name, info in decoded:
            match = None
            for keeper, keep_info in keepers:
                reason = None; metrics = {}
                if info['sha256'] == keep_info['sha256']:
                    reason = 'exact_bytes'
                elif info['pixels'] == keep_info['pixels']:
                    reason = 'exact_pixels'
                else:
                    found, metrics = similar(info, keep_info)
                    if found: reason = 'similar'
                if reason:
                    if reason != 'similar':
                        match=(keeper, keep_info, reason, metrics); break
                    if match is None:
                        match=(keeper, keep_info, reason, metrics)
            if match is None:
                keepers.append((row, info)); continue
            keeper, keep_info, reason, metrics = match
            candidate=dict(figure_id=fid, name_original=name, variant_id=row.variant_id,
                           keep=snapshot(keeper), remove=snapshot(row), reason=reason, metrics=metrics,
                           keep_sha256=keep_info['sha256'], remove_sha256=info['sha256'],
                           keep_size=[keep_info['width'],keep_info['height']], remove_size=[info['width'],info['height']])
            report['candidates'].append(candidate)
            cards.append((candidate, keep_info['thumb'], info['thumb']))
            # A similarity candidate stays a keeper for clustering purposes: exact
            # copies of it must not be hidden behind a merely similar image by default.
            if reason == 'similar': keepers.append((row, info))
        if number % 100 == 0:
            print(json.dumps(dict(progress_variants=number, total_variants=len(groups))),flush=True)
    # Do not permit transitive chains with a keeper that is removed in the same plan.
    removed = {c['remove']['id'] for c in report['candidates'] if c['reason'] != 'similar'}
    report['candidates']=[c for c in report['candidates'] if c['keep']['id'] not in removed]
    allowed={c['remove']['id'] for c in report['candidates']}
    cards=[card for card in cards if card[0]['remove']['id'] in allowed]
    report['summary']=dict(Counter(c['reason'] for c in report['candidates']))
    write_json(output, report)
    e=lambda value:html.escape(str(value),quote=True)
    parts=['<!doctype html><meta charset="utf-8"><title>O_DOCK 중복 이미지 검사</title><style>body{font:16px sans-serif;background:#151515;color:#eee;max-width:1000px;margin:30px auto}article{padding:18px;border:1px solid #555;margin:16px 0}figure{display:inline-block;vertical-align:top}img{background:white;max-width:220px}code{color:#ffb36b}</style><h1>O_DOCK 중복 이미지 검사</h1><p>왼쪽은 유지, 오른쪽은 제외 후보입니다. similar는 추정이며 자동 삭제 확정이 아닙니다. 다른 버전 간 비교는 하지 않습니다.</p>']
    for c, left, right in cards:
        parts.append(f'<article><h2>상품 {c["figure_id"]}: {e(c["name_original"])}</h2><p><code>{e(c["reason"])} / 제외 ID {c["remove"]["id"]}</code> {e(c["metrics"])}</p><figure><img src="{left}"><figcaption>유지 {c["keep"]["id"]} / {e(c["keep_size"])}</figcaption></figure><figure><img src="{right}"><figcaption>제외 후보 {c["remove"]["id"]} / {e(c["remove_size"])}</figcaption></figure></article>')
    Path(output).with_suffix('.html').write_text(''.join(parts),encoding='utf-8')
    return dict(mode='AUDIT', db_changed=False, checked_images=report['checked_images'],
                candidates=report['summary'], skipped=len(report['skipped']), report=str(output))


def apply(db, media, report_path, journal_path, include_similar=False, image_ids=None):
    from app.models.entities import ProductImage
    report=json.loads(Path(report_path).read_text(encoding='utf-8'))
    if report.get('version') != VERSION or report.get('mode') != 'AUDIT': raise ValueError('NOT_A_SUPPORTED_AUDIT')
    if Path(journal_path).exists(): raise ValueError('JOURNAL_ALREADY_EXISTS')
    plan=[c for c in report['candidates'] if c['reason'] in ('exact_bytes','exact_pixels') or (include_similar and c['reason']=='similar')]
    if image_ids is not None:
        plan=[c for c in plan if c['remove']['id'] in image_ids]
    removed={c['remove']['id'] for c in plan}
    # Conservatively keep intermediate candidates when applying mixed plans.
    plan=[c for c in plan if c['keep']['id'] not in removed]
    changes=[]
    for c in plan:
        keep=db.get(ProductImage,c['keep']['id'],with_for_update=True)
        row=db.get(ProductImage,c['remove']['id'],with_for_update=True)
        if not keep or not row or snapshot(keep)!=c['keep'] or snapshot(row)!=c['remove']:
            raise ValueError('DATABASE_CHANGED_REAUDIT')
        if row.id==keep.id or row.variant_id!=keep.variant_id: raise ValueError('INVALID_PAIR')
        a=inspect_image(local_path(keep.image_url,media)); b=inspect_image(local_path(row.image_url,media))
        if a['sha256']!=c['keep_sha256'] or b['sha256']!=c['remove_sha256']: raise ValueError('IMAGE_CHANGED_REAUDIT')
        if c['reason']=='exact_bytes' and a['sha256']!=b['sha256']: raise ValueError('NOT_EXACT')
        if c['reason']=='exact_pixels' and a['pixels']!=b['pixels']: raise ValueError('NOT_EXACT_PIXELS')
        if c['reason']=='similar' and not similar(a,b)[0]: raise ValueError('NOT_SIMILAR')
        changes.append(snapshot(row))
    # Durable recovery journal BEFORE the single atomic database commit.
    journal=dict(version=VERSION,mode='APPLY_JOURNAL',state='prepared',changes=changes)
    write_json(journal_path,journal)
    for old in changes: db.get(ProductImage,old['id']).usage_status=HIDDEN
    db.commit()
    journal['state']='committed';write_json(journal_path,journal)
    return dict(mode='APPLY',hidden=len(changes),files_deleted=0,journal=str(journal_path))


def restore(db, journal_path):
    from app.models.entities import ProductImage
    journal=json.loads(Path(journal_path).read_text(encoding='utf-8'))
    if journal.get('mode')!='APPLY_JOURNAL' or journal.get('version')!=VERSION: raise ValueError('NOT_A_JOURNAL')
    restored=0
    for old in journal['changes']:
        row=db.get(ProductImage,old['id'],with_for_update=True)
        if not row or any(getattr(row,k)!=v for k,v in old.items() if k!='usage_status'):
            raise ValueError('DATABASE_CHANGED_RESTORE_STOPPED')
        if row.usage_status==old['usage_status']: continue
        if row.usage_status!=HIDDEN: raise ValueError('STATUS_CHANGED_RESTORE_STOPPED')
        row.usage_status=old['usage_status'];restored+=1
    db.commit()
    return dict(mode='RESTORE',restored=restored,files_deleted=0)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['audit','apply','restore'])
    parser.add_argument('--report',type=Path,required=True)
    parser.add_argument('--journal',type=Path)
    parser.add_argument('--figure-ids')
    parser.add_argument('--include-similar',action='store_true')
    parser.add_argument('--image-ids',help='Only apply these remove image IDs; similar also requires --include-similar')
    args=parser.parse_args()
    from app.core.database import SessionLocal
    from app.core.config import get_settings
    ids=lambda value: {int(s) for s in value.split(',')} if value else None
    with SessionLocal() as db:
        try:
            if args.mode=='audit': result=audit(db,get_settings().media_dir,args.report,ids(args.figure_ids))
            elif args.mode=='apply':
                if not args.journal: parser.error('apply requires --journal (new path)')
                result=apply(db,get_settings().media_dir,args.report,args.journal,args.include_similar,ids(args.image_ids))
            else: result=restore(db,args.report)
            print(json.dumps(result,ensure_ascii=False),flush=True)
        except Exception:
            db.rollback();raise


if __name__=='__main__': main()
