"""Derived translations and entity extraction; original catalog fields stay intact."""
from datetime import datetime
from sqlalchemy import ForeignKey, String, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.models.entities import Base, now


class ProductSemantics(Base):
    __tablename__ = 'product_semantics'
    figure_id: Mapped[int] = mapped_column(ForeignKey('figures.id', ondelete='CASCADE'), primary_key=True)
    source_hash: Mapped[str] = mapped_column(String(64))
    source: Mapped[dict] = mapped_column(JSON)
    fields: Mapped[dict] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String(20), index=True)
    model: Mapped[str] = mapped_column(String(200))
    issues: Mapped[list] = mapped_column(JSON)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
