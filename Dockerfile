FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYLAGE_APP_FILE=/app/working_demo/app.py

COPY pyproject.toml README.md LICENSE ./
COPY pylage ./pylage
COPY working_demo ./working_demo

RUN pip install --no-cache-dir .

EXPOSE 8000

CMD ["sh", "-c", "exec granian pylage.ENGINE.runtime.granian:create_application_from_file --interface asgi --factory --host 0.0.0.0 --port ${PORT:-8000}"]
