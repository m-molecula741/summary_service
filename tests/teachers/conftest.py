import pytest
from uuid_extensions import uuid7

from app.models.teacher import TeacherModel


@pytest.fixture(scope="function")
def teacher_in_db() -> TeacherModel:
    return TeacherModel(id=uuid7(), full_name="test", is_moderated=True)
