# Use an official lightweight Python runtime as a parent image
FROM python:3.10-slim

# Set system environment variables to prevent Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /backend

# Install system dependencies required for psycopg2 compilation if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# RECTIFICACIÓN DE RUTA PARA RENDER: Copia directa del archivo en la raíz del contexto
COPY requirements.txt .

# Install production-grade Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido directo de la carpeta app en la raíz del contenedor
COPY app/ ./app

# Create necessary static directory for PDF reports compilation
RUN mkdir -p static/reports

# Expose the network port that FastAPI runs on
EXPOSE 8000

# Command to ignite the Uvicorn production server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
