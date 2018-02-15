FROM python:3.5

ADD . /app
WORKDIR /app/timemachine

RUN pip install -r ../requirements.txt
CMD python manage.py runserver 0.0.0.0:80
