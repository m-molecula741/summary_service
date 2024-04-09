from typing import Sequence
from uuid import UUID

from sqlalchemy import select

from app.core.logger import logger
from app.db.repositories.base_repo import BaseRepository
from app.models.lecture import LectureModel


class LecturesRepository(BaseRepository[LectureModel]):
    async def get_lectures_by_summary_id(
        self, summary_id: UUID
    ) -> tuple[Sequence[LectureModel] | None, str | None]:
        try:
            stmt = select(self.model).filter(self.model.summary_id == summary_id)
            result = await self.session.execute(stmt)  # type: ignore
            res = result.scalars().all()
        except Exception as e:
            logger.error(f"DB error : {e}")
            return None, f"DB error : {e}"
        if res is None:
            return None, "Data not found"

        return res, None

    async def get_lectures_by_summary_ids(
        self, summary_ids: set[UUID]
    ) -> tuple[Sequence[LectureModel] | None, str | None]:
        try:
            stmt = select(self.model).filter(self.model.summary_id.in_(summary_ids))
            result = await self.session.execute(stmt)  # type: ignore
            res = result.scalars().all()
        except Exception as e:
            logger.error(f"DB error : {e}")
            return None, f"DB error : {e}"
        if res is None:
            return None, "Data not found"

        return res, None
