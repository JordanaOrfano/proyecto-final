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
        self.datos_ganancias = {
            "labels": ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio'],
            "values": [7000, 8000, 6000, 9000, 6000, 7000, 7000]
        }
        self.crear_grafico(column_left, "Ganancias", self.grafico_linea, self.datos_ganancias)
        
        # Pérdidas
        self.datos_perdidas = {
            "labels": ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
            "values": [700, 800, 600, 900, 200, 1000, 270, 500, 400, 200, 600, 1000]
        }
        self.crear_grafico(column_right, "Pérdidas", self.grafico_barras, self.datos_perdidas)
        
        # Ventas mensuales
        self.datos_ventas = {
            "labels": ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
            "values": [7000, 8000, 6000, 9000, 6000, 7000, 7000, 500, 400, 2000, 6000, 1000]
        }
        self.crear_grafico(column_right, "Ventas mensuales", self.grafico_barras, self.datos_ventas)
        
        # Ventas según empleado
        self.datos_ventas = {
            "labels": ['Fernando', 'Maria', 'Pepe', 'Jordana', 'José'],
            "values": [800, 600, 400, 900, 280]
        }
        self.crear_grafico(column_left, "Ventas según empleado", self.grafico_barras, self.datos_ventas)


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
        ax.bar(datos["labels"], datos["values"], color=self.colors)

        # Estética del gráfico
        ax.set_xlabel("Meses")
        ax.set_ylabel("Dinero ($)")
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
        ax.set_ylabel("Ganancias ($)")
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
        perdidas = self.conexion.ejecutar_bd(
        """
        SELECT SUM(productos.precio_compra * lotes.cantidad) AS perdidas
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

        # self.contador_ganancias.configure(
        #     text=f" Ganancias | {}"
        # )
        # self.contador_ventas.configure(
        #     text=f" Ventas | {}"
        # )
        self.contador_perdidas.configure(text=f" Pérdidas | ${perdidas}")