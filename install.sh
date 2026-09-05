#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if command -v python3 >/dev/null 2>&1; then
  python3 -m pip install -r requirements.txt
elif command -v python >/dev/null 2>&1; then
  python -m pip install -r requirements.txt
else
  echo "Не найден Python 3. Установите python3 и pip." >&2
  exit 1
fi

echo
echo "Готово. Запуск: python3 run.py"
