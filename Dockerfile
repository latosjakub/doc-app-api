FROM python:3.10-alpine3.18
LABEL maintainer='Jakub Latos'

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV="true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt; \
        fi && \
    rm -r /tmp/ && \
    apk del .tmp-build-deps && \
    adduser \
        --no-create-home \
        --disabled-password \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user

