import pytest

from app.models.university import UniversityModel


@pytest.fixture(scope="function")
def university_in_db() -> UniversityModel:
    return UniversityModel(id=1, name="test", short_name="test")
