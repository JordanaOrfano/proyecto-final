import customtkinter as ctk
from config.config import *
from gui.componentes import *
from gui.crear_producto import *


class Estadisticas:
    def __init__(self, contenedor):
        self.contenedor = contenedor

        frame_estadisticas = ctk.CTkFrame(master=self.contenedor, fg_color=COLOR_BG)
        frame_estadisticas.pack(expand=True, fill="both", padx=150)

        crear_label(
            frame_estadisticas,
            text="Estadísticas",
            font=("Roboto", 32, "bold"),
            pady=(30, 10),
            padx=0
        )

        # Frame para las estadísticas
        frame_stats = ctk.CTkFrame(frame_estadisticas, fg_color=COLOR_BG)
        frame_stats.pack(fill="x", pady=20)

        crear_stat(frame_stats, "Publicaciones", 5)
        crear_stat(frame_stats, "Votos", 20, 30)
        crear_stat(frame_stats, "Participaciones", 10)
