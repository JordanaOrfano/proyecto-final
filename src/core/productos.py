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

    def buscar_productos(self, busqueda, orden):
        conexion = Database()
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
                    JOIN productos ON lotes.producto_id = productos.id
                    """

        sql_lotes = """
                    SELECT 
                        lotes.lote, 
                        productos.nombre, 
                        productos.marca, 
                        lotes.cantidad, 
                        lotes.fecha_vencimiento
                    FROM 
                        lotes
                    JOIN
                        productos ON lotes.producto_id = productos.id
                """

        if busqueda:
            sql_productos += f" WHERE productos.id LIKE %s OR productos.nombre LIKE %s OR productos.marca LIKE %s OR productos.categoria LIKE %s"
            sql_lotes += f" WHERE lotes.lote LIKE %s OR productos.nombre LIKE %s OR productos.marca LIKE %s"
            criterio_busqueda = busqueda

        if not busqueda:
            sql_productos += f" WHERE lotes.fecha_vencimiento >= CURDATE()"
            sql_lotes += f" WHERE lotes.fecha_vencimiento >= CURDATE()"

        sql_productos += f"GROUP BY productos.id, productos.nombre, productos.marca, productos.categoria, productos.precio_compra, productos.precio_venta"

        if orden != "Ordenar por":
            orden_tabla_productos, orden_tabla_lotes = self.ordenamiento(orden)
            sql_productos += f" ORDER BY {orden_tabla_productos};"
            sql_lotes += f" ORDER BY {orden_tabla_lotes};"
            

        if criterio_busqueda:
            tabla_productos = conexion.consultar_bd(sql_productos, ("%" + criterio_busqueda + "%",) * 4)
            tabla_lotes = conexion.consultar_bd(sql_lotes, ("%" + criterio_busqueda + "%",) * 3)
            return tabla_productos, tabla_lotes


        tabla_productos = conexion.consultar_bd(sql_productos, None)
        tabla_lotes = conexion.consultar_bd(sql_lotes, None)
        return tabla_productos, tabla_lotes


    def ordenamiento(self, orden):
        orden_tabla_lotes = "lotes.lote"

        if orden == "ID":
            orden_tabla_productos = "productos.id"

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
            fecha_vencimiento = fila[4]
            fecha_formateada = fecha_vencimiento.strftime("%d/%m/%Y")
            fila[4] = fecha_formateada
            lotes_acomodados.append(fila)

        return lotes_acomodados

class MenuTablas:
    def editar_producto(tree):
        item = tree.selection()[0]
        valores = tree.item(item, "values")  # obtiene los valores de la fila
        # Código para abrir una ventana de edición, falta

        CTkAlert(
            state="warning",
            title="Editar producto",
            body_text=f"Editar producto: {valores[1]}",
            btn1="Ok",
        )

    def eliminar_producto(tree):
        item = tree.selection()[0]
        valores = tree.item(item, "values")
        respuesta = CTkAlert(
            state="warning",
            title="Eliminar producto",
            body_text=f"¿Desea eliminar el producto {valores[1]}?",
            btn1="Si",
            btn2="No",
        )

        if respuesta.get() == "Si":
            tree.delete(item)
            # Código para eliminar el producto de la base de datos, falta

            CTkAlert(
                state="warning",
                title="Eliminar producto",
                body_text=f"Producto {valores[1]} eliminado.",
                btn1="Ok",
            )

    def agregar_a_carrito(tree):
        item = tree.selection()[0]
        valores = tree.item(item, "values")
        # Código para agregar el producto al carrito, falta

        CTkAlert(
            state="info",
            title="Agregar al producto",
            body_text=f"Producto {valores[1]} agregado.",
            btn1="Ok",
        )
