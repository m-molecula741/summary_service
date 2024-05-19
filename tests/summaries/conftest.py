import pytest
from uuid_extensions import uuid7

from app.models.enums.status import Status
from app.models.subject import SubjectModel
from app.models.summary import SummaryModel
from app.models.teacher import TeacherModel
from app.models.university import UniversityModel


@pytest.fixture(scope="function")
def summary_in_db() -> SummaryModel:
    return SummaryModel(
        id=uuid7(),
        name="test",
        university_id=uuid7(),
        subject_id=uuid7(),
        teacher_id=uuid7(),
        status=Status.approved,
        moderation_comment="test",
        user_id=uuid7(),
        university=UniversityModel(id=1, name="test", short_name="test"),
        subject=SubjectModel(id=1, name="test", is_moderated=True),
        teacher=TeacherModel(id=uuid7(), full_name="test", is_moderated=True),
    )
