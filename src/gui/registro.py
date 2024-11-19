from gui.terminos_condiciones import Terminos_CondicionesFrame
from core.usuarios import *
from config.config import *
from gui.componentes import *
from core.verificar_correo_dni import *


class RegistroFrame(ctk.CTkFrame):
    def __init__(self, master, frame_cambiar):
        super().__init__(master)
        self.frame_cambiar = frame_cambiar

        frameFondo = ctk.CTkFrame(master=self, fg_color=COLOR_BG)
        frameFondo.pack(expand=True, fill="both")

        # Frame izquierdo con imagen
        imgFrame = ctk.CTkFrame(master=frameFondo, width=1000, fg_color="#e3f0df")
        imgFrame.pack(side="left", fill="y")

        # Cargar imagen y ajustarla con CTkImage
        self.image_original = Image.open("src/assets/bg.png")
        self.image_ctk = ctk.CTkImage(self.image_original, size=(imgFrame.winfo_width(), imgFrame.winfo_height()))

        # Label con la imagen redimensionable
        self.image_label = ctk.CTkLabel(imgFrame, text="", image=self.image_ctk)
        self.image_label.pack(expand=True, fill="both")

        # Redimensionar la imagen al cambiar el tamaño de imgFrame
        imgFrame.bind("<Configure>", self.resize_image)

        # Botón en el frame izquierdo
        self.login_button = crear_boton(imgFrame, text="", fill="x", width=470)

        # Frame derecho con formulario de registro
        frameRegistro = ctk.CTkFrame(master=frameFondo, fg_color=COLOR_BG)
        frameRegistro.pack(expand=True, fill="x", padx=110)

        # Configuración de grid para organizar los elementos
        frameRegistro.grid_rowconfigure(0, weight=1)
        frameRegistro.grid_rowconfigure(1, weight=1)
        frameRegistro.grid_columnconfigure(0, weight=1)
        frameRegistro.grid_columnconfigure(1, weight=1)

        # Título
        label_bienvenida = crear_label(frameRegistro, metodo="grid", text="Registrarse", font=("Roboto", 32, "bold"), anchor="center")
        label_bienvenida.grid(row=0, column=0, columnspan=2, pady=(0, 30))

        # Documento
        label_dni = crear_label(frameRegistro,metodo="grid", text=" Documento (D.N.I)", font=("Roboto", 18, "bold"), pady=(20, 0), padx=(90, 170),
                    image=crear_imagen("src/assets/icons/id.png", size=(22, 22)))
        label_dni.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        self.usuario_dni = crear_entry(frameRegistro,metodo="grid", placeholder_text="Ingresa tu documento sin puntos (.)", fill="x")
        self.usuario_dni.grid(row=2, column=0, columnspan=2, sticky="ew")
        
        # Correo
        label_correo = crear_label(frameRegistro, metodo="grid", text=" Correo electrónico", font=("Roboto", 18, "bold"), pady=(20, 0), padx=(90, 170),
                    image=crear_imagen("src/assets/icons/login-mail.png", size=(22, 22)))
        label_correo.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        self.usuario_correo = crear_entry(frameRegistro,metodo="grid", placeholder_text="Correo electrónico", fill="x")
        self.usuario_correo.grid(row=4, column=0, columnspan=2, sticky="ew")

        # Nombre
        label_nombre = crear_label(frameRegistro, metodo="grid", text=" Nombre", font=("Roboto", 18, "bold"), pady=(20, 0), padx=(90, 170),
                    image=crear_imagen("src/assets/icons/user.png", size=(22, 22)))
        label_nombre.grid(row=5, column=0, sticky="ew", pady=(10, 0))
        
        self.usuario_nombre = crear_entry(frameRegistro, metodo="grid", placeholder_text="Nombre", fill="x")
        self.usuario_nombre.grid(row=6, column=0, sticky="ew", padx=(0, 5))

        # Apellido
        label_apellido = crear_label(frameRegistro, metodo="grid", text=" Apellido", font=("Roboto", 18, "bold"), pady=(20, 0), padx=(90, 170),
                    image=crear_imagen("src/assets/icons/user.png", size=(22, 22)))
        label_apellido.grid(row=5, column=1, sticky="ew", pady=(10, 0))
        
        self.usuario_apellido = crear_entry(frameRegistro, metodo="grid", placeholder_text="Apellido", fill="x")
        self.usuario_apellido.grid(row=6, column=1, sticky="ew", padx=(5, 0))

        # Contraseña
        label_contrasena = crear_label(frameRegistro, metodo="grid", text=" Contraseña", font=("Roboto", 18, "bold"), pady=(20, 0), padx=(90, 170),
                    image=crear_imagen("src/assets/icons/login-password.png", size=(22, 22)))
        label_contrasena.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        self.__usuario_contrasena = crear_entry(frameRegistro, metodo="grid", show="*", placeholder_text="**********", fill="x")
        self.__usuario_contrasena.grid(row=8, column=0, columnspan=2, sticky="ew")

        # Botones de registrarse y volver
        self.registrar_button = crear_boton(frameRegistro, metodo="grid", text="Registrarse", command=lambda: self.verificar_campos(frameFondo), pady=10, fill="x")
        self.registrar_button.grid(row=9, column=0, pady=20, sticky="ew", padx=(0, 5))

        self.volver_button = crear_boton(frameRegistro, metodo="grid", text="Volver", command=self.volver_login, pady=10, fill="x")
        self.volver_button.grid(row=9, column=1, pady=20, sticky="ew", padx=(5, 0))

        # # Checkbox de términos y condiciones
        # self.terminosCheckbox = ctk.CTkCheckBox(frameRegistro, 
        #                                         text="",
        #                                         onvalue="on", 
        #                                         offvalue="off", 
        #                                         border_color=COLOR_PRIMARIO, 
        #                                         checkmark_color=COLOR_BG,
        #                                         fg_color=COLOR_PRIMARIO)
        # self.terminosCheckbox.grid(row=9, column=0, sticky="w")

        # self.terminos_button = ctk.CTkButton(
        #     frameRegistro,
        #     fg_color="transparent",
        #     text="Acepto los términos y condiciones",
        #     text_color="black",
        #     anchor="w",
        #     command=self.ver_terminos,
        # )
        # self.terminos_button.grid(row=9, column=1, sticky="w")
    
    def resize_image(self, event):
        # Ajusta la imagen al tamaño actual de imgFrame
        new_width = event.width
        new_height = event.height
        self.image_ctk.configure(size=(new_width, new_height))

    def ver_terminos(self):
        Terminos_CondicionesFrame(self)

    def volver_login(self):
        self.frame_cambiar("login")

    def verificar_campos(self, frame):
        # Validar campos vacíos
        dni, correo = chequear(self.usuario_dni.get().strip(), self.usuario_correo.get().strip())
        
        if not self.usuario_dni.get().strip() or not dni:
            notificacion = CTkNotification(master=frame, state="info", message="Documento inválido o ya registrado", side="right_bottom")
            frame.after(3000, notificacion.destroy)
            return
        
        if not self.usuario_correo.get().strip() or not correo:
            notificacion = CTkNotification(master=frame, state="info", message="Correo electronico inválido o en uso", side="right_bottom")
            frame.after(3000, notificacion.destroy)
            return

        if not self.usuario_nombre.get().strip():
            notificacion = CTkNotification(master=frame, state="info", message="Nombre inválido", side="right_bottom")
            frame.after(3000, notificacion.destroy)
            return
        
        if not self.usuario_apellido.get().strip():
            notificacion = CTkNotification(master=frame, state="info", message="Apellido inválido", side="right_bottom")
            frame.after(3000, notificacion.destroy)
            return
        
        if (
            not self.__usuario_contrasena.get()
            or len(self.__usuario_contrasena.get()) < 8
        ):
            notificacion = CTkNotification(master=frame, state="info", message="Contraseña inválida. Mínimo de 8 caracteres", side="right_bottom")
            frame.after(3000, notificacion.destroy)
            return

        # Si los campos son correctos, registrar usuario
        usuario = Usuario(
            self.usuario_correo.get().strip(), self.__usuario_contrasena.get()
        )

        usuario.registrar_usuario(
            dni,
            self.usuario_nombre.get().strip(),
            self.usuario_apellido.get().strip(),
        )
