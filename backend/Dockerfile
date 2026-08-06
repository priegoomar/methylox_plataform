FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /backend

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# VERIFICACIÓN TEMPORAL DEL ARCHIVO SECURITY
RUN echo "========== SECURITY FILE =========="
RUN nl -ba app/security.py | sed -n '90,120p'

RUN mkdir -p static/reports

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
