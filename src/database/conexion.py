import mysql.connector


class Database:
    def __init__(self):
        self.conexion = None

    def conectar_db(self):
        try:
            if self.conexion is None or not self.conexion.is_connected():
                self.conexion = mysql.connector.connect(
                    host="localhost", user="root", password="root"
                )

                self.crear_schema_tablas()
                
                print("Conexión exitosa a la base de datos")
            return self.conexion

        except mysql.connector.Error as error:
            print(f"Error al conectarse: {error}")
            return None
                
    def ejecutar_bd(self, sql, valores=None, tipo="select"):
        try:
            conexion = self.conectar_db()

            if tipo == "diccionario":
                with conexion.cursor(dictionary=True) as cursor:
                    if valores:
                        cursor.execute(sql, valores) 

                    else:
                        cursor.execute(sql)

                    resultados = cursor.fetchall()  
                    return resultados
            else:
                with conexion.cursor() as cursor:

                    if valores:
                        cursor.execute(sql, valores) 

                    else:
                        cursor.execute(sql)

                    # Si es un SELECT, retornar resultados
                    if tipo == "select":
                        resultados = cursor.fetchall()
                        return resultados
                    
                    # Si es un INSERT, UPDATE, DELETE, hacer commit
                    if tipo != "diccionario" and tipo !="select":
                        conexion.commit()
                        if tipo == "insert":
                            return cursor.lastrowid # Obtengo el id del último registro ingresado para usarlo como clave foranea
                        return True  # Sirve para retornar true y señalar que todo fue correcto

        except mysql.connector.Error as error:
            print(f"Error al ejecutar la consulta SQL {error}")
            return False
        finally:
            self.cerrar_conexion()

    def crear_schema_tablas(self):
        try:
            conexion = self.conectar_db()
            with conexion.cursor() as cursor:
                nombre_schema = "proyecto_final"

                # Verificar si el esquema existe
                cursor.execute(f"SHOW DATABASES LIKE '{nombre_schema}';")
                result = cursor.fetchone()

                if not result:
                    cursor.execute(f"CREATE DATABASE {nombre_schema};")
                    self.conexion.database = "proyecto_final"   
                    print(f"Base de datos '{nombre_schema}' creada exitosamente.")

                    # Crear tablas
                    self._crear_tablas(cursor)

                conexion.database = nombre_schema
                return True

        except mysql.connector.Error as err:
            print(f"Error al crear el esquema o las tablas: {err}")
            return False
        
    def cerrar_conexion(self):
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()
            print("Conexión cerrada correctamente")

    def _crear_tablas(self, cursor):
        tabla_productos = """
        CREATE TABLE IF NOT EXISTS productos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(30) NOT NULL,
            marca VARCHAR(30) NOT NULL,
            categoria VARCHAR(30) NOT NULL, 
            precio_compra DECIMAL(10, 2) NOT NULL,
            precio_venta DECIMAL(10, 2) NOT NULL
        ) ENGINE=INNODB;
        """
        tabla_lotes = """
        CREATE TABLE IF NOT EXISTS lotes (
            lote INT AUTO_INCREMENT PRIMARY KEY,
            producto_id INT NOT NULL,
            cantidad INT NOT NULL,
            fecha_vencimiento DATE,
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        ) ENGINE=INNODB;
        """
        tabla_usuarios = """
        CREATE TABLE IF NOT EXISTS usuarios (
            documento INT PRIMARY KEY,
            correo VARCHAR(60) NOT NULL,
            contrasena VARCHAR(60) NOT NULL,
            nombre VARCHAR(50) NOT NULL,
            apellido VARCHAR(50) NOT NULL,
            rol VARCHAR(20) DEFAULT 'empleado'
        ) ENGINE=INNODB;
        """
        tabla_ventas = """
        CREATE TABLE IF NOT EXISTS ventas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            producto_id INT NOT NULL,
            cantidad_vendida INT NOT NULL,
            ganancia_venta DECIMAL(10, 2) NOT NULL,
            fecha_venta DATE,
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        ) ENGINE=INNODB;
        """

        # Crear las tablas
        cursor.execute(tabla_productos)
        cursor.execute(tabla_lotes)
        cursor.execute(tabla_usuarios)
        cursor.execute(tabla_ventas)
        print("Tablas creadas exitosamente.")
