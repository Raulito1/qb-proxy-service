# ─────────── Build Stage ───────────
FROM python:3.10-slim AS builder

# Install Poetry
RUN pip install --no-cache-dir poetry

WORKDIR /app
# Copy only pyproject & lock to leverage Docker cache
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

# Copy your application code
COPY src ./src

# ─────────── Run Stage ───────────
FROM python:3.10-slim

WORKDIR /app
# Copy installed dependencies & code from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /app/src ./src

# Expose port and define startup command
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]