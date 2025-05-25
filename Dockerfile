FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH="${PYTHONPATH}:/app/Finance_application"

COPY pyproject.toml poetry.lock ./
COPY Finance_application/ ./Finance_application/

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

CMD ["sh", "-c", "alembic -c Finance_application/alembic.ini upgrade head && uvicorn Finance_application.main:main_app --host 0.0.0.0 --port 8000"]