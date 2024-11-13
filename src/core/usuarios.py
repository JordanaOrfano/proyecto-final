# Lógica de registro e inicio sesión
from database.conexion import *
import bcrypt  # Para enscriptar contraseñas


class Usuario:
    def __init__(self, correo, contrasena):
        self.correo = correo
        self.__contrasena = contrasena
        self.conexion = Database()

    def encriptar_contrasena(self):
        # Genera una cadena de texto aleatoria en formato de bytes
        salt = bcrypt.gensalt()
        self.__hashed = bcrypt.hashpw(self.__contrasena.encode("utf-8"), salt)
        return self.__hashed

    def registrar_usuario(self, dni, nombre, apellido):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

        try:
            self.__hashed = self.encriptar_contrasena()
            valores = (self.dni, self.correo, self.__hashed, self.nombre, self.apellido)
            sql = "insert into usuarios values(%s, %s, %s, %s, %s, 'empleado')"

            consulta = self.conexion.consultar_bd(sql, valores)

        except mysql.connector.Error as error:
            print("Ocurrio un error al guardar los datos", error)

    def verificar_usuario(self, correo_ingresado, contrasena_ingresada):
        try:
            correo_ingresado = correo_ingresado
            self.__contrasena_ingresada = contrasena_ingresada

            conexion = self.conexion.conectar_db()

            if conexion is None:
                print("Error: No se pudo establecer la conexión a la base de datos")
                return False

            cursor = conexion.cursor()
            sql = "SELECT contrasena FROM usuarios WHERE correo = %s"
            cursor.execute(sql, (correo_ingresado,))
            resultado = (
                cursor.fetchone()
            )  # Devuelve la primer fila con los valores, si no lo encuentra devuelve none

            sql = "SELECT nombre, apellido, rol FROM usuarios WHERE correo = %s"
            cursor.execute(sql, (correo_ingresado,))

            Usuario.usuario_actual = cursor.fetchone()
            

            cursor.close()
            conexion.close()

            if resultado:
                self.__hashed = resultado[0]  # Obtiene la contraseña del resultado
                if bcrypt.checkpw(
                    self.__contrasena_ingresada.encode("utf-8"),
                    self.__hashed.encode("utf-8"),
                ):
                    return True
                else:
                    return False
            else:
                return False

        except mysql.connector.Error as error:
            print("Ocurrio un error al verificar los datos", error)
