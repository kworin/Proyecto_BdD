def agregar_cliente(nombre, ap_paterno, ap_materno, direccion, telefono, email):
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        query = """INSERT INTO Clientes (Nombre, Ap_Paterno, Ap_Materno, Direccion, Telefono, Email)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        valores = (nombre, ap_paterno, ap_materno, direccion, telefono, email)
        cursor.execute(query, valores)
        conexion.commit()
        print("Cliente agregado exitosamente")
    except Error as e:
        print(f"Error al agregar cliente: {e}")
    finally:
        cursor.close()
        cerrar_conexion(conexion)

# Ejemplo de uso
agregar_cliente('Ana', 'Perez', 'Gomez', 'Calle Azul 123', '8145678901', 'ana@gmail.com')
