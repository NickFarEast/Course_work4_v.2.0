FROM python:3.9-slim-bullseye



WORKDIR /code
COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
COPY game game