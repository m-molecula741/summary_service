from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_schemas import ObjSchema
from app.db.database import Base


class FileModel(Base):
    __tablename__ = "file"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(
        sa.String(255), nullable=False, doc="Наименование файла"
    )


class FileInfoResponse(ObjSchema):
    id: str
    name: str
    file_url: str
