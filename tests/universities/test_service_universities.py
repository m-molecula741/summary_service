import unittest.mock as mock

from fastapi import status
from app.core.config import config
from fastapi.testclient import TestClient
from app.db.repositories.universities_repository import UniversitiesRepository
from app.models.university import UniversityModel


def test_upload_universities_positive(
    client: TestClient, university_in_db: UniversityModel
) -> None:
    with mock.patch.object(
        UniversitiesRepository, "get_universities_ids"
    ) as mock_get_universities_ids, mock.patch.object(
        UniversitiesRepository, "bulk_add"
    ) as mock_add:
        mock_get_universities_ids.return_value = [1], None
        mock_add.return_value = [university_in_db.id], None

        with open("tests/universities/universities.csv", "rb") as file:
            files = {"file": ("university.csv", file, "text/csv")}

            response = client.post(
                f"{config.admin_prefix}/universities/upload", files=files
            )

    assert response.status_code == status.HTTP_201_CREATED


def test_upload_universities_negative(
    client: TestClient, university_in_db: UniversityModel
) -> None:
    with mock.patch.object(
        UniversitiesRepository, "get_universities_ids"
    ) as mock_get_universities_ids, mock.patch.object(
        UniversitiesRepository, "bulk_add"
    ) as mock_add:
        mock_get_universities_ids.return_value = [1], None
        mock_add.return_value = None, "DB error"

        with open("tests/universities/universities.csv", "rb") as file:
            files = {"file": ("university.csv", file, "text/csv")}

            response = client.post(
                f"{config.admin_prefix}/universities/upload", files=files
            )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
