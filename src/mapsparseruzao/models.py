from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Company:
    name: str
    category: str
    kind: str
    district: str
    address: str
    phone: str
    email: str
    website: str
    opening_hours: str
    lat: float | None
    lon: float | None
    osm_url: str
    source: str = "OpenStreetMap"

    @property
    def has_website(self) -> bool:
        return bool(self.website.strip())

    def to_row(self) -> tuple[object, ...]:
        return (
            self.name,
            self.category,
            self.kind,
            self.district,
            self.address,
            self.phone,
            self.email,
            self.website,
            "да" if self.has_website else "нет",
            self.opening_hours,
            self.lat,
            self.lon,
            self.osm_url,
            self.source,
        )
