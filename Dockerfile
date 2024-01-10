FROM python:3.10-alpine3.18
LABEL maintainer='Jakub Latos'

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -r /tmp/ && \
    adduser \
        --no-create-home \
        --disabled-password \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user

