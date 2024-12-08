from config.config import *
from gui.componentes import *
from gui.revisar_ventas import *
from gui.agregar_producto import *
from gui.estadisticas import *
from gui.vencimientos import *
from gui.configuracion import *
from core.usuarios import *


class InicioFrame(ctk.CTkFrame):
    def __init__(self, master, frame_cambiar):
        super().__init__(master)
        
        self.frame_cambiar = frame_cambiar
        self.conexion = Database()
        self.funciones_productos = Productos()
        self.productos_del_carrito = []

        self.frame_contenido = None
        self.botones_sideframe = {}  # Diccionario para almacenar botones del sideFrame
        self.side_frame()
        self.inicio()

    def side_frame(self):
        sideFrame = ctk.CTkFrame(master=self, width=240, fg_color=COLOR_PRIMARIO)
        sideFrame.pack(side="left", fill="y")

        # Centra el contenido del sideFrame
        centrar_frame = ctk.CTkFrame(sideFrame, fg_color=COLOR_PRIMARIO)
        centrar_frame.pack(expand=True)

        ctk.CTkLabel(
            centrar_frame,
            text="StockUp!",
            font=("Roboto", 32, "bold"),
            text_color=COLOR_BG,
            width=210,
        ).pack(pady=0)

        ctk.CTkLabel(
            centrar_frame,
            text="",
            image=crear_imagen("src/assets/menu-icon.png", size=(210, 210)),
        ).pack(pady=20)

        # Creación de botones en el sideFrame con el estado de selección inicial
        self.botones_sideframe["inicio"] = crear_boton_sideframe(
            centrar_frame,
            text="Inicio",
            command=self.inicio,
            image=crear_imagen("src/assets/icons/home.png"),
        )

        if Usuario.usuario_actual[0][2] == "supervisor":
            self.botones_sideframe["Revisar ventas"] = crear_boton_sideframe(
                centrar_frame,
                text="Revisar ventas",
                command=self.revisar_ventas,
                image=crear_imagen("src/assets/icons/shopping-cart-share.png"),
            )

        self.botones_sideframe["crear_producto"] = crear_boton_sideframe(
            centrar_frame,
            text="Añadir producto",
            command=self.crear_producto,
            image=crear_imagen("src/assets/icons/pencil-plus.png"),
        )
        if Usuario.usuario_actual[0][2] == "supervisor":
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
            pady=(5, 0),
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
        contador_carrito = self.obtener_productos_carrito()

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

        self.boton_carrito = crear_boton(
            parent=frame_titulo,
            text=f"{len(contador_carrito)}",
            width=100,
            padx=10,
            pady=0,
            metodo="grid",  
            image=crear_imagen("src/assets/icons/cart.png", size=(24, 24)),
            command=self.carrito
        )
        self.boton_carrito.pack(side="right")

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
        
        # Obtenemos los productos y lotes para insertarlos en una tabla
        tabla_productos, tabla_lotes = self.funciones_productos.buscar_productos(None, self.filtro_ordenamiento.get())
        
        # --------------- tabla lotes ---------------
        # Crear las columnas y encabezados
        columnas = ("lote", "id", "producto", "marca", "cantidad", "fecha_vencimiento", "precio")
        encabezados = ("Lote", "ID", "Producto", "Marca", "Cantidad", "Fecha vencimiento", "Precio")     

        # Pasamos los lotes por una lista, para acomodarle la fecha y que sea en formato dia/mes/año
        lotes_acomodados = self.funciones_productos.transformar_lotes_a_lista(tabla_lotes)

        crear_label(
            frame_inicio_cont,
            text="Lotes",
            font=("Roboto", 24, "bold"),
            pady=(24, 0),
        )
        
        lotes, self.tree_lotes = crear_tabla(frame_inicio_cont, columnas, encabezados, lotes_acomodados, pady=(10, 30), menu="lotes", funciones_inicio = self)

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

        crear_label(
            frame_inicio_cont,
            text="Productos",
            font=("Roboto", 24, "bold"),
            pady=(24, 0),
        )

        productos, self.tree_productos = crear_tabla(frame_inicio_cont, columnas, encabezados, tabla_productos, pady=10, menu="productos", funciones_inicio = self)
        
        self.frame_inicio_cont = frame_inicio_cont
        self.cambiar_contenido(frame_inicio, "inicio")
    
    def revisar_ventas(self):
        # frame_ventas = ctk.CTkFrame(master=self, fg_color=COLOR_BG)
        frame_ventas = ctk.CTkScrollableFrame(master=self, fg_color=COLOR_BG)
        
        RevisarVentas(contenedor=frame_ventas)
        self.cambiar_contenido(frame_ventas, "Revisar ventas")

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

    # ----- Carrito de productos -----
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
        
        columnas = ("lote", "id", "producto", "marca", "cantidad", "vencimiento", "precio")
        encabezados = ("Lote", "ID", "Producto", "Marca", "Cantidad", "Vencimiento", "Precio")
        
        productos_carrito = self.obtener_productos_carrito()

        tabla, self.tree = crear_tabla(frame_carrito, columnas=columnas, encabezados=encabezados, lotes=productos_carrito, pady=10, menu = "carrito", funciones_inicio = self)
        total = 0
        for producto in productos_carrito:
            total += float(producto[6]) * int(producto[4])

        # Sección Pago
        frame_pago = ctk.CTkFrame(master=frame_carrito, fg_color=COLOR_BG)
        frame_pago.pack(pady=(20, 10), fill="x") 
        
        crear_label(frame_pago, text="Pago", font=("Roboto", 24, "bold"), metodo="grid").pack(fill="x", side="left")
        self.pago = crear_entry(frame_pago, placeholder_text="$", fill="x", metodo="grid")
        self.pago.pack(side="right", fill="x", expand=True)
        
        # Sección Total y Vuelto
        frame_info = ctk.CTkFrame(master=frame_carrito, fg_color=COLOR_BG)
        frame_info.pack(pady=15, fill="x") 
        
        self.label_total = crear_label(frame_info, text=f"Total: ${total}", font=("Roboto", 24, "bold"), metodo="grid")
        self.label_total.pack(side="left", fill="x")
        
        # Sección botones
        frame_botones = ctk.CTkFrame(master=frame_carrito, fg_color=COLOR_BG)
        frame_botones.pack(fill="x") 

        btn_finalizar_compra = crear_boton(frame_botones, text="Finalizar compra", command=lambda: self.evento_finalizar_compra(self.productos_del_carrito, total))
        btn_finalizar_compra.pack(side="left", padx=5, pady=0, fill="x", expand=True) 
        
        btn_cancelar_compra = crear_boton(frame_botones, text="Vaciar Carrito", command=self.vaciar_productos_carro)
        btn_cancelar_compra.pack(side="left", padx=5, pady=0, fill="x", expand=True)
        
        btn_volver = crear_boton(frame_botones, text="Volver", command=self.inicio)
        btn_volver.pack(side="left", padx=5, pady=0, fill="x", expand=True)
        
        self.cambiar_contenido(frame_carrito_fondo, "ventas")

    def agregar_productos_carrito(self, valores):
        valores_lista = list(valores)
        valores_lista[4] = 1

        if not valores_lista in self.productos_del_carrito:
            self.productos_del_carrito.append(valores_lista)
            crear_notificacion(self, "info", f"Producto {valores[2]} agregado")

        else:
            crear_notificacion(self, "info", f"El producto {valores[2]} ya está en el carrito.")

    def obtener_productos_carrito(self):
        return self.productos_del_carrito

    def vaciar_productos_carro(self):
        self.productos_del_carrito = []
        self.carrito()
        
    def validar_pago(self, pago, total):
        try:
            pago = str(pago).strip().replace(",", ".")
            
            pago = float(pago)

            if pago > 0 and pago < 100000000 and pago >= total:
                return pago
            
            return False
        except (ValueError, AttributeError):  
            return False


    def evento_finalizar_compra(self, productos_carrito, total):
        # Alerta para confirmar venta
        respuesta = CTkAlert(
            state="warning",
            title="Registrar venta",
            body_text=f"¿Desea confirmar la venta? Esta acción no se puede deshacer.",
            btn1="Registrar Venta",
            btn2="Cancelar",
        )

        if respuesta.get() != "Registrar Venta":
            return

        pago_valido = self.validar_pago(self.pago.get(), total)
        if not pago_valido:
            crear_notificacion(self, "warning", "Debes ingresar un monto de pago válido.")
            return

        if not productos_carrito:
            CTkNotification(
                master=self,
                state="warning",
                message="No hay productos en el carrito.",
                side="right_bottom",
            ).after(3000, lambda: None)
            return

        try:
                                    
            # ----- QUERY UPDATE TABLA LOTES -----
            case_statements = []  # Almacena las instrucciones CASE WHEN
            ids = []  # Almacena todos los ids de los productos
            ganancia_unitaria = []  # Almacena la ganancia por la venta de cada producto
            cantidades = []  # Almacena todas las cantidades para hacer un join separadas por comas
            valores = []  
            lotes = []  # Almacena los lotes únicos

            # Construir los CASE WHEN para cada producto
            for producto in productos_carrito:
                lote_id = producto[0]  
                cantidad_vendida = int(producto[4])  # Cantidad vendida
                ganancia_recibida = float(producto[4]) * float(producto[6])  # Ganancia por unidad

                # Generar el CASE WHEN para actualizar la cantidad del lote
                case_statements.append("WHEN lote = %s THEN cantidad - %s")
                valores.extend([lote_id, cantidad_vendida])  # Agregar lote y cantidad a los parámetros

                if lote_id not in lotes:
                    lotes.append(lote_id)

                # Almacenar el id y la ganancia para la tabla de ventas
                ids.append(producto[1])  # ID del producto
                cantidades.append(cantidad_vendida)
                ganancia_unitaria.append(ganancia_recibida)

            sql = f"""
                UPDATE lotes
                SET cantidad = CASE
                    {' '.join(case_statements)}
                END
                WHERE lote IN ({', '.join(['%s'] * len(lotes))})
            """

            # El CASE se utiliza para colocar multiples WHEN, y el THEN se utiliza para modificar la cantidad actual
            # EL WHEN se utiliza cómo un if pero para un resultado especifico, esa es la diferencia entre el WHERE y WHEN. WHERE es para señalar las condiciones de una fila.
            # El END se utiliza despues del CASE para señalar el fin de las condiciones.

            # Agregar los lotes al final de los parámetros
            valores.extend(lotes)

            # Ejecutar la consulta para actualizar las cantidades en la tabla lotes
            self.conexion.ejecutar_bd(sql, valores, "update")

            # ----- Ocultar Lotes sin cantidades a mostrar = False -----
            sql_lotes_invisibles = """
                UPDATE lotes
                SET mostrar = 0
                WHERE cantidad = 0
            """
            self.conexion.ejecutar_bd(sql_lotes_invisibles, tipo = "update")

            # ----- Ocultar Productos sin lotes asociados mostrar = False -----
            sql_productos_invisibles = """
                UPDATE productos
                SET mostrar = 0
                WHERE id NOT IN (
                    SELECT DISTINCT producto_id
                    FROM lotes
                    WHERE mostrar = 1
                )
            """
            self.conexion.ejecutar_bd(sql_productos_invisibles, tipo = "update")


            # ----- QUERY INSERT TABLA VENTAS -----
            fecha_venta = datetime.now()

            ids_productos_str = ",".join(map(str, ids))  # Juntar todas las ids de los productos
            ganancias_unitarias_str = ",".join(map(str, ganancia_unitaria))  
            cantidades_str = ",".join(map(str, cantidades))  # Juntar todas las cantidades en un string, el map itera sobre todas y las transforma en strings.

            sql = """
                INSERT INTO VENTAS (producto_id, cantidad_vendida, ganancia_unitaria, ganancia_venta, fecha_venta, empleado_documento)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            valores_ventas = (ids_productos_str, cantidades_str, ganancias_unitarias_str, total, fecha_venta, Usuario.usuario_actual[0][5])

            self.conexion.ejecutar_bd(sql, valores_ventas, "insert")
            
            total = 0
            for producto in productos_carrito:
                total += float(producto[6]) * int(producto[4])
            
            CTkAlert(
                state="info",
                title="Venta realizada",
                body_text=f"El vuelto que corresponde al cliente es de: ${(pago_valido - total):.2f}.",
                btn1="Ok",
            )

            # Vaciar el carrito de productos
            self.vaciar_productos_carro()

        except Exception as e:
            print(f"Error al ejecutar las consultas: {e}")

    def crear_producto(self):
        frame_publicar = ctk.CTkFrame(master=self, fg_color=COLOR_BG)

        CrearProducto(contenedor=frame_publicar, frame_origen = self.inicio)
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
        notificacion = CTkNotification(master=self, state="info", message="Cerrando sesión...", side="right_bottom")
        self.after(3000, notificacion.destroy)
        self.after(1500, lambda: self.frame_cambiar("login"))
