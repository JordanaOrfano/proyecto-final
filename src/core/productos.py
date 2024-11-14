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
    
    def buscar_productos(self):
        pass

    # def buscar_productos(self, criterio_busqueda):
    #     conexion = Database()
        
    #     try:
    #         sql = """
    #             SELECT 
    #                 lotes.lote, 
    #                 productos.nombre,
    #                 productos.marca, 
    #                 productos.categoria, 
    #                 productos.precio_compra, 
    #                 productos.precio_venta, 
    #                 lotes.cantidad, 
    #                 lotes.fecha_vencimiento 
    #             FROM 
    #                 lotes
    #             JOIN 
    #                 productos ON lotes.producto_id = productos.id
    #             WHERE 
    #                 productos.nombre LIKE %s 
    #                 OR productos.marca LIKE %s 
    #                 OR productos.categoria LIKE %s
    #             ORDER BY productos.nombre, lotes.fecha_vencimiento;
    #         """

    #         valores = ("%" + criterio_busqueda + "%",) * 3
    #         resultado = conexion.consultar_bd(sql=sql, valores=valores)

    #         return resultado

    #     except mysql.connector.Error as error:
    #         print(f"Ocurrió un error al buscar productos: {error}")

    #     finally:
    #         conexion.conectar_db().close()
    
    # # def filtrar_productos(self, tree, filtro, productos_vencidos, proximo_vencimiento):
    #     # Limpiar la tabla antes de aplicar el filtro
    #     for item in tree.get_children():
    #         tree.delete(item)

    #     if not productos_vencidos and not proximo_vencimiento:
    #         return  # Añadir mensaje para tabla vacía

    #     else:
    #         if filtro in ["Próximos a vencer", "Todos"]:
    #             for proximo in proximo_vencimiento:
    #                 tree.insert("", tk.END, values=proximo, tags=("proximo",))

    #         if filtro in ["Vencidos", "Todos"]:
    #             for vencido in productos_vencidos:
    #                 tree.insert("", tk.END, values=vencido, tags=("vencido",))

    #     ajustar_altura_tabla(tree, len(tree.get_children()))


class MenuTablas:
    def editar_producto(tree):
        item = tree.selection()[0]
        valores = tree.item(item, "values") # obtiene los valores de la fila
        # Código para abrir una ventana de edición, falta
        
        CTkAlert(state="warning", title="Editar producto", body_text=f"Editar producto: {valores[1]}", btn1="Ok")
    
    def eliminar_producto(tree):
        item = tree.selection()[0]
        valores = tree.item(item, "values")
        respuesta = CTkAlert(state="warning", title="Eliminar producto", body_text=f"¿Desea eliminar el producto {valores[1]}?", btn1="Si", btn2="No")
        
        if respuesta.get() == "Si":
            tree.delete(item)
            # Código para eliminar el producto de la base de datos, falta
            
            CTkAlert(state="warning", title="Eliminar producto", body_text=f"Producto {valores[1]} eliminado.", btn1="Ok")

    def agregar_a_carrito(tree):
        item = tree.selection()[0]
        valores = tree.item(item, "values")
        # Código para agregar el producto al carrito, falta
        
        CTkAlert(state="info", title="Agregar al producto", body_text=f"Producto {valores[1]} agregado.", btn1="Ok")
