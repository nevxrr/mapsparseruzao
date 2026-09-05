from mapsparseruzao.parse import (
    companies_from_overpass,
    company_from_element,
    format_address,
    has_website,
)


def test_has_website_accepts_contact_website() -> None:
    assert has_website({"contact:website": "https://example.ru"})
    assert not has_website({"name": "Кафе"})
    assert not has_website({"website": "   "})


def test_format_address_prefers_full_then_parts() -> None:
    assert format_address({"addr:full": "Москва, ул. Профсоюзная, 1"}) == "Москва, ул. Профсоюзная, 1"
    assert (
        format_address(
            {
                "addr:postcode": "117292",
                "addr:city": "Москва",
                "addr:suburb": "Академический",
                "addr:street": "улица Кедрова",
                "addr:housenumber": "5",
            }
        )
        == "117292, Москва, Академический, улица Кедрова 5"
    )


def test_company_from_element_reads_node_and_center() -> None:
    company = company_from_element(
        {
            "type": "node",
            "id": 1,
            "lat": 55.65,
            "lon": 37.55,
            "tags": {
                "name": "Пекарня",
                "shop": "bakery",
                "phone": "+7 495 000-00-00",
            },
        }
    )
    assert company is not None
    assert company.name == "Пекарня"
    assert company.category == "shop"
    assert company.kind == "bakery"
    assert company.phone == "+7 495 000-00-00"
    assert company.has_website is False
    assert company.osm_url == "https://www.openstreetmap.org/node/1"

    way = company_from_element(
        {
            "type": "way",
            "id": 9,
            "center": {"lat": 55.6, "lon": 37.5},
            "tags": {"office": "company", "name": "ООО Ромашка", "website": "https://romashka.ru"},
        }
    )
    assert way is not None
    assert way.lat == 55.6
    assert way.has_website is True


def test_companies_from_overpass_filters_and_deduplicates() -> None:
    payload = {
        "elements": [
            {
                "type": "node",
                "id": 1,
                "lat": 55.65,
                "lon": 37.55,
                "tags": {"name": "Без сайта", "shop": "hairdresser"},
            },
            {
                "type": "node",
                "id": 1,
                "lat": 55.65,
                "lon": 37.55,
                "tags": {"name": "Дубль", "shop": "hairdresser"},
            },
            {
                "type": "node",
                "id": 2,
                "lat": 55.66,
                "lon": 37.56,
                "tags": {"name": "С сайтом", "shop": "beauty", "website": "https://a.ru"},
            },
        ]
    }
    only_missing = companies_from_overpass(payload, only_without_website=True)
    assert [item.name for item in only_missing] == ["Без сайта"]

    everyone = companies_from_overpass(payload, only_without_website=False)
    assert {item.name for item in everyone} == {"Без сайта", "С сайтом"}
