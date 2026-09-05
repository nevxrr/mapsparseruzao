import pytest

from mapsparseruzao.constants import YUZAO_AREA_ID
from mapsparseruzao.overpass import OverpassClient, OverpassError, build_yuzao_query


def test_build_yuzao_query_uses_official_area_and_categories() -> None:
    query = build_yuzao_query(categories=("shop", "amenity"), amenities=("pharmacy", "cafe"))
    assert f"area({YUZAO_AREA_ID})->.yuzao;" in query
    assert 'nwr(area.yuzao)["shop"];' in query
    assert 'nwr(area.yuzao)["amenity"~"^(pharmacy|cafe)$"];' in query
    assert "out center tags;" in query
    assert '["office"]' not in query


def test_build_yuzao_query_rejects_empty_categories() -> None:
    with pytest.raises(ValueError):
        build_yuzao_query(categories=())


class _FakeResponse:
    def __init__(self, payload: dict, status_code: int = 200) -> None:
        self._payload = payload
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self) -> dict:
        return self._payload


class _FakeSession:
    def __init__(self, response: _FakeResponse) -> None:
        self.response = response
        self.calls: list[tuple[str, dict]] = []

    def post(self, url: str, data: dict, timeout: int, headers: dict) -> _FakeResponse:
        self.calls.append((url, data))
        return self.response


def test_overpass_client_posts_query() -> None:
    session = _FakeSession(_FakeResponse({"elements": []}))
    client = OverpassClient(url="https://example.test/interpreter", session=session, fallback_urls=())
    payload = client.query("out;")
    assert payload == {"elements": []}
    assert session.calls[0][0] == "https://example.test/interpreter"
    assert session.calls[0][1]["data"] == "out;"


def test_overpass_client_raises_after_retries(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("mapsparseruzao.overpass.time.sleep", lambda _seconds: None)

    class _FailingSession:
        def post(self, *args, **kwargs):
            raise ConnectionError("offline")

    client = OverpassClient(
        url="https://example.test/interpreter",
        session=_FailingSession(),  # type: ignore[arg-type]
        fallback_urls=(),
        max_retries=2,
    )
    with pytest.raises(OverpassError):
        client.query("out;")
