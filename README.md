# Mesa de ayuda web

Proyecto final de Computación en la nube — Universidad Cooperativa de Colombia
Integrantes: [Santiago Muñoz Perdomo, Jhonatan Figueroa, Alejandro Velasquez Rodriguez] | Código(s): [892883, 892658, 850777]

## Descripción
Aplicación web para registrar y consultar solicitudes de soporte técnico
(equipos, internet, software).

## Tecnologías
Python 3, Flask, gunicorn, Docker. Almacenamiento en archivo JSON.

## Procedencia del código y uso de IA
Aplicación desarrollada con apoyo de IA (Claude) con ayuda
para el código base. El grupo revisó, probó y
adaptó el código

## Requisitos
- Python 3.8 o superior
- Git
- Docker Desktop

## Ejecución local (sin Docker)
    pip install -r requirements.txt
    python app.py
Abrir http://localhost:8000

## Ejecución con Docker
    docker build -t mesa-ayuda .
    docker run -d --name mesa -p 8000:8000 -v mesa-datos:/data mesa-ayuda
    docker ps
    docker logs mesa

## Prueba de persistencia
    docker rm -f mesa
    docker run -d --name mesa -p 8000:8000 -v mesa-datos:/data mesa-ayuda
No se elimina el volumen `mesa-datos`: las solicitudes siguen disponibles.

## Almacenamiento
Las solicitudes se guardan en `/data/solicitudes.json` dentro del contenedor.
Esa carpeta está montada sobre el volumen `mesa-datos`, por eso los datos
sobreviven si el contenedor se elimina y se vuelve a crear.

## Pruebas de aceptación
Datos válidos, campo vacío, correo inválido, descripción corta y tres
solicitudes en la consulta. [Resultados en el informe]

## Despliegue en la nube
URL pública: https://mesa-ayuda-ww7a.onrender.com/

## Prueba de persistencia 17/11/2026 2:02 PM
se realizaron pruebas de persistencias para confirmar que los datos son consistentes
los resultados fueron positivos, todos los datos están correctos