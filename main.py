@app.post("/generar_preguntas")
async def generar_preguntas(request: Request):
    datos = await request.json()

    prompt = f"""Eres un médico que interroga al paciente. Según estos datos clínicos, genera 10 preguntas semiológicas muy específicas que consideres importantes para complementar la historia clínica y hacer más preciso el diagnóstico.

Datos del paciente:
{json.dumps(datos, indent=2, ensure_ascii=False)}

Preguntas:"""

    # Aquí tú puedes cambiar el endpoint si quieres usar LLaMA local, DeepSeek, OpenAI o ngrok
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

    # Devuelve las preguntas como lista
    preguntas = [p.strip("- ").strip() for p in response["response"].split("\n") if p.strip()]
    return {"preguntas": preguntas}
