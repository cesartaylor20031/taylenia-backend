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

@app.post("/generar_preguntas")
async def generar_preguntas(request: Request):
    datos = await request.json()

    prompt = f"""Eres un médico que interroga al paciente. Según estos datos clínicos, genera 10 preguntas semiológicas muy específicas que consideres importantes para complementar la historia clínica y hacer más preciso el diagnóstico.

Datos del paciente:
{json.dumps(datos, indent=2, ensure_ascii=False)}

Preguntas:"""

    # Simulación local de respuesta de modelo
    response = {
        "response": """1. ¿Desde cuándo inició el dolor que mencionas?
2. ¿El dolor aumenta al hacer ciertos movimientos o actividades?
3. ¿Cómo describirías el tipo de dolor: punzante, sordo, ardoroso?
4. ¿El dolor se presenta en algún momento específico del día o es constante?
5. ¿Has notado si el dolor se irradia hacia otras zonas del cuerpo?
6. ¿Has presentado fiebre, pérdida de peso o fatiga recientemente?
7. ¿El dolor ha afectado tu sueño o tu capacidad para realizar actividades cotidianas?
8. ¿Has tenido antecedentes similares en el pasado?
9. ¿El dolor mejora o empeora con algún medicamento o tratamiento?
10. ¿Hay factores emocionales o de estrés que consideres estén relacionados con este dolor?"""
    }

    preguntas = [p.strip("- ").strip() for p in response["response"].split("\n") if p.strip()]
    return {"preguntas": preguntas}
