# Capa imagen base
FROM python:3.11-slim

# Capa directorio de trabajo
WORKDIR /app

# capa instalar utilidades necesarias para Kaggle
RUN apt-get update && apt-get install -y --no-install-recommends \
    unzip curl && \
    rm -rf /var/lib/apt/lists/*

# Capa copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Capa donde se copia el codigo de la aplicación
COPY app/ ./

# Capa para copiar credenciales de Kaggle
COPY kaggle.json /root/.kaggle/kaggle.json
RUN chmod 600 /root/.kaggle/kaggle.json

# Capa para crear carpeta de datos
RUN mkdir -p /app/datos

# Arranque por defecto en modo interactivo (bash)
CMD ["bash"]




