from __future__ import annotations

import csv
from typing import TYPE_CHECKING

import sqlalchemy as sa
from fastapi import HTTPException
from humps import decamelize
from pydantic import validator
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_schemas import ObjSchema, PaginatedResponse, PaginationSchema
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.teacher import TeacherModel


class UniversityModel(Base):
    __tablename__ = "university"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    short_name: Mapped[str] = mapped_column(
        sa.String(50), nullable=False, doc="Краткое наименование"
    )
    name: Mapped[str] = mapped_column(
        sa.String(255), nullable=False, doc="Наименование"
    )
    teachers: Mapped[list[TeacherModel]] = relationship(back_populates="university")


class UniversityBase(ObjSchema):
    id: int
    short_name: str
    name: str


class UniversityIn(UniversityBase):
    @classmethod
    async def from_csv(cls, csv_file: bytes) -> list[UniversityIn] | None:
        lines = csv_file.decode(encoding="utf-8-sig").split("\n")
        reader = csv.DictReader(lines, delimiter=";")
        if reader.fieldnames != ["Id", "ShortName", "Name"]:
            return None

        universities = [
            UniversityIn(
                id=int(str(read.get("Id"))),
                short_name=read.get("ShortName"),
                name=(read.get("Name")),
            )
            for read in reader
        ]

        return universities


class UniversitiesAddedResponse(ObjSchema):
    count_added_universities: int


class UniversityResponse(UniversityBase):
    pass


class QueryUniversities(PaginationSchema):
    """Схема запроса списка университетов"""

    name: str | None = None

    @validator("sort_by")
    def verify_sort_by(cls, value: str) -> str:  # noqa: N805
        """Проверка формата поля, по которому сортируется список."""
        if value is not None:
            value = decamelize(value)
            if value not in UniversityModel.__table__.columns:
                raise HTTPException(
                    status_code=422, detail={"sortBy": "Неверное значение"}
                )
        return value


class UniversitiesResponse(PaginatedResponse):
    result: list[UniversityResponse]


class DataUniv(ObjSchema):
    name: str
    age: int
