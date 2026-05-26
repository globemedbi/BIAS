FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ../shared ./shared

COPY . .

RUN useradd -m -u 1000 biasuser && chown -R biasuser:biasuser /app
USER biasuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8003/health || exit 1

EXPOSE 8003

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8003"]
