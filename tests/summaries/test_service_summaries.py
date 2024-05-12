import unittest.mock as mock

from fastapi import status
from fastapi.encoders import jsonable_encoder
from uuid_extensions import uuid7
from app.core.config import config
from fastapi.testclient import TestClient
from app.db.repositories.summaries_repository import SummariesRepository
from app.db.repositories.subjects_repository import SubjectsRepository
from app.db.repositories.teachers_repository import TeachersRepository
from app.models.summary import SummaryChangeStatusRequest, SummaryModel


def test_set_approved_summary_status_positive(
    client: TestClient, summary_in_db: SummaryModel
) -> None:
    with mock.patch.object(
        SummariesRepository, "update"
    ) as mock_update_summary, mock.patch.object(
        SummariesRepository, "find_one"
    ) as mock_get_summary, mock.patch.object(
        SubjectsRepository, "update"
    ) as mock_update_subject, mock.patch.object(
        TeachersRepository, "update"
    ) as mock_update_teacher:
        mock_update_summary.return_value = True, None
        mock_get_summary.return_value = summary_in_db, None
        mock_update_subject.return_value = summary_in_db.subject, None
        mock_update_teacher.return_value = summary_in_db.teacher, None

        summary = SummaryChangeStatusRequest(id=uuid7(), modearation_comment="test")

        response = client.patch(
            f"{config.admin_prefix}/summaries/status/approved",
            json=jsonable_encoder(summary),
        )
    assert response.status_code == status.HTTP_200_OK


def test_set_approved_summary_status_negative(
    client: TestClient, summary_in_db: SummaryModel
) -> None:
    with mock.patch.object(
        SummariesRepository, "update"
    ) as mock_update_summary, mock.patch.object(
        SummariesRepository, "find_one"
    ) as mock_get_summary, mock.patch.object(
        SubjectsRepository, "update"
    ) as mock_update_subject, mock.patch.object(
        TeachersRepository, "update"
    ) as mock_update_teacher:
        mock_update_summary.return_value = None, "DB error"
        mock_get_summary.return_value = summary_in_db, None
        mock_update_subject.return_value = summary_in_db.subject, None
        mock_update_teacher.return_value = summary_in_db.teacher, None

        summary = SummaryChangeStatusRequest(id=uuid7(), modearation_comment="test")

        response = client.patch(
            f"{config.admin_prefix}/summaries/status/approved",
            json=jsonable_encoder(summary),
        )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_set_rejected_summary_status_positive(
    client: TestClient, summary_in_db: SummaryModel
) -> None:
    with mock.patch.object(
        SummariesRepository, "update"
    ) as mock_update_summary, mock.patch.object(
        SummariesRepository, "find_one"
    ) as mock_get_summary, mock.patch.object(
        SubjectsRepository, "update"
    ) as mock_update_subject, mock.patch.object(
        TeachersRepository, "update"
    ) as mock_update_teacher:
        mock_update_summary.return_value = True, None
        mock_get_summary.return_value = summary_in_db, None
        mock_update_subject.return_value = summary_in_db.subject, None
        mock_update_teacher.return_value = summary_in_db.teacher, None

        summary = SummaryChangeStatusRequest(id=uuid7(), modearation_comment="test")

        response = client.patch(
            f"{config.admin_prefix}/summaries/status/rejected",
            json=jsonable_encoder(summary),
        )
    assert response.status_code == status.HTTP_200_OK


def test_set_rejected_summary_status_negative(
    client: TestClient, summary_in_db: SummaryModel
) -> None:
    with mock.patch.object(
        SummariesRepository, "update"
    ) as mock_update_summary, mock.patch.object(
        SummariesRepository, "find_one"
    ) as mock_get_summary, mock.patch.object(
        SubjectsRepository, "update"
    ) as mock_update_subject, mock.patch.object(
        TeachersRepository, "update"
    ) as mock_update_teacher:
        mock_update_summary.return_value = None, "DB error"
        mock_get_summary.return_value = summary_in_db, None
        mock_update_subject.return_value = summary_in_db.subject, None
        mock_update_teacher.return_value = summary_in_db.teacher, None

        summary = SummaryChangeStatusRequest(id=uuid7(), modearation_comment="test")

        response = client.patch(
            f"{config.admin_prefix}/summaries/status/rejected",
            json=jsonable_encoder(summary),
        )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
