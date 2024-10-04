from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Conexión a la base de datos
def conectar():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            database='Avance_proyecto',
            user='root',
            password='Sargento0708'
        )
        return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Ruta principal para la página de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para gestionar clientes
@app.route('/clientes')
def clientes():
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Clientes")
        clientes = cursor.fetchall()
        cursor.close()
        conexion.close()
        return render_template('clientes.html', clientes=clientes)
    return "Error al conectar a la base de datos"

# Ruta para agregar un nuevo cliente
@app.route('/add_client', methods=['POST'])
def agregar_cliente():
    nombre = request.form['nombre']
    ap_paterno = request.form['apellido_paterno']
    ap_materno = request.form['apellido_materno']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    email = request.form['email']
    
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        try:
            query = """INSERT INTO Clientes (Nombre, Ap_Paterno, Ap_Materno, Direccion, Telefono, Email)
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (nombre, ap_paterno, ap_materno, direccion, telefono, email))
            conexion.commit()
        except Error as e:
            print(f"Error al agregar cliente: {e}")
        finally:
            cursor.close()
            conexion.close()
    
    return redirect(url_for('clientes'))

# Ruta para editar un cliente
@app.route('/editar_cliente/<int:id_cliente>', methods=['GET', 'POST'])
def editar_cliente(id_cliente):
    conexion = conectar()
    if request.method == 'POST':
        nombre = request.form['nombre']
        ap_paterno = request.form['apellido_paterno']
        ap_materno = request.form['apellido_materno']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        email = request.form['email']
        
        if conexion:
            cursor = conexion.cursor()
            try:
                query = """UPDATE Clientes
                           SET Nombre = %s, Ap_Paterno = %s, Ap_Materno = %s, Direccion = %s, Telefono = %s, Email = %s
                           WHERE ID_Cliente = %s"""
                cursor.execute(query, (nombre, ap_paterno, ap_materno, direccion, telefono, email, id_cliente))
                conexion.commit()
            except Error as e:
                print(f"Error al actualizar cliente: {e}")
            finally:
                cursor.close()
                conexion.close()
        return redirect(url_for('clientes'))

    # Si el método es GET, mostramos el formulario de edición
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Clientes WHERE ID_Cliente = %s", (id_cliente,))
        cliente = cursor.fetchone()
        cursor.close()
        conexion.close()
        return render_template('editar_cliente.html', cliente=cliente)
    return "Error al conectar a la base de datos"

# Ruta para eliminar un cliente
@app.route('/eliminar_cliente/<int:id_cliente>', methods=['POST'])
def eliminar_cliente(id_cliente):
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM Clientes WHERE ID_Cliente = %s", (id_cliente,))
            conexion.commit()
        except Error as e:
            print(f"Error al eliminar cliente: {e}")
        finally:
            cursor.close()
            conexion.close()
    return redirect(url_for('clientes'))

# Ruta para mostrar clientes y sus pedidos
@app.route('/clientes_pedidos')
def clientes_pedidos():
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT Pedidos.ID_Pedido, Clientes.Nombre, Clientes.Ap_Paterno, Pedidos.Fecha_Hora, Pedidos.Estado
            FROM Clientes
            JOIN Pedidos ON Clientes.ID_Cliente = Pedidos.ID_Cliente;
        """)
        clientes_pedidos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return render_template('clientes_pedidos.html', clientes_pedidos=clientes_pedidos)
    return "Error al conectar a la base de datos"

# Ruta para hacer un pedido
@app.route('/hacer_pedido', methods=['POST'])
def hacer_pedido():
    conexion = conectar()
    if conexion:
        nombre = request.form['nombre']
        ap_paterno = request.form['ap_paterno']
        fecha_hora = request.form['fecha_hora']
        direccion_entrega = request.form['direccion_entrega']
        estado = request.form['estado']

        cursor = conexion.cursor()
        # Busca el ID del cliente por nombre y apellido
        query_cliente = """
            SELECT ID_Cliente FROM Clientes 
            WHERE TRIM(LOWER(Nombre)) = TRIM(LOWER(%s)) 
            AND TRIM(LOWER(Ap_Paterno)) = TRIM(LOWER(%s))
        """

        cursor.execute(query_cliente, (nombre, ap_paterno))
        cliente = cursor.fetchone()

        if cliente:
            id_cliente = cliente[0]
            query = """
            INSERT INTO Pedidos (ID_Cliente, Fecha_Hora, Direccion_Entrega, Estado)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (id_cliente, fecha_hora, direccion_entrega, estado))
            conexion.commit()
            cursor.close()
            conexion.close()
            return redirect(url_for('clientes_pedidos'))
        else:
            cursor.close()
            conexion.close()
            return "Cliente no encontrado"
    return "Error al conectar a la base de datos"

# Ruta para editar un pedido
@app.route('/editar_pedido/<int:id_pedido>', methods=['GET', 'POST'])
def editar_pedido(id_pedido):
    conexion = conectar()
    if conexion:
        if request.method == 'POST':
            fecha_hora = request.form['fecha_hora']
            direccion_entrega = request.form['direccion_entrega']
            estado = request.form['estado']

            cursor = conexion.cursor()
            query = """
                UPDATE Pedidos 
                SET Fecha_Hora = %s, Direccion_Entrega = %s, Estado = %s 
                WHERE ID_Pedido = %s
            """
            cursor.execute(query, (fecha_hora, direccion_entrega, estado, id_pedido))
            conexion.commit()
            cursor.close()
            conexion.close()
            return redirect(url_for('clientes_pedidos'))
        
        # Si es GET, obtener los detalles del pedido
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Pedidos WHERE ID_Pedido = %s", (id_pedido,))
        pedido = cursor.fetchone()
        cursor.close()
        conexion.close()
        return render_template('editar_pedido.html', pedido=pedido)
    return "Error al conectar a la base de datos"

# Ruta para eliminar un pedido
@app.route('/eliminar_pedido/<int:id_pedido>', methods=['POST'])
def eliminar_pedido(id_pedido):
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        query = "DELETE FROM Pedidos WHERE ID_Pedido = %s"
        cursor.execute(query, (id_pedido,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect(url_for('clientes_pedidos'))
    return "Error al conectar a la base de datos"

if __name__ == '__main__':
    app.run(port=3000, debug=True)
