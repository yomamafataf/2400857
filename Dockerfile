FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY webapp/requirements.txt .
RUN pip install -r requirements.txt \
    && useradd --no-create-home --uid 10001 appuser

COPY --chown=appuser:appuser webapp ./webapp
COPY --chown=appuser:appuser data ./data

USER appuser
EXPOSE 8000

CMD ["sh", "-c", "python -m webapp.db && exec gunicorn --bind 0.0.0.0:8000 webapp.app:app"]
