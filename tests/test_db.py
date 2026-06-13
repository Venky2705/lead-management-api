from app.main import db_check


def test_db_check():

    result = db_check()

    assert "postgres_version" in result