FROM python:3.11-slim

RUN pip install poetry


RUN apt-get update && apt-get install -y \
    gcc libpq-dev g++ libgeos-dev proj-bin libproj-dev && \
    rm -rf /var/lib/apt/lists/*

RUN touch README.md
COPY pyproject.toml .
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root
WORKDIR /app
COPY /pin_voyage .
COPY .env .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["python", "database.py"]
