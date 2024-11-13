from database.conexion import *
from email_validator import validate_email, EmailNotValidError


def chequear(email):
    conexion = Database()
    conexion = conexion.conectar_db()
    cursor = conexion.cursor()

    # Consulta para verificar si el correo ya está registrado
    sql = "SELECT * FROM usuarios WHERE correo = %s"
    cursor.execute(sql, (email,))
    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()
    if not resultado:
        try:
            v = validate_email(email)
            email = v.email
            return True

        except EmailNotValidError:
            return

    return
