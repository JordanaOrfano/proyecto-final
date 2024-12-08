from config.config import *
from gui.componentes import *
from core.productos import *

from collections import defaultdict


class RevisarVentas:
    def __init__(self, contenedor):
        self.contenedor = contenedor
        self.conexion = Database()

        frame_ventas = ctk.CTkFrame(self.contenedor, fg_color=COLOR_BG)
        frame_ventas.pack(expand=True, fill="x", padx=40)

        crear_label(
            frame_ventas,
            text="Revisar ventas",
            font=("Roboto", 32, "bold"),
            pady=(30, 0),
            padx=0
        )

        # Contadores
        frame_contadores = ctk.CTkFrame(frame_ventas, fg_color=COLOR_BG)
        frame_contadores.pack(fill="x", pady=(0, 20))
        
        self.contador_ventas = crear_stat(
            frame_contadores,
            " Productos vendidos",
            "0",
            padx=5,
            pady=30,
            image=crear_imagen("src/assets/icons/alarm.png", size=(40, 40)),
        )

        self.contador_ganancias = crear_stat(
            frame_contadores,
            " Ganancias",
            "$0.00",
            padx=5,
            pady=30,
            image=crear_imagen("src/assets/icons/dollar.png", size=(40, 40)),
        )

        ventas_hoy = self.obtener_ventas_hoy()
        ventas_totales = self.obtener_ventas_totales()
        self.generar_tablas(frame_ventas, ventas_hoy, ventas_totales)

    def obtener_ventas_hoy(self):
        VALORES_HOY = []
        ventas_agrupadas_hoy = defaultdict(lambda: {"cantidad": 0, "ganancia": 0.0}) # Creamos defaultdict para facilitar el contar las apariciciones de un producto en la tabla ventas y ganancia
        productos_agrupados_hoy = defaultdict(lambda: {"cantidad": 0, "ganancia": 0.0}) 

        # ----- Ventas Últimas 24 horas -----

        # QUERY para ventas de las últimas 24 horas
        sql_detalles_hoy = """
            SELECT 
                productos.id AS producto_id,
                productos.nombre,
                productos.marca,
                SUM(COALESCE(ventas.ganancia_venta, 0)) AS ganancia_total
            FROM 
                ventas
            JOIN 
                productos
            ON 
                FIND_IN_SET(productos.id, ventas.producto_id) > 0
            WHERE 
                ventas.fecha_venta >= NOW() - INTERVAL 1 DAY  
            GROUP BY 
                productos.id, productos.nombre, productos.marca;
        """

        detalles_ventas_hoy = self.conexion.ejecutar_bd(sql_detalles_hoy, valores=None)

        ventas_hoy = self.conexion.ejecutar_bd(
            sql="""
                SELECT 
                    producto_id, 
                    cantidad_vendida,
                    ganancia_unitaria
                FROM 
                    ventas
                WHERE 
                    fecha_venta >= NOW() - INTERVAL 1 DAY
            """,
            valores=None,
        )

        # Agrupar ventas diarias
        for productos, cantidades, ganancias in ventas_hoy: 
            ids = productos.split(",")
            cantidades_vendidas = cantidades.split(",")
            ganancias_venta = ganancias.split(",")

            # Almacenamos los valores en un diccionario para limpiar los datos
            # El zip itera simultaneamente sobre las listas id_producto, cantidad y ganancia. Ahorra unos for.
            for id_producto, cantidad, ganancia in zip(
                ids, cantidades_vendidas, ganancias_venta
            ):
                ventas_agrupadas_hoy[id_producto]["cantidad"] += int(cantidad)
                ventas_agrupadas_hoy[id_producto]["ganancia"] += float(ganancia)

        # Agrupamos las ventas y productos para mostrar la cantidad y ganancia en una fila 
        for detalle in detalles_ventas_hoy:
            producto_id = str(detalle[0])
            nombre = detalle[1]
            marca = detalle[2]
            cantidad_vendida = ventas_agrupadas_hoy[producto_id]["cantidad"]
            ganancia_total = ventas_agrupadas_hoy[producto_id]["ganancia"]
            key = (nombre, marca)
            productos_agrupados_hoy[key]["cantidad"] += cantidad_vendida
            productos_agrupados_hoy[key]["ganancia"] += ganancia_total

        # Organizamos todo en una lista limpia para pasarlo a la tabla
        for (nombre, marca), data in productos_agrupados_hoy.items():
            cantidad = data["cantidad"]
            ganancia = data["ganancia"]
            VALORES_HOY.append((nombre, marca, cantidad, ganancia))

        return VALORES_HOY

    def obtener_ventas_totales(self):
        ganancia_total = 0
        VALORES_TOTALES = []
        productos_agrupados_totales = defaultdict(lambda: {"cantidad": 0, "ganancia": 0.0})
        ventas_agrupadas_totales = defaultdict(lambda: {"cantidad": 0, "ganancia": 0.0})

        # ----- Ventas Totales -----
        # Consulta para ventas totales
        sql_detalles_totales = """
            SELECT 
                productos.id AS producto_id,
                productos.nombre,
                productos.marca
            FROM 
                ventas
            JOIN 
                productos
            ON 
                FIND_IN_SET(productos.id, ventas.producto_id) > 0
            GROUP BY 
                productos.id, productos.nombre, productos.marca;
        """
        detalles_ventas_totales = self.conexion.ejecutar_bd(
            sql_detalles_totales, valores=None
        )

        ventas_totales = self.conexion.ejecutar_bd(
            sql="""
                SELECT 
                    producto_id, 
                    cantidad_vendida,
                    ganancia_unitaria
                FROM 
                    ventas
            """,
            valores=None,
        )

        # Agrupar ventas totales
        for productos, cantidades, ganancias in ventas_totales:
            ids = productos.split(",")
            cantidades_vendidas = cantidades.split(",")
            ganancias_venta = ganancias.split(",")
            for id_producto, cantidad, ganancia in zip(
                ids, cantidades_vendidas, ganancias_venta
            ):
                ventas_agrupadas_totales[id_producto]["cantidad"] += int(cantidad)
                ventas_agrupadas_totales[id_producto]["ganancia"] += float(ganancia)
                
        # Unificar productos totales por nombre y marca
        for detalle in detalles_ventas_totales:
            producto_id = str(detalle[0])
            nombre = detalle[1]
            marca = detalle[2]
            cantidad_vendida = ventas_agrupadas_totales[producto_id]["cantidad"]
            ganancia_venta_producto = ventas_agrupadas_totales[producto_id]["ganancia"]
            key = (nombre, marca)
            productos_agrupados_totales[key]["cantidad"] += cantidad_vendida
            productos_agrupados_totales[key]["ganancia"] += ganancia_venta_producto

        for (nombre, marca), data in productos_agrupados_totales.items():
            cantidad = data["cantidad"]
            ganancia = data["ganancia"]
            ganancia_total += ganancia
            VALORES_TOTALES.append((nombre, marca, cantidad, ganancia))


        self.contador_ventas.configure(
            text=f" Productos vendidos | {len(VALORES_TOTALES)}"
        )

        self.contador_ganancias.configure(
            text=f" Ganancias ${ganancia_total}"
        )

        return VALORES_TOTALES

    def generar_tablas(self, frame_ventas, VALORES_HOY, VALORES_TOTALES):
        # Crear columnas y encabezados
        columnas = [
            "nombre",
            "marca",
            "cantidad_vendida",
            "ganancias_venta",
        ]

        encabezados = [
            "Nombre",
            "Marca",
            "Cantidad vendida",
            "Ganancias",
        ]

        # Creamos las tablas con un label arriba
        crear_label(
            frame_ventas,
            text="Ventas hoy",
            font=("Roboto", 24, "bold"),
            pady=(0, 0),
        )

        crear_tabla(frame_ventas, columnas, encabezados, VALORES_HOY, pady=10)

        crear_label(
            frame_ventas,
            text="Ventas",
            font=("Roboto", 24, "bold"),
            pady=(20, 0),
        )

        crear_tabla(frame_ventas, columnas, encabezados, VALORES_TOTALES, pady=(10, 20))