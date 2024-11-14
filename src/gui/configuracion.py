from config.config import *
from gui.componentes import *


class Configuracion:
    def __init__(self, contenedor):
        self.contenedor = contenedor

        frame_config = ctk.CTkFrame(master=self.contenedor, fg_color=COLOR_BG)
        frame_config.pack(expand=True, fill="x", padx=100)

        crear_label(
            frame_config,
            text="Configuración",
            font=("Roboto", 32, "bold"),
            pady=(30, 10),
            padx=0
        )
        
        crear_label(frame_config, text="Tema", font=("Roboto", 18, "bold"))
        crear_label(frame_config, text="Cambiar nombre", font=("Roboto", 18, "bold"))
        crear_label(frame_config, text="Cambiar contraseña", font=("Roboto", 18, "bold"))