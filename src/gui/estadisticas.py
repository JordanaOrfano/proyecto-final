from config.config import *
from gui.componentes import *
from gui.agregar_producto import *
from core.productos import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Permite renderizar los gráficos directamente en CustomTkinter


class Estadisticas:
    def __init__(self, contenedor):
        self.contenedor = contenedor
        self.productos = Productos()
        self.conexion = Database()
        self.colors = ("#0c955a", "#6a994e", "#386641", "#0a7e4c", "#43B56B", "#8CC263", "#3A8C61")

        # ------------------------------------- Interfaz -------------------------------------
        frame_estadisticas = ctk.CTkScrollableFrame(master=self.contenedor, fg_color=COLOR_BG)
        frame_estadisticas.pack(expand=True, fill="both", padx=0)

        crear_label(
            frame_estadisticas,
            text="Estadísticas",
            font=("Roboto", 32, "bold"),
            pady=(30, 10),
            padx=30
        )
        
        crear_label(
            frame_estadisticas,
            text=" Mensual",
            font=("Roboto", 24, "bold"),
            pady=(20, 10),
            padx=30
        )
        
        # Contadores de productos
        frame_contadores = ctk.CTkFrame(frame_estadisticas, fg_color=COLOR_BG)
        frame_contadores.pack(fill="x", pady=(5, 10), padx=40)

        self.contador_ganancias = crear_stat(frame_contadores, " Ganancias", "$0", image=crear_imagen("src/assets/icons/dollar.png", size=(40, 40)))
        self.contador_ventas = crear_stat(frame_contadores, " Ventas", "0", padx=10, image=crear_imagen("src/assets/icons/basket.png", size=(40, 40)))
        self.contador_perdidas = crear_stat(frame_contadores, " Pérdidas", "$0", image=crear_imagen("src/assets/icons/cash-off.png", size=(40, 40)))
        
        self.actualizar_contadores()
        
        crear_label(
            frame_estadisticas,
            text=f" {(datetime.now()).year}",
            font=("Roboto", 24, "bold"),
            pady=(30, 0),
            padx=30
        )

        # Contenedores
        columns_frame = ctk.CTkFrame(frame_estadisticas, fg_color=COLOR_BG)
        columns_frame.pack(fill="both", expand=True, padx=30, pady=(5, 20))

        column_left = ctk.CTkFrame(columns_frame, fg_color=COLOR_BG)
        column_left.pack(side="left", fill="both", expand=True, padx=(0, 4))

        column_right = ctk.CTkFrame(columns_frame, fg_color=COLOR_BG)
        column_right.pack(side="right", fill="both", expand=True, padx=(4, 0))

        # ------------------------------------- Gráficos -------------------------------------
        # Categorías más vendidas
        self.datos_categorias = {
            "labels": ['Categoría A', 'Categoría B', 'Categoría C', 'Categoría D'],
            "values": [450, 300, 150, 100]
        }
        self.crear_grafico(column_left, "Categorías más vendidas", self.grafico_pastel, self.datos_categorias)
        
        # Productos más vendidos
        self.datos_productos = {
            "labels": ['Producto A', 'Producto B', 'Producto C', 'Producto D'],
            "values": [450, 300, 150, 700]
        }
        self.crear_grafico(column_right, "Productos más vendidos", self.grafico_pastel, self.datos_productos)
        
        # Ganancias
        self.actualizar_ganancias()
        self.crear_grafico(column_left, "Ganancias", self.grafico_linea, self.datos_ganancias)
        
        # Pérdidas
        self.actualizar_perdidas()
        self.crear_grafico(column_right, "Pérdidas", self.grafico_barras, self.datos_perdidas)
        
        # Ventas mensuales
        self.actualizar_ventas_mensuales()
        self.crear_grafico(column_right, "Ventas mensuales", self.grafico_barras, self.datos_ventas_mensuales)
        
        # Ventas según empleado
        self.actualizar_ventas_empleado()
        self.crear_grafico(column_left, "Ventas según empleado", self.grafico_barras, self.datos_ventas_empleados)


    def crear_grafico(self, frame, title, chart_function, datos):
        frame_grafico = ctk.CTkFrame(frame, fg_color=COLOR_PRIMARIO, corner_radius=8)
        frame_grafico.pack(fill="x", expand=True, padx=10, pady=10)
        
        crear_label(frame_grafico, text=title, font=("Roboto", 18, "bold"), text_color="#ffffff", pady=10, padx=15, anchor="center")
        self.crear_canvas_grafico(frame_grafico, chart_function, datos)

    def crear_canvas_grafico(self, frame, chart_function, datos):  # Para poder eliminar graficos correctamente en el cierre del programa
        fig, canvas = chart_function(frame, datos)

        # Si la figura es válida, integrarla
        if fig:
            canvas.draw()
            canvas.get_tk_widget().pack(fill="x", expand=True, pady=(0, 8))
            self.limpiar_recursos(fig)

    def grafico_pastel(self, frame, datos):
        fig, ax = plt.subplots(figsize=(3, 3), facecolor="#FFFFFF")
        wedges, texts, autotexts = ax.pie(
            datos["values"], labels=datos["labels"], colors=self.colors, autopct='%1.1f%%', startangle=90
        )

        for autotext in autotexts:
            autotext.set_color(COLOR_BG)
            autotext.set_fontsize(9)

        # Integrar el gráfico en CustomTkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        return fig, canvas

    def grafico_barras(self, frame, datos):
        fig, ax = plt.subplots(figsize=(3, 3), facecolor="#FFFFFF")
        bars =ax.bar(datos["labels"], datos["values"], color=self.colors)
        
        # Label del valor de la barra
        ax.bar_label(bars, labels=[f"{value}" for value in datos["values"]], label_type='edge', fontsize=8, color="#000000")

        # Estética del gráfico
        ax.tick_params(axis='x', rotation=45, labelsize=8)  # Rotar etiquetas si son largas
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Ajustar para evitar cortes
        fig.tight_layout()

        # Integrar el gráfico en CustomTkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        return fig, canvas

    def grafico_linea(self, frame, datos):
        fig, ax = plt.subplots(figsize=(3, 3), facecolor="#FFFFFF")
        ax.plot(datos["labels"], datos["values"], marker='o', color=self.colors[0], linestyle='-', linewidth=2, markersize=6)

        # Estética del gráfico
        ax.set_xlabel("Meses")
        ax.set_ylabel("($)")
        ax.tick_params(axis='x', rotation=45, labelsize=7)  # Rotar etiquetas si son largas
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Ajustar para evitar cortes
        fig.tight_layout()

        # Integrar el gráfico en CustomTkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        return fig, canvas

    def limpiar_recursos(self, fig):
        # Cierra el gráfico creado después de ser renderizado
        if fig:
            plt.close(fig)
    
    def actualizar_contadores(self):
        # ---------------------------- Pérdidas ----------------------------
        perdidas = self.conexion.ejecutar_bd(
        """
        SELECT 
            SUM(productos.precio_compra * lotes.cantidad) AS perdidas
        FROM 
            lotes 
        JOIN 
            productos ON lotes.producto_id = productos.id
        WHERE 
            (MONTH(lotes.fecha_vencimiento) = MONTH(CURRENT_DATE)) AND (lotes.fecha_vencimiento <= CURRENT_DATE);
        """
        )

        if perdidas and perdidas[0][0] is not None:
            perdidas = round(perdidas[0][0])

        else:
            perdidas = 0
        
        # ---------------------------- Ganancias ----------------------------
        ganancias = self.conexion.ejecutar_bd(
        """
        SELECT 
            SUM(ganancia_venta) AS ganancias
        FROM 
            ventas
        WHERE 
            MONTH(fecha_venta) = MONTH(CURRENT_DATE) AND YEAR(fecha_venta) = YEAR(CURRENT_DATE);
        """
        )

        if ganancias and ganancias[0][0] is not None:
            ganancias = round(ganancias[0][0])
        else:
            ganancias = 0

        
        # ---------------------------- Ventas ----------------------------
        ventas_mensuales = self.conexion.ejecutar_bd(
        """
        SELECT 
            SUM(cantidad_vendida) AS total_ventas
        FROM 
            ventas
        WHERE 
            MONTH(fecha_venta) = MONTH(CURRENT_DATE) AND YEAR(fecha_venta) = YEAR(CURRENT_DATE);
        """
        )

        if ventas_mensuales and ventas_mensuales[0][0] is not None:
            ventas_mensuales = round(ventas_mensuales[0][0])
        else:
            ventas_mensuales = 0
            
        self.contador_ganancias.configure(
            text=f" Ganancias | ${ganancias}"
        )
        self.contador_ventas.configure(
            text=f" Ventas | {ventas_mensuales}"
        )
        
        self.contador_perdidas.configure(text=f" Pérdidas | ${perdidas}")
    
    def actualizar_perdidas(self):
        datos = self.conexion.ejecutar_bd(
        """
        SELECT 
            MONTH(lotes.fecha_vencimiento) AS mes_vencimiento, 
            SUM(lotes.cantidad * productos.precio_compra) AS perdidas
        FROM 
            lotes
        JOIN 
            productos ON lotes.producto_id = productos.id
        WHERE 
            (lotes.fecha_vencimiento <= CURDATE()) AND (YEAR(lotes.fecha_vencimiento) = YEAR(CURDATE()))
        GROUP BY 
            mes_vencimiento
        ORDER BY 
            mes_vencimiento;
        """
        )
        
        meses_abreviados = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        labels = []
        values = []
        
        for i in range(len(datos)):
            mes_numero = datos[i][0]  # Obtiene el numero del mes
            labels.append(meses_abreviados[mes_numero - 1])  # Convierte el numero del mes en texto
            
            values.append(datos[i][1])
        
        self.datos_perdidas = {
            "labels": labels,
            "values": values,
        }
    
    def actualizar_ventas_mensuales(self):
            datos = self.conexion.ejecutar_bd(
            """
            SELECT 
                MONTH(fecha_venta) AS mes,
                SUM(cantidad_vendida) AS total_ventas
            FROM 
                ventas
            WHERE 
                YEAR(fecha_venta) = YEAR(CURDATE())
            GROUP BY 
                mes
            ORDER BY 
                mes
            """
            )

            # Formatear los datos para el gráfico
            meses_abreviados = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
            labels = []
            values = []

            for fila in datos:
                mes_numero = fila[0]  # Mes (número)
                labels.append(meses_abreviados[mes_numero - 1])  # Convertir número a nombre abreviado
                values.append(round(fila[1]))  # Total de ventas

            # Actualizar los datos del gráfico
            self.datos_ventas_mensuales = {
                "labels": labels,
                "values": values
            }

    def actualizar_ventas_empleado(self):
        datos = self.conexion.ejecutar_bd(
        """
        SELECT 
            empleado_documento,
            SUM(cantidad_vendida) AS total_ventas
        FROM 
            ventas
        WHERE 
            YEAR(fecha_venta) = YEAR(CURDATE())
        GROUP BY 
            empleado_documento
        ORDER BY 
            total_ventas DESC
        """
        )

        labels = []
        values = []

        for fila in datos:
            labels.append(f"{fila[0]}")  # Documento del empleado como label
            values.append(round(fila[1]))  # Total de ventas

        # Actualizar los datos del gráfico
        self.datos_ventas_empleados = {
            "labels": labels,
            "values": values
        }

    def actualizar_ganancias(self):
        datos = self.conexion.ejecutar_bd(
        """
        SELECT 
            MONTH(fecha_venta) AS mes,
            SUM(ganancia_venta) AS total_ganancias
        FROM 
            ventas
        WHERE 
            YEAR(fecha_venta) = YEAR(CURDATE())
        GROUP BY 
            mes
        ORDER BY 
            mes
        """
        )

        # Formatear los datos para el gráfico
        meses_abreviados = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        labels = []
        values = []

        for fila in datos:
            mes_numero = fila[0]  # Mes (número)
            labels.append(meses_abreviados[mes_numero - 1])  # Convertir número a nombre abreviado
            values.append(fila[1])  # Total de ganancias

        # Actualizar los datos del gráfico
        self.datos_ganancias = {
            "labels": labels,
            "values": values
        }
