from __future__ import annotations

import sqlalchemy as sa
from fastapi import HTTPException
from humps import decamelize
from pydantic import validator
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_schemas import ObjSchema, PaginatedResponse, PaginationSchema
from app.db.database import Base
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.summary import SummaryModel


class SubjectModel(Base):
    __tablename__ = "subject"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(
        sa.String(255), nullable=False, unique=True, index=True, doc="Наименование"
    )
    is_moderated: Mapped[bool] = mapped_column(
        sa.Boolean, nullable=False, doc="Статус модерации"
    )
    summaries: Mapped[list[SummaryModel]] = relationship(back_populates="subject")


class SubjectBase(ObjSchema):
    name: str


class SubjectCreate(SubjectBase):
    is_moderated: bool = False


class SubjectResponse(SubjectBase):
    id: int
    is_moderated: bool


class QuerySubjects(PaginationSchema):
    name: str | None = None

    @validator("sort_by")
    def verify_sort_by(cls, value: str) -> str:  # noqa: N805
        """Проверка формата поля, по которому сортируется список."""
        if value is not None:
            value = decamelize(value)
            if value not in SubjectModel.__table__.columns:
                raise HTTPException(
                    status_code=422, detail={"sortBy": "Неверное значение"}
                )
        return value


class SubjectsResponse(PaginatedResponse):
    result: list[SubjectResponse]


class SubjectIsModeratedUpdate(ObjSchema):
    is_moderated: bool = True
