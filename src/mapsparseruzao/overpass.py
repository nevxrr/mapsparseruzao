from __future__ import annotations

import time
from collections.abc import Iterable, Sequence

import requests

from mapsparseruzao.constants import (
    DEFAULT_AMENITIES,
    DEFAULT_OVERPASS_URL,
    DEFAULT_TOURISM,
    FALLBACK_OVERPASS_URLS,
    YUZAO_AREA_ID,
)


class OverpassError(RuntimeError):
    """Overpass недоступен или вернул ошибку."""


def build_yuzao_query(
    *,
    area_id: int = YUZAO_AREA_ID,
    categories: Sequence[str] = ("shop", "office", "craft", "amenity", "tourism"),
    amenities: Sequence[str] = DEFAULT_AMENITIES,
    tourism: Sequence[str] = DEFAULT_TOURISM,
    timeout: int = 180,
) -> str:
    """Собирает Overpass QL по официальной границе ЮЗАО."""
    clauses: list[str] = []
    selected = {item.strip().lower() for item in categories}

    if "shop" in selected:
        clauses.append('  nwr(area.yuzao)["shop"];')
    if "office" in selected:
        clauses.append('  nwr(area.yuzao)["office"];')
    if "craft" in selected:
        clauses.append('  nwr(area.yuzao)["craft"];')
    if "amenity" in selected and amenities:
        joined = "|".join(amenities)
        clauses.append(f'  nwr(area.yuzao)["amenity"~"^({joined})$"];')
    if "tourism" in selected and tourism:
        joined = "|".join(tourism)
        clauses.append(f'  nwr(area.yuzao)["tourism"~"^({joined})$"];')

    if not clauses:
        raise ValueError("Нужно выбрать хотя бы одну категорию: shop, office, craft, amenity, tourism")

    body = "\n".join(clauses)
    return (
        f"[out:json][timeout:{timeout}];\n"
        f"area({area_id})->.yuzao;\n"
        "(\n"
        f"{body}\n"
        ");\n"
        "out center tags;"
    )


class OverpassClient:
    def __init__(
        self,
        url: str = DEFAULT_OVERPASS_URL,
        *,
        fallback_urls: Sequence[str] = FALLBACK_OVERPASS_URLS,
        request_timeout: int = 180,
        session: requests.Session | None = None,
        max_retries: int = 3,
    ) -> None:
        self.urls = (url, *tuple(item for item in fallback_urls if item != url))
        self.request_timeout = request_timeout
        self.session = session or requests.Session()
        self.max_retries = max_retries

    def query(self, ql: str) -> dict:
        last_error: Exception | None = None
        for url in self.urls:
            for attempt in range(self.max_retries):
                try:
                    response = self.session.post(
                        url,
                        data={"data": ql},
                        timeout=self.request_timeout,
                        headers={"User-Agent": "mapsparseruzao/1.0 (YUZAO OSM research)"},
                    )
                    if response.status_code in {429, 504, 502}:
                        time.sleep(2 ** attempt)
                        continue
                    response.raise_for_status()
                    payload = response.json()
                    if not isinstance(payload, dict):
                        raise OverpassError("Overpass вернул не JSON-объект")
                    return payload
                except (requests.RequestException, ValueError, OSError) as exc:
                    last_error = exc
                    time.sleep(2 ** attempt)
            last_error = last_error or OverpassError(f"Не удалось запросить {url}")
        raise OverpassError(f"Все зеркала Overpass недоступны: {last_error}") from last_error

    def fetch_yuzao(
        self,
        *,
        categories: Iterable[str] = ("shop", "office", "craft", "amenity", "tourism"),
        amenities: Sequence[str] = DEFAULT_AMENITIES,
        tourism: Sequence[str] = DEFAULT_TOURISM,
    ) -> dict:
        ql = build_yuzao_query(
            categories=tuple(categories),
            amenities=amenities,
            tourism=tourism,
        )
        return self.query(ql)
