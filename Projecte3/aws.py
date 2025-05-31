import requests
import json

# Configuración
BASE_URL = "https://5zxrivslp3.execute-api.us-east-1.amazonaws.com/v1"
KNOWLEDGE_BASE_ID = "ASFECI7"  # ID correcto según el ejemplo de /advance
MODEL_ARN = "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-text-premier-v1:0"

HEADERS = {
    "Content-Type": "application/json"
    # Si necesitas autenticarte, añade:
    # "Authorization": "Bearer TU_TOKEN"
}

# Consulta simple
def consulta_simple(prompt):
    url = f"{BASE_URL}/simple"
    payload = {"prompt": prompt}
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def consulta_avanzada(texto, numero_resultados=3):
    url = f"{BASE_URL}/advance"
    payload = {
        "input": {"text": texto},
        "retrieveAndGenerateConfiguration": {
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                "modelArn": MODEL_ARN,
                "retrievalConfiguration": {
                    "vectorSearchConfiguration": {
                        "numberOfResults": numero_resultados
                    }
                }
            }
        }
    }
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()  # Raise HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}", "details": response.text if 'response' in locals() else None}

# Mostrar respuesta con manejo de errores
def mostrar_respuesta(respuesta):
    if "error" in respuesta:
        print(f"\n❌ Error: {respuesta['error']}")
        return

    texto = respuesta.get("text")
    if texto:
        print("\n📄 Respuesta:")
        print(texto)
    else:
        print("\n⚠️ No se ha encontrado una respuesta.")
        print("🧪 Respuesta cruda (debug):")
        print(json.dumps(respuesta, indent=2, ensure_ascii=False))

    citas = respuesta.get("citations", [])
    if citas:
        print("\n🔎 Citas:")
        for cita in citas:
            ref = cita.get("retrievedReference")
            if ref:
                titulo = ref.get("title", "Sin título")
                uri = ref.get("location", {}).get("s3Location", {}).get("uri", "Sin enlace")
                print(f"- {titulo} ({uri})")
            else:
                print("- Cita no estructurada o faltan datos.")
    elif texto:
        print("\nℹ️ No se encontraron citas específicas.")

# Menú principal
def main():
    print("🧠 Bot GVA – Consulta la Knowledge Base")
    while True:
        print("\n1. Consulta simple\n2. Consulta avanzada\n3. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            pregunta = input("¿Qué quieres saber?\n> ")
            respuesta = consulta_simple(pregunta)
            mostrar_respuesta(respuesta)

        elif opcion == "2":
            pregunta = input("¿Qué pregunta detallada quieres hacer?\n> ")
            try:
                num = int(input("¿Cuántos resultados quieres recuperar? (ej. 3)\n> "))
            except ValueError:
                num = 3
            respuesta = consulta_avanzada(pregunta, numero_resultados=num)
            mostrar_respuesta(respuesta)

        elif opcion == "3":
            print("¡Hasta luego! 🖖")
            break

        else:
            print("Opción no válida. Intenta con 1, 2 o 3.")

if __name__ == "__main__":
    main()
