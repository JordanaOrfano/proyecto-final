import customtkinter as ctk
from config.config import *
from gui.componentes import *
from gui.crear_producto import *
from core.usuarios import *
from gui.perfil import *


class InicioFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.frame_contenido = None
        self.botones_sideframe = {}  # Diccionario para almacenar botones del sideFrame
        self.side_frame()
        
        if Usuario.usuario_actual[2].strip('"') == "usuario":
            self.inicio()

        if Usuario.usuario_actual[2].strip('"') == "administrador":
            self.inicio_administrador()

    def side_frame(self):
        sideFrame = ctk.CTkFrame(master=self, width=240, fg_color=COLOR_PRIMARIO)
        sideFrame.pack(side="left", fill="y")

        # Centra el contenido del sideFrame
        centrar_frame = ctk.CTkFrame(sideFrame, fg_color=COLOR_PRIMARIO)
        centrar_frame.pack(expand=True)

        ctk.CTkLabel(
            centrar_frame,
            text="EcoPrint",
            font=("Roboto", 32, "bold"),
            text_color=COLOR_BG,
            width=210,
        ).pack(pady=0)

        ctk.CTkLabel(
            centrar_frame,
            text="",
            image=crear_imagen("src/assets/eco.png", size=(220, 220)),
        ).pack(pady=50)

        # Creación de botones en el sideFrame con el estado de selección inicial
        self.botones_sideframe["inicio"] = crear_boton_sideframe(
            centrar_frame,
            text="Inicio",
            command=self.inicio,
            pady=0,
            image=crear_imagen("src/assets/icons/home.png"),
        )

        self.botones_sideframe["crear_producto"] = crear_boton_sideframe(
            centrar_frame,
            text="Añadir producto",
            command=self.crear_producto,
            image=crear_imagen("src/assets/icons/pencil-plus.png"),
        )

        self.botones_sideframe["perfil"] = crear_boton_sideframe(
            centrar_frame,
            text="Mi perfil",
            command=self.perfil,
            image=crear_imagen("src/assets/icons/user-circle-white.png"),
        )

        self.botones_sideframe["configuracion"] = crear_boton_sideframe(
            centrar_frame, text="Configuración", command=self.configuracion,
            image=crear_imagen("src/assets/icons/settings.png")
        )

        self.botones_sideframe["cerrar_sesion"] = crear_boton_sideframe(
            centrar_frame,
            text="Cerrar sesión",
            command=self.cerrar_sesion,
            image=crear_imagen("src/assets/icons/logout.png"),
        )

    def actualizar_estado_botones(self, boton_activo):
        # Actualiza el color del botón activo y resetea los demás
        for nombre, boton in self.botones_sideframe.items():
            if nombre == boton_activo:
                # Fondo verde oscuro para el botón activo
                boton.configure(fg_color=COLOR_PRIMARIO_HOVER)
            else:
                # Fondo predeterminado para los demás botones
                boton.configure(fg_color=COLOR_PRIMARIO)

    def cambiar_contenido(self, nuevo_frame, boton_activo):
        # Cambia el contenido principal y actualiza el estado del botón activo
        if self.frame_contenido:
            self.frame_contenido.pack_forget()  # Oculta el frame anterior

        self.actualizar_estado_botones(boton_activo)
        self.frame_contenido = nuevo_frame
        self.frame_contenido.pack(side="left", fill="both", expand=True)

    # ------------------------------------- FRAMES DE CONTENIDO -------------------------------------
    def inicio(self):
        frame_inicio = ctk.CTkScrollableFrame(master=self, fg_color=COLOR_BG)
        crear_label(
            frame_inicio,
            text="Inicio",
            font=("Roboto", 32, "bold"),
            pady=(30, 10),
        )
        publicaciones = Publicaciones()
        publicaciones.mostrar_publicaciones(contenedor=frame_inicio)

        self.cambiar_contenido(frame_inicio, "inicio")

    def inicio_administrador(self):
        frame_inicio = ctk.CTkScrollableFrame(master=self, fg_color=COLOR_BG)
        crear_label(
            frame_inicio,
            text="Inicio ADMINISTRADOR",
            font=("Roboto", 32, "bold"),
            pady=(30, 10),
        )
        publicaciones = Publicaciones()
        publicaciones.mostrar_publicaciones(contenedor=frame_inicio)

        self.cambiar_contenido(frame_inicio, "inicio")

    def crear_publicacion(self):
        frame_publicar = ctk.CTkFrame(master=self, fg_color=COLOR_BG)

        FormularioPublicacion(contenedor=frame_publicar)

        # Cambiar el contenido principal para mostrar el formulario
        self.cambiar_contenido(frame_publicar, "crear_publicacion")

    def perfil(self):
        frame_perfil = ctk.CTkFrame(master=self, fg_color=COLOR_BG)
        
        
        Perfil(contenedor=frame_perfil)
        self.cambiar_contenido(frame_perfil, "perfil")

    def configuracion(self):
        frame_configuracion = ctk.CTkFrame(
            master=self, fg_color=COLOR_BG)
        crear_label(
            frame_configuracion,
            text="Configuración",
            font=("Roboto", 32, "bold"),
            pady=(30, 10),
        )
        
        crear_label(frame_configuracion, text="Tema", font=("Roboto", 18, "bold"))
        crear_label(frame_configuracion, text="Cambiar nombre", font=("Roboto", 18, "bold"))
        crear_label(frame_configuracion, text="Cambiar contraseña", font=("Roboto", 18, "bold"))
        
        self.cambiar_contenido(frame_configuracion, "configuracion")

    def cerrar_sesion(self):
        self.quit()
