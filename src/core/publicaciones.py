# Lógica publicaciones
from database.conexion import *
from config.config import *
from PIL import Image
from gui.componentes import *
from datetime import datetime

import customtkinter as ctk


class Publicaciones:
    def subir_publicacion_a_bd(
        self, titulo, descripcion, ubicacion, fecha_creacion, fecha_evento, creador
    ):
        try:
            sql = (
                "insert into publicaciones values(null,%s, %s, %s, %s, NULL, %s, 0, %s)"
            )
            valores = (
                titulo,
                descripcion,
                ubicacion,
                fecha_creacion,
                fecha_evento,
                creador,
            )
            conexion = conectar_db()
            cursor = conexion.cursor()
            cursor.execute(sql, valores)
            conexion.commit()
            cursor.close()
            conexion.close()

        except mysql.connector.Error as error:
            print(f"Ocurrió un error {error}")

    def obtener_publicaciones(self):
        try:
            sql = "SELECT * FROM publicaciones ORDER BY id_publicacion DESC"
            conexion = conectar_db()

            # Vamos a usar el cursor como un diccionario para acceder con claves y valores
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(sql)

            # Obtenemos todas las publicaciones
            publicaciones = cursor.fetchall()

            cursor.close()
            conexion.close()

            return publicaciones

        except mysql.connector.Error as error:
            print("Ocurrió un error al pedir las publicaciones", error)

    def mostrar_publicaciones(self, contenedor):
        publicaciones = self.obtener_publicaciones()

        for publicacion in publicaciones:
            fecha_edicion = publicacion["fecha_edicion"]

            if fecha_edicion is not None:
                acomodar_fecha_edicion = fecha_edicion.strftime("%d/%m/%Y")
            else:
                acomodar_fecha_edicion = None

            fecha_creacion = publicacion["fecha"]
            fecha_evento = publicacion["fecha_evento"]

            acomodar_fecha_creacion = fecha_creacion.strftime("%d/%m/%Y")
            acomodar_fecha_evento = fecha_evento.strftime("%d/%m/%Y")

            MostrarPublicacion(
                contenedor,
                publicacion["titulo"],
                publicacion["descripcion"],
                publicacion["ubicacion"],
                acomodar_fecha_creacion,
                acomodar_fecha_edicion,
                acomodar_fecha_evento,
                publicacion["contador_votos"],
                publicacion["creador"],
            )


class MostrarPublicacion:
    def __init__(
        self,
        contenedor,
        titulo,
        descripcion,
        ubicacion,
        fecha_creacion,
        fecha_edicion,
        fecha_evento,
        contador_votos,
        creador,
    ):
        self.contenedor = contenedor
        self.titulo = titulo
        self.descripcion = descripcion
        self.ubicacion = ubicacion
        self.fecha_creacion = fecha_creacion
        self.fecha_edicion = fecha_edicion
        self.fecha_evento = fecha_evento
        self.contador_votos = contador_votos
        self.creador = creador

        self.tarjeta_frame = self.tarjeta_publicacion()

    def tarjeta_publicacion(self):
        # Crear un frame para la tarjeta de publicación
        tarjeta_frame = ctk.CTkFrame(
            master=self.contenedor,
            fg_color=COLOR_BG,
            corner_radius=15,
            border_color=COLOR_PRIMARIO_HOVER,
            border_width=2,
        )
        tarjeta_frame.pack(padx=190, pady=20, expand=False, fill="x")

        # Titulo de la tarjeta
        titulo_frame = ctk.CTkFrame(
            tarjeta_frame, fg_color=COLOR_PRIMARIO_HOVER, corner_radius=8
        )
        titulo_frame.pack(pady=(0, 15), padx=0, fill="x")

        titulo_label = ctk.CTkLabel(
            titulo_frame,
            text=self.titulo,
            text_color=COLOR_BG,
            font=("Roboto", 16, "bold"),
            height=40,
        )
        titulo_label.pack(expand=True)

        # Descripción de la tarjeta
        self.descripcion_label = ctk.CTkLabel(
            tarjeta_frame,
            text=self.descripcion,
            font=("Roboto", 14),
            text_color="#333333",
            anchor="w",
            justify="left",
        )
        self.descripcion_label.pack(pady=(0, 10), padx=20, anchor="w")

        # Ajustar el wraplength dinámicamente después de renderizar el frame
        tarjeta_frame.bind("<Configure>", self.ajustar_wraplength)

        # Frame de información
        info_frame = ctk.CTkFrame(tarjeta_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=15, pady=10)

        # Creador
        creador_label = ctk.CTkLabel(
            info_frame,
            text=f" Creador: {self.creador}",
            font=("Roboto", 12, "bold"),
            compound="left",
            image=crear_imagen("src/assets/icons/title.png"),
            text_color=COLOR_PRIMARIO_HOVER,
        )
        creador_label.grid(row=0, column=0, padx=5, pady=0, sticky="w")

        # Fecha de creación y edición
        if self.fecha_edicion is not None:
            fecha_edicion_label = ctk.CTkLabel(
                info_frame,
                text=f" Fecha de creación: {self.fecha_edicion}",
                font=("Roboto", 12, "bold"),
                compound="left",
                image=crear_imagen("src/assets/icons/title.png"),
                text_color=COLOR_PRIMARIO_HOVER,
            )
            fecha_edicion_label.grid(row=1, column=0, padx=5, pady=0, sticky="w")

        else:
            fecha_creacion_label = ctk.CTkLabel(
                info_frame,
                text=f" Fecha de creación: {self.fecha_creacion}",
                font=("Roboto", 12, "bold"),
                compound="left",
                image=crear_imagen("src/assets/icons/title.png"),
                text_color=COLOR_PRIMARIO_HOVER,
            )
            fecha_creacion_label.grid(row=1, column=0, padx=5, pady=0, sticky="w")

        # Fecha del evento
        fecha_evento_label = ctk.CTkLabel(
            info_frame,
            text=f" Fecha del evento: {self.fecha_evento}",
            font=("Roboto", 12, "bold"),
            compound="left",
            image=crear_imagen("src/assets/icons/title.png"),
            text_color=COLOR_PRIMARIO_HOVER,
        )
        fecha_evento_label.grid(row=1, column=1, padx=5, pady=0, sticky="e")

        # Ubicación
        ubicacion_label = ctk.CTkLabel(
            info_frame,
            text=f" Ubicación: {self.ubicacion}",
            font=("Roboto", 12, "bold"),
            compound="left",
            image=crear_imagen("src/assets/icons/title.png"),
            text_color=COLOR_PRIMARIO_HOVER,
        )
        ubicacion_label.grid(row=0, column=1, padx=5, pady=0, sticky="e")

        # Ajuste de las columnas para que ocupen el ancho total
        info_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(1, weight=1)

        # Sección de votos
        votos_frame = ctk.CTkFrame(tarjeta_frame, fg_color="transparent")
        votos_frame.pack(padx=15, pady=(10, 0), fill="x")

        # Botón de voto positivo
        boton_voto_positivo = ctk.CTkButton(
            votos_frame,
            text="Votar Positivo",
            fg_color=COLOR_PRIMARIO_HOVER,
            height=34,
            text_color=COLOR_BG,
            corner_radius=8,
            font=("Roboto", 14, "bold"),
            command=lambda: self.votar(),
            compound="left",
            image=crear_imagen("src/assets/icons/thumb-up.png"),
        )
        boton_voto_positivo.pack(side="left", fill="x", padx=5, expand=True)

        # Contador de votos
        self.contador_label = ctk.CTkLabel(
            votos_frame,
            text=f"{self.contador_votos}",
            font=("Roboto", 14, "bold"),
            height=34,
            text_color=COLOR_BG,
            corner_radius=80,
            fg_color=COLOR_PRIMARIO_HOVER,
        )
        self.contador_label.pack(side="left", padx=10)

        # Botón "Voy a participar"
        boton_participar = ctk.CTkButton(
            votos_frame,
            text="Voy a Participar",
            fg_color=COLOR_PRIMARIO_HOVER,
            text_color=COLOR_BG,
            height=34,
            corner_radius=10,
            font=("Roboto", 14, "bold"),
            command=lambda: self.participar(),
            compound="right",
            image=crear_imagen("src/assets/icons/mood-plus.png"),
        )
        boton_participar.pack(side="left", fill="x", padx=5, expand=True)

        return tarjeta_frame

    def ajustar_wraplength(self, event):
        # Calcular el ancho de la tarjeta y ajustar el wraplength dinámicamente
        ancho_tarjeta = self.tarjeta_frame.winfo_width() - 30  # Resta márgenes
        self.descripcion_label.configure(wraplength=ancho_tarjeta)

    def votar(self):
        self.contador_votos += 1
        self.actualizar_contador()

    def participar(self):
        print("Participo en el evento.")

    def actualizar_contador(self):
        self.contador_label.configure(text=f"{self.contador_votos}")
