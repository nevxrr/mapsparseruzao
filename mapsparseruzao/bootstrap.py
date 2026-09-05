from __future__ import annotations

import sys

REQUIRED_MODULES = ("requests", "openpyxl")
MIN_PYTHON = (3, 9)


def missing_dependencies() -> list[str]:
    missing: list[str] = []
    for name in REQUIRED_MODULES:
        try:
            __import__(name)
        except ImportError:
            missing.append(name)
    return missing


def python_too_old() -> bool:
    return sys.version_info < MIN_PYTHON


def install_help_text(missing: list[str] | None = None) -> str:
    names = ", ".join(missing or list(REQUIRED_MODULES))
    return (
        f"Не установлены библиотеки: {names}\n"
        "В папке проекта выполните одну команду:\n"
        "    python -m pip install -r requirements.txt\n"
        "На Windows можно просто запустить install.bat, затем run.bat."
    )


def python_help_text() -> str:
    needed = ".".join(str(part) for part in MIN_PYTHON)
    current = f"{sys.version_info.major}.{sys.version_info.minor}"
    return (
        f"Нужен Python {needed} или новее, сейчас {current}.\n"
        "Скачайте с https://www.python.org/downloads/\n"
        "При установке на Windows включите галочку «Add python.exe to PATH»."
    )


def preflight() -> str | None:
    if python_too_old():
        return python_help_text()
    missing = missing_dependencies()
    if missing:
        return install_help_text(missing)
    return None
