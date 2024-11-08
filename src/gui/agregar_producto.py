from config.config import *
from core.productos import *
from core.usuarios import *
from gui.componentes import *


class CrearProducto:
    def __init__(self, contenedor):
        self.contenedor = contenedor

        # Frame principal que ocupa toda la ventana y se expande
        self.frame_crear = ctk.CTkFrame(master=self.contenedor, fg_color=COLOR_BG)
        self.frame_crear.grid(sticky="nsew", padx=130)
        
        # Configuración para centrar el frame en ambas direcciones
        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)
        self.frame_crear.grid_rowconfigure(0, weight=1)
        self.frame_crear.grid_rowconfigure(2, weight=1)  # Fila extra para centrar verticalmente
        self.frame_crear.grid_columnconfigure(0, weight=1)

        # Frame del formulario centrado y ajustable
        formulario_frame = ctk.CTkFrame(self.frame_crear, fg_color=COLOR_BG)
        formulario_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        formulario_frame.grid_columnconfigure((0, 1), weight=1)  # Hacer que las columnas se expandan

        # Título
        label_titulo = crear_label(formulario_frame, 
                                   metodo="grid", 
                                   text="Añadir producto", 
                                   font=("Roboto", 32, "bold"))
        label_titulo.grid(row=0, column=0, columnspan=2, pady=(0, 25), sticky="ew")

        # Campo de entrada para Nombre del producto
        label_nombre_producto = crear_label(formulario_frame, 
                                   metodo="grid", 
                                   text=" Nombre del producto", 
                                   font=("Roboto", 18, "bold"), 
                                   image=crear_imagen("src/assets/icons/title.png", size=(22, 22)))
        label_nombre_producto.grid(row=1, column=0, sticky="w", pady=(10,0), padx=10)
        
        self.nombre_producto = crear_entry(formulario_frame, placeholder_text="Nombre del producto", metodo="grid")
        self.nombre_producto.grid(row=2, column=0, sticky="ew", padx=(10, 10), pady=(0, 10))

        # Campo de entrada para Nombre del lote
        label_nombre_lote = crear_label(formulario_frame, 
                                   metodo="grid", 
                                   text=" Nombre del lote", 
                                   font=("Roboto", 18, "bold"), 
                                   image=crear_imagen("src/assets/icons/lote.png", size=(22, 22)))
        label_nombre_lote.grid(row=1, column=1, sticky="w", pady=(10,0), padx=10)
        
        self.nombre_lote = crear_entry(formulario_frame, placeholder_text="Nombre del lote", metodo="grid")
        self.nombre_lote.grid(row=2, column=1, sticky="ew", padx=(10, 10), pady=(0, 10))

        # Campo de entrada para Marca
        label_marca = crear_label(formulario_frame, 
                                  metodo="grid", 
                                  text=" Marca", 
                                  font=("Roboto", 18, "bold"), 
                                  image=crear_imagen("src/assets/icons/description.png", size=(22, 22)))
        label_marca.grid(row=3, column=0, sticky="w", pady=(10,0), padx=10)
        
        self.marca = crear_entry(formulario_frame, placeholder_text="Marca del producto", metodo="grid")
        self.marca.grid(row=4, column=0, sticky="ew", padx=10, pady=(0, 10))

        # Campo de entrada para Categoría
        label_categoria = crear_label(formulario_frame, 
                                      metodo="grid", 
                                      text=" Categoría", 
                                      font=("Roboto", 18, "bold"), 
                                      image=crear_imagen("src/assets/icons/category.png", size=(22, 22)))
        label_categoria.grid(row=3, column=1, sticky="w", pady=(10,0), padx=10)
        
        categorias = Productos()
        categorias = categorias.obtener_categorias()


        self.categoria = crear_dropdown(formulario_frame, 
                                        values=["Elija o escriba una categoría"] + categorias, metodo="grid")
        self.categoria.grid(row=4, column=1, sticky="ew", padx=10, pady=(0, 10))


        # Campo de entrada para Precio de compra
        label_precio_compra = crear_label(formulario_frame, 
                                          metodo="grid", 
                                          text=" Precio de compra", 
                                          font=("Roboto", 18, "bold"), 
                                          image=crear_imagen("src/assets/icons/currency-dollar.png", size=(22, 22)))
        label_precio_compra.grid(row=5, column=0, sticky="w", pady=(10,0), padx=10)
        
        self.precio_compra = crear_entry(formulario_frame, placeholder_text="$", metodo="grid")
        self.precio_compra.grid(row=6, column=0, sticky="ew", padx=10, pady=(0, 10))

        # Campo de entrada para Precio de venta
        label_precio_venta = crear_label(formulario_frame, 
                                         metodo="grid", 
                                         text=" Precio de venta", 
                                         font=("Roboto", 18, "bold"), 
                                         image=crear_imagen("src/assets/icons/report-money.png", size=(22, 22)))
        label_precio_venta.grid(row=5, column=1, sticky="w", pady=(10,0), padx=10)
        
        self.precio_venta = crear_entry(formulario_frame, 
                                        placeholder_text="$", metodo="grid")
        self.precio_venta.grid(row=6, column=1, sticky="ew", padx=10, pady=(0, 10))

        # Campo de entrada para Cantidad
        label_cantidad = crear_label(formulario_frame, 
                                     metodo="grid", 
                                     text=" Cantidad", 
                                     font=("Roboto", 18, "bold"), 
                                     image=crear_imagen("src/assets/icons/pencil.png", size=(22, 22)))
        label_cantidad.grid(row=9, column=0, sticky="w", pady=(10,0), padx=10)

        self.cantidad = crear_entry(formulario_frame, placeholder_text="0", metodo="grid")
        self.cantidad.grid(row=10, column=0, sticky="ew", padx=10, pady=(0, 10))

        # Campo de entrada para Vencimiento
        label_vencimiento = crear_label(formulario_frame, 
                                        metodo="grid", 
                                        text=" Vencimiento", 
                                        font=("Roboto", 18, "bold"), 
                                        image=crear_imagen("src/assets/icons/calendar.png", size=(22, 22)))
        label_vencimiento.grid(row=9, column=1, sticky="w", pady=(10,0), padx=10)

        self.vencimiento = crear_entry(formulario_frame, placeholder_text="DD/MM/AA", metodo="grid")
        self.vencimiento.grid(row=10, column=1, sticky="ew", padx=10, pady=(0, 10))


        # Botón de enviar
        boton_crear = crear_boton(formulario_frame, 
                                  metodo="grid",
                                  text="Crear", 
                                  command=self.enviar_producto_a_bd)
        boton_crear.grid(row=13, column=0, columnspan=2, pady=(20, 10), padx=10, sticky="ew")

    def enviar_producto_a_bd(self):
        # creador = f"{Usuario.usuario_actual[0]} {Usuario.usuario_actual[1]}"

        Productos.subir_producto_a_bd(self, self.nombre_lote.get(), self.nombre_producto.get(), self.marca.get(), self.precio_compra.get(), self.precio_venta.get(), self.categoria.get(), self.cantidad.get(), self.vencimiento.get())
 