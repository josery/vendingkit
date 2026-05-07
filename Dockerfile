FROM python:3.11-slim

WORKDIR /app

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements
COPY requirements.txt .

# Instala dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código
COPY . .

# Expone puerto
EXPOSE 8000

# Variables de entorno
ENV PORT=8000
ENV HOST=0.0.0.0
ENV DEBUG=False

# Comando de inicio
CMD ["python", "-m", "uvicorn", "agent.main:app", "--host", "0.0.0.0", "--port", "8000"]
