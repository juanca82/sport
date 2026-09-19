from fastapi import FastAPI
from pydantic import BaseModel

# 1. Inicialización de la aplicación con metadatos
app = FastAPI(
    title="Gym Performance & 1RM API",
    version="1.0.0",
    description="Microservicio para el análisis de fuerza y cargas de entrenamiento"
)

# 2. Modelo de datos con validación de seguridad (Pydantic)
class WorkoutInput(BaseModel):
    exercise: str
    weight_kg: float
    reps: int

# 3. Endpoint de Salud (Vital para Kubernetes)
@app.get("/health")
def health_check():
    return {
        "status": "UP",
        "service": "gym-analytics",
        "security": "hardened"
    }

# 4. Endpoint Principal de Cálculo de 1RM
@app.post("/api/v1/calculate-1rm")
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