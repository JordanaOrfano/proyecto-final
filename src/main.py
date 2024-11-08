from gui.login import LoginFrame
from gui.inicio import InicioFrame
from gui.registro import RegistroFrame
from config.config import *


# Utilizamos frames para que todo se muestre en una ventana
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        centrar_ventana(self, 1300, 700)
        self.title("EcoPrint")
        self.minsize(width=1300, height=700)
        self.frame_actual = None
        self.frame_cambiar("login")  # Mostrar el frame de inicio de sesión al iniciar
        self.frame_cambiar("inicio")  # Mostrar el frame de inicio de sesión al iniciar

    def frame_cambiar(self, frame_nombre):
        # Destruir el frame actual para poner el nuevo
        if self.frame_actual is not None:
            self.frame_actual.destroy()

        # Cambiar al nuevo frame seleccionado
        if frame_nombre == "login":
            self.frame_actual = LoginFrame(self, self.frame_cambiar)

        if frame_nombre == "registrar":
            self.frame_actual = RegistroFrame(self, self.frame_cambiar)

        if frame_nombre == "inicio":
            self.frame_actual = InicioFrame(self)

        self.frame_actual.pack(fill="both", expand=True)


def run_app():
    app = App()
    app.mainloop()  # Ejecutar la ventana principal


if (
    __name__ == "__main__"
):  # Nos aseguramos que el programa se ejecuta desde el archivo main
    run_app()
