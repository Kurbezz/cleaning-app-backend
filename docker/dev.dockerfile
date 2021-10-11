FROM python:3.10-slim as build-image

ENV VENV_PATH=/opt/venv

RUN apt-get update \
    && apt-get install --no-install-recommends -y gcc build-essential python3-dev libpq-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN python -m venv $VENV_PATH \
    && pip install -r /app/requirements.txt --no-cache-dir


FROM build-image as runtime-image

WORKDIR /app

COPY --from=build-image $VENV_PATH $VENV_PATH
ENV PATH="$VENV_PATH/bin:$PATH"

EXPOSE 8080

CMD bash ./start.sh
