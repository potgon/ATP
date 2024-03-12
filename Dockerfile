FROM python:3.9.18-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    python3-dev \
    default-libmysqlclient-dev \
    libmariadb-dev-compat \
    pkg-config

COPY static_dependencies/ta-lib-0.4.0-src.tar.gz /tmp/ta-lib-0.4.0-src.tar.gz

RUN tar -xzf /tmp/ta-lib-0.4.0-src.tar.gz -C /tmp && \
    cd /tmp/ta-lib && \
    ./configure --prefix=/usr && \
    make && \
    make install

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/ta-lib

RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* /app/

RUN poetry lock --no-update

RUN poetry install

COPY . /app

RUN python src/manage.py collectstatic --noinput

EXPOSE 8000

CMD ["poetry", "run", "python", "src/manage.py", "runserver", "0.0.0.0:8000"]