"""Translations are derivatives; original manufacturer records are preserved."""

from datetime import datetime
from sqlalchemy import ForeignKey, String, Text, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.models.entities import Base, now


class KoreanProfile(Base):
    __tablename__ = "korean_profiles"
    figure_id: Mapped[int] = mapped_column(
        ForeignKey("figures.id", ondelete="CASCADE"), primary_key=True
    )
    source_hash: Mapped[str] = mapped_column(String(64))
    fields: Mapped[dict] = mapped_column(JSON)
    model: Mapped[str] = mapped_column(String(200))
    translated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=now
    )


class KoreanChunk(Base):
    __tablename__ = "korean_chunks"
    document_id: Mapped[int] = mapped_column(
        ForeignKey("source_documents.id", ondelete="CASCADE"), primary_key=True
    )
    part: Mapped[int] = mapped_column(primary_key=True)
    source_hash: Mapped[str] = mapped_column(String(64))
    body_ko: Mapped[str] = mapped_column(Text)
    model: Mapped[str] = mapped_column(String(200))
    translated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=now
    )
