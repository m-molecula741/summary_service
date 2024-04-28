from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID as py_UUID

import sqlalchemy as sa
from fastapi import HTTPException
from humps import decamelize
from pydantic import validator
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_schemas import ObjSchema, PaginatedResponse, PaginationSchema
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.university import UniversityModel


class TeacherModel(Base):
    __tablename__ = "teacher"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    full_name: Mapped[str] = mapped_column(
        sa.String(255), nullable=False, index=True, doc="Полное имя"
    )
    date_birth: Mapped[date] = mapped_column(
        sa.Date, nullable=True, doc="Дата рождения"
    )
    university_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey("university.id"),
        nullable=False,
        doc="Идентификатор университета",
    )
    subject_ids: Mapped[list[int]] = mapped_column(
        ARRAY(sa.Integer),
        nullable=False,
        doc="Идентификаторы предметов",
    )
    is_moderated: Mapped[bool] = mapped_column(
        sa.Boolean, nullable=False, doc="Статус модерации"
    )
    university: Mapped[UniversityModel] = relationship(back_populates="teachers")


class TeacherBase(ObjSchema):
    full_name: str
    date_birth: date
    university_id: int
    subject_ids: list[int]


class TeacherRequest(TeacherBase):
    pass


class TeacherCreate(TeacherBase):
    id: py_UUID
    is_moderated: bool = False


class QueryTeachers(PaginationSchema):
    """Схема запроса списка преподов"""

    subject_id: int | None = None
    full_name: str | None = None

    @validator("sort_by")
    def verify_sort_by(cls, value: str) -> str:  # noqa: N805
        """Проверка формата поля, по которому сортируется список."""
        if value is not None:
            value = decamelize(value)
            if value not in TeacherModel.__table__.columns:
                raise HTTPException(
                    status_code=422, detail={"sortBy": "Неверное значение"}
                )
        return value


class TeacherResponse(TeacherBase):
    id: py_UUID
    is_moderated: bool


class TeachersResponse(PaginatedResponse):
    result: list[TeacherResponse]


class TeacherUpdateRequest(ObjSchema):
    id: py_UUID
    full_name: str | None
    date_birth: date | None
    university_id: int | None
    subject_ids: list[int] | None


class TeacherUpdate(ObjSchema):
    pass


class TeacherIsModeratedUpdate(ObjSchema):
    is_moderated: bool = True
