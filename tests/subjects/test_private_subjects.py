import unittest.mock as mock

from fastapi import status
from app.core.config import config
from fastapi.testclient import TestClient
from app.db.repositories.subjects_repository import SubjectsRepository
from app.models.subject import SubjectModel


def test_add_subject_positive(client: TestClient, subject_in_db: SubjectModel) -> None:
    with mock.patch.object(
        SubjectsRepository, "find_one"
    ) as mock_find_one, mock.patch.object(SubjectsRepository, "add") as mock_add:
        mock_find_one.return_value = None, "Data not found"
        mock_add.return_value = subject_in_db, None

        response = client.post(
            f"{config.private_prefix}/subjects",
            json={"name": "test"},
        )
    assert response.status_code == status.HTTP_201_CREATED


def test_add_subject_negative(client: TestClient, subject_in_db: SubjectModel) -> None:
    with mock.patch.object(
        SubjectsRepository, "find_one"
    ) as mock_find_one, mock.patch.object(SubjectsRepository, "add") as mock_add:
        mock_find_one.return_value = None, "DB error"
        mock_add.return_value = subject_in_db, None

        response = client.post(
            f"{config.private_prefix}/subjects",
            json={"name": "test"},
        )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
