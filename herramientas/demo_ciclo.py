"""Módulo 4 · Ejemplo práctico: el ciclo de tool calling sin modelo de por medio.

Simula lo que hace la aplicación cuando el modelo pide una herramienta:
1. recibe la solicitud (nombre + argumentos JSON),
2. valida los argumentos contra el esquema,
3. ejecuta la herramienta,
4. devuelve el resultado (o un error que le enseña al modelo cómo corregir).

Uso:
    python herramientas/demo_ciclo.py '{"name": "ejecutar_suite", "arguments": {"suite": "api-transferencias", "ambiente": "dev"}}'
    python herramientas/demo_ciclo.py '{"name": "ejecutar_suite", "arguments": {"suite": "api-transferencias", "ambiente": "produccion"}}'
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from herramientas import qa_tools  # noqa: E402

DEFINICIONES = {d["name"]: d for d in json.loads(Path(__file__).with_name("definiciones.json").read_text(encoding="utf-8"))}
FUNCIONES = {
    "ejecutar_suite": qa_tools.ejecutar_suite,
    "obtener_resultados_ci": qa_tools.obtener_resultados_ci,
    "crear_borrador_defecto": qa_tools.crear_borrador_defecto,
}


def validar_argumentos(nombre: str, argumentos: dict) -> list[str]:
    esquema = DEFINICIONES[nombre]["input_schema"]
    errores = [f"falta el argumento obligatorio '{r}'" for r in esquema.get("required", []) if r not in argumentos]
    for clave, valor in argumentos.items():
        propiedad = esquema["properties"].get(clave)
        if propiedad is None:
            errores.append(f"argumento desconocido '{clave}'")
        elif "enum" in propiedad and valor not in propiedad["enum"]:
            errores.append(f"'{clave}'='{valor}' no permitido; valores válidos: {propiedad['enum']}")
    return errores


def procesar(solicitud: dict) -> dict:
    nombre, argumentos = solicitud["name"], solicitud.get("arguments", {})
    if nombre not in FUNCIONES:
        return {"error": f"Herramienta desconocida '{nombre}'. Disponibles: {list(FUNCIONES)}"}
    errores = validar_argumentos(nombre, argumentos)
    if errores:
        return {"error": "; ".join(errores)}
    try:
        return FUNCIONES[nombre](**argumentos)
    except qa_tools.ErrorHerramienta as error:
        return {"error": str(error)}


if __name__ == "__main__":
    solicitud = json.loads(sys.argv[1])
    print("1. Solicitud del modelo:", json.dumps(solicitud, ensure_ascii=False))
    resultado = procesar(solicitud)
    print("2. Resultado devuelto al modelo:")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
