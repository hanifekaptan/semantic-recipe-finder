FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install runtime dependencies from requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.10

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN pip install --upgrade pip && pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
