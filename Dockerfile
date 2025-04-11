# Imagen base
FROM python:3.11-slim

# Copia los archivos de la app
COPY api.py /api.py

# Instala dependencias necesarias
RUN pip install flask pyjwt

# Expone el puerto donde corre Flask
EXPOSE 5000

# Variable de entorno opcional (puede ser sobreescrita en runtime)
ENV SECRET_KEY=mysecretkey

# Comando para ejecutar la app
CMD ["python", "api.py"]