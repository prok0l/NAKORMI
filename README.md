# NAKORMI BOT


### Cтарт проекта:
- установка зависимостей
    ```bash
        pip install -r nakormi_back/requirements.txt
        pip install -r nakormi_bot/requirements.txt
    ```
- создание .env файла (/nakormi_back/)
    ```dotenv
    DB_NAME=
    DB_USER=
    DB_PASSWORD=
    DB_ADDRESS=
    DB_PORT=
    
    SERVER_ADDRESS=
    SERVER_PORT=
    RANDOM_SECRET=
    
    DEBUG=False
    ```

- создание .env файла (/nakormi_bot/)
    ```dotenv
    API_KEY=
    BOT_TOKEN=
    API_ADDRESS=
    ```
- запуск api (/nakormi_back/)
    ```bash
        python manage.py migrate
        python manage.py createsuperuser
        python manage.py runserver
    ```

- запуск бота
    ```bash
        pip install -r requirements.txt
        python -m nakormi_bot
    ```