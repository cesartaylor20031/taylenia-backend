from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
        "optin_whatsapp": datos.get("optin_whatsapp")
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
