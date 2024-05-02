from typing import Sequence, TypeVar
from uuid import UUID

from sqlalchemy import desc, func, select
from sqlalchemy.orm import selectinload, QueryableAttribute

from app.consts import SortType
from app.core.logger import logger
from app.db.database import Base
from app.db.repositories.base_repo import BaseRepository
from app.models.enums.status import Status
from app.models.summary import QuerySummaries, SummaryModel

ModelType = TypeVar("ModelType", bound=Base)


class SummariesRepository(BaseRepository[SummaryModel]):
    async def get_summaries(  # noqa: C901
        self,
        query: QuerySummaries,
        user_id: UUID = None,
        loadopt: QueryableAttribute | None = None,
    ) -> tuple[Sequence[SummaryModel], int | None, str | None]:
        """Получение списка сущностей с учетом пагинации и сортировки"""
        select_count = select(func.count(self.model.id)).filter(
            self.model.status == Status.approved
        )

        stmt = (
            select(self.model)
            .filter(self.model.status == Status.approved)
            .options(*[selectinload(opt) for opt in loadopt])
        )

        if user_id:
            select_count = select_count.filter(self.model.user_id == user_id)
            stmt = stmt.filter(self.model.user_id == user_id)

        if query.name:
            select_count = select_count.filter(  # type: ignore
                self.model.name.ilike("%" + query.name + "%")
            )
            stmt = stmt.filter(self.model.name.ilike("%" + query.name + "%"))  # type: ignore

        if query.university_id:
            select_count = select_count.filter(  # type: ignore
                self.model.university_id == query.university_id
            )
            stmt = stmt.filter(self.model.university_id == query.university_id)  # type: ignore

        if query.subject_id:
            select_count = select_count.filter(  # type: ignore
                self.model.subject_id == query.university_id
            )
            stmt = stmt.filter(self.model.subject_id == query.subject_id)  # type: ignore

        if query.teacher_id:
            select_count = select_count.filter(  # type: ignore
                self.model.teacher_id == query.teacher_id
            )
            stmt = stmt.filter(self.model.teacher_id == query.teacher_id)  # type: ignore

        # Применяем параметры пагинации
        if query.page_size is not None:
            stmt = stmt.offset((query.page - 1) * query.page_size)  # type: ignore
            stmt = stmt.limit(query.page_size)  # type: ignore

        try:
            # Проверяем, есть ли параметр для сортировки
            if query.sort_by is not None:
                sort_field = query.sort_by

                if sort_field is not None:
                    # Применяем сортировку в зависимости от указанного направления
                    if query.sort_type == SortType.desc:
                        stmt = stmt.order_by(desc(sort_field))  # type: ignore
                    else:
                        stmt = stmt.order_by(sort_field)  # type: ignore

            # Выполняем запрос
            summaries_count = await self.session.execute(select_count)  # type: ignore
            count = summaries_count.scalar()
            result = await self.session.execute(stmt)  # type: ignore
            summaries = result.scalars().all()
            return summaries, count, None
        except Exception as e:
            logger.error(f"DB error for {stmt}: {str(e)}")
            return [], None, f"DB error: {str(e)}"
