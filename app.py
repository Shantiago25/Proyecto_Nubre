import json, os, re, threading
from datetime import datetime, timezone, timedelta
from flask import Flask, request, render_template

app = Flask(__name__)
DATA_DIR = os.environ.get("DATA_DIR", "data")
DATA_FILE = os.path.join(DATA_DIR, "solicitudes.json")
LOCK = threading.Lock()
TIPOS = ["Equipo", "Internet", "Software", "Otro"]
PRIORIDADES = ["Baja", "Media", "Alta"]
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
BOGOTA = timezone(timedelta(hours=-5))


def leer():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def guardar(lista):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)


def validar(d):
    errores = []
    if not d["nombre"]:
        errores.append("El nombre del solicitante es obligatorio.")
    if not d["correo"]:
        errores.append("El correo electrónico es obligatorio.")
    elif not EMAIL_RE.match(d["correo"]):
        errores.append("El correo electrónico no tiene un formato válido.")
    if d["tipo"] not in TIPOS:
        errores.append("Seleccione un tipo de problema válido.")
    if not d["descripcion"]:
        errores.append("La descripción es obligatoria.")
    elif len(d["descripcion"]) < 15:
        errores.append("La descripción debe tener al menos 15 caracteres.")
    if d["prioridad"] not in PRIORIDADES:
        errores.append("Seleccione una prioridad válida.")
    return errores


@app.route("/", methods=["GET", "POST"])
def registrar():
    datos = {k: "" for k in ["nombre", "correo", "tipo", "descripcion", "prioridad"]}
    errores, creada = [], None
    if request.method == "POST":
        datos = {k: request.form.get(k, "").strip() for k in datos}
        errores = validar(datos)
        if not errores:
            with LOCK:
                lista = leer()
                creada = {
                    "id": f"SOL-{len(lista) + 1:04d}",
                    "solicitante": datos["nombre"],
                    "correo": datos["correo"],
                    "tipo": datos["tipo"],
                    "descripcion": datos["descripcion"],
                    "prioridad": datos["prioridad"],
                    "fecha": datetime.now(BOGOTA).strftime("%Y-%m-%d %H:%M:%S"),
                }
                lista.append(creada)
                guardar(lista)
            datos = {k: "" for k in datos}
    return render_template("registrar.html", datos=datos, errores=errores,
                           creada=creada, tipos=TIPOS, prioridades=PRIORIDADES)


@app.route("/solicitudes")
def consultar():
    return render_template("consultar.html", solicitudes=list(reversed(leer())))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
