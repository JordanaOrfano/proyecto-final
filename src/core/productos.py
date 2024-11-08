from config.config import *
from gui.componentes import *


class Productos:
    def subir_producto_a_bd(
        self,
        nombre_lote,
        nombre_producto,
        marca,
        precio_compra,
        precio_venta,
        categoria,
        cantidad,
        vencimiento,
    ):

        try:
            conexion = conectar_db()
            cursor = conexion.cursor()
            fecha_creacion = datetime.now().date()

            sql = "SELECT id, nombre FROM productos WHERE nombre = %s"

            cursor.execute(sql, (nombre_producto,))
            existe = cursor.fetchone()

            if not existe:
                sql = "insert into productos values(null, %s, %s, %s, %s, %s)"

                valores = (
                    nombre_producto,
                    marca,
                    categoria,
                    precio_compra,
                    precio_venta,
                )

                cursor.execute(sql, valores)
                producto_id = cursor.lastrowid

            else:
                producto_id = existe[0]  # Obtiene el id del producto existente

            sql = "INSERT INTO lotes VALUES(null, %s, %s, %s, %s, %s)"
            valores = (nombre_lote, producto_id, cantidad, vencimiento, fecha_creacion)

            cursor.execute(sql, valores)
            conexion.commit()

        except mysql.connector.Error as error:
            conexion.rollback()
            print(f"Ocurrió un error {error}")

        finally:
            cursor.close()
            conexion.close()

    def obtener_productos(self):
        try:
            sql = "SELECT * FROM productos ORDER BY id DESC"
            conexion = conectar_db()

            # Vamos a usar el cursor como un diccionario para acceder con claves y valores
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(sql)

            # Obtenemos todas los productos
            productos = cursor.fetchall()

            cursor.close()
            conexion.close()

            return productos

        except mysql.connector.Error as error:
            print("Ocurrió un error al pedir los productos", error)
