from config.config import *
from gui.componentes import *


class Productos:
    def subir_producto_a_bd(
        self,
        nombre_producto,
        marca,
        precio_compra,
        precio_venta,
        categoria,
        cantidad,
        vencimiento,
    ):

        try:
            conexion = Database()
            conexion = conexion.conectar_db()
            cursor = conexion.cursor()

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

            sql = "INSERT INTO lotes VALUES(null, %s, %s, %s)"
            valores = (producto_id, cantidad, vencimiento)

            cursor.execute(sql, valores)
            conexion.commit()

        except mysql.connector.Error as error:
            conexion.rollback()
            print(f"Ocurrió un error {error}")

        finally:
            cursor.close()
            conexion.close()

    def obtener_categorias(self):
        try:
            sql = "SELECT distinct categoria FROM proyecto_final.productos"
            conexion = Database()
            conexion = conexion.conectar_db()

            cursor = conexion.cursor()
            cursor.execute(sql)

            categorias = cursor.fetchall()
            categorias_lista = [categoria[0] for categoria in categorias]

            cursor.close()
            conexion.close()

            return categorias_lista

        except mysql.connector.Error as error:
            print("Ocurrió un error al obtener las categorias", error)
