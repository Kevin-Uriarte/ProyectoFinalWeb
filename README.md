# Proyecto Final Programación Web

## Procesamiento Distribuido con FastAPI, Redis y Docker

### Autor
Kevin Ernesto Uriarte Parra
22211668
 
---

## Descripción

Aplicación web distribuida desarrollada con FastAPI, Redis y Docker. El sistema permite enviar tareas de análisis de texto desde un frontend en JavaScript hacia múltiples workers ejecutándose en contenedores Docker.

Los resultados se actualizan en tiempo real utilizando Server-Sent Events (SSE).

---

## Tecnologías Utilizadas

- FastAPI
- Python
- Redis
- Docker
- Docker Compose
- HTML/CSS/JavaScript
- AWS EC2

---

## Arquitectura

```text
Frontend JS
     ↓
FastAPI Backend
     ↓
Redis Queue
     ↓
Workers Docker
     ↓
Resultados en tiempo real
```

---

## Funcionalidades

- Envío de tareas desde frontend
- Procesamiento distribuido
- 3 workers Docker
- Cola de mensajes Redis
- SSE en tiempo real
- Conteo de palabras
- Conteo de caracteres
- Palabras frecuentes
- Palabras clave

---

## Ejecución

```bash
docker compose up --build --scale worker=3
```

---

## Servicios

| Servicio | Puerto |
|---|---|
| Frontend | 8080 |
| Backend | 8000 |
| Redis | 6379 |

---

## Repositorio

https://github.com/Kevin-Uriarte/ProyectoFinalWeb

---

## Conclusión

Este proyecto implementa una arquitectura Cloud Native utilizando procesamiento distribuido con Docker, FastAPI y Redis, ejecutándose en AWS EC2 y mostrando resultados en tiempo real mediante SSE.
