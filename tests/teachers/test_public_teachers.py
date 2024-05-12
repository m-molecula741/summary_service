import unittest.mock as mock

from fastapi import status
from app.core.config import config
from fastapi.testclient import TestClient
from app.db.repositories.teachers_repository import TeachersRepository
from app.models.teacher import TeacherModel


def test_get_teachers_positive(client: TestClient, teacher_in_db: TeacherModel) -> None:
    with mock.patch.object(TeachersRepository, "get_teachers") as mock_get_subjects:
        mock_get_subjects.return_value = ([teacher_in_db], 1, None)

        response = client.get(
            f"{config.public_prefix}/teachers",
        )
    assert response.status_code == status.HTTP_200_OK


def test_get_teachers_negative(client: TestClient, teacher_in_db: TeacherModel) -> None:
    with mock.patch.object(TeachersRepository, "get_teachers") as mock_get_subjects:
        mock_get_subjects.return_value = ([], None, "DB error")

        response = client.get(
            f"{config.public_prefix}/teachers",
        )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
