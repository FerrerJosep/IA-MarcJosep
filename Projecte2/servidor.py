import json
from flask import Flask, request, jsonify
# conectarse a la base de datos de postgresql
import psycopg2

# Datos de tu conexión
conn = psycopg2.connect(
    dbname="Aparcamiento",
    user="postgres",
    password="josep",
    host="localhost",   # o IP del servidor
    port="5432"         # 5432 es el puerto por defecto
)

# Crear cursor para ejecutar consultas
cur = conn.cursor()

app = Flask(__name__)

@app.route("/entraCoche", methods=["POST"])
def entra_coche():
    
    print("HEADERS:", request.headers)
    print("BODY:", request.data)
    
    data = request.get_json(force=False, silent=False)
    print("DATA PARSED:", data)

    matricula = data.get("matricula") if data else None
    
    # Ejecutar una consulta simple
    if matricula is None:
        print("No se ha recibido matrícula")
        conn.rollback()
    else:   
        #cur.execute(f"select * from insertar_vehiculo('{matricula}')")
        cur.execute("SELECT insertar_vehiculo(%s);", (json.dumps({"matricula": matricula}),))

        conn.commit()

    return jsonify({"mensaje": f"Coche con matrícula {matricula} registrado"}), 200

@app.route("/saleCoche", methods=["POST"])
def sale_coche():
    matricula=request.json.get("matricula")

    if matricula is None:
        conn.rollback()
    else:
        
        cur.execute("SELECT eliminar_vehiculo(%s);", (json.dumps({"matricula": matricula}),))

        conn.commit()
    
    return jsonify({"mensaje": f"Sale con matrícula {matricula} registrado"}), 200


@app.route("/estadoAparcamiento", methods=["POST"])
def estado_aparcamiento():
    try:
        matricula=request.json.get("matricula")
        # Ejecutar una consulta simple
        cur.execute(f"SELECT vehi_esta_dentro from vehiculos where vehi_matricula='{matricula}';")
        estado = cur.fetchone()[0]

         # Devolver el resultado como JSON
        return jsonify({"vehi_esta_dentro": estado}), 200

    except Exception as e:

        
        return jsonify({"Info": "Se ha insertado el coche en la base de datos"}), 200


@app.route("/calcularMinutos", methods=["POST"])
def calcular_importe():
    try:
        # Obtener la matrícula del JSON recibido
        matricula = request.json.get("matricula")

        print('---------------------------------')
        print(f"Matrícula recibida: {matricula}")
        print('---------------------------------')

        # Ejecutar la función SQL
        cur.execute("SELECT calcular_minutos(%s);", (json.dumps({"matricula": matricula}),))
        minutos = cur.fetchone()[0]
        conn.commit()

        print(f"Minutos calculados: {minutos}")

        # Devolver el resultado como JSON
        return jsonify({"minutos": minutos}), 200

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        return jsonify({"Info": "Error en el cálculo de minutos en el servidor"}), 500

   

if __name__ == "__main__":
    app.run(debug=True, port=5000)