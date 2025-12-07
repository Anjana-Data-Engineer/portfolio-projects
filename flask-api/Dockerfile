# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# copy only needed files
COPY . .

# Ensure migrations folder exists (if running migrations later)
RUN mkdir -p migrations

EXPOSE 8000

CMD ["gunicorn", "app:create_app()", "--bind", "0.0.0.0:8000", "--workers", "2", "--worker-class", "gthread"]
