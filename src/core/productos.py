from config.config import *
from gui.componentes import *


class Productos:
    def __init__(self):
        self.database = Database()

from config.config import *
from gui.componentes import *

class Productos:
    def __init__(self):
        self.database = Database()

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

        # Manejar productos categorizados en 3 categorias: "Producto Nuevo", "Producto con todos los datos iguales" y "Producto con precios diferentes al existente"
        try:
            sql_principal = """
                SELECT 
                    productos.id,
                    productos.nombre, 
                    productos.marca, 
                    productos.precio_compra, 
                    productos.precio_venta,
                    lotes.cantidad,
                    lotes.fecha_vencimiento 
                FROM productos 
                JOIN lotes ON lotes.producto_id = productos.id
                WHERE productos.mostrar = 1
            """

            valores = (nombre_producto, marca, precio_compra, precio_venta, vencimiento)

            # Comprobar si el producto tiene la misma fecha de vencimiento al existente
            sql_misma_fecha = sql_principal + """
                AND productos.nombre = %s 
                AND productos.marca = %s 
                AND productos.precio_compra = %s 
                AND productos.precio_venta = %s 
                AND lotes.fecha_vencimiento = %s
            """

            # Comprobar si el producto tiene diferente fecha de vencimiento al existente
            sql_diferente_fecha = sql_principal + """
                AND productos.nombre = %s 
                AND productos.marca = %s 
                AND productos.precio_compra = %s 
                AND productos.precio_venta = %s 
                AND lotes.fecha_vencimiento != %s
            """

            producto_misma_fecha = self.database.ejecutar_bd(sql_misma_fecha, valores)
            producto_diferente_fecha = self.database.ejecutar_bd(sql_diferente_fecha, valores)

            # Productos con todos los datos iguales, incluso la fecha solo se suma a su lote.
            if producto_misma_fecha:
                for producto in producto_misma_fecha:
                    cantidad_existente = producto[5]
                    cantidad += cantidad_existente
                    id = producto[0]
                sql = """
                    UPDATE lotes 
                    SET cantidad = %s
                    WHERE producto_id = %s AND fecha_vencimiento = %s
                """
                valores = (cantidad, id, vencimiento)
                self.database.ejecutar_bd(sql, valores, "update")
                return True  # Retorna true si todo se ejecutó correctamente

            # Productos con todos los datos iguales, excepto la fecha. Solo se introduce en lotes pero no en la tabla productos.
            if producto_diferente_fecha:
                for producto in producto_diferente_fecha:
                    producto_id = producto[0]

                sql = "INSERT INTO lotes VALUES(null, %s, %s, %s, %s)"

                valores = (producto_id, cantidad, vencimiento, 1)
                self.database.ejecutar_bd(sql, valores, "insert")
                return True

            # Subir como producto nuevo a la tabla productos y lotes
            sql = """
                INSERT INTO productos values(null, %s, %s, %s, %s, %s, %s)
            """
            
            valores = (nombre_producto, marca, categoria, precio_compra, precio_venta, 1)
            producto_id = self.database.ejecutar_bd(sql, valores, "insert")

            # Subir a lotes
            sql = "INSERT INTO lotes VALUES(null, %s, %s, %s, %s)"
            valores = (producto_id, cantidad, vencimiento, 1)
            self.database.ejecutar_bd(sql, valores, "insert")
            
            # Mostrar Productos con lotes asociados mostrar = True
            sql_productos_visibles = """
                UPDATE productos
                SET mostrar = 1
                WHERE id IN (
                    SELECT DISTINCT producto_id
                    FROM lotes
                    WHERE mostrar = 1
                )
            """
            self.database.ejecutar_bd(sql_productos_visibles, tipo="update")

            return True

        except mysql.connector.Error as error:
            print(f"Ocurrió un error {error}")
            return False


    def obtener_categorias(self):
        try:
            sql = "SELECT distinct categoria FROM proyecto_final.productos"

            categorias = self.database.ejecutar_bd(sql)
            categorias_lista = []
            for categoria in categorias:
                categorias_lista.append(categoria[0])

            return categorias_lista

        except mysql.connector.Error as error:
            print("Ocurrió un error al obtener las categorias", error)

    def buscar_productos(self, busqueda, orden):
        criterio_busqueda = None

        sql_productos = """
                    SELECT
                        productos.id,
                        productos.nombre, 
                        productos.marca, 
                        productos.categoria, 
                        productos.precio_compra, 
                        productos.precio_venta, 
                        SUM(lotes.cantidad) AS cantidad 
                    FROM 
                        lotes 
                    JOIN 
                        productos ON lotes.producto_id = productos.id
                    """

        sql_lotes = """
                    SELECT 
                        lotes.lote, 
                        productos.id,
                        productos.nombre, 
                        productos.marca, 
                        lotes.cantidad, 
                        lotes.fecha_vencimiento,
                        productos.precio_venta
                    FROM 
                        lotes
                    JOIN
                        productos ON lotes.producto_id = productos.id
                """

        if busqueda:
            sql_productos += f" WHERE (productos.id LIKE %s OR productos.nombre LIKE %s OR productos.marca LIKE %s OR productos.categoria LIKE %s) AND lotes.fecha_vencimiento >= CURDATE() AND productos.mostrar = 1 AND lotes.cantidad > 0"
            sql_lotes += f" WHERE (lotes.lote LIKE %s OR productos.nombre LIKE %s OR productos.marca LIKE %s) AND lotes.fecha_vencimiento >= CURDATE() AND productos.mostrar = 1 AND lotes.cantidad > 0"
            criterio_busqueda = busqueda

        if not busqueda:
            sql_productos += f" WHERE lotes.fecha_vencimiento >= CURDATE() AND productos.mostrar = 1 AND lotes.cantidad > 0"
            sql_lotes += f" WHERE lotes.fecha_vencimiento >= CURDATE() AND productos.mostrar = 1 AND lotes.cantidad > 0"

        sql_productos += f" GROUP BY productos.id, productos.nombre, productos.marca, productos.categoria, productos.precio_compra, productos.precio_venta"

        if orden != "Ordenar por":
            orden_tabla_productos, orden_tabla_lotes = self.ordenamiento(orden)
            sql_productos += f" ORDER BY {orden_tabla_productos};"
            sql_lotes += f" ORDER BY {orden_tabla_lotes};"

        if orden == "Ordenar por":
            orden_tabla_lotes = "productos.nombre"
            sql_lotes += f" ORDER BY {orden_tabla_lotes};"

        if criterio_busqueda:
            tabla_productos = self.database.ejecutar_bd(
                sql_productos, ("%" + criterio_busqueda + "%",) * 4, "select"
            )
            tabla_lotes = self.database.ejecutar_bd(
                sql_lotes, ("%" + criterio_busqueda + "%",) * 3, "select"
            )
            return tabla_productos, tabla_lotes

        tabla_productos = self.database.ejecutar_bd(sql_productos, None)
        tabla_lotes = self.database.ejecutar_bd(sql_lotes, None)
        return tabla_productos, tabla_lotes

    def ordenamiento(self, orden):
        orden_tabla_lotes = "productos.nombre"

        if orden == "ID":
            orden_tabla_productos = "productos.id"
            orden_tabla_lotes = "lotes.lote"

        if orden == "Nombre":
            orden_tabla_productos = "productos.nombre"
            orden_tabla_lotes = "productos.nombre"

        if orden == "Marca":
            orden_tabla_productos = "productos.marca"
            orden_tabla_lotes = "productos.marca"

        if orden == "Categoría":
            orden_tabla_productos = "productos.categoria"

        return orden_tabla_productos, orden_tabla_lotes

    def transformar_lotes_a_lista(self, lotes):
        lotes_lista = []
        lotes_acomodados = []

        for fila in lotes:
            lotes_lista.append(list(fila))

        for fila in lotes_lista:
            fecha_vencimiento = fila[5]
            fecha_formateada = fecha_vencimiento.strftime("%d/%m/%Y")
            fila[5] = fecha_formateada
            lotes_acomodados.append(fila)

        return lotes_acomodados

