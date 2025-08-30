# Paso 1: Usar una imagen base oficial y ligera de Python
FROM python:3.11-slim

# Paso 2: Establecer el directorio de trabajo dentro del contenedor
WORKDIR /code

# Paso 3: Copiar e instalar las dependencias
# Copiamos solo el requirements.txt primero para aprovechar la caché de Docker.
# Si este archivo no cambia, Docker no volverá a instalar las dependencias en futuras builds.
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Paso 4: Copiar el resto del código de la aplicación y los datos
COPY ./app /code/app
COPY ./restaurants.db /code/restaurants.db
COPY ./.env /code/.env

# Paso 5: Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 8000

# Paso 6: Comando para iniciar la aplicación cuando se lance el contenedor
# Usamos --host 0.0.0.0 para que la API sea accesible desde fuera del contenedor.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]