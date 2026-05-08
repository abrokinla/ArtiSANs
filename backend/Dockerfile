FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# system deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

# install pip requirements
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r /app/requirements.txt

# copy project
COPY . /app

# make entrypoint executable
RUN chmod +x /app/entrypoint.sh || true

# create user
RUN useradd --create-home appuser && chown -R appuser:appuser /app

USER appuser

ENV DJANGO_SETTINGS_MODULE=Artisans.settings

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "Artisans.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--log-level", "info"]
