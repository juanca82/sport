# 🏋️‍♂️ Gym Telemetry & Strength Performance Platform

[![DevSecOps CI/CD](https://github.com/juanca82/sport/actions/workflows/devsecops-pipeline.yml/badge.svg)](https://github.com/juanca82/sport/actions)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Kind%20v1.28-blue?logo=kubernetes)
![Terraform](https://img.shields.io/badge/IaC-Terraform-7B42BC?logo=terraform)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit)

Plataforma enterprise de telemetría deportiva y análisis de rendimiento de fuerza (cálculo de 1RM y zonas de carga). Diseñada bajo metodología **DevSecOps**, con arquitectura de microservicios, contenedorización hardening, orquestación en Kubernetes e Infraestructura como Código (IaC) para AWS.

---

## 🏗️ Arquitectura del Sistema

```text
┌─────────────────┐     HTTP/JSON      ┌─────────────────────────────┐
│  Streamlit UI   │ ─────────────────> │  Kubernetes Cluster (Kind)  │
│ (app_frontend)  │  X-API-Key Auth    │  ┌───────────────────────┐  │
└─────────────────┘                    │  │ Gym Telemetry Service │  │
                                       │  └──────────┬────────────┘  │
                                       │             │               │
                                       │  ┌──────────▼────────────┐  │
                                       │  │ FastAPI Pods (2 Replic)│  │
                                       │  └───────────────────────┘  │
                                       └─────────────────────────────┘

🧩 Componentes del Repositorio
Backend REST API (app_gym.py): Microservicio en FastAPI con validación estricta de límites vía Pydantic y autenticación por cabecera HTTP (X-API-Key).

Frontend Web (app_frontend.py): Dashboard interactivo en Streamlit para visualización y análisis de cargas.
Seguridad & Contenedorización (Dockerfile): Imagen en dos fases (multi-stage build) basada en python:3.11-slim, ejecutada como usuario sin privilegios root (appuser, UID 1000).
Orquestación K8s (deployment.yaml, service.yaml): Despliegue en clúster con 2 réplicas, actualización progresiva (Rolling Updates), balanceo de carga y probes de salud (/health).
Infraestructura como Código (terraform/): Módulos HCL para aprovisionamiento automatizado en AWS (EKS, ECR con escaneo de imágenes en push, VPC).
Pipeline CI/CD (.github/workflows/): Automatización con GitHub Actions que realiza compilación de contenedores y análisis de vulnerabilidades (CVEs) con Trivy.

🚀 Guía de Despliegue Local

1. Pre-requisitos
Docker Desktop / Engine
Kind (kind create cluster)
kubectl
Python 3.11+ con entorno virtual (.venv)

2. Despliegue en Kubernetes
Bash

# 1. Crear el clúster local
kind create cluster --name sport-telemetry-cluster

# 2. Compilar la imagen versión v2
docker build -t sport-gym-api:v2 .

# 3. Cargar la imagen en Kind
kind load docker-image sport-gym-api:v2 --name sport-telemetry-cluster

# 4. Aplicar los manifiestos de Kubernetes
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

3. Exposición y Conexión
Bash
# Reenvío de puertos para conectar con el servicio localmente
kubectl port-forward svc/gym-telemetry-service 8001:8001

4. Ejecución del Dashboard (Frontend)
Bash
# En una nueva pestaña de terminal:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app_frontend.py

🔒 Especificación de la API
Endpoints
GET /health: Health Check público para Kubernetes Liveness/Readiness Probes.
POST /api/v1/calculate-1rm: Endpoint protegido para el cálculo de repetición máxima y volumen total.
Autenticación Requerida
Header: X-API-Key: sport-secure-key-2026

Ejemplo de Payload (JSON)
JSON
{
  "exercise": "Press de Banca",
  "weight_kg": 100.0,
  "reps": 5
}

Ejemplo de Respuesta
JSON
{
  "exercise": "Press de Banca",
  "weight_kg": 100.0,
  "reps": 5,
  "estimated_1rm_kg": 116.7,
  "total_volume_kg": 500.0,
  "recommendation": "Carga óptima para trabajo de hipertrofia y fuerza base."
}

🛡️ Estándares de Seguridad Aplicados (DevSecOps)
Least Privilege Principle: El contenedor corre bajo un usuario no-root (appuser).
Boundary Validation: Pydantic restringe valores fuera de rango o tipos de datos no válidos en la entrada HTTP.
Automated Vulnerability Scanning: Escaneo continuo de imágenes Docker con Trivy en GitHub Actions ante cada push.
Secret Management: Claves expuestas como variables de entorno (API_KEY_SECRET) en los manifiestos de Kubernetes.
