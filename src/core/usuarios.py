# Lógica de registro e inicio sesión
from database.conexion import *
import bcrypt  # Para encriptar contraseñas


class Usuario:
    def __init__(self, correo, contrasena):
        self.correo = correo
        self.__contrasena = contrasena
        self.database = Database()


    def encriptar_contrasena(self):
        # Genera una cadena de texto aleatoria en formato de bytes
        salt = bcrypt.gensalt()
        self.__hashed = bcrypt.hashpw(self.__contrasena.encode("utf-8"), salt)
        return self.__hashed

    def registrar_usuario(self, dni, nombre, apellido, rol = "empleado"):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

        try:
            self.__hashed = self.encriptar_contrasena()
            valores = (self.dni, self.correo, self.__hashed, self.nombre, self.apellido, rol)
            sql = "insert into usuarios values(%s, %s, %s, %s, %s, %s)"

            consulta = self.database.ejecutar_bd(sql, valores, "insert")

        except mysql.connector.Error as error:
            print("Ocurrio un error al guardar los datos", error)

    def verificar_usuario(self, correo_ingresado, contrasena_ingresada):
        try:
            correo_ingresado = correo_ingresado
            self.__contrasena_ingresada = contrasena_ingresada

            sql = "SELECT nombre, apellido, rol, contrasena, correo, documento FROM usuarios WHERE correo = %s"
            Usuario.usuario_actual = self.database.ejecutar_bd(sql, (correo_ingresado,))

            if Usuario.usuario_actual:
                self.__hashed = Usuario.usuario_actual[0][3]  # Obtiene la contraseña de Usuario.usuario_actual
                
                if bcrypt.checkpw(self.__contrasena_ingresada.encode("utf-8"), self.__hashed.encode("utf-8")):
                    return True
                else:
                    return False
            else:
                return False

        except mysql.connector.Error as error:
            print("Ocurrio un error al verificar los datos", error)
