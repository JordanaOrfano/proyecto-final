from database.conexion import *
from email_validator import validate_email, EmailNotValidError


def chequear(documento, correo):
    conexion = Database()
    dni_limpio = False

    if documento:
        dni_limpio = documento.replace(".", "").replace(",", "").replace("-", "")
        
        # Verificar que el dni_limpio solo contenga números
        if not dni_limpio.isdigit():
            return False, False
            # Retorna False si contiene letras u otros caracteres no numéricos
            
        if int(dni_limpio) < 20000000 or int(dni_limpio) > 200000000:
            return False, False

    if correo and len(correo) < 60:
        try:
            # Verifica el correo
            v = validate_email(correo)
            correo_valido = v.email

        except EmailNotValidError:
            return dni_limpio, False
    
    if dni_limpio:
        # Consulta para verificar si el documento o correo ya están registrados
        sql = "SELECT * FROM usuarios WHERE documento = %s OR correo = %s"
        valores = (dni_limpio, correo)
        resultado = conexion.ejecutar_bd(sql, valores, "diccionario")
    
        # Si no hay resultados        
        if not resultado:
            return dni_limpio, True
            # Retorna True para documento sin comas ni puntos y True para correo válido.
        
        else:
            if resultado[0]["documento"] == dni_limpio and resultado[0]["correo"] == correo:
                return False, False
            
            if resultado[0]["documento"] == dni_limpio:
                return False, True
            
            if resultado[0]["correo"] == correo:
                return dni_limpio, False
            
        return False, False
    return dni_limpio, False

