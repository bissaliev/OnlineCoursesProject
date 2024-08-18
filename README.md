
# Тестовое задание Django/Backend

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

Проект представляет собой площадку для размещения онлайн-курсов с набором уроков. Доступ к урокам предоставляется после покупки курса (подписки). Внутри курса студенты автоматически распределяются по группам.

## __Установка на локальном компьютере__

1. Клонируйте репозиторий:

    ```bash
    git clone git@github.com:bissaliev/OnlineCoursesProject.git
    ```

2. Установите и активируйте виртуальное окружение:

    ```bash
    python -m venv venv
    source venv/Scripts/activate  - для Windows
    source venv/bin/activate - для Linux
    ```

3. Установите зависимости:

    ```bash
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. Перейдите в папку product и выполните миграции:

    ```bash
    cd product
    python manage.py migrate
    ```

5. Создайте суперпользователя:

    ```bash
    python manage.py createsuperuser
    ```

6. Загрузить фикстуры:

    ```bash
    python manage.py load_fixtures
    ```

7. Запустите проект:

    ```bash
    python manage.py runserver
    ```

### __OpenAPI документация__

* Swagger: http://127.0.0.1:8000/api/v1/swagger/
* ReDoc: http://127.0.0.1:8000/api/v1/redoc/

### __Технологии__

* [Python 3.10.12](https://www.python.org/doc/)
* [Django 4.2.10](https://docs.djangoproject.com/en/4.2/)
* [Django REST Framework  3.14.0](https://www.django-rest-framework.org/)
* [Djoser  2.2.0](https://djoser.readthedocs.io/en/latest/getting_started.html)

### __Автор__

[Биссалиев Олег](https://github.com/bissaliev)
