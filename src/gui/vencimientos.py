import customtkinter as ctk
from config.config import *
from gui.componentes import *


class Vencimientos:
    def __init__(self, contenedor):
        self.contenedor = contenedor

        frame_vencimientos = ctk.CTkFrame(master=self.contenedor, fg_color=COLOR_BG)
        frame_vencimientos.pack(expand=True, fill="both", padx=150)

        crear_label(
            frame_vencimientos,
            text="Vencimientos",
            font=("Roboto", 32, "bold"),
            pady=(30, 10),
            padx=0
        )