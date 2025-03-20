from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)


#aqui estamos estabeciendo la conecccion con nuestra base de datos
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ejercicio1"
    )


# Ruta principal que renderiza la página de inicio
@app.route ("/")
def home1():
    return render_template("inicio.html")


# Ruta para mostrar los estudiantes registrados
@app.route("/index")
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM estudiantes_registro")
    estudiantes_registro = cursor.fetchall()
    conn.close()
    return render_template("index.html", actividades=estudiantes_registro)

# Función para agregar un nuevo alumno
@app.route("/add", methods=["POST"])
def add():
    nombre = request.form.get('nombre')
    matricula = request.form.get('matricula')
    edad = request.form.get('edad')
    grado = request.form.get('grado')
    estado = request.form.get('estado')

    if nombre and matricula and edad and grado and estado:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO estudiantes_registro (nombre, matricula, edad, grado, estado)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, matricula, edad, grado, estado))
        conn.commit()
        conn.close()
    return redirect('/index')



# Función para eliminar un alumno
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM estudiantes_registro WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect('/index')



# Función para actualizar los datos de un alumno
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    nombre = request.form.get('nombre')
    matricula = request.form.get('matricula')
    edad = request.form.get('edad')
    grado = request.form.get('grado')
    estado = request.form.get('estado')

    if nombre and matricula and edad and grado and estado:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE estudiantes_registro
            SET nombre = %s, matricula = %s, edad = %s, grado = %s, estado = %s
            WHERE id = %s
        """, (nombre, matricula, edad, grado, estado, id))
        conn.commit()
        conn.close()
    return redirect('/index')

if __name__ == "__main__":
    app.run(debug=True)
