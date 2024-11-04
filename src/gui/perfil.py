import customtkinter as ctk
from config.config import *
from gui.componentes import *
from gui.crear_producto import *


class Perfil:
    def __init__(self, contenedor):
        self.contenedor = contenedor

        # Crear el fondo principal del perfil
        self.frame_bg = ctk.CTkFrame(master=self.contenedor, fg_color=COLOR_BG)
        self.frame_bg.pack(expand=True, fill="both")

        # Frame para el perfil y centrado
        frame_perfil = ctk.CTkFrame(self.frame_bg, fg_color=COLOR_BG)
        frame_perfil.pack(expand=True, fill="x", padx=170)

        # Nombre y correo del usuario
        crear_label(
            frame_perfil,
            text="Jordana Orfano",
            # text=f"{Usuario.usuario_actual[0]} {Usuario.usuario_actual[1]}",
            font=("Roboto", 32, "bold"),
            pady=(30, 0),
            padx=0
        )

        crear_label(
            frame_perfil,
            text="jordanaorfano@gmail.com",
            # text=f"{}",
            font=("Roboto", 16, "bold"),
            pady=0,
            padx=0
        )

        # Frame para las estadísticas (mantener el mismo ancho)
        frame_stats = ctk.CTkFrame(frame_perfil, fg_color=COLOR_BG)
        frame_stats.pack(fill="x", pady=20)

        # Crear las estadísticas con ajuste automático de ancho
        crear_stat(frame_stats, "Publicaciones", 5)
        crear_stat(frame_stats, "Votos", 20, 30)
        crear_stat(frame_stats, "Participaciones", 10)
