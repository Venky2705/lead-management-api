from app.main import root


def test_root():
    result = root()

    assert result["message"] == "Lead API Running"