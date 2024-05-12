import unittest.mock as mock

from fastapi import status
from app.core.config import config
from fastapi.testclient import TestClient
from app.db.repositories.universities_repository import UniversitiesRepository
from app.models.university import UniversityModel


def test_get_universities_positive(
    client: TestClient, university_in_db: UniversityModel
) -> None:
    with mock.patch.object(
        UniversitiesRepository, "get_universities"
    ) as mock_get_subjects:
        mock_get_subjects.return_value = ([university_in_db], 1, None)

        response = client.get(
            f"{config.public_prefix}/universities",
        )
    assert response.status_code == status.HTTP_200_OK


def test_get_universities_negative(
    client: TestClient, university_in_db: UniversityModel
) -> None:
    with mock.patch.object(
        UniversitiesRepository, "get_universities"
    ) as mock_get_subjects:
        mock_get_subjects.return_value = ([], None, "DB error")

        response = client.get(
            f"{config.public_prefix}/universities",
        )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
