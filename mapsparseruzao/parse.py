from __future__ import annotations

from collections.abc import Mapping

from mapsparseruzao.constants import (
    EMAIL_KEYS,
    PHONE_KEYS,
    WEBSITE_KEYS,
    YUZAO_CITY,
    YUZAO_NAME,
)
from mapsparseruzao.models import Company

_CATEGORY_KEYS = ("shop", "office", "craft", "amenity", "tourism")


def first_tag(tags: Mapping[str, str], keys: tuple[str, ...]) -> str:
    for key in keys:
        value = (tags.get(key) or "").strip()
        if value:
            return value
    return ""


def has_website(tags: Mapping[str, str]) -> bool:
    return bool(first_tag(tags, WEBSITE_KEYS))


def format_address(tags: Mapping[str, str]) -> str:
    street = (tags.get("addr:street") or "").strip()
    house = (tags.get("addr:housenumber") or "").strip()
    street_part = " ".join(part for part in (street, house) if part)

    city = (tags.get("addr:city") or YUZAO_CITY).strip()
    suburb = (tags.get("addr:suburb") or tags.get("addr:district") or "").strip()
    postcode = (tags.get("addr:postcode") or "").strip()
    full = (tags.get("addr:full") or "").strip()

    if full:
        return full

    parts = [part for part in (postcode, city, suburb, street_part) if part]
    return ", ".join(parts)


def format_district(tags: Mapping[str, str]) -> str:
    for key in ("addr:suburb", "addr:district", "is_in:suburb"):
        value = (tags.get(key) or "").strip()
        if value:
            return value
    return YUZAO_NAME


def classify(tags: Mapping[str, str]) -> tuple[str, str]:
    for key in _CATEGORY_KEYS:
        value = (tags.get(key) or "").strip()
        if value:
            return key, value
    return "other", "unknown"


def coordinates(element: Mapping[str, object]) -> tuple[float | None, float | None]:
    if element.get("type") == "node":
        lat = element.get("lat")
        lon = element.get("lon")
        if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
            return float(lat), float(lon)

    center = element.get("center")
    if isinstance(center, Mapping):
        lat = center.get("lat")
        lon = center.get("lon")
        if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
            return float(lat), float(lon)
    return None, None


def company_from_element(element: Mapping[str, object]) -> Company | None:
    tags = element.get("tags")
    if not isinstance(tags, Mapping):
        return None

    str_tags = {str(key): str(value) for key, value in tags.items() if value is not None}
    name = (str_tags.get("name") or str_tags.get("name:ru") or "").strip() or "без названия"
    category, kind = classify(str_tags)
    lat, lon = coordinates(element)
    osm_type = str(element.get("type") or "node")
    osm_id = element.get("id")
    osm_url = f"https://www.openstreetmap.org/{osm_type}/{osm_id}" if osm_id is not None else ""

    return Company(
        name=name,
        category=category,
        kind=kind,
        district=format_district(str_tags),
        address=format_address(str_tags),
        phone=first_tag(str_tags, PHONE_KEYS),
        email=first_tag(str_tags, EMAIL_KEYS),
        website=first_tag(str_tags, WEBSITE_KEYS),
        opening_hours=(str_tags.get("opening_hours") or "").strip(),
        lat=lat,
        lon=lon,
        osm_url=osm_url,
    )


def companies_from_overpass(
    payload: Mapping[str, object],
    *,
    only_without_website: bool = True,
) -> list[Company]:
    elements = payload.get("elements")
    if not isinstance(elements, list):
        return []

    seen: set[str] = set()
    result: list[Company] = []
    for raw in elements:
        if not isinstance(raw, Mapping):
            continue
        company = company_from_element(raw)
        if company is None:
            continue
        if only_without_website and company.has_website:
            continue
        if company.osm_url in seen:
            continue
        if company.osm_url:
            seen.add(company.osm_url)
        result.append(company)
    return result
