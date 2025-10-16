# Dockerfile
FROM python:3.13-slim

# Configura directorio de trabajo
WORKDIR /app

# Copia requerimientos y los instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del proyecto
COPY . .

# Expone puerto (el que usa uvicorn)
EXPOSE 8000

# Comando para levantar la API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
