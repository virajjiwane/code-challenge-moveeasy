FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
CMD [ "touch", "weatherproject/db.sqlite3" ]

RUN python weatherproject/manage.py migrate

EXPOSE 8000