from core.usuarios import *
from config.config import *
from gui.componentes import *


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, frame_cambiar):
        super().__init__(master)

        # Guardamos la función para cambiar de frame
        self.frame_cambiar = frame_cambiar
        
        frameFondo = ctk.CTkFrame(master=self, fg_color="#e3f0df")
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

        # Frame derecho con formulario de login
        frameLogin = ctk.CTkFrame(master=frameFondo, fg_color="#e3f0df")
        frameLogin.pack(expand=True, fill="x")

        crear_label(
            frameLogin, text="¡Bienvenido a EcoPrint!", font=("Roboto", 32, "bold"), pady=(0, 50), padx=(110, 170), anchor="center"
        )

        crear_label(frameLogin, text=" Correo electrónico", font=("Roboto", 18, "bold"), pady=(20, 0), padx=(90, 170),
                    image=crear_imagen(
                        "src/assets/icons/login-mail.png", size=(22, 22))
                    )

        self.usuario_correo = crear_entry(self, placeholder_text="Correo electrónico")
        self.usuario_correo = crear_entry(
            frameLogin, placeholder_text="Correo electrónico", padx=(110, 170), pady=0, fill="x")

        crear_label(frameLogin, text=" Contraseña", font=("Roboto", 18, "bold"), pady=(20, 0), padx=(90, 170),
                    image=crear_imagen(
                        "src/assets/icons/login-password.png", size=(22, 22))
                    )

        self.__usuario_contrasena = crear_entry(
            frameLogin, placeholder_text="**********", show="*", padx=(110, 170), pady=0, fill="x")

        self.login_button = crear_boton(self, text="Iniciar Sesión", command=self.login)

        self.label_registrar = crear_label(
            self,
            text="¿No tienes una cuenta? ¡Registrate!",
            font=("Roboto", 18, "bold"),
            pady=(90, 0),
        )
        self.login_button = crear_boton(
            frameLogin, text="Iniciar Sesión", command=self.login, padx=(110, 170), fill="x")

        self.label_registrar = crear_label(
            frameLogin, text="¿No tienes una cuenta?",
            font=("Roboto", 18, "bold"), pady=(50, 0), padx=(110, 170), anchor="center"
        )

        self.registrar_button = crear_boton(
            frameLogin, text="¡Registrate!", command=self.registrarse, padx=(110, 170), pady=(10, 0), fill="x")

    def resize_image(self, event):
        # Ajusta la imagen al tamaño actual de imgFrame
        new_width = event.width
        new_height = event.height
        self.image_ctk.configure(size=(new_width, new_height))

    def login(self):
        if not self.usuario_correo.get():
            # FALTA label "Debes ingresar un correo"
            return
        if not self.__usuario_contrasena.get():
            # FALTA label "Debes ingresar una contrasena"
            return

        logear_usuario = Usuario(
            self.usuario_correo.get(), self.__usuario_contrasena.get()
        )

        # Verificar usuario
        if not logear_usuario.verificar_usuario(
            self.usuario_correo.get(), self.__usuario_contrasena.get()
        ):
            # FALTA label "Usuario o contrasena incorrecto"
            return
        self.frame_cambiar("inicio")

    def registrarse(self):
        self.frame_cambiar("registrar")
