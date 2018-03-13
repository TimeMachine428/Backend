FROM python:3.5

ADD requirements.txt /app/
WORKDIR /app/
RUN pip install -r requirements.txt

ADD timemachine/ /app
RUN python manage.py collectstatic --no-input
CMD python manage.py runserver 0.0.0.0:80
