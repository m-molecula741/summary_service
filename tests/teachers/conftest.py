import pytest
from uuid_extensions import uuid7

from app.models.teacher import TeacherModel


@pytest.fixture(scope="function")
def teacher_in_db() -> TeacherModel:
    return TeacherModel(
        id=uuid7(), full_name="test", date_birth="2024-05-10", is_moderated=True
    )
