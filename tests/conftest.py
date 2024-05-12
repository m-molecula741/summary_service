import asyncio
from asyncio import AbstractEventLoop
from typing import Generator
from uuid_extensions import uuid7
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.user import User
from app.routers.dependencies import (
    check_access_lecture,
    check_access_lecture_for_add,
    check_access_summary,
    check_is_superuser,
    get_current_user,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    try:
        yield loop
    finally:
        loop.close()


@pytest.fixture(scope="function", autouse=True)
def client(
    event_loop: AbstractEventLoop,
) -> Generator[TestClient, None, None]:
    asyncio.set_event_loop(event_loop)
    # Возвращаем тестового клиента

    async def mock_get_current_user() -> User:
        user = User(
            id=uuid7(), nickname="test", email="test@mail.ru", is_superuser=True
        )

        return user

    app.dependency_overrides[get_current_user] = mock_get_current_user

    with TestClient(app) as client:
        yield client


def mock_check_access_lecture_for_add() -> None:
    return None


def mock_check_access_lecture() -> None:
    return None


def mock_check_access_summary() -> None:
    return None


def mock_check_is_superuser() -> None:
    return None


app.dependency_overrides[
    check_access_lecture_for_add
] = mock_check_access_lecture_for_add
app.dependency_overrides[check_access_lecture] = mock_check_access_lecture
app.dependency_overrides[check_access_summary] = mock_check_access_summary
app.dependency_overrides[check_is_superuser] = mock_check_is_superuser
