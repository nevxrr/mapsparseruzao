from __future__ import annotations

import argparse
import sys
from pathlib import Path

from mapsparseruzao.bootstrap import preflight
from mapsparseruzao.constants import DEFAULT_AMENITIES, DEFAULT_OVERPASS_URL
from mapsparseruzao.overpass import OverpassClient, OverpassError
from mapsparseruzao.parse import companies_from_overpass
from mapsparseruzao.xlsx_export import export_xlsx


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Скачивает компании ЮЗАО (Москва) из OpenStreetMap и сохраняет "
            "в .xlsx тех, у кого не указан сайт."
        )
    )
    parser.add_argument(
        "-o",
        "--output",
        default="yuzao-companies-no-website.xlsx",
        help="Путь к .xlsx (по умолчанию yuzao-companies-no-website.xlsx)",
    )
    parser.add_argument(
        "--categories",
        default="shop,office,craft,amenity,tourism",
        help="Категории через запятую: shop,office,craft,amenity,tourism",
    )
    parser.add_argument(
        "--amenities",
        default=",".join(DEFAULT_AMENITIES),
        help="Список amenity через запятую",
    )
    parser.add_argument(
        "--include-with-website",
        action="store_true",
        help="Не отфильтровывать компании, у которых сайт указан",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Ограничить число строк в таблице (0 = без ограничения)",
    )
    parser.add_argument(
        "--overpass-url",
        default=DEFAULT_OVERPASS_URL,
        help="URL интерпретатора Overpass",
    )
    return parser


def run(argv: list[str] | None = None) -> int:
    problem = preflight()
    if problem:
        print(problem, file=sys.stderr)
        return 2

    args = build_parser().parse_args(argv)
    categories = [item.strip() for item in args.categories.split(",") if item.strip()]
    amenities = [item.strip() for item in args.amenities.split(",") if item.strip()]
    only_without_website = not args.include_with_website

    client = OverpassClient(url=args.overpass_url)
    try:
        payload = client.fetch_yuzao(categories=categories, amenities=amenities)
    except OverpassError as exc:
        print(f"Ошибка Overpass: {exc}", file=sys.stderr)
        return 1

    companies = companies_from_overpass(payload, only_without_website=only_without_website)
    companies.sort(key=lambda item: (item.district, item.category, item.name.casefold()))
    if args.limit and args.limit > 0:
        companies = companies[: args.limit]

    path = export_xlsx(companies, Path(args.output))
    mode = "без сайта" if only_without_website else "все найденные"
    print(f"Сохранено {len(companies)} компаний ({mode}) → {path.resolve()}")
    return 0


def main() -> None:
    sys.exit(run())
