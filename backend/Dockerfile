# Use official Python image
FROM python:3.14-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create directories
RUN mkdir -p staticfiles media logs

# Production settings for collectstatic
ENV DJANGO_SETTINGS_MODULE=config.settings.production

# Collect static files
RUN python manage.py collectstatic --noinput

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Railway exposes PORT=8080 automatically
EXPOSE 8080

ENTRYPOINT ["/app/entrypoint.sh"]