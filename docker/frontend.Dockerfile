FROM python:3.10-slim

WORKDIR /workspace

# Install runtime dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy only frontend to keep image focused
COPY frontend/ ./frontend

EXPOSE 8501

ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    API_BASE_URL=http://backend:8000

CMD ["streamlit", "run", "frontend/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /workspace

COPY pyproject.toml poetry.lock* /workspace/

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction

COPY . /workspace

EXPOSE 8501

CMD ["streamlit", "run", "frontend/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
