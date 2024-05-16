import unittest.mock as mock

from fastapi import status
from app.core.config import config
from fastapi.testclient import TestClient
from app.db.repositories.teachers_repository import TeachersRepository
from app.models.teacher import TeacherModel


def test_add_teacher_positive(client: TestClient, teacher_in_db: TeacherModel) -> None:
    with mock.patch.object(
        TeachersRepository, "find_one"
    ) as mock_find_one, mock.patch.object(TeachersRepository, "add") as mock_add:
        mock_find_one.return_value = None, "Data not found"
        mock_add.return_value = teacher_in_db, None

        response = client.post(
            f"{config.private_prefix}/teachers",
            json={"full_name": "test"},
        )
    assert response.status_code == status.HTTP_201_CREATED


def test_add_teacher_negative(client: TestClient, teacher_in_db: TeacherModel) -> None:
    with mock.patch.object(
        TeachersRepository, "find_one"
    ) as mock_find_one, mock.patch.object(TeachersRepository, "add") as mock_add:
        mock_find_one.return_value = None, "DB error"
        mock_add.return_value = teacher_in_db, None

        response = client.post(
            f"{config.private_prefix}/teachers",
            json={"full_name": "test"},
        )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
