import pytest
from uuid_extensions import uuid7

from app.models.lecture import LectureModel


@pytest.fixture(scope="function")
def lecture_in_db() -> LectureModel:
    return LectureModel(
        id=uuid7(),
        name="test",
        description="test",
        pdf_file_url="https://fake.ru",
        date="2024-05-03",
        video_url=None,
        summary_id=uuid7(),
    )
