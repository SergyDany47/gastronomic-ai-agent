# Agente de Inteligencia Gastronómica con GenAI y SQL 🚀

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-009688?style=for-the-badge&logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-0.3-8A2BE2?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-24-2496ED?style=for-the-badge&logo=docker)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI/CD-2088FF?style=for-the-badge&logo=githubactions)

Este proyecto es un agente conversacional de IA, empaquetado como una API REST, capaz de responder preguntas complejas en lenguaje natural sobre un conjunto de datos de más de 23,000 restaurantes en Madrid y Barcelona.

## 🎯 Objetivo del Proyecto

El objetivo principal es demostrar la creación de una solución de IA de extremo a extremo, desde el procesamiento de datos crudos hasta un servicio productivo y automatizado. Este proyecto sirve como una pieza de portfolio para ilustrar habilidades en **Ingeniería de IA**, **Desarrollo de APIs** y **prácticas de DevOps (CI/CD)**.

---

## ✨ Características Principales

* **Procesamiento de Lenguaje Natural (PLN)**: Acepta preguntas complejas en español.
* **Agente SQL Inteligente**: Utiliza un Agente de LangChain para traducir dinámicamente el lenguaje natural a consultas SQL.
* **API REST Robusta**: Expone la lógica del agente a través de un endpoint `/ask` construido con FastAPI.
* **ETL de Datos**: Incluye un script para limpiar, transformar y cargar los datos de CSV a una base de datos SQLite.
* **Containerización**: Toda la aplicación está empaquetada en una imagen de Docker para portabilidad y consistencia.
* **CI/CD Automatizado**: Un pipeline de GitHub Actions construye y publica automáticamente la imagen de Docker en Docker Hub en cada push a la rama `main`.

---

## 🛠️ Stack Tecnológico

* **Backend**: Python, FastAPI
* **Base de Datos**: SQLite
* **Procesamiento de Datos**: Pandas
* **Framework de IA**: LangChain (SQL Agent con Google Gemini)
* **Containerización**: Docker
* **CI/CD**: GitHub Actions

---

## 🔧 Cómo Empezar

La forma recomendada de ejecutar este proyecto es usando Docker.

### Prerrequisitos
* Tener [Docker](https://www.docker.com/products/docker-desktop/) instalado.
* Un archivo `.env` en la raíz del proyecto.

### 1. Clonar el Repositorio
```bash
git clone [https://github.com/tu-usuario/gastronomic-ai-agent.git](https://github.com/tu-usuario/gastronomic-ai-agent.git)
cd gastronomic-ai-agent
```

### 2. Configurar Variables de Entorno
```bash
# .env
GOOGLE_API_KEY="tu-clave-de-api-aqui"
```

### 3. Construir y Ejecutar con Docker
```bash
# Construir la imagen de Docker
docker build -t gastronomic-ai-agent .

# Ejecutar el contenedor
docker run -p 8000:8000 -d --name agent-container gastronomic-ai-agent
```

¡La API estará disponible en http://127.0.0.1:8000!

## 🚀 Uso de la API

Puedes interactuar con la API a través de la documentación interactiva autogenerada o usando una herramienta como curl.

Documentación Interactiva
Una vez que el contenedor esté en ejecución, abre tu navegador y ve a:
http://127.0.0.1:8000/docs


**Ejemplo con curl**

```bash
curl -X 'POST' \
  '[http://127.0.0.1:8000/ask](http://127.0.0.1:8000/ask)' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "question": "¿Cuál es el tipo de cocina con la mejor valoración media de comida en Barcelona?"
}'
```