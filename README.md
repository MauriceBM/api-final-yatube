# api_final
api final

# Технологии

Python 3.10+
Django 4.x
Django REST Framework
SimpleJWT (для аутентификации)
django-filter (для фильтрации и поиска)
SQLite (база данных по умолчанию)

# Cоздать и активировать виртуальное окружение:

python -m venv env
source env/Scripts/activate

# Установить зависимости из файла requirements.txt:

python -m pip install --upgrade pip
pip install -r requirements.txt

# Выполнить миграции:
cd yatube_api
python manage.py migrate

# Запустить проект:
python manage.py runserver
