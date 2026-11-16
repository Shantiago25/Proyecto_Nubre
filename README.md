# Mesa de ayuda web (Computación en la nube)

Aplicación Flask para registrar y consultar solicitudes de soporte. Datos en `solicitudes.json` (ficticios).
Plantilla: desarrollo propio, apoyado con IA (declarar uso y fuentes en el informe).

## Ejecución local (sin Docker)
    pip install -r requirements.txt
    python app.py          # http://localhost:8000

## Docker
    docker build -t mesa-ayuda .
    docker run -d --name mesa -p 8000:8000 -v mesa-datos:/data mesa-ayuda
    docker ps
    docker logs mesa

## Prueba de persistencia
    docker rm -f mesa
    docker run -d --name mesa -p 8000:8000 -v mesa-datos:/data mesa-ayuda
    (NO ejecutar `docker volume rm mesa-datos`)

## Almacenamiento
JSON en `/data/solicitudes.json` dentro del contenedor, respaldado por el volumen `mesa-datos`.
En la nube: explicar aquí si es persistente o temporal y qué pasa al reiniciar/redesplegar.
