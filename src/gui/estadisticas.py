from config.config import *
from gui.componentes import *
from gui.agregar_producto import *


class Estadisticas:
    def __init__(self, contenedor):
        self.contenedor = contenedor

        frame_estadisticas = ctk.CTkFrame(master=self.contenedor, fg_color=COLOR_BG)
        frame_estadisticas.pack(expand=True, fill="x", padx=100)

        crear_label(
            frame_estadisticas,
            text="Estadísticas",
            font=("Roboto", 32, "bold"),
            pady=(30, 10),
            padx=0
        )

        crear_label(frame_estadisticas, text="Categorías más vendidas", font=("Roboto", 18, "bold"))
        crear_label(frame_estadisticas, text="Producto más vendido", font=("Roboto", 18, "bold"))
        crear_label(frame_estadisticas, text="Ganancia total", font=("Roboto", 18, "bold"))
        crear_label(frame_estadisticas, text="Pérdidas", font=("Roboto", 18, "bold"))
