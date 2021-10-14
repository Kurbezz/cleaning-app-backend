FROM python:3.10-slim as build-image

ENV VENV_PATH=/opt/venv

RUN apt-get update \
    && apt-get install --no-install-recommends -y gcc build-essential python3-dev libpq-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root/poetry
COPY pyproject.toml poetry.lock /root/poetry/
RUN python -m venv $VENV_PATH \
    && . /opt/venv/bin/activate \
    && pip install poetry --no-cache-dir \
    && poetry install

FROM build-image as runtime-image

WORKDIR /app

COPY --from=build-image $VENV_PATH $VENV_PATH
ENV PATH="$VENV_PATH/bin:$PATH"

EXPOSE 8080

CMD bash /root/start.sh
