from config.config import *


class Terminos_CondicionesFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.terminosVentana = ctk.CTkToplevel(master)
        self.terminosVentana.title("EcoPrint | Términos y condiciones")
        centrar_ventana(self.terminosVentana, 600, 400)
        
        self.terminosVentana.resizable(False, False) # La ventana no puede cambiar su tamaño
        self.terminosVentana.attributes("-topmost", "true") # Aparece adelante de la ventana actual

        self.frame = ctk.CTkScrollableFrame(self.terminosVentana)
        self.frame.pack(pady=0, padx=0, fill="both", expand=True)

        self.terminosTxt = "\nBases y Condiciones del Software de EcoPrint.\n\nParticipación:\nEl software está disponible para la participación de interesados en compartir proyectos para ayudar al medio-ambiente e informar sobre eventos locales relacionados. La participación es voluntaria y abierta a personas mayores de 18 años.\n\nContenido:\nSe invita a los usuarios a subir proyectos relacionadas al tema, incluyendo eventos de interés comunitario.\n\nVeracidad de la Información:\nLos participantes deben proporcionar información veraz y corroborada en la medida de lo posible. La difusión de información falsa puede resultar en la exclusión del usuario del programa.\n\nRespeto y Ética:\nSe prohíbe la publicación de contenido difamatorio, ofensivo o que viole los derechos de privacidad de terceros. El respeto y la ética son fundamentales para mantener un ambiente colaborativo y seguro.\n\nConfidencialidad:\nLos usuarios deben ser conscientes de no compartir información que viole la privacidad de otras personas o comprometa la seguridad de la comunidad.\n\nUso Responsable:\nEl programa se proporciona con el propósito de mejorar el medio-ambiente y la conciencia comunitaria. Su uso debe ser responsable y respetuoso. Cualquier mal uso del software puede resultar en la desactivación de la cuenta del usuario.\n\nPropiedad Intelectual:\nAl subir contenido, los usuarios otorgan una licencia no exclusiva para su uso en la plataforma.\n\nColaboración Comunitaria:\nSe fomenta la colaboración y el intercambio constructivo de información entre los usuarios. La plataforma se reserva el derecho de moderar y eliminar contenido que viole las normas de colaboración.\n\nDuración:\nEl uso del software no tiene limitaciones de tiempo y estará sujeto a revisiones periódicas para garantizar su eficacia y cumplimiento de normas.\n"

        self.terminosTexto = ctk.CTkLabel(
            self.frame, wraplength=500, justify="left", text=self.terminosTxt
        )
        self.terminosTexto.pack(pady=0, padx=0, fill="x")

        self.terminosLabel = ctk.CTkLabel(
            self.terminosVentana,
            justify="left",
            wraplength=550,
            text="Al utilizar este software, los usuarios aceptan adherirse a estas bases y condiciones. La plataforma se reserva el derecho de modificar estas condiciones con notificación previa a los usuarios.",
        )
        self.terminosLabel.pack(pady=20, padx=0, fill="x")
