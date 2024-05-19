from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID as py_UUID

import sqlalchemy as sa
from fastapi import HTTPException, status
from humps import decamelize
from pydantic import validator
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_schemas import ObjSchema, PaginatedResponse, PaginationSchema
from app.db.database import Base
from app.models.enums.status import Status
from app.models.lecture import LectureResponse
from app.models.subject import SubjectResponse
from app.models.teacher import TeacherResponse
from app.models.university import UniversityResponse

if TYPE_CHECKING:
    from app.models.lecture import LectureModel
    from app.models.university import UniversityModel
    from app.models.subject import SubjectModel
    from app.models.teacher import TeacherModel


class SummaryModel(Base):
    __tablename__ = "summary"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(
        sa.String(255), nullable=False, doc="Наименование_конспекта"
    )
    university_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey("university.id"),
        nullable=False,
        doc="Идентификатор университета",
    )
    subject_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey("subject.id"),
        nullable=False,
        doc="Идентификатор предмета",
    )
    teacher_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        sa.ForeignKey("teacher.id"),
        nullable=False,
        doc="Идентификатор преподавателя",
    )
    status: Mapped[Status] = mapped_column(sa.Enum(Status), doc="Статус конспекта")
    moderation_comment: Mapped[str] = mapped_column(
        sa.Text, nullable=True, doc="Комментарий модерации"
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, doc="Идентификатор пользователя"
    )
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime,
        onupdate=datetime.utcnow,
        nullable=True,
    )
    lectures: Mapped[list[LectureModel]] = relationship(back_populates="summary")
    university: Mapped[UniversityModel] = relationship(back_populates="summaries")
    subject: Mapped[SubjectModel] = relationship(back_populates="summaries")
    teacher: Mapped[TeacherModel] = relationship(back_populates="summaries")


class SummaryBase(ObjSchema):
    name: str
    university_id: int
    subject_id: int
    teacher_id: py_UUID


class SummaryRequest(SummaryBase):
    pass


class SummaryCreate(SummaryBase):
    id: py_UUID
    status: Status
    moderation_comment: str | None = None
    user_id: py_UUID


class SummaryBaseUpdate(ObjSchema):
    name: str | None
    university_id: int | None
    subject_id: int | None
    teacher_id: py_UUID | None


class SummaryUpdateRequest(SummaryBaseUpdate):
    id: py_UUID


class SummaryUpdate(SummaryBaseUpdate):
    status: Status


class SummaryResponse(ObjSchema):
    id: py_UUID
    name: str
    university: UniversityResponse
    subject: SubjectResponse
    teacher: TeacherResponse
    moderation_comment: str | None
    user_id: py_UUID
    status: Status
    lectures: list[LectureResponse]

    @staticmethod
    async def check_conspect_access(
        user_id: py_UUID | None, summary: SummaryModel
    ) -> bool:
        if not user_id and summary.status != Status.approved:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Не авторизован"
            )

        if user_id and (
            user_id != summary.user_id and summary.status != Status.approved
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Нет прав на просмотр"
            )

        return True


class SummaryChangeStatusRequest(ObjSchema):
    id: py_UUID
    moderation_comment: str | None = None


class SummaryApprovedStatus(ObjSchema):
    status: Status = Status.approved
    moderation_comment: str


class SummaryRejectedStatus(ObjSchema):
    status: Status = Status.rejected
    moderation_comment: str


class SummaryShortResponse(ObjSchema):
    id: py_UUID
    name: str
    user_id: py_UUID
    university_name: str
    subject_name: str
    teacher_full_name: str
    status: Status
    lectures_count: int


class QuerySummaries(PaginationSchema):
    name: str | None = None
    university_id: int | None = None
    subject_id: int | None = None
    teacher_id: py_UUID | None = None

    @validator("sort_by")
    def verify_sort_by(cls, value: str) -> str:  # noqa: N805
        """Проверка формата поля, по которому сортируется список."""
        if value is not None:
            value = decamelize(value)
            if value not in SummaryModel.__table__.columns:
                raise HTTPException(
                    status_code=422, detail={"sortBy": "Неверное значение"}
                )
        return value


class SummariesResponse(PaginatedResponse):
    result: list[SummaryShortResponse]
