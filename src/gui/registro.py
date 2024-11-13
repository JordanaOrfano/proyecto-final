from gui.terminos_condiciones import Terminos_CondicionesFrame
from core.usuarios import *
from config.config import *
from gui.componentes import *
from core.verificar_correo import *


class RegistroFrame(ctk.CTkFrame):
    def __init__(self, master, frame_cambiar):
        super().__init__(master)
        self.frame_cambiar = frame_cambiar

        frameFondo = ctk.CTkFrame(master=self, fg_color=COLOR_BG)
        frameFondo.pack(expand=True, fill="both")

        
        # Frame izquierdo con imagen
        imgFrame = ctk.CTkFrame(
            master=frameFondo, width=1000, fg_color="#e3f0df")
        imgFrame.pack(side="left", fill="y")

        # Cargar imagen y ajustarla con CTkImage
        self.image_original = Image.open("src/assets/pic.jpeg")
        self.image_ctk = ctk.CTkImage(self.image_original, size=(
            imgFrame.winfo_width(), imgFrame.winfo_height()))

        # Label con la imagen redimensionable
        self.image_label = ctk.CTkLabel(
            imgFrame, text="", image=self.image_ctk)
        self.image_label.pack(expand=True, fill="both")

        # Redimensionar la imagen al cambiar el tamaño de imgFrame
        imgFrame.bind("<Configure>", self.resize_image)

        # Botón en el frame izquierdo
        self.login_button = crear_boton(
            imgFrame, text="", fill="x", width=470)

        # crear_boton(
        #     imgFrame, text="", fill="x", width=470)

        # Frame derecho con formulario de registro
        frameRegistro = ctk.CTkFrame(master=frameFondo, fg_color=COLOR_BG)
        frameRegistro.pack(expand=True, fill="x")

        self.label_bienvenida = crear_label(
            frameRegistro, text="Registrarse", font=("Roboto", 32, "bold"), pady=0, padx=(110, 170), anchor="center"
        )

        crear_label(frameRegistro, text="Documento", font=("Roboto", 18, "bold"), pady=(20, 0), padx=(90, 170),
                    image=crear_imagen(
                        "src/assets/icons/login-mail.png", size=(22, 22))
                    )

        self.usuario_dni = crear_entry(
            frameRegistro, placeholder_text="Ingresa tu documento sin puntos (.)", padx=(110, 170), pady=0, fill="x")
        
        crear_label(frameRegistro, text=" Correo electrónico", font=("Roboto", 18, "bold"), pady=(20, 0), padx=(90, 170),
                    image=crear_imagen(
                        "src/assets/icons/login-mail.png", size=(22, 22))
                    )

        self.usuario_correo = crear_entry(
            frameRegistro, placeholder_text="Correo electrónico", padx=(110, 170), pady=0, fill="x")

        crear_label(frameRegistro, text=" Nombre", font=("Roboto", 18, "bold"), pady=(20, 0), padx=(90, 170),
                    image=crear_imagen(
                        "src/assets/icons/user.png", size=(22, 22))
                    )
        self.usuario_nombre = crear_entry(
            frameRegistro, placeholder_text="Nombre", padx=(110, 170), pady=0, fill="x")

        crear_label(frameRegistro, text=" Apellido", font=("Roboto", 18, "bold"), pady=(20, 0), padx=(90, 170),
                    image=crear_imagen(
                        "src/assets/icons/user.png", size=(22, 22))
                    )

        self.usuario_apellido = crear_entry(
            frameRegistro, placeholder_text="Apellido", padx=(110, 170), pady=0, fill="x")

        crear_label(frameRegistro, text=" Contraseña", font=("Roboto", 18, "bold"), pady=(20, 0), padx=(90, 170),
                    image=crear_imagen(
                        "src/assets/icons/login-password.png", size=(22, 22))
                    )

        self.__usuario_contrasena = crear_entry(
            frameRegistro, show="*", placeholder_text="**********", padx=(110, 170), pady=0, fill="x"
        )

        self.registrar_button = crear_boton(
            frameRegistro, text="Registrarse", command=self.verificar_campos, padx=(110, 170), fill="x"
        )

        self.registrar_button = crear_boton(
            frameRegistro, text="Volver", command=self.volver_login, padx=(110, 170), pady=0, fill="x"
        )

        self.terminosCheckbox = ctk.CTkCheckBox(
            frameRegistro, width=0, text="", onvalue="on", offvalue="off"
        )
        self.terminosCheckbox.pack(pady=0, padx=(110, 0), side="left")

        self.terminos_button = ctk.CTkButton(
            frameRegistro,
            fg_color="transparent",
            text="Acepto los términos y condiciones",
            text_color="black",
            anchor="w",
            command=self.ver_terminos,
        )
        self.terminos_button.pack(pady=0, padx=0, side="left")
    
    def resize_image(self, event):
        # Ajusta la imagen al tamaño actual de imgFrame
        new_width = event.width
        new_height = event.height
        self.image_ctk.configure(size=(new_width, new_height))

    def ver_terminos(self):
        Terminos_CondicionesFrame(self)

    def volver_login(self):
        self.frame_cambiar("login")

    def verificar_campos(self):
        # Validar campos vacíos
        if not self.usuario_dni.get().strip():
            # FALTA label "Dni erroneo o no ingresado"
            return
        
        if not self.usuario_correo.get().strip() or not chequear(self.usuario_correo.get().strip()):
            # FALTA label "Correo electronico invalido o en uso"
            return
        if (
            not self.__usuario_contrasena.get()
            or len(self.__usuario_contrasena.get()) < 8
        ):
            # FALTA label debes ingresar una contrasena válida, recuerda que debe tener al menos 8 caracteres
            return

        if not self.usuario_nombre.get().strip():
            # FALTA label debes ingresar un nombre
            return
        if not self.usuario_apellido.get().strip():
            # FALTA label debes ingresar un apellido
            return
        if not self.terminosCheckbox.get() == "on":
            # Falta label debes aceptar los terminos y condiciones
            return

        # Si los campos son correctos, registrar usuario
        usuario = Usuario(
            self.usuario_correo.get(), self.__usuario_contrasena.get()
        )
        usuario.registrar_usuario(
            self.usuario_dni.get(),
            self.usuario_nombre.get(),
            self.usuario_apellido.get(),
        )
