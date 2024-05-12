import unittest.mock as mock

from fastapi import status
from app.core.config import config
from fastapi.testclient import TestClient
from app.db.repositories.subjects_repository import SubjectsRepository
from app.models.subject import SubjectModel


def test_get_subjects_positive(client: TestClient, subject_in_db: SubjectModel) -> None:
    with mock.patch.object(SubjectsRepository, "get_subjects") as mock_get_subjects:
        mock_get_subjects.return_value = ([subject_in_db], 1, None)

        response = client.get(
            f"{config.public_prefix}/subjects",
        )
    assert response.status_code == status.HTTP_200_OK


def test_get_subjects_negative(client: TestClient, subject_in_db: SubjectModel) -> None:
    with mock.patch.object(SubjectsRepository, "get_subjects") as mock_get_subjects:
        mock_get_subjects.return_value = ([], None, "DB error")

        response = client.get(
            f"{config.public_prefix}/subjects",
        )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
