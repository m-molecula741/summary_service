from typing import TypeVar

from app.db.database import Base
from app.db.repositories.base_repo import BaseRepository
from app.models.file import FileModel

ModelType = TypeVar("ModelType", bound=Base)


class FilesRepository(BaseRepository[FileModel]):
    pass
