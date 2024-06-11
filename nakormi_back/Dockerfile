FROM python:3.11
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "makemigrations", "user"]
CMD ["python", "manage.py", "makemigrations", "point"]
CMD ["python", "manage.py", "makemigrations", "feed"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "createsuperuser"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["python", "main.py"]