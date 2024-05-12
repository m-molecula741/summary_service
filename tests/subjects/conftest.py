import pytest

from app.models.subject import SubjectModel


@pytest.fixture(scope="function")
def subject_in_db() -> SubjectModel:
    return SubjectModel(id=1, name="test", is_moderated=True)
