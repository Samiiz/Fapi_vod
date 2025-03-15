from app.utils.base62 import Base62


def test_base62_encode() -> None:
    assert Base62.encode(0) == "a"
    assert Base62.encode(1) == "b"
    assert Base62.encode(61) == "9"
    assert Base62.encode(62) == "ab"
    assert Base62.encode(1000) == "iq"


def test_base62_encode_negative() -> None:
    try:
        Base62.encode(-1)
    except ValueError as e:
        assert "Base62.encode() needs positive integer but you passed: -1" in str(e)
