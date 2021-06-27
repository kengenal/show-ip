FROM python:3.8.10-alpine3.13

ENV PYTHONUNBUFFERED=1
ENV DEBUG=1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

RUN apk add --no-cache \
    gcc \
    libc-dev \
    libffi-dev \
    python3-dev \
    musl-dev \
    mariadb-dev

RUN mkdir -p /app
RUN adduser -Ds /bin/bash django
RUN chown -R django:django /app
RUN chmod 755 /app

RUN pip install -U pip
RUN pip install poetry

COPY ./pyproject.toml pyproject.toml

RUN poetry config virtualenvs.create false \
    && poetry install

RUN pip install gunicorn

COPY --chown=django:django ./build/python-prod/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

USER django

WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["sh", "/entrypoint"]
