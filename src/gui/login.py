from core.usuarios import *
from config.config import *
from gui.componentes import *


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, frame_cambiar):
        super().__init__(master)

        # Guardamos la función para cambiar de frame
        self.frame_cambiar = frame_cambiar
        
        frameFondo = ctk.CTkFrame(master=self, fg_color=COLOR_BG)
        frameFondo.pack(expand=True, fill="both")

        # Frame izquierdo con imagen
        imgFrame = ctk.CTkFrame(
            master=frameFondo, width=1000, fg_color=COLOR_BG)
        imgFrame.pack(side="left", fill="y")

        # Cargar imagen y ajustarla con CTkImage
        self.image_original = Image.open("src/assets/bg.png")
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
        frameLogin = ctk.CTkFrame(master=frameFondo, fg_color=COLOR_BG)
        frameLogin.pack(expand=True, fill="x", padx=110)

        crear_label(
            frameLogin, text="¡Bienvenido a StockUp!", font=("Roboto", 32, "bold"), pady=(0, 30), anchor="center"
        )

        crear_label(frameLogin, text=" Correo electrónico", font=("Roboto", 18, "bold"), pady=(10, 0), padx=0,
                    image=crear_imagen(
                        "src/assets/icons/login-mail.png", size=(22, 22))
                    )

        self.usuario_correo = crear_entry(
            frameLogin, placeholder_text="Correo electrónico", pady=0, fill="x")

        crear_label(frameLogin, text=" Contraseña", font=("Roboto", 18, "bold"), pady=(10, 0), padx=0,
                    image=crear_imagen(
                        "src/assets/icons/login-password.png", size=(22, 22))
                    )

        self.__usuario_contrasena = crear_entry(
            frameLogin, placeholder_text="**********", show="*", pady=0, fill="x")

        self.login_button = crear_boton(
            frameLogin, text="Iniciar Sesión", command=lambda: self.login(frameFondo), fill="x", padx=0)
        
        crear_label(frameLogin, text="¿Tenés alguna duda o consulta? Contactanos por mail a horizonweb@gmail.com", anchor="center", font=("Roboto", 16, "bold"), pady=(30, 0))

    def resize_image(self, event):
        # Ajusta la imagen al tamaño actual de imgFrame
        nuevo_width = event.width
        nuevo_height = event.height
        self.image_ctk.configure(size=(nuevo_width, nuevo_height))

    def mostrar_notificacion(self, frame, mensaje):
        notificacion = CTkNotification(master=frame, state="info", message=mensaje, side="right_bottom")
        frame.after(3000, notificacion.destroy)

    def login(self, frame):
        if not self.usuario_correo.get().strip() or len(self.usuario_correo.get().strip()) < 6:
            self.mostrar_notificacion(frame, "Debes ingresar un correo válido.")
            return
        
        if not self.__usuario_contrasena.get() or len(self.__usuario_contrasena.get()) < 8:
            self.mostrar_notificacion(frame, "Debes ingresar una contraseña válida")
            return

        logear_usuario = Usuario(
            self.usuario_correo.get(), self.__usuario_contrasena.get()
        )

        # Verificar usuario
        if not logear_usuario.verificar_usuario(
            self.usuario_correo.get(), self.__usuario_contrasena.get()
        ):
            self.mostrar_notificacion(frame, "Usuario o contraseña incorrecto")
            return

        self.mostrar_notificacion(frame, "Sesión iniciada con éxito, redirigiendo...")
        frame.after(2000, lambda: self.frame_cambiar("inicio"))
