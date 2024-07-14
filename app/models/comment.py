from __future__ import annotations

import sqlalchemy as sa
from datetime import datetime
from uuid import UUID as py_UUID
from fastapi import HTTPException
from humps import decamelize
from pydantic import validator
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.core.base_schemas import ObjSchema, PaginatedResponse, PaginationSchema
from app.db.database import Base


class CommentModel(Base):
    __tablename__ = "comment"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    text: Mapped[str] = mapped_column(
        sa.String(255), nullable=False, doc="Наименование"
    )
    summary_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        doc="Идентификатор конспекта",
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
    is_moderated: Mapped[bool] = mapped_column(
        sa.Boolean, nullable=False, doc="Статус модерации"
    )
    is_complain: Mapped[bool] = mapped_column(
        sa.Boolean, nullable=False, doc="Статус жалобы"
    )


class CommentCreateRequest(ObjSchema):
    summary_id: py_UUID
    text: str


class CommentComplainRequest(ObjSchema):
    comment_id: py_UUID
    user_from: py_UUID


class CommentComplain(ObjSchema):
    is_complain: bool = True


class CommentApprove(ObjSchema):
    is_moderated: bool = True
    is_complain: bool = False


class CommentCreate(ObjSchema):
    id: py_UUID
    text: str
    summary_id: py_UUID
    user_id: py_UUID
    is_moderated: bool = False
    is_complain: bool = False


class CommentResponse(ObjSchema):
    id: py_UUID
    text: str
    summary_id: py_UUID
    user_id: py_UUID
    is_moderated: bool = False
    is_complain: bool = False


class QueryComments(PaginationSchema):
    @validator("sort_by")
    def verify_sort_by(cls, value: str) -> str:  # noqa: N805
        """Проверка формата поля, по которому сортируется список."""
        if value is not None:
            value = decamelize(value)
            if value not in CommentModel.__table__.columns:
                raise HTTPException(
                    status_code=422, detail={"sortBy": "Неверное значение"}
                )
        return value


class CommentsResponse(PaginatedResponse):
    result: list[CommentResponse]
