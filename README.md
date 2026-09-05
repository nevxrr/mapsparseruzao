# Парсер компаний ЮЗАО без сайта → Excel

Скачивает компании Юго-Западного округа Москвы (открытые данные OpenStreetMap) и сохраняет в `.xlsx` те, у кого **не указан сайт**.

Ключ Яндекса, аккаунт и `pip install -e` не нужны.

## Установка и запуск

Нужен [Python 3.9+](https://www.python.org/downloads/). На Windows при установке включите галочку **Add python.exe to PATH**.

Скачайте репозиторий: кнопка **Code → Download ZIP**, распакуйте. Или:

```bash
git clone https://github.com/nevxrr/mapsparseruzao.git
cd mapsparseruzao
```

### Windows

1. Дважды нажмите `install.bat`
2. Дважды нажмите `run.bat`
3. В этой же папке появится файл `yuzao-companies-no-website.xlsx`

Из командной строки то же самое:

```bat
python -m pip install -r requirements.txt
python run.py
```

### Linux / macOS

```bash
python3 -m pip install -r requirements.txt
python3 run.py
```

или `./install.sh`, затем `python3 run.py`.

Готово. Пакет в режиме разработки, venv и `pyproject.toml` для обычного запуска не требуются.

## Если пишет, что нет модуля или конфига

Вы в папке без файлов `run.py` и `requirements.txt`. На ветке `main` должен быть весь проект, не пустой README.

Проверьте, что рядом с вами лежат:

- `run.py`
- `requirements.txt`
- `install.bat` / `run.bat`
- папка `mapsparseruzao`

Потом снова:

```bat
python -m pip install -r requirements.txt
python run.py
```

Не запускайте `pip install -e ".[dev]"` — это было для разработки и на части ноутбуков падает.

## Параметры

| Флаг | Смысл |
| --- | --- |
| `-o`, `--output` | путь к `.xlsx` |
| `--categories` | `shop,office,craft,amenity,tourism` |
| `--amenities` | список amenity через запятую |
| `--include-with-website` | оставить и компании с сайтом |
| `--limit N` | обрезать таблицу до N строк |

Пример быстрой проверки (аптеки, 20 строк):

```bat
python run.py --categories amenity --amenities pharmacy --limit 20 -o sample.xlsx
```

Полный обход округа может занять 1–3 минуты: запрос идёт в публичный Overpass. Если одно зеркало не отвечает, пробуются запасные.

## Ограничение данных

«Нет сайта» значит, что в OpenStreetMap не заполнены теги `website` / `contact:website`. Это не выгрузка Яндекс.Карт.

JS API Яндекс Карт [не умеет легально сохранять справочник в Excel](https://yandex.ru/legal/maps_api/). Здесь используется граница ЮЗАО в OSM: [relation 1304596](https://www.openstreetmap.org/relation/1304596). Данные © участники OpenStreetMap, [ODbL](https://www.openstreetmap.org/copyright).
