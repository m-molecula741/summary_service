from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType
from typing import Type

from app.db.database import async_session_maker
from app.db.repositories import (
    files_repository,
    lectures_repository,
    subjects_repository,
    summaries_repository,
    teachers_repository,
    universities_repository,
)


class AbstractUOW(ABC):
    async def __aenter__(self) -> AbstractUOW:
        """Точка входа в контекстный менеджер"""
        raise NotImplementedError

    async def __aexit__(
        self,
        err_type: Type[BaseException] | None,
        err: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Точка выхода из контекстного менеджера"""
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        """Сохраняем транзакцию"""
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        """Откатываем транзакцию"""
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUOW):
    """SQLAlchemy реализация Unit of work"""

    def __init__(self) -> None:
        """Конструктор"""
        self.session = async_session_maker()

    async def __aenter__(self) -> SqlAlchemyUnitOfWork:
        """Точка входа в контекстный менеджер"""
        return self

    async def __aexit__(
        self,
        err_type: Type[BaseException] | None,
        err: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Точка выхода из контекстного менеджера"""
        if err is None:
            await self.commit()
            await self.session.close()
        else:
            await self.rollback()
            await self.session.close()

    async def commit(self) -> None:
        """Сохраняем транзакцию"""
        await self.session.commit()

    async def rollback(self) -> None:
        """Откатываем транзакцию"""
        await self.session.rollback()

    @property
    def lectures(self) -> lectures_repository.LecturesRepository:
        """Доступ к репозиторию продуктов"""
        return lectures_repository.LecturesRepository(self.session)

    @property
    def subjects(self) -> subjects_repository.SubjectsRepository:
        """Доступ к репозиторию продуктов"""
        return subjects_repository.SubjectsRepository(self.session)

    @property
    def teachers(self) -> teachers_repository.TeachersRepository:
        """Доступ к репозиторию продуктов"""
        return teachers_repository.TeachersRepository(self.session)

    @property
    def universities(self) -> universities_repository.UniversitiesRepository:
        """Доступ к репозиторию продуктов"""
        return universities_repository.UniversitiesRepository(self.session)

    @property
    def summaries(self) -> summaries_repository.SummariesRepository:
        """Доступ к репозиторию продуктов"""
        return summaries_repository.SummariesRepository(self.session)

    @property
    def files(self) -> files_repository.FilesRepository:
        """Доступ к репозиторию файлов"""
        return files_repository.FilesRepository(self.session)
