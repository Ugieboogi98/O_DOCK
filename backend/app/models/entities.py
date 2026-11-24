from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import (
    String,
    Text,
    ForeignKey,
    Numeric,
    DateTime,
    UniqueConstraint,
    CheckConstraint,
    JSON,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def now():
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class Manufacturer(Base):
    __tablename__ = "manufacturers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    name_ko: Mapped[str] = mapped_column(String(120))
    official_url: Mapped[str] = mapped_column(Text)


class ProductLine(Base):
    __tablename__ = "product_lines"
    __table_args__ = (UniqueConstraint("manufacturer_id", "name"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey("manufacturers.id"))
    name: Mapped[str] = mapped_column(String(200))


class Figure(Base):
    __tablename__ = "figures"
    id: Mapped[int] = mapped_column(primary_key=True)
    manufacturer_id: Mapped[int] = mapped_column(
        ForeignKey("manufacturers.id"), index=True
    )
    product_line_id: Mapped[int | None] = mapped_column(ForeignKey("product_lines.id"))
    name_original: Mapped[str] = mapped_column(Text)
    name_ko: Mapped[str | None] = mapped_column(Text)
    franchise: Mapped[str | None] = mapped_column(Text)
    character: Mapped[str | None] = mapped_column(Text)
    type: Mapped[str] = mapped_column(String(60), default="figure")
    scale: Mapped[str | None] = mapped_column(String(40))
    height_mm: Mapped[int | None]
    material: Mapped[str | None] = mapped_column(String(200))
    official_url: Mapped[str] = mapped_column(Text, unique=True)
    collected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    quality: Mapped[str] = mapped_column(String(40), default="official_metadata")
    manufacturer: Mapped[Manufacturer] = relationship()
    product_line: Mapped[ProductLine | None] = relationship()
    variants: Mapped[list["FigureVariant"]] = relationship(
        back_populates="figure", cascade="all, delete-orphan"
    )


class FigureVariant(Base):
    __tablename__ = "figure_variants"
    __table_args__ = (UniqueConstraint("figure_id", "variant_key"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    figure_id: Mapped[int] = mapped_column(ForeignKey("figures.id"), index=True)
    variant_key: Mapped[str] = mapped_column(String(200), default="source-page")
    sku: Mapped[str | None] = mapped_column(String(120))
    jan_code: Mapped[str | None] = mapped_column(String(30))
    edition: Mapped[str | None] = mapped_column(String(200))
    reissue_no: Mapped[int | None]
    release_date: Mapped[str | None] = mapped_column(String(40))
    release_precision: Mapped[str | None] = mapped_column(String(20))
    figure: Mapped[Figure] = relationship(back_populates="variants")


class ReleasePrice(Base):
    __tablename__ = "release_prices"
    __table_args__ = (
        UniqueConstraint("variant_id", "source_url", "price_kind"),
        CheckConstraint("price_amount >= 0"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    variant_id: Mapped[int] = mapped_column(
        ForeignKey("figure_variants.id"), index=True
    )
    price_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    currency: Mapped[str] = mapped_column(String(3))
    price_kind: Mapped[str] = mapped_column(String(40), default="official_list")
    tax_included: Mapped[bool | None]
    source_url: Mapped[str] = mapped_column(Text)
    checked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Retailer(Base):
    __tablename__ = "retailers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160), unique=True)
    site_url: Mapped[str] = mapped_column(Text)
    seller_type: Mapped[str] = mapped_column(String(60), default="unverified")


class SellerVerification(Base):
    __tablename__ = "seller_verifications"
    id: Mapped[int] = mapped_column(primary_key=True)
    retailer_id: Mapped[int] = mapped_column(ForeignKey("retailers.id"))
    verification_type: Mapped[str] = mapped_column(String(60))
    evidence_url: Mapped[str] = mapped_column(Text)
    verified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class RetailPriceRecord(Base):
    __tablename__ = "retail_price_records"
    __table_args__ = (
        UniqueConstraint("variant_id", "product_url", "observed_at", "price_type"),
        CheckConstraint("amount >= 0"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    variant_id: Mapped[int] = mapped_column(
        ForeignKey("figure_variants.id"), index=True
    )
    retailer_id: Mapped[int] = mapped_column(ForeignKey("retailers.id"))
    price_type: Mapped[str] = mapped_column(String(40))
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    currency: Mapped[str] = mapped_column(String(3), default="KRW")
    shipping: Mapped[Decimal | None] = mapped_column(Numeric(14, 2))
    availability: Mapped[str] = mapped_column(String(40))
    match_status: Mapped[str] = mapped_column(String(40))
    product_url: Mapped[str] = mapped_column(Text)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    retailer: Mapped[Retailer] = relationship()


class UsedMarketplace(Base):
    __tablename__ = "used_marketplaces"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    url: Mapped[str] = mapped_column(Text)
    currency: Mapped[str] = mapped_column(String(3))


class UsedListing(Base):
    __tablename__ = "used_listings"
    __table_args__ = (
        UniqueConstraint("listing_url", "observed_at"),
        CheckConstraint("asking_price >= 0"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    variant_id: Mapped[int] = mapped_column(
        ForeignKey("figure_variants.id"), index=True
    )
    marketplace_id: Mapped[int] = mapped_column(ForeignKey("used_marketplaces.id"))
    listing_url: Mapped[str] = mapped_column(Text)
    asking_price: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    currency: Mapped[str] = mapped_column(String(3))
    condition: Mapped[str] = mapped_column(String(60))
    listing_status: Mapped[str] = mapped_column(String(40))
    is_set: Mapped[bool] = mapped_column(default=False)
    match_status: Mapped[str] = mapped_column(String(40))
    region: Mapped[str | None] = mapped_column(String(120))
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    marketplace: Mapped[UsedMarketplace] = relationship()


class ProductImage(Base):
    __tablename__ = "product_images"
    id: Mapped[int] = mapped_column(primary_key=True)
    variant_id: Mapped[int] = mapped_column(ForeignKey("figure_variants.id"))
    image_url: Mapped[str] = mapped_column(Text)
    source_url: Mapped[str] = mapped_column(Text)
    usage_status: Mapped[str] = mapped_column(String(40), default="unverified")
    license_evidence: Mapped[str | None] = mapped_column(Text)
    checked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class SourceDocument(Base):
    __tablename__ = "source_documents"
    __table_args__ = (UniqueConstraint("variant_id", "url"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    variant_id: Mapped[int] = mapped_column(
        ForeignKey("figure_variants.id"), index=True
    )
    title: Mapped[str] = mapped_column(Text)
    url: Mapped[str] = mapped_column(Text)
    source_type: Mapped[str] = mapped_column(String(60))
    language: Mapped[str] = mapped_column(String(10), default="en")
    body: Mapped[str] = mapped_column(Text)
    usage_status: Mapped[str] = mapped_column(
        String(80), default="factual_metadata_only"
    )
    content_hash: Mapped[str] = mapped_column(String(64))
    collected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class CollectionJob(Base):
    __tablename__ = "collection_jobs"
    id: Mapped[int] = mapped_column(primary_key=True)
    collector: Mapped[str] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(40))
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    count: Mapped[int] = mapped_column(default=0)
    error_summary: Mapped[str | None] = mapped_column(Text)


class SearchRun(Base):
    __tablename__ = "search_runs"
    __table_args__ = (UniqueConstraint("variant_id", "query", "provider"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    variant_id: Mapped[int] = mapped_column(ForeignKey("figure_variants.id"))
    query: Mapped[str] = mapped_column(Text)
    provider: Mapped[str] = mapped_column(String(60))
    status: Mapped[str] = mapped_column(String(40))
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    executed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(40), unique=True)
    password_hash: Mapped[str | None] = mapped_column(Text)
    failed_attempts: Mapped[int] = mapped_column(default=0)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class UserSession(Base):
    __tablename__ = 'user_sessions'
    token_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class Favorite(Base):
    __tablename__ = "favorites"
    figure_id: Mapped[int] = mapped_column(ForeignKey("figures.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Purchase(Base):
    __tablename__ = "purchases"
    __table_args__ = (CheckConstraint("amount >= 0"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    variant_id: Mapped[int] = mapped_column(
        ForeignKey("figure_variants.id"), index=True
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    currency: Mapped[str] = mapped_column(String(3), default="KRW")
    purchased_on: Mapped[str] = mapped_column(String(10))
    delivery_status: Mapped[str] = mapped_column(String(20), default="pending")
    shop: Mapped[str] = mapped_column(String(200), default="")
    memo: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"
    pair: Mapped[str] = mapped_column(String(10), primary_key=True)
    rate: Mapped[Decimal] = mapped_column(Numeric(18, 8))
    rate_date: Mapped[str] = mapped_column(String(10))
    source_url: Mapped[str] = mapped_column(Text)
    checked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
