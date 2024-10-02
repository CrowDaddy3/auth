# Se selecciona la version 3.12 de python
FROM python:3.12-slim

# Se crea un directorio llamado "app" en el sistema de archivos del contenedor
WORKDIR /app

COPY requirements/base.txt /app/requirements/base.txt

RUN pip install --no-cache-dir -r /app/requirements/base.txt

COPY . /app

EXPOSE 8000

RUN pytest

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]