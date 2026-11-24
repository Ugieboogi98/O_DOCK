"""Domestic store listings and their latest observed offer."""
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.entities import Base


class RetailListing(Base):
    __tablename__ = 'retailer_listings'
    __table_args__ = (
        UniqueConstraint('source_code', 'external_product_id', 'option_key'),
        UniqueConstraint('source_code', 'canonical_url', 'option_key'),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    retailer_id: Mapped[int] = mapped_column(ForeignKey('retailers.id'), index=True)
    source_code: Mapped[str] = mapped_column(String(40), index=True)
    external_product_id: Mapped[str] = mapped_column(String(120))
    option_key: Mapped[str] = mapped_column(String(120), default='')
    canonical_url: Mapped[str] = mapped_column(Text)
    title_raw: Mapped[str] = mapped_column(Text)
    manufacturer_raw: Mapped[str | None] = mapped_column(Text)
    jan_ean: Mapped[str | None] = mapped_column(String(30), index=True)
    model_code: Mapped[str | None] = mapped_column(String(200))
    catalog_variant_id: Mapped[int | None] = mapped_column(ForeignKey('figure_variants.id'), index=True)
    match_status: Mapped[str] = mapped_column(String(40), index=True)
    match_evidence: Mapped[dict] = mapped_column(JSON)
    facts: Mapped[dict] = mapped_column(JSON)
    first_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)


class RetailOffer(Base):
    __tablename__ = 'retailer_offers'
    __table_args__ = (
        CheckConstraint("currency = 'KRW'"),
        CheckConstraint('sale_price IS NULL OR sale_price >= 0'),
        CheckConstraint('list_price IS NULL OR list_price >= 0'),
        CheckConstraint("availability IN ('IN_STOCK','PREORDER','SOLD_OUT','COMING_SOON','UNKNOWN')"),
    )
    listing_id: Mapped[int] = mapped_column(ForeignKey('retailer_listings.id'), primary_key=True)
    currency: Mapped[str] = mapped_column(String(3), default='KRW')
    list_price: Mapped[int | None]
    sale_price: Mapped[int | None]
    availability: Mapped[str] = mapped_column(String(30), index=True)
    conditions: Mapped[dict] = mapped_column(JSON)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    source_url: Mapped[str] = mapped_column(Text)
    observation_hash: Mapped[str] = mapped_column(String(64))
