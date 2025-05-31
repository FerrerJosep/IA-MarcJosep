import json
from flask import Flask, request, jsonify
import psycopg2


conn = psycopg2.connect(
    dbname="Aparcamiento",
    user="postgres",
    password="josep",
    host="localhost",  
    port="5432"        
    password="josep",
    host="localhost",   # o IP del servidor
    port="5432"         # 5432 es el puerto por defecto
)

cur = conn.cursor()

app = Flask(__name__)

@app.route("/entraCoche", methods=["POST"])
def entra_coche():
    
    
    data = request.get_json(force=False, silent=False)

    matricula = data.get("matricula") if data else None
    
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
        cur.execute(f"SELECT vehi_esta_dentro from vehiculos where vehi_matricula='{matricula}';")
        estado = cur.fetchone()[0]

        
        return jsonify({"vehi_esta_dentro": estado}), 200

    except Exception as e:

        
        return jsonify({"Info": "Se ha insertado el coche en la base de datos"}), 200


@app.route("/calcularMinutos", methods=["POST"])
def calcular_importe():
    try:
        
        matricula = request.json.get("matricula")
       
        cur.execute("SELECT calcular_minutos(%s);", (json.dumps({"matricula": matricula}),))
        print('---------------------------------')
        print(matricula)
        print('---------------------------------')
        # Ejecutar una consulta simple
        cur.execute("SELECT calcular_minutos(%s);", (json.dumps({"matricula": matricula}),))
        importe = cur.fetchone()[0]
        conn.commit()
       
        return jsonify({"minutos": importe}), 200
    
    except Exception as e:
        conn.rollback()
        return jsonify({"Info": "Error en el calculo de importe en el servidor "}), 200
   

if __name__ == "__main__":
    app.run(debug=True, port=5000)