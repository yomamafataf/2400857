FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY webapp/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --create-home --uid 10001 appuser \
    && mkdir -p /app/certs \
    && chown -R appuser:appuser /app

COPY --chown=appuser:appuser webapp ./webapp
COPY --chown=appuser:appuser data ./data

USER appuser
EXPOSE 8443

CMD ["sh", "-c", "python -m webapp.db && exec gunicorn --bind 0.0.0.0:8443 --workers 2 --certfile /app/certs/localhost.crt --keyfile /app/certs/localhost.key webapp.app:app"]
