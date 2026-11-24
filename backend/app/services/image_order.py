"""Choose display images by actual local dimensions, without modifying stored assets."""

from functools import lru_cache
from pathlib import Path
import struct


def dimensions(data):
    """Read PNG, JPEG and WebP dimensions from a bounded header; never decode pixels."""
    try:
        if data.startswith(b"\x89PNG\r\n\x1a\n") and data[12:16] == b"IHDR":
            return struct.unpack(">II", data[16:24])
        if data.startswith(b"\xff\xd8"):
            i = 2
            while i + 4 <= len(data):
                if data[i] != 255:
                    i += 1
                    continue
                while i < len(data) and data[i] == 255:
                    i += 1
                marker = data[i]
                i += 1
                if marker in (0xD9, 0xDA):
                    break
                if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
                    continue
                length = int.from_bytes(data[i : i + 2], "big")
                if length < 2:
                    break
                if marker in (
                    0xC0,
                    0xC1,
                    0xC2,
                    0xC3,
                    0xC5,
                    0xC6,
                    0xC7,
                    0xC9,
                    0xCA,
                    0xCB,
                    0xCD,
                    0xCE,
                    0xCF,
                ):
                    h, w = struct.unpack(">HH", data[i + 3 : i + 7])
                    return w, h
                i += length
        if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
            kind = data[12:16]
            if kind == b"VP8X":
                return (
                    1 + int.from_bytes(data[24:27], "little"),
                    1 + int.from_bytes(data[27:30], "little"),
                )
            if kind == b"VP8 " and data[23:26] == b"\x9d\x01\x2a":
                w, h = struct.unpack("<HH", data[26:30])
                return w & 16383, h & 16383
            if kind == b"VP8L" and data[20] == 47:
                bits = int.from_bytes(data[21:25], "little")
                return (bits & 16383) + 1, ((bits >> 14) & 16383) + 1
    except (IndexError, struct.error):
        pass
    return None


@lru_cache(maxsize=8192)
def _header_size(filename, mtime_ns, file_size):
    try:
        with open(filename, "rb") as stream:
            size = dimensions(stream.read(131072))
        return size if size and min(size) > 0 else None
    except OSError:
        return None


def local_size(image_url, media_dir):
    if not image_url.startswith("/api/media/"):
        return None
    root = Path(media_dir).resolve()
    path = (root / image_url.removeprefix("/api/media/")).resolve()
    if not path.is_relative_to(root):
        return None
    try:
        stat = path.stat()
    except OSError:
        return None
    return _header_size(str(path), stat.st_mtime_ns, stat.st_size)


def quality_key(record, media_dir):
    size = local_size(record.image_url, media_dir)
    # Full-size images first; retain original insertion order within a quality tier.
    # Unknown remote images remain available, and no network requests occur here.
    tier = (0 if min(size) >= 512 else 2) if size else 1
    return tier, record.id


def ordered_images(db, figure):
    return ordered_images_many(db, [figure])[figure.id]


def ordered_images_many(db, figures):
    """Load visible gallery images for a page while retaining single-item order."""
    from sqlalchemy import select
    from app.models.entities import ProductImage
    from app.core.config import get_settings

    owners = {v.id: f.id for f in figures for v in f.variants}
    result = {f.id: [] for f in figures}
    if not owners:
        return result
    rows = list(
        db.scalars(
            select(ProductImage)
            .where(
                ProductImage.variant_id.in_(owners),
                ProductImage.usage_status.in_(["authorized", "personal_local"]),
            )
            .order_by(ProductImage.id)
        )
    )
    for row in rows:
        result[owners[row.variant_id]].append(row)
    media_dir = get_settings().media_dir
    return {fid: sorted(images, key=lambda row: quality_key(row, media_dir))
            for fid, images in result.items()}
