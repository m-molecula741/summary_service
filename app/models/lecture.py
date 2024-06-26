from __future__ import annotations

from datetime import date as py_date
from typing import TYPE_CHECKING
from uuid import UUID as py_UUID

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_schemas import ObjSchema
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.summary import SummaryModel


class LectureModel(Base):
    __tablename__ = "lecture"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(
        sa.String(255), nullable=False, doc="Наименование лекции"
    )
    description: Mapped[str] = mapped_column(
        sa.String(255), nullable=False, doc="Описание лекции"
    )
    pdf_file_url: Mapped[str] = mapped_column(
        sa.String(500), nullable=False, doc="Ссылка на pdf файл"
    )
    video_url: Mapped[str] = mapped_column(
        sa.String(500), nullable=True, doc="Ссылка на ролик ютуб"
    )
    summary_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        sa.ForeignKey("summary.id"),
        nullable=False,
        doc="Идентификатор конспекта",
    )
    date: Mapped[py_date] = mapped_column(
        sa.Date,
        default=py_date.today,
        nullable=False,
    )
    summary: Mapped[SummaryModel] = relationship(back_populates="lectures")


class LectureBase(ObjSchema):
    name: str
    description: str
    pdf_file_url: str
    video_url: str | None = None
    date: py_date


class LectureCreateRequest(LectureBase):
    summary_id: py_UUID


class LectureCreate(LectureBase):
    id: py_UUID
    summary_id: py_UUID


class LectureUpdateBase(ObjSchema):
    name: str | None
    description: str | None
    pdf_file_url: str | None
    video_url: str | None = None
    date: py_date | None


class LectureUpdateRequest(LectureUpdateBase):
    id: py_UUID


class LectureUpdate(LectureUpdateBase):
    pass


class LectureResponse(LectureBase):
    id: py_UUID
