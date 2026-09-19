# ---------------------------------------------------
# Etapa 1: Build (Compilación e instalación de dependencias)
# ---------------------------------------------------
FROM python:3.11-slim AS builder

WORKDIR /app

# Copiamos solo el archivo de requerimientos
COPY requirements.txt .

# Instalamos las librerías dentro de un directorio de usuario
RUN pip install --no-cache-dir --user -r requirements.txt

# ---------------------------------------------------
# Etapa 2: Runtime (Imagen final ligera y segura)
# ---------------------------------------------------
FROM python:3.11-slim

# Creamos un usuario sin privilegios por seguridad (Non-Root User)
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copiamos las dependencias desde la etapa anterior
COPY --from=builder /root/.local /home/appuser/.local
COPY app_gym.py .

# Asignamos permisos al usuario no privilegiado
RUN chown -R appuser:appuser /app
USER appuser

# Añadimos la ruta de ejecutables al PATH del usuario
ENV PATH=/home/appuser/.local/bin:$PATH

# Exponemos el puerto de la API
EXPOSE 8001

# Comando para arrancar la API con Uvicorn
CMD ["uvicorn", "app_gym:app", "--host", "0.0.0.0", "--port", "8001"]