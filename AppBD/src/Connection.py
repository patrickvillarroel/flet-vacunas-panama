import pyodbc


def conexion():
    try:
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=PATRICHENKO;DATABASE=MINSA;Trusted_Connection=yes;')
        print("Conexion existosa")
        return connection
    except Exception as ex:
        print(ex)

def conexionU(user, password, tipo):
    try:
        conn = 0
        connection = conexion()
        cursor = connection.cursor()
        query = f"exec spUsuarios '{user}', '{tipo}'"
        print(query)
        result = cursor.execute(query)
        datos = result.fetchall()
        for row in datos:
            cedula = row[0]
            usuario = row[1]
            tipo = row[2]
            clave = row[3]

        print(cedula, clave, password)
        if datos is None:
            return f"No se encontró ningún usuario con el nombre de usuario: ", user
        else:
            if (usuario == user and tipo == tipo and clave == password):
                return "None"
            else:
                return f"Clave Invalida"
    except Exception as ex:
        print(ex)

def insertP(nombre, user, password, tipo):
    try:
        conn = 0
        connection = conexion()
        cursor = connection.cursor()
        query = f"exec crearUsuario'{nombre}', '{user}', '{password}','{tipo}'"
        print(query)
        cursor.execute(query)
        cursor.commit()
        datos = conexionU(user, password, tipo)
        if datos is None:
            return f"No se pudo crear la cuenta, vuelva a intentarlo: "
        else:
            return "None"

    except Exception as ex:
        print(ex)


def fetch_data():
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("select * from [Vista Paciente]")
    data = cursor.fetchall()
    conn.close()
    return data
