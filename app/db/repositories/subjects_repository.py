from typing import Sequence, TypeVar

from sqlalchemy import desc, func, select

from app.consts import SortType
from app.core.logger import logger
from app.db.database import Base
from app.db.repositories.base_repo import BaseRepository
from app.models.subject import QuerySubjects, SubjectModel

ModelType = TypeVar("ModelType", bound=Base)


class SubjectsRepository(BaseRepository[SubjectModel]):
    async def get_subjects(
        self, query: QuerySubjects
    ) -> tuple[Sequence[SubjectModel], int | None, str | None]:
        """Получение списка сущностей с учетом пагинации и сортировки"""
        select_count = select(func.count(self.model.id))

        stmt = select(self.model)

        if query.name:
            select_count = select_count.filter(
                self.model.name.ilike("%" + query.name + "%")
            )
            stmt = stmt.filter(self.model.name.ilike("%" + query.name + "%"))  # type: ignore

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
            subjects_count = await self.session.execute(select_count)  # type: ignore
            count = subjects_count.scalar()
            result = await self.session.execute(stmt)  # type: ignore
            subjects = result.scalars().all()
            return subjects, count, None
        except Exception as e:
            logger.error(f"DB error for {stmt}: {str(e)}")
            return [], None, f"DB error: {str(e)}"
