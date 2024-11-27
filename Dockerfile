FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements2.txt /app/
RUN pip install -r requirements2.txt

COPY . /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]