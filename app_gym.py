import os
from fastapi import FastAPI, HTTPException, Security, Depends, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field

# 1. Inicialización de la aplicación
app = FastAPI(
    title="Gym Performance & 1RM API",
    version="1.0.0",
    description="Microservicio blindado para análisis de fuerza y cargas de entrenamiento"
)

# 2. Configuración de Seguridad (API Key Authentication)
API_KEY_NAME = "X-API-Key"
# En producción, esta clave se lee desde una variable de entorno de Kubernetes / AWS Secrets Manager
API_KEY_VALUE = os.getenv("API_KEY_SECRET", "sport-secure-key-2026")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def verify_api_key(api_key: str = Depends(api_key_header)):
    if not api_key or api_key != API_KEY_VALUE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso no autorizado: API Key inválida o ausente"
        )
    return api_key

# 3. Modelo de datos con Validación Estricta de Límites (Boundaries)
class WorkoutInput(BaseModel):
    exercise: str = Field(..., min_length=2, max_length=50, example="Press de Banca")
    weight_kg: float = Field(..., gt=0, le=1000, description="El peso debe ser mayor a 0 y máximo 1000 kg")
    reps: int = Field(..., gt=0, le=30, description="Las repeticiones deben estar entre 1 y 30")

# 4. Endpoint de Salud (PÚBLICO - Requerido para Kubernetes Liveness/Readiness Probes)
@app.get("/health")
def health_check():
    return {
        "status": "UP",
        "service": "gym-analytics",
        "security": "hardened"
    }

# 5. Endpoint Principal (PROTEGIDO con API Key)
@app.post("/api/v1/calculate-1rm", dependencies=[Depends(verify_api_key)])
def calculate_1rm(workout: WorkoutInput):
    # Cálculo de 1RM estimado usando la Fórmula de Epley
    if workout.reps == 1:
        estimated_1rm = workout.weight_kg
    else:
        estimated_1rm = workout.weight_kg * (1 + (workout.reps / 30.0))
    
    # Cálculo del volumen total movido
    total_volume = workout.weight_kg * workout.reps
    
    # Recomendación de rango de entrenamiento
    if 1 <= workout.reps <= 5:
        recommendation = "Rango orientativo de Fuerza Máxima"
    elif 6 <= workout.reps <= 12:
        recommendation = "Rango óptimo para Hipertrofia"
    else:
        recommendation = "Rango orientativo de Resistencia Muscular"

    return {
        "exercise": workout.exercise,
        "input_weight_kg": workout.weight_kg,
        "input_reps": workout.reps,
        "estimated_1rm_kg": round(estimated_1rm, 2),
        "total_volume_kg": round(total_volume, 2),
        "recommendation": recommendation
    }