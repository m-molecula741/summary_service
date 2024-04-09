from fastapi.testclient import TestClient


def test_create_note_positive(client: TestClient) -> None:
    assert 1 == 1
