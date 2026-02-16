FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc libpq-dev g++ libgeos-dev proj-bin libproj-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install poetry

RUN touch README.md
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root
WORKDIR /app

COPY /alembic ./alembic
COPY /pin_voyage ./pin_voyage
COPY .env alembic.ini ./
EXPOSE 8000

CMD ["uvicorn", "pin_voyage.main:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["python", "database.py"]
