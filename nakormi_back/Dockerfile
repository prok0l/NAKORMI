FROM python:3.11
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

#ARG SERVER_ADDRESS
#ARG SERVER_PORT

#RUN echo "${SERVER_ADDRESS}"

CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "makemigrations", "user"]
CMD ["python", "manage.py", "makemigrations", "point"]
CMD ["python", "manage.py", "makemigrations", "feed"]
CMD ["python", "manage.py", "migrate"]
#CMD ["python", "manage.py", "createsuperuser"]

#RUN ["python", "manage.py", "runserver", "${SERVER_ADDRESS}:${SERVER_PORT}"]
#CMD ["python", "manage.py", "runserver", ]