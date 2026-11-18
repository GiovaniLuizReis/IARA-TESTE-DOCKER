FROM python:3.13.3-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dependências de sistema para o psycopg3 e compilação
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instala as bibliotecas Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do IARA-SAÚDE para dentro do contêiner
COPY . .

EXPOSE 8000

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]