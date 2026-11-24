from sqlalchemy import select, func, or_, exists
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from app.models.entities import Figure, FigureVariant, Manufacturer

_UNSET = object()


def serialize(row):
    return {c.name: getattr(row, c.name) for c in row.__table__.columns}


def card(f, semantic=_UNSET, images=_UNSET, favorite=_UNSET):
    from sqlalchemy.orm import object_session

    db = object_session(f)
    from app.services.image_order import ordered_images

    if images is _UNSET:
        images = ordered_images(db, f) if db else []
    image = images[0].image_url if images else None
    if favorite is _UNSET:
        favorite = False  # Unscoped cards must never reveal another user's personal state.
    from app.services.product_semantics import current

    if semantic is _UNSET:
        semantic = current(db, f) if db else None
    fields = semantic.fields if semantic else {}
    return {
        **serialize(f),
        "name_ko": f.name_ko or fields.get("name_ko"),
        "semantic_name_ko": fields.get("name_ko"),
        "franchise_ko": fields.get("franchise_ko"),
        "character_ko": fields.get("character_ko"),
        "characters": fields.get("characters", []),
        "figure_form": fields.get("figure_form"),
        "figure_form_ko": fields.get("figure_form_ko"),
        "semantic_status": semantic.status if semantic else "pending",
        "semantic_missing_fields": fields.get("missing_fields", []),
        "semantic_field_status": fields.get("field_status", {}),
        "semantic_field_issues": fields.get("field_issues", {}),
        "translation_status": "translated" if f.name_ko or fields.get("name_ko") else "pending",
        "thumbnail": image,
        "favorite": favorite,
        "manufacturer": f.manufacturer.name,
        "manufacturer_ko": f.manufacturer.name_ko,
        "product_line": f.product_line.name if f.product_line else None,
        "variants": [serialize(v) for v in f.variants],
    }


def get_figure(db, fid):
    f = db.get(Figure, fid)
    if not f:
        raise HTTPException(404, "제품을 찾을 수 없습니다.")
    return f


def choose_variant(f, vid=None):
    v = next((v for v in f.variants if vid is None or v.id == vid), None)
    if not v:
        raise HTTPException(404, "제품 버전을 찾을 수 없습니다.")
    return v


def translated_match(field, value):
    from app.models.korean import KoreanProfile
    from app.models.semantics import ProductSemantics
    from app.services.product_semantics import valid_sql

    # A current semantic decision takes precedence over an older translation.
    return ~exists(select(ProductSemantics.figure_id).where(*valid_sql())) & exists(
        select(KoreanProfile.figure_id).where(
            KoreanProfile.figure_id == Figure.id,
            KoreanProfile.fields[field].as_string().icontains(value, autoescape=True),
        )
    )


def _text_conditions(term, semantic_match):
    return [
        *(column.icontains(term, autoescape=True) for column in (
            Figure.name_original, Figure.name_ko, Figure.franchise, Figure.character)),
        *(translated_match(field, term) for field in ("name_ko", "franchise_ko", "character_ko")),
        *(semantic_match(field, term) for field in ("name_ko", "franchise_ko", "character_ko", "figure_form_ko")),
    ]


def list_figures(
    db,
    q=None,
    manufacturer_id=None,
    scale=None,
    year=None,
    height_max=None,
    height_min=None,
    franchise=None,
    character=None,
    product_line_id=None,
    page=1,
    page_size=24,
    figure_form=None,
    user_id=None,
):
    from app.services.product_semantics import semantic_match
    from app.services.reference_classifier import search_title_aliases

    s = select(Figure)
    if figure_form:
        s = s.where(semantic_match("figure_form", figure_form))
    if q:
        title_aliases = search_title_aliases(q)
        groups = [title_aliases] if len(title_aliases) > 1 else [search_title_aliases(t) for t in q.split()]
        for terms in groups:
            conditions = []
            for term in terms:
                conditions.extend(_text_conditions(term, semantic_match))
            s = s.where(or_(*conditions))
    if manufacturer_id:
        s = s.where(Figure.manufacturer_id == manufacturer_id)
    if product_line_id:
        s = s.where(Figure.product_line_id == product_line_id)
    if scale:
        s = s.where(Figure.scale == scale)
    if franchise:
        s = s.where(or_(*[
            condition for alias in search_title_aliases(franchise) for condition in (
                Figure.franchise.icontains(alias, autoescape=True),
                translated_match("franchise_ko", alias),
                semantic_match("franchise_ko", alias),
            )]))
    if character:
        s = s.where(
            or_(
                Figure.character.icontains(character, autoescape=True),
                translated_match("character_ko", character),
                semantic_match("character_ko", character),
            )
        )
    if height_max is not None:
        s = s.where(Figure.height_mm <= height_max)
    if height_min is not None:
        s = s.where(Figure.height_mm >= height_min)
    if year:
        s = s.where(
            Figure.variants.any(FigureVariant.release_date.like(str(year) + "%"))
        )
    total = db.scalar(select(func.count()).select_from(s.subquery()))
    rows = db.scalars(
        s.options(
            selectinload(Figure.variants),
            selectinload(Figure.manufacturer),
            selectinload(Figure.product_line),
        )
        .order_by(Figure.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()
    from app.services.product_semantics import current_many
    from app.services.image_order import ordered_images_many
    from app.models.entities import Favorite
    semantics = current_many(db, rows)
    images = ordered_images_many(db, rows)
    favorites = set(db.scalars(select(Favorite.figure_id).where(Favorite.user_id == user_id, Favorite.figure_id.in_([f.id for f in rows])))) if rows and user_id is not None else set()
    return {
        "items": [card(f, semantics.get(f.id), images[f.id], f.id in favorites) for f in rows],
        "total": total,
        "page": page,
        "page_size": page_size,
    }
