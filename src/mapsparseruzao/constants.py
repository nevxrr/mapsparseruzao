"""Граница ЮЗАО и набор коммерческих объектов для поиска."""

# https://www.openstreetmap.org/relation/1304596
# area id в Overpass = 3600000000 + relation id
YUZAO_RELATION_ID = 1304596
YUZAO_AREA_ID = 3_600_000_000 + YUZAO_RELATION_ID
YUZAO_NAME = "Юго-Западный административный округ"
YUZAO_CITY = "Москва"

DEFAULT_OVERPASS_URL = "https://overpass-api.de/api/interpreter"
FALLBACK_OVERPASS_URLS = (
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.openstreetmap.ru/api/interpreter",
)

# Коммерческие amenity, которые обычно ведут бизнес и могут иметь сайт.
DEFAULT_AMENITIES = (
    "arts_centre",
    "bank",
    "bar",
    "beauty",
    "bureau_de_change",
    "cafe",
    "car_rental",
    "car_repair",
    "car_wash",
    "cinema",
    "clinic",
    "community_centre",
    "coworking_space",
    "dentist",
    "doctors",
    "fast_food",
    "fuel",
    "hospital",
    "internet_cafe",
    "marketplace",
    "nightclub",
    "pharmacy",
    "post_office",
    "pub",
    "restaurant",
    "studio",
    "theatre",
    "veterinary",
)

DEFAULT_TOURISM = (
    "guest_house",
    "hostel",
    "hotel",
    "motel",
)

WEBSITE_KEYS = (
    "website",
    "contact:website",
    "url",
    "contact:url",
)

PHONE_KEYS = ("phone", "contact:phone", "mobile", "contact:mobile")
EMAIL_KEYS = ("email", "contact:email")

XLSX_HEADERS = (
    "Название",
    "Категория",
    "Тип",
    "Район / округ",
    "Адрес",
    "Телефон",
    "Email",
    "Сайт",
    "Есть сайт",
    "Часы работы",
    "Широта",
    "Долгота",
    "OSM URL",
    "Источник",
)
