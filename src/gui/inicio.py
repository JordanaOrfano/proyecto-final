from config.config import *
from gui.componentes import *
from gui.agregar_producto import *
from gui.estadisticas import *
from gui.vencimientos import *
from gui.configuracion import *
from core.usuarios import *


class InicioFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.conexion = Database()
        self.funciones_productos = Productos()

        self.frame_contenido = None
        self.botones_sideframe = {}  # Diccionario para almacenar botones del sideFrame
        self.side_frame()
        if Usuario.usuario_actual[0][2].strip('"') == "empleado":
            self.inicio()

        if Usuario.usuario_actual[0][2].strip('"') == "supervisor":
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
            image=crear_imagen("src/assets/menu-icon.png", size=(200, 200)),
        ).pack(pady=30)

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
        
        self.botones_sideframe["vencimientos"] = crear_boton_sideframe(
            centrar_frame,
            text="Vencimientos",
            command=self.vencimientos,
            image=crear_imagen("src/assets/icons/calendar-exclamation.png"),
        )

        self.botones_sideframe["estadisticas"] = crear_boton_sideframe(
            centrar_frame,
            text="Estadísticas",
            command=self.estadisticas,
            image=crear_imagen("src/assets/icons/stats.png"),
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
        
        # Centrar contenido
        frame_inicio_cont = ctk.CTkFrame(master=frame_inicio, fg_color=COLOR_BG)
        frame_inicio_cont.pack( fill="both", padx=40)
        
        # Crear contenedor para "Inicio" y "Carrito"
        frame_titulo = ctk.CTkFrame(master=frame_inicio_cont, fg_color=COLOR_BG)
        frame_titulo.pack(fill="x", pady=(30, 20))

        crear_label(
            frame_titulo,
            text="Inicio",
            font=("Roboto", 32, "bold"),
            pady=0,
            metodo="grid"
        ).pack(fill="x", pady=0, side="left")

        boton_carrito = crear_boton(
            parent=frame_titulo,
            text="0",
            width=100,
            padx=10,
            pady=0,
            metodo="grid",  
            image=crear_imagen("src/assets/icons/cart.png", size=(24, 24)),
            command=self.carrito
        )
        boton_carrito.pack(side="right")

        # Búsqueda y filtro
        frame_busqueda = ctk.CTkFrame(frame_inicio_cont, fg_color=COLOR_BG)
        frame_busqueda.pack(fill="x", pady=(10, 0))

        self.entry_busqueda = crear_entry(
            parent=frame_busqueda,
            placeholder_text="Buscar por nombre, marca o categoría",
            fill="x",
            padx=0,
            pady=0,
            metodo="pack",
        )
        self.entry_busqueda.pack(side="left", expand=True, fill="x")

        boton_buscar = crear_boton(
            parent=frame_busqueda,
            text="Buscar",
            width=100,
            padx=0,
            pady=0, 
            command=self.evento_buscar
        )
        boton_buscar.pack(side="right")
        
        # Dropdown de filtro para seleccionar orden
        self.filtro_ordenamiento = crear_optionmenu(
            parent=frame_busqueda,
            values=("Ordenar por", "ID", "Nombre", "Marca", "Categoría"),
            pady=0,
            padx=15,
        )

        self.filtro_ordenamiento.pack(side="left")
        
        # --------------- tabla productos ---------------
        # Crear las columnas y encabezados
        columnas = (
            "id",
            "producto",
            "marca",
            "categoria",
            "precio_compra",
            "precio_venta",
            "cantidad",
        )
        encabezados = (
            "ID",
            "Producto",
            "Marca",
            "Categoría",
            "Precio compra",
            "Precio venta",
            "Cantidad",
        )
        # Obtenemos los productos y lotes para insertarlos en una tabla
        tabla_productos, tabla_lotes = self.funciones_productos.buscar_productos(None, self.filtro_ordenamiento.get())

        crear_label(
            frame_inicio_cont,
            text="Productos",
            font=("Roboto", 24, "bold"),
            pady=(24, 0),
        )
        productos, self.tree_productos = crear_tabla(frame_inicio_cont, columnas, encabezados, tabla_productos, pady=10, menu="productos")
        
        
        # --------------- tabla lotes ---------------
        # Crear las columnas y encabezados
        columnas = ("lote", "id", "producto", "marca", "cantidad", "fecha_vencimiento")
        encabezados = ("Lote", "ID", "Producto", "Marca", "Cantidad", "Fecha vencimiento")     

        # Pasamos los lotes por una lista, para acomodarle la fecha y que sea en formato dia/mes/año
        lotes_acomodados = self.funciones_productos.transformar_lotes_a_lista(tabla_lotes)

        crear_label(
            frame_inicio_cont,
            text="Lotes",
            font=("Roboto", 24, "bold"),
            pady=(24, 0),
        )
        
        lotes, self.tree_lotes = crear_tabla(frame_inicio_cont, columnas, encabezados, lotes_acomodados, pady=(10, 30), menu="lotes")
        
        self.cambiar_contenido(frame_inicio, "inicio")
    
    def inicio_administrador(self):
        frame_inicio = ctk.CTkScrollableFrame(master=self, fg_color=COLOR_BG)
        crear_label(
            frame_inicio,
            text="Inicio ADMINISTRADOR",
            font=("Roboto", 32, "bold"),
            pady=(30, 10),
        )

        productos = Productos()
        productos.mostrar_publicaciones(contenedor=frame_inicio)

        self.cambiar_contenido(frame_inicio, "inicio")

    # Obtiene el click cuando el usuario toca "buscar" y hace una funcion
    def evento_buscar(self):
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
    
        for item in self.tree_lotes.get_children():
            self.tree_lotes.delete(item)

        tabla_productos, tabla_lotes = self.funciones_productos.buscar_productos(self.entry_busqueda.get().strip(), self.filtro_ordenamiento.get())

        for producto in tabla_productos:
            self.tree_productos.insert("", tk.END, values=producto)
    
        lotes_acomodados = self.funciones_productos.transformar_lotes_a_lista(tabla_lotes)

        for lote in lotes_acomodados:
            self.tree_lotes.insert("", tk.END, values=lote)

    
    def carrito(self):
        frame_carrito_fondo = ctk.CTkFrame(master=self, fg_color=COLOR_BG)
        
        frame_carrito = ctk.CTkFrame(master=frame_carrito_fondo, fg_color=COLOR_BG)
        frame_carrito.pack(expand=True, fill="x", padx=40)
        
        crear_label(
            frame_carrito,
            text="Carrito",
            font=("Roboto", 32, "bold"),
            pady=(0, 10),
        )
        
        columnas = ("id", "nombre", "marca", "precio_venta", "cantidad")
        encabezados = ("ID", "Nombre", "Marca", "Precio", "Cantidad")
        
        productos_carrito = self.conexion.ejecutar_bd(
            sql="""
                   SELECT
                        productos.id,
                        productos.nombre, 
                        productos.marca, 
                        productos.precio_venta, 
                        SUM(lotes.cantidad) AS cantidad 
                    FROM 
                        lotes 
                    JOIN 
                        productos ON lotes.producto_id = productos.id 
                    GROUP BY 
                        productos.id, 
                        productos.nombre, 
                        productos.marca, 
                        productos.precio_venta;
                """,
            valores=None,
        )

        # Transformamos a una lista
        productos_carrito_lista = []

        for fila in productos_carrito:
            productos_carrito_lista.append(list(fila))
        
        crear_tabla(frame_carrito, columnas=columnas, encabezados=encabezados, lotes=productos_carrito_lista, pady=10)
        
        # Sección Pago
        frame_pago = ctk.CTkFrame(master=frame_carrito, fg_color=COLOR_BG)
        frame_pago.pack(pady=(20, 10), fill="x") 
        
        crear_label(frame_pago, text="Pago", font=("Roboto", 24, "bold"), metodo="grid").pack(fill="x", side="left")
        pago = crear_entry(frame_pago, placeholder_text="$", fill="x", metodo="grid")
        pago.pack(side="right", fill="x", expand=True)
        
        # Sección Total y Vuelto
        frame_info = ctk.CTkFrame(master=frame_carrito, fg_color=COLOR_BG)
        frame_info.pack(pady=15, fill="x") 
        
        label_total = crear_label(frame_info, text=f"Total: ${0}", font=("Roboto", 24, "bold"), metodo="grid")
        label_total.pack(side="left", fill="x")
        
        label_vuelto = crear_label(frame_info, text=f"Vuelto: ${0}", font=("Roboto", 24, "bold"), metodo="grid")
        label_vuelto.pack(side="right", fill="x")
        
        # Sección botones
        frame_botones = ctk.CTkFrame(master=frame_carrito, fg_color=COLOR_BG)
        frame_botones.pack(fill="x") 

        btn_finalizar_compra = crear_boton(frame_botones, text="Finalizar compra")
        btn_finalizar_compra.pack(side="left", padx=5, pady=0, fill="x", expand=True) 
        
        btn_cancelar_compra = crear_boton(frame_botones, text="Cancelar")
        btn_cancelar_compra.pack(side="left", padx=5, pady=0, fill="x", expand=True)
        
        btn_volver = crear_boton(frame_botones, text="Volver", command=self.inicio)
        btn_volver.pack(side="left", padx=5, pady=0, fill="x", expand=True)
        
        self.cambiar_contenido(frame_carrito_fondo, "ventas")

    def crear_producto(self):
        frame_publicar = ctk.CTkFrame(master=self, fg_color=COLOR_BG)

        CrearProducto(contenedor=frame_publicar)
        self.cambiar_contenido(frame_publicar, "crear_producto")

    def estadisticas(self):
        frame_estadisticas = ctk.CTkFrame(master=self, fg_color=COLOR_BG)
        
        Estadisticas(contenedor=frame_estadisticas)
        self.cambiar_contenido(frame_estadisticas, "estadisticas")

    def vencimientos(self):
        frame_vencimientos = ctk.CTkFrame(master=self, fg_color=COLOR_BG)
        
        Vencimientos(contenedor=frame_vencimientos)
        self.cambiar_contenido(frame_vencimientos, "vencimientos")
    
    def configuracion(self):
        frame_configuracion = ctk.CTkFrame(
            master=self, fg_color=COLOR_BG)
        
        Configuracion(contenedor=frame_configuracion)
        self.cambiar_contenido(frame_configuracion, "configuracion")

    def cerrar_sesion(self):
        self.quit()
