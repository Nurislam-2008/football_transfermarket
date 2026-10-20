#!/usr/bin/env bash
# Выход при ошибке
set -o errexit

# Установка зависимостей
pip install -r requirements.txt

# Сбор статики
python manage.py collectstatic --no-input

# Применение миграций к базе данных
python manage.py migrate