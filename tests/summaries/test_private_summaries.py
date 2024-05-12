import unittest.mock as mock

from fastapi import status
from fastapi.encoders import jsonable_encoder
from uuid_extensions import uuid7
from app.core.config import config
from fastapi.testclient import TestClient
from app.db.repositories.summaries_repository import SummariesRepository
from app.db.repositories.subjects_repository import SubjectsRepository
from app.db.repositories.teachers_repository import TeachersRepository
from app.models.summary import SummaryModel, SummaryRequest, SummaryUpdateRequest


def test_create_summary_positive(
    client: TestClient, summary_in_db: SummaryModel
) -> None:
    with mock.patch.object(
        SubjectsRepository, "find_one"
    ) as mock_get_subject, mock.patch.object(
        TeachersRepository, "find_one"
    ) as mock_get_teacher, mock.patch.object(
        SummariesRepository, "add"
    ) as mock_add_summary:
        mock_get_subject.return_value = summary_in_db.subject, None
        mock_get_teacher.return_value = summary_in_db.teacher, None
        mock_add_summary.return_value = summary_in_db, None

        summary = SummaryRequest(
            name="test", university_id=1, subject_id=uuid7(), teacher_id=uuid7()
        )

        response = client.post(
            f"{config.private_prefix}/summaries", json=jsonable_encoder(summary)
        )
    assert response.status_code == status.HTTP_201_CREATED


def test_create_summary_positive2(
    client: TestClient, summary_in_db: SummaryModel
) -> None:
    summary_in_db.subject.is_moderated = False
    summary_in_db.teacher.is_moderated = False
    with mock.patch.object(
        SubjectsRepository, "find_one"
    ) as mock_get_subject, mock.patch.object(
        TeachersRepository, "find_one"
    ) as mock_get_teacher, mock.patch.object(
        SummariesRepository, "add"
    ) as mock_add_summary:
        mock_get_subject.return_value = summary_in_db.subject, None
        mock_get_teacher.return_value = summary_in_db.teacher, None
        mock_add_summary.return_value = summary_in_db, None

        summary = SummaryRequest(
            name="test", university_id=1, subject_id=uuid7(), teacher_id=uuid7()
        )

        response = client.post(
            f"{config.private_prefix}/summaries", json=jsonable_encoder(summary)
        )
    assert response.status_code == status.HTTP_201_CREATED


def test_create_summary_negative(
    client: TestClient, summary_in_db: SummaryModel
) -> None:
    with mock.patch.object(
        SubjectsRepository, "find_one"
    ) as mock_get_subject, mock.patch.object(
        TeachersRepository, "find_one"
    ) as mock_get_teacher, mock.patch.object(
        SummariesRepository, "add"
    ) as mock_add_summary:
        mock_get_subject.return_value = summary_in_db.subject, None
        mock_get_teacher.return_value = summary_in_db.teacher, None
        mock_add_summary.return_value = None, "DB error"

        summary = SummaryRequest(
            name="test", university_id=1, subject_id=uuid7(), teacher_id=uuid7()
        )

        response = client.post(
            f"{config.private_prefix}/summaries", json=jsonable_encoder(summary)
        )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_summary_positive(
    client: TestClient, summary_in_db: SummaryModel
) -> None:
    with mock.patch.object(
        SummariesRepository, "find_one"
    ) as mock_get_summary, mock.patch.object(
        SubjectsRepository, "find_one"
    ) as mock_get_subject, mock.patch.object(
        TeachersRepository, "find_one"
    ) as mock_get_teacher, mock.patch.object(
        SummariesRepository, "update"
    ) as mock_update_summary:
        mock_get_summary.return_value = summary_in_db, None
        mock_get_subject.return_value = summary_in_db.subject, None
        mock_get_teacher.return_value = summary_in_db.teacher, None
        mock_update_summary.return_value = True, None

        summary = SummaryUpdateRequest(
            id=uuid7(),
            name="test",
            university_id=1,
            subject_id=uuid7(),
            teacher_id=uuid7(),
        )

        response = client.patch(
            f"{config.private_prefix}/summaries", json=jsonable_encoder(summary)
        )
    assert response.status_code == status.HTTP_200_OK


def test_update_summary_negative(
    client: TestClient, summary_in_db: SummaryModel
) -> None:
    with mock.patch.object(
        SummariesRepository, "find_one"
    ) as mock_get_summary, mock.patch.object(
        SubjectsRepository, "find_one"
    ) as mock_get_subject, mock.patch.object(
        TeachersRepository, "find_one"
    ) as mock_get_teacher, mock.patch.object(
        SummariesRepository, "update"
    ) as mock_update_summary:
        mock_get_summary.return_value = None, "DB error"
        mock_get_subject.return_value = summary_in_db.subject, None
        mock_get_teacher.return_value = summary_in_db.teacher, None
        mock_update_summary.return_value = True, None

        summary = SummaryUpdateRequest(
            id=uuid7(),
            name="test",
            university_id=1,
            subject_id=uuid7(),
            teacher_id=uuid7(),
        )

        response = client.patch(
            f"{config.private_prefix}/summaries", json=jsonable_encoder(summary)
        )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
