# syntax=docker/dockerfile:1

FROM python:3.9-slim

# install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# copy source
COPY main.py .
COPY templates/ ./templates/

# drop to non-root user (optional but recommended)
RUN useradd --no-create-home appuser \
 && chown -R appuser:appuser /app
USER appuser

# listen on 8080
ENV FLASK_ENV=production
ENV QDRANT_HOST=qdrant
ENV QDRANT_PORT=6333
ENV FLASK_DISABLE_FILE_WATCHERS=1
EXPOSE 8080

CMD ["python", "main.py"]