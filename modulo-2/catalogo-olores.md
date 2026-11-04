# Catálogo de olores de un prompt y su refactor

Un "olor" es una señal de que el prompt va a producir resultados pobres o inestables.
Refactorizar es cambiar la estructura del prompt **sin cambiar su objetivo**, un olor a la vez, y medir.

| Olor | Cómo se nota en la salida | Refactor |
| --- | --- | --- |
| Tarea vaga | Casos genéricos ("probar la transferencia") | Verbo concreto + alcance + técnica |
| Tarea monolítica | Mezcla riesgos, casos y datos; olvida partes | Dividir en pasos o en una cadena de prompts |
| Contexto de más | Ignora reglas importantes, se distrae con lo irrelevante | Recortar al contexto que la tarea necesita |
| Contexto de menos | Inventa reglas o mensajes | Agregar la regla, el mensaje exacto o el dato |
| Instrucciones contradictorias | Resultados distintos en cada ejecución | Unificar y dar prioridad explícita |
| Sin formato de salida | Texto libre difícil de revisar o reutilizar | Formato estructurado (CSV, tabla, JSON, Gherkin) |
| Sin ejemplos | Estilo y nivel de detalle variables | 1 a 3 ejemplos y, si ayuda, un contraejemplo |
| Supone en vez de preguntar | Supuestos escondidos en los casos | "Si falta información, pregunta antes de generar" |
| Sin verificación | Errores que nadie pidió revisar | Checklist de autoverificación al final |
| Datos mezclados con instrucciones | Confunde datos con órdenes | Separar con etiquetas o variables `{historia}` |
| Instrucciones en negativo | "No hagas casos malos" no orienta | Decir qué hacer, en positivo y concreto |
| Límites a medias | Prueba un extremo del rango pero no el otro | Checklist de límites en ambos extremos |

## Reglas del refactor de prompts
1. Mide la versión actual antes de cambiar nada (`modulo-2/evaluar_salida.py`).
2. Un olor por versión. Si cambias tres cosas, no sabrás cuál funcionó.
3. Vuelve a medir con las mismas entradas.
4. Registra la versión en la bitácora: cambio, motivo y métrica antes y después.
5. Si empeora, vuelve a la versión anterior.
