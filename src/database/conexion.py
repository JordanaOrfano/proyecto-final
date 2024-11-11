import mysql.connector

class Database:
    def conectar_db(self):
        try:
            conexion = mysql.connector.connect(
                host="localhost", user="root", password="root"
            )
            cursor = conexion.cursor()

            if self.crear_schema_tablas(cursor, conexion):

                conexion.database = "proyecto_final"

                if conexion.is_connected():
                    print("Conexión exitosa a la base de datos")
                return conexion

            conexion.close()
            print("ocurrio un error con la conexion")

        except mysql.connector.Error as error:
            print(f"Error al conectarse: {error}")
            return None

    def consultar_bd(self, sql, valores):
        try:
            conexion = self.conectar_db()
            cursor = conexion.cursor()

            if valores != None:
                cursor.execute(sql, valores)
            else:
                cursor.execute(sql)

            resultados = cursor.fetchall()

            cursor.close()
            conexion.close()

            return resultados

        except mysql.connector.Error as error:
            print(f"Error al hacer la consulta SQL {error}")
            return []


    def crear_schema_tablas(self, cursor, conexion):
        try:
            nombre_schema = "proyecto_final"

            # Verificar si el esquema existe
            cursor.execute(f"SHOW DATABASES LIKE '{nombre_schema}';")
            result = cursor.fetchone()

            if not result:
                cursor.execute(f"CREATE DATABASE {nombre_schema};")
                print(f"Base de datos '{nombre_schema}' creada exitosamente.")

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
                # (ENGINE-INNODB;) Es el motor de almacenamiento Avanzado

                tabla_usuarios = """
                CREATE TABLE IF NOT EXISTS usuarios (
                documento INT PRIMARY KEY,
                correo VARCHAR(60) NOT NULL,
                contrasena VARCHAR(60) NOT NULL,
                nombre VARCHAR(50) NOT NULL,
                apellido VARCHAR(50) NOT NULL
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

                # Seleccionamos el nuevo schema
                conexion.database = nombre_schema

                # Crear la tabla en el nuevo esquema
                cursor.execute(tabla_productos)
                cursor.execute(tabla_lotes)
                cursor.execute(tabla_usuarios)
                cursor.execute(tabla_ventas)
                print("Se creó una base de datos nueva.")

            return True

        except mysql.connector.Error as err:
            print(f"Error al crear el esquema o la tabla: {err}")
            return False