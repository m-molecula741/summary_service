import unittest.mock as mock

from fastapi import status
from app.core.config import config
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from uuid_extensions import uuid7
from app.db.repositories.lectures_repository import LecturesRepository
from app.models.lecture import LectureCreateRequest, LectureModel, LectureUpdateRequest


def test_add_lecture_positive(client: TestClient, lecture_in_db: LectureModel) -> None:
    with mock.patch.object(LecturesRepository, "add") as mock_add:
        mock_add.return_value = lecture_in_db, None

        lecture_for_add = LectureCreateRequest(
            name="test",
            description="test",
            pdf_file_url="https://fake.ru",
            video_url=None,
            date="2024-05-03",
            summary_id=uuid7(),
        )

        response = client.post(
            f"{config.private_prefix}/lectures", json=jsonable_encoder(lecture_for_add)
        )
    assert response.status_code == status.HTTP_201_CREATED


def test_add_lecture_negative(client: TestClient, lecture_in_db: LectureModel) -> None:
    with mock.patch.object(LecturesRepository, "add") as mock_add:
        mock_add.return_value = None, "DB error"

        lecture_for_add = LectureCreateRequest(
            name="test",
            description="test",
            pdf_file_url="https://fake.ru",
            video_url=None,
            date="2024-05-03",
            summary_id=uuid7(),
        )

        response = client.post(
            f"{config.private_prefix}/lectures", json=jsonable_encoder(lecture_for_add)
        )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_lecture_positive(
    client: TestClient, lecture_in_db: LectureModel
) -> None:
    with mock.patch.object(LecturesRepository, "update") as mock_upd:
        mock_upd.return_value = True, None

        lecture_for_upd = LectureUpdateRequest(
            id=uuid7(),
            name="test",
            description="test",
            pdf_file_url="https://fake.ru",
            video_url=None,
            date="2024-05-03",
            summary_id=uuid7(),
        )

        response = client.patch(
            f"{config.private_prefix}/lectures", json=jsonable_encoder(lecture_for_upd)
        )

    assert response.status_code == status.HTTP_200_OK


def test_update_lecture_negative(
    client: TestClient, lecture_in_db: LectureModel
) -> None:
    with mock.patch.object(LecturesRepository, "update") as mock_upd:
        mock_upd.return_value = False, "DB error"

        lecture_for_upd = LectureUpdateRequest(
            id=uuid7(),
            name="test",
            description="test",
            pdf_file_url="https://fake.ru",
            video_url=None,
            date="2024-05-03",
            summary_id=uuid7(),
        )

        response = client.patch(
            f"{config.private_prefix}/lectures", json=jsonable_encoder(lecture_for_upd)
        )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_delete_lecture_positive(client: TestClient) -> None:
    with mock.patch.object(LecturesRepository, "delete") as mock_delete:
        mock_delete.return_value = True, None

        lecture_id = uuid7()

        response = client.delete(f"{config.private_prefix}/lectures/{lecture_id}")
    assert response.status_code == status.HTTP_200_OK


def test_delete_lecture_negative(client: TestClient) -> None:
    with mock.patch.object(LecturesRepository, "delete") as mock_delete:
        mock_delete.return_value = False, "DB error"

        lecture_id = uuid7()

        response = client.delete(f"{config.private_prefix}/lectures/{lecture_id}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
