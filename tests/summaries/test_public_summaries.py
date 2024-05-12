import unittest.mock as mock

from fastapi import status
from uuid_extensions import uuid7
from app.core.config import config
from fastapi.testclient import TestClient
from app.db.repositories.summaries_repository import SummariesRepository
from app.models.summary import SummaryModel


def test_get_summaries_positive(
    client: TestClient, summary_in_db: SummaryModel
) -> None:
    with mock.patch.object(SummariesRepository, "get_summaries") as mock_get_summaries:
        mock_get_summaries.return_value = ([summary_in_db], 1, None)

        response = client.get(
            f"{config.public_prefix}/summaries",
        )
    assert response.status_code == status.HTTP_200_OK


def test_get_summaries_negative(
    client: TestClient, summary_in_db: SummaryModel
) -> None:
    with mock.patch.object(SummariesRepository, "get_summaries") as mock_get_summaries:
        mock_get_summaries.return_value = ([], None, "DB error")

        response = client.get(
            f"{config.public_prefix}/summaries",
        )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_summary_by_id_positive(
    client: TestClient, summary_in_db: SummaryModel
) -> None:
    with mock.patch.object(SummariesRepository, "find_summary") as mock_get_summaries:
        mock_get_summaries.return_value = summary_in_db, None

        summary_id = uuid7()

        response = client.get(
            f"{config.public_prefix}/summaries/{summary_id}",
        )
    assert response.status_code == status.HTTP_200_OK


def test_get_summary_by_id_negative(
    client: TestClient, summary_in_db: SummaryModel
) -> None:
    with mock.patch.object(SummariesRepository, "find_summary") as mock_get_summaries:
        mock_get_summaries.return_value = None, "DB error"

        summary_id = uuid7()

        response = client.get(
            f"{config.public_prefix}/summaries/{summary_id}",
        )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
