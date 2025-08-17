from flask import Flask, jsonify, request
from DB.db_connection import conectar
from DB.create_tables import crear_base_si_no_existe, crear_tablas

app = Flask(__name__)


# Endpoint para obtener todos los usuarios en detalle http://localhost/usuarios

@app.route("/usuarios", methods=['GET'])
def get_usuarios():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Usuario")
    rows = cursor.fetchall()
    columns = [c[0] for c in cursor.description]
    usuarios = [dict(zip(columns, r)) for r in rows]

    conn.close()
    return jsonify(usuarios)



@app.route("/usuarios", methods=['POST'])
def add_usuario():
    nuevo_usuario = request.get_json()

    # Validación simple
    if not nuevo_usuario or 'nombre' not in nuevo_usuario or 'identificacion' not in nuevo_usuario or 'rol' not in nuevo_usuario:
        return jsonify({'error': 'Campos requeridos: nombre, identificacion, rol'}), 400

    conn = conectar()
    cursor = conn.cursor()

    query = """
        INSERT INTO Usuario (nombre, identificacion, rol)
        VALUES (?, ?, ?)
    """

    try:
        cursor.execute(
            query,
            (
                nuevo_usuario['nombre'],
                nuevo_usuario['identificacion'],
                nuevo_usuario['rol']
            )
        )
        conn.commit()
        conn.close()
        return jsonify({'success': True}), 201
    except Exception as ex:
        conn.close()
        return jsonify({'error': str(ex)}), 500


if __name__ == "__main__":
    from DB.create_tables import crear_base_si_no_existe, crear_tablas
    crear_base_si_no_existe()
    crear_tablas()
    app.run(debug=True)
