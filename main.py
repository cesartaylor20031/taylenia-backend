from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from datetime import datetime
import requests

app = FastAPI()

# Middleware CORS para aceptar peticiones desde cualquier lugar
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/guardar_historia")
async def guardar_historia(request: Request):
    datos = await request.json()

    historia = {
        "nombre": datos.get("nombre"),
        "whatsapp": datos.get("whatsapp"),
        "correo": datos.get("correo"),
        "edad_sexo_ocupacion": datos.get("edad_sexo_ocupacion"),
        "heredofamiliares": datos.get("heredofamiliares"),
        "estilo_vida": datos.get("estilo_vida"),
        "patologicos": datos.get("patologicos"),
        "padecimiento": datos.get("padecimiento"),
        "extra": datos.get("extra"),
        "medicamentos": datos.get("medicamentos"),
        "optin_whatsapp": datos.get("optin_whatsapp"),
        "respuestas_preguntas": datos.get("respuestas_preguntas")  # Asegura guardar respuestas también
    }

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
        json.dump(historia, f, ensure_ascii=False, indent=2)

    return {"mensaje": "Historial guardado exitosamente", "expediente": id_paciente}

# 🚑 Nueva ruta para generar preguntas semiológicas
@app.post("/generar_preguntas")
async def generar_preguntas(request: Request):
    datos = await request.json()

    prompt = f"""Eres un médico experto en semiología clínica.
Con base en estos datos del paciente, genera 10 preguntas semiológicas específicas para complementar su historia clínica.

Datos del paciente:
{json.dumps(datos, indent=2, ensure_ascii=False)}

Preguntas:"""

    llama_response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt, "stream": False}
    )

    respuesta_texto = llama_response.json()["response"]
    preguntas = [p.strip("- ").strip() for p in respuesta_texto.split("\n") if p.strip()]
    
    return {"preguntas": preguntas}

    preguntas = [p.strip("- ").strip() for p in respuesta_modelo.split("\n") if p.strip()]
    return {"preguntas": preguntas}
