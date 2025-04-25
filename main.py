from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from datetime import datetime
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/guardar_historia")
async def guardar_historia(request: Request):
    data = await request.json()

    fecha_hoy = datetime.now().strftime("%d%m%y")
    carpeta_base = "data/RespaldoPacientes"
    os.makedirs(carpeta_base, exist_ok=True)

    consecutivo = 1
    while True:
        id_paciente = f"{fecha_hoy}{consecutivo:02}"
        ruta_paciente = os.path.join(carpeta_base, id_paciente)
        if not os.path.exists(ruta_paciente):
            break
        consecutivo += 1

    os.makedirs(ruta_paciente)
    with open(os.path.join(ruta_paciente, "historia_clinica.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return {"mensaje": "Historial guardado", "expediente": id_paciente}

@app.post("/generar_preguntas")
async def generar_preguntas(request: Request):
    datos = await request.json()
    prompt = f"""Eres un médico que interroga al paciente. Según estos datos clínicos, genera 10 preguntas semiológicas muy específicas que consideres importantes para complementar la historia clínica y hacer más preciso el diagnóstico.

Datos del paciente:
{json.dumps(datos, indent=2, ensure_ascii=False)}

Preguntas:"""
    response = requests.post(
        "https://0cfa-2806-2f0-9fe0-fb4d-e528-37a0-170c-94e2.ngrok-free.app/api/generate",
        json={"model": "llama3", "prompt": prompt}
    )

    respuesta = response.json()["response"]
    preguntas = [p.strip("- ").strip() for p in respuesta.strip().split("\n") if p.strip()]
    return {"preguntas": preguntas}
