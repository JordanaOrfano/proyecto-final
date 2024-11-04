import customtkinter as ctk
from datetime import datetime
from config.config import *
from core.publicaciones import *
from core.usuarios import *

class CrearProducto:
    def __init__(self, contenedor):
        self.contenedor = contenedor

        # Frame principal que ocupa toda la ventana y se expande
        self.frame_publicar = ctk.CTkFrame(master=self.contenedor, fg_color=COLOR_BG)
        self.frame_publicar.grid(sticky="nsew", padx=165)
        
        # Configuración para centrar el frame en ambas direcciones
        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)
        self.frame_publicar.grid_rowconfigure(0, weight=1)
        self.frame_publicar.grid_rowconfigure(2, weight=1)  # Fila extra para centrar verticalmente
        self.frame_publicar.grid_columnconfigure(0, weight=1)

        # Frame del formulario centrado y ajustable
        formulario_frame = ctk.CTkFrame(self.frame_publicar, fg_color=COLOR_BG)
        formulario_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        formulario_frame.grid_columnconfigure((0, 1), weight=1)  # Hacer que las columnas se expandan

        # Título
        label_titulo = crear_label(formulario_frame, 
                                   metodo="grid", 
                                   text="Crear producto", 
                                   font=("Roboto", 32, "bold"))
        label_titulo.grid(row=0, column=0, columnspan=2, pady=(0, 25), sticky="ew")

        # Campo de entrada para Nombre
        label_nombre = crear_label(formulario_frame, 
                                   metodo="grid", 
                                   text=" Nombre", 
                                   font=("Roboto", 18, "bold"), 
                                   image=crear_imagen("src/assets/icons/title.png", size=(22, 22)))
        label_nombre.grid(row=1, column=0, sticky="w", pady=(10,0), padx=10)
        
        self.nombre = crear_entry(formulario_frame, placeholder_text="Nombre del producto")
        self.nombre.grid(row=2, column=0, columnspan=2, sticky="ew", padx=(10, 10), pady=(0, 10))

        # Campo de entrada para Marca
        label_marca = crear_label(formulario_frame, 
                                  metodo="grid", 
                                  text=" Marca", 
                                  font=("Roboto", 18, "bold"), 
                                  image=crear_imagen("src/assets/icons/description.png", size=(22, 22)))
        label_marca.grid(row=3, column=0, sticky="w", pady=(10,0), padx=10)
        
        self.marca = crear_entry(formulario_frame, placeholder_text="Marca del producto")
        self.marca.grid(row=4, column=0, sticky="ew", padx=10, pady=(0, 10))

        # Campo de entrada para Categoría
        label_categoria = crear_label(formulario_frame, 
                                      metodo="grid", 
                                      text=" Categoría", 
                                      font=("Roboto", 18, "bold"), 
                                      image=crear_imagen("src/assets/icons/category.png", size=(22, 22)))
        label_categoria.grid(row=3, column=1, sticky="w", pady=(10,0), padx=10)
        
        self.categoria = crear_dropdown(formulario_frame, 
                                        values=["Elija una Opción", "Opción 1", "Opción 2", "Opción 3"])
        self.categoria.grid(row=4, column=1, sticky="ew", padx=10, pady=(0, 10))

        # Campo de entrada para Precio de compra
        label_precio_compra = crear_label(formulario_frame, 
                                          metodo="grid", 
                                          text=" Precio de compra", 
                                          font=("Roboto", 18, "bold"), 
                                          image=crear_imagen("src/assets/icons/currency-dollar.png", size=(22, 22)))
        label_precio_compra.grid(row=5, column=0, sticky="w", pady=(10,0), padx=10)
        
        self.precio_compra = crear_entry(formulario_frame, placeholder_text="$")
        self.precio_compra.grid(row=6, column=0, sticky="ew", padx=10, pady=(0, 10))

        # Campo de entrada para Precio de venta
        label_precio_venta = crear_label(formulario_frame, 
                                         metodo="grid", 
                                         text=" Precio de venta", 
                                         font=("Roboto", 18, "bold"), 
                                         image=crear_imagen("src/assets/icons/report-money.png", size=(22, 22)))
        label_precio_venta.grid(row=5, column=1, sticky="w", pady=(10,0), padx=10)
        
        self.precio_venta = crear_entry(formulario_frame, 
                                        placeholder_text="$")
        self.precio_venta.grid(row=6, column=1, sticky="ew", padx=10, pady=(0, 10))

        # Campo de entrada para Cantidad
        label_cantidad = crear_label(formulario_frame, 
                                     metodo="grid", 
                                     text=" Cantidad", 
                                     font=("Roboto", 18, "bold"), 
                                     image=crear_imagen("src/assets/icons/pencil.png", size=(22, 22)))
        label_cantidad.grid(row=9, column=0, sticky="w", pady=(10,0), padx=10)

        self.cantidad = crear_entry(formulario_frame, placeholder_text="0")
        self.cantidad.grid(row=10, column=0, sticky="ew", padx=10, pady=(0, 10))

        # Campo de entrada para Vencimiento
        label_vencimiento = crear_label(formulario_frame, 
                                        metodo="grid", 
                                        text=" Vencimiento", 
                                        font=("Roboto", 18, "bold"), 
                                        image=crear_imagen("src/assets/icons/calendar.png", size=(22, 22)))
        label_vencimiento.grid(row=9, column=1, sticky="w", pady=(10,0), padx=10)

        self.vencimiento = crear_entry(formulario_frame, placeholder_text="DD/MM/AA")
        self.vencimiento.grid(row=10, column=1, sticky="ew", padx=10, pady=(0, 10))


        # Botón de enviar
        boton_crear = crear_boton(formulario_frame, 
                                  metodo="grid",
                                  text="Crear", 
                                  command=self.enviar_publicacion)
        boton_crear.grid(row=13, column=0, columnspan=2, pady=(20, 10), padx=10, sticky="ew")

    def enviar_publicacion(self):
        # Obtener los datos de los campos de entrada
        nombre = self.nombre.get()
        marca = self.marca.get()
        precio_compra = self.precio_compra.get()
        precio_venta = self.precio_venta.get()
        categoria = self.categoria.get()
        cantidad = self.cantidad.get()
        vencimiento = self.vencimiento.get()

        # Procesar datos antes de enviar a la base de datos
        fecha_creacion = datetime.now().date()
        creador = f"{Usuario.usuario_actual[0]} {Usuario.usuario_actual[1]}"

        publicar = Publicaciones()
        publicar.subir_publicacion_a_bd(nombre, marca, precio_compra, precio_venta, categoria, cantidad, vencimiento, fecha_creacion, creador)
