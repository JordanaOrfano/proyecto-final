from config.config import *
from core.productos import *
from core.usuarios import *
from gui.componentes import *
from database.conexion import *


class CrearProducto:
    def __init__(self, contenedor, frame_origen = None, procedencia = "inicio", valor = None):
        self.contenedor = contenedor
        self.productos_funciones = Productos()
        self.frame_origen = frame_origen # Se utiliza para volver al frame anterior

        # Frame principal que ocupa toda la ventana y se expande
        self.frame_crear = ctk.CTkFrame(master=self.contenedor, fg_color=COLOR_BG)
        self.frame_crear.grid(sticky="nsew", padx=100)
        
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
        if procedencia == "inicio":
            label_titulo = crear_label(formulario_frame, 
                                    metodo="grid", 
                                    text="Añadir producto", 
                                    font=("Roboto", 32, "bold"))
            label_titulo.grid(row=0, column=0, columnspan=2, pady=(0, 25), sticky="ew")

        if procedencia == "tabla_producto":
            label_titulo = crear_label(formulario_frame, 
                                    metodo="grid", 
                                    text=f"Editar '{valor[1]}'", 
                                    font=("Roboto", 32, "bold"))
            label_titulo.grid(row=0, column=0, columnspan=2, pady=(0, 25), sticky="ew")

        if procedencia == "tabla_lote":
            label_titulo = crear_label(formulario_frame, 
                                    metodo="grid", 
                                    text=f"Editar lote {valor[0]} de '{valor[2]}'", 
                                    font=("Roboto", 32, "bold"))
            label_titulo.grid(row=0, column=0, columnspan=2, pady=(0, 25), sticky="ew")

        label_producto_nombre = crear_label(formulario_frame, 
                                metodo="grid", 
                                text=" Nombre del producto", 
                                font=("Roboto", 18, "bold"), 
                                image=crear_imagen("src/assets/icons/title.png", size=(22, 22)))

        # Si se accede desde la tabla_lote no debería poder modificar el nombre del producto, marca, categoria, precio_compra ni precio_venta
        if procedencia != "tabla_lote":
            self.producto_nombre = crear_entry(formulario_frame, placeholder_text="Nombre del producto", metodo="grid")

        else:
            self.producto_nombre = crear_entry(formulario_frame, placeholder_text="Deshabilitado desde 'Editar Lote'", metodo="grid", fg_color="#dbd5cd")
            self.producto_nombre.configure(state="disabled")

        label_producto_nombre.grid(row=1, column=0, columnspan=2, sticky="w", pady=(10,0), padx=10)
        self.producto_nombre.grid(row=2, column=0, columnspan=2, sticky="ew", padx=(10, 10), pady=(0, 10))

        # Campo de entrada para Marca
        label_producto_marca = crear_label(formulario_frame, 
                                  metodo="grid", 
                                  text=" Marca", 
                                  font=("Roboto", 18, "bold"), 
                                  image=crear_imagen("src/assets/icons/description.png", size=(22, 22)))
        label_producto_marca.grid(row=3, column=0, sticky="w", pady=(10,0), padx=10)
        
        if procedencia != "tabla_lote":
            self.producto_marca = crear_entry(formulario_frame, placeholder_text="Marca del producto", metodo="grid")
        else:
            self.producto_marca = crear_entry(formulario_frame, placeholder_text="Deshabilitado desde 'Editar Lote'", metodo="grid", fg_color="#dbd5cd")
            self.producto_marca.configure(state="disabled")

        self.producto_marca.grid(row=4, column=0, sticky="ew", padx=10, pady=(0, 10))

        # Campo de entrada para Categoría
        label_producto_categoria = crear_label(formulario_frame, 
                                      metodo="grid", 
                                      text=" Categoría", 
                                      font=("Roboto", 18, "bold"), 
                                      image=crear_imagen("src/assets/icons/category.png", size=(22, 22)))
        label_producto_categoria.grid(row=3, column=1, sticky="w", pady=(10,0), padx=10)
        
        if procedencia != "tabla_lote":
            categorias = self.productos_funciones.obtener_categorias()
            self.producto_categoria = crear_dropdown(formulario_frame, 
                                            values=["Elija o escriba una categoría"] + categorias, metodo="grid")
            
        else:
            self.producto_categoria = crear_dropdown(formulario_frame, 
                                            values=["Deshabilitado desde 'Editar Lote'"], metodo="grid")
            self.producto_categoria.configure(state="disabled", fg_color="#dbd5cd")

        self.producto_categoria.grid(row=4, column=1, sticky="ew", padx=10, pady=(0, 10))

        # Campo de entrada para Precio de compra
        label_producto_precio_compra = crear_label(formulario_frame, 
                                          metodo="grid", 
                                          text=" Precio de compra", 
                                          font=("Roboto", 18, "bold"), 
                                          image=crear_imagen("src/assets/icons/currency-dollar.png", size=(22, 22)))
        label_producto_precio_compra.grid(row=5, column=0, sticky="w", pady=(10,0), padx=10)
        
        if procedencia != "tabla_lote":
            self.producto_precio_compra = crear_entry(formulario_frame, placeholder_text="$", metodo="grid")

        else:
            self.producto_precio_compra = crear_entry(formulario_frame, placeholder_text="Deshabilitado desde 'Editar Lote'", metodo="grid", fg_color="#dbd5cd")
            self.producto_precio_compra.configure(state="disabled")

        self.producto_precio_compra.grid(row=6, column=0, sticky="ew", padx=10, pady=(0, 10))

        # Campo de entrada para Precio de venta
        label_producto_precio_venta = crear_label(formulario_frame, 
                                         metodo="grid", 
                                         text=" Precio de venta", 
                                         font=("Roboto", 18, "bold"), 
                                         image=crear_imagen("src/assets/icons/report-money.png", size=(22, 22)))
        label_producto_precio_venta.grid(row=5, column=1, sticky="w", pady=(10,0), padx=10)
        
        if procedencia != "tabla_lote":
            self.producto_precio_venta = crear_entry(formulario_frame, 
                                            placeholder_text="$", metodo="grid")
            
        else:
            self.producto_precio_venta = crear_entry(formulario_frame, 
                                            placeholder_text="Deshabilitado desde 'Editar Lote'", metodo="grid", fg_color="#dbd5cd")
            self.producto_precio_venta.configure(state="disabled")


        self.producto_precio_venta.grid(row=6, column=1, sticky="ew", padx=10, pady=(0, 10))

        # Campo de entrada para Cantidad
        label_producto_cantidad = crear_label(formulario_frame, 
                                     metodo="grid", 
                                     text=" Cantidad", 
                                     font=("Roboto", 18, "bold"), 
                                     image=crear_imagen("src/assets/icons/pencil.png", size=(22, 22)))
        label_producto_cantidad.grid(row=9, column=0, sticky="w", pady=(10,0), padx=10)

        if procedencia != "tabla_producto":
            self.producto_cantidad = crear_entry(formulario_frame, placeholder_text="0", metodo="grid")

        else:
            self.producto_cantidad = crear_entry(formulario_frame, placeholder_text="Deshabilitado desde 'Editar Producto'", metodo="grid", fg_color="#dbd5cd")
            self.producto_cantidad.configure(state="disabled")

        self.producto_cantidad.grid(row=10, column=0, sticky="ew", padx=10, pady=(0, 10))

        # Campo de entrada para Vencimiento
        label_producto_vencimiento = crear_label(formulario_frame, 
                                        metodo="grid", 
                                        text=" Vencimiento", 
                                        font=("Roboto", 18, "bold"), 
                                        image=crear_imagen("src/assets/icons/calendar.png", size=(22, 22)))
        label_producto_vencimiento.grid(row=9, column=1, sticky="w", pady=(10,0), padx=10)

        if procedencia != "tabla_producto":
            self.producto_vencimiento = crear_entry(formulario_frame, placeholder_text="DD/MM/AA", metodo="grid")
        else:
            self.producto_vencimiento = crear_entry(formulario_frame, placeholder_text="Deshabilitado desde 'Editar Producto'", metodo="grid", fg_color="#dbd5cd")
            self.producto_vencimiento.configure(state="disabled")


        self.producto_vencimiento.grid(row=10, column=1, sticky="ew", padx=10, pady=(0, 10))

        if procedencia == "inicio":
            # Botón de enviar
            boton_crear = crear_boton(formulario_frame, 
                                    metodo="grid",
                                    text="Crear", 
                                    command=self.enviar_producto_a_bd)
            boton_crear.grid(row=13, column=0, columnspan=2, pady=(20, 10), padx=10, sticky="ew")
        
        if procedencia == "tabla_producto":
            boton_editar = crear_boton(formulario_frame, 
                                    metodo="grid",
                                    text="Editar Producto", 
                                    command=lambda: self.editar_producto(procedencia, id_producto = valor[0]))
            boton_editar.grid(row=13, column=0, pady=(20, 10), padx=10, sticky="ew")

        if procedencia == "tabla_lote":
            boton_editar = crear_boton(formulario_frame, 
                                    metodo="grid",
                                    text="Editar Lote", 
                                    command=lambda: self.editar_lote(procedencia, id_producto = valor[0]))
            boton_editar.grid(row=13, column=0, pady=(20, 10), padx=10, sticky="ew")

        
        if procedencia in ("tabla_lote", "tabla_producto"):
            boton_volver = crear_boton(formulario_frame, 
                                    metodo="grid",
                                    text="Volver", command=self.frame_origen
                                    )
            boton_volver.grid(row=13, column=1, pady=(20, 10), padx=10, sticky="ew")

        # ------------- Datos previos -------------
        
        # Datos previos - Productos
        if procedencia == "tabla_producto":
            # Separador, línea horizontal
            separador = ttk.Separator(formulario_frame, orient='horizontal')
            separador.grid(row=14, column=0, columnspan=2, pady=(30, 10), sticky="ew")
            
            label_titulo = crear_label(formulario_frame, 
                                    metodo="grid", 
                                    text="Datos previos",  
                                    font=("Roboto", 24, "bold"))
            label_titulo.grid(row=15, column=0, columnspan=2, pady=(25, 10), sticky="ew")
            
            # Nombre
            label_nombre = crear_label(formulario_frame, 
                                metodo="grid", 
                                text=" Nombre del producto", 
                                font=("Roboto", 18, "bold"), 
                                image=crear_imagen("src/assets/icons/title.png", size=(22, 22)))
            label_nombre.grid(row=16, columnspan=2, sticky="ew", pady=(10,0), padx=10)
            
            
            info_nombre = crear_info(formulario_frame, text=f"{valor[1]}", metodo="grid")
            info_nombre.grid(row=17, columnspan=2, sticky="ew", pady=(0, 10), padx=10)
            
            # Marca
            label_marca = crear_label(formulario_frame, 
                                metodo="grid", 
                                text=" Marca", 
                                font=("Roboto", 18, "bold"), 
                                image=crear_imagen("src/assets/icons/description.png", size=(22, 22)))
            label_marca.grid(row=18, column=0, sticky="ew", pady=(10,0), padx=10)
            
            
            info_marca = crear_info(formulario_frame, text=f"{valor[2]}", metodo="grid")
            info_marca.grid(row=19, column=0, sticky="ew", pady=(0, 10), padx=10)
            
            # Categoria
            label_categoria = crear_label(formulario_frame, 
                                metodo="grid", 
                                text=" Categoría", 
                                font=("Roboto", 18, "bold"), 
                                image=crear_imagen("src/assets/icons/category.png", size=(22, 22)))
            label_categoria.grid(row=18, column=1, sticky="ew", pady=(10,0), padx=10)
            
            
            info_categoria = crear_info(formulario_frame, text=f"{valor[3]}", metodo="grid")
            info_categoria.grid(row=19, column=1, sticky="ew", pady=(0, 10), padx=10)
            
            # Precio compra
            label_precio_compra = crear_label(formulario_frame, 
                                metodo="grid", 
                                text=" Precio de compra", 
                                font=("Roboto", 18, "bold"), 
                                image=crear_imagen("src/assets/icons/currency-dollar.png", size=(22, 22)))
            label_precio_compra.grid(row=20, column=0, sticky="ew", pady=(10,0), padx=10)
            
            
            info_precio_venta = crear_info(formulario_frame, text=f"{valor[4]}", metodo="grid")
            info_precio_venta.grid(row=21, column=0, sticky="ew", pady=(0, 10), padx=10)
            
            # Precio venta
            label_precio_venta = crear_label(formulario_frame, 
                                metodo="grid", 
                                text=" Precio de venta", 
                                font=("Roboto", 18, "bold"), 
                                image=crear_imagen("src/assets/icons/report-money.png", size=(22, 22)))
            label_precio_venta.grid(row=20, column=1, sticky="ew", pady=(10,0), padx=10)
            
            
            info_precio_venta = crear_info(formulario_frame, text=f"{valor[5]}", metodo="grid")
            info_precio_venta.grid(row=21, column=1, sticky="ew", pady=(0, 10), padx=10)
            
            # Cantidad
            label_cantidad = crear_label(formulario_frame, 
                                metodo="grid", 
                                text=" Cantidad total", 
                                font=("Roboto", 18, "bold"), 
                                image=crear_imagen("src/assets/icons/pencil.png", size=(22, 22)))
            label_cantidad.grid(row=22, column=0, sticky="ew", pady=(10,0), padx=10)
            
            
            info_cantidad = crear_info(formulario_frame, text=f"{valor[6]}", metodo="grid")
            info_cantidad.grid(row=23, column=0, sticky="ew", pady=(0, 20), padx=10)
            
            # Vencimiento
            label_id = crear_label(formulario_frame, 
                                metodo="grid", 
                                text=" ID", 
                                font=("Roboto", 18, "bold"), 
                                image=crear_imagen("src/assets/icons/hash.png", size=(22, 22)))
            label_id.grid(row=22, column=1, sticky="ew", pady=(10,0), padx=10)
            
            info_id = crear_info(formulario_frame, text=f"{valor[0]}", metodo="grid")
            info_id.grid(row=23, column=1, sticky="ew", pady=(0, 20), padx=10)
            
        # Datos previos - Lotes
        if procedencia == "tabla_lote":
            # Separador, línea horizontal
            separador = ttk.Separator(formulario_frame, orient='horizontal')
            separador.grid(row=14, column=0, columnspan=2, pady=(30, 10), sticky="ew")
            
            label_titulo = crear_label(formulario_frame, 
                                    metodo="grid", 
                                    text="Datos previos",  
                                    font=("Roboto", 24, "bold"))
            label_titulo.grid(row=15, columnspan=2, pady=(25, 10), sticky="ew")
            
            # Nombre
            label_nombre = crear_label(formulario_frame, 
                                metodo="grid", 
                                text=" Nombre del producto", 
                                font=("Roboto", 18, "bold"), 
                                image=crear_imagen("src/assets/icons/title.png", size=(22, 22)))
            label_nombre.grid(row=16, columnspan=2, sticky="ew", pady=(10,0), padx=10)
            
            
            info_nombre = crear_info(formulario_frame, text=f"{valor[2]}", metodo="grid")
            info_nombre.grid(row=17, columnspan=2, sticky="ew", pady=(0, 10), padx=10)
            
            # Lote
            label_lote = crear_label(formulario_frame, 
                                metodo="grid", 
                                text=" Lote", 
                                font=("Roboto", 18, "bold"), 
                                image=crear_imagen("src/assets/icons/lote.png", size=(22, 22)))
            label_lote.grid(row=18, column=0, sticky="ew", pady=(10,0), padx=10)
            
            
            info_lote = crear_info(formulario_frame, text=f"{valor[0]}", metodo="grid")
            info_lote.grid(row=19, column=0, sticky="ew", pady=(0, 10), padx=10)
            
            # Marca
            label_marca = crear_label(formulario_frame, 
                                metodo="grid", 
                                text=" Marca", 
                                font=("Roboto", 18, "bold"), 
                                image=crear_imagen("src/assets/icons/description.png", size=(22, 22)))
            label_marca.grid(row=18, column=1, sticky="ew", pady=(10,0), padx=10)
            
            
            info_marca = crear_info(formulario_frame, text=f"{valor[3]}", metodo="grid")
            info_marca.grid(row=19, column=1, sticky="ew", pady=(0, 10), padx=10)
            
            # Cantidad
            label_cantidad = crear_label(formulario_frame, 
                                metodo="grid", 
                                text=" Cantidad",  
                                font=("Roboto", 18, "bold"), 
                                image=crear_imagen("src/assets/icons/pencil.png", size=(22, 22)))
            label_cantidad.grid(row=20, column=0, sticky="ew", pady=(10,0), padx=10)
            
            
            info_cantidad = crear_info(formulario_frame, text=f"{valor[4]}", metodo="grid")
            info_cantidad.grid(row=21, column=0, sticky="ew", pady=(0, 20), padx=10)
            
            # Vencimiento
            label_vencimiento = crear_label(formulario_frame, 
                                metodo="grid", 
                                text=" Vencimiento",  
                                font=("Roboto", 18, "bold"), 
                                image=crear_imagen("src/assets/icons/calendar.png", size=(22, 22)))
            label_vencimiento.grid(row=20, column=1, sticky="ew", pady=(10,0), padx=10)
            
            info_vencimiento = crear_info(formulario_frame, text=f"{valor[5]}", metodo="grid")
            info_vencimiento.grid(row=21, column=1, sticky="ew", pady=(0, 20), padx=10)
            
        
    def validar_y_convertir_fecha(self, fecha_ingresada):
        try:
            fecha = datetime.strptime(fecha_ingresada, "%d/%m/%Y")
        except ValueError:
            # Error, no se puede convertir porque se ingresó en formato dia/mes/24
            try:
                fecha = datetime.strptime(fecha_ingresada, "%d/%m/%y")

                # Transforma el año al formato AAAA
                if fecha.year % 100 == datetime.now().year % 100:
                    fecha = fecha.replace(year=datetime.now().year)
                    
            except ValueError:
                return None

        # Convertir a formato año/dia/mes
        fecha_formateada = fecha.strftime("%Y/%m/%d")
        return fecha_formateada
            
    def validar_precio(self, precio):
        try:
            # Reemplazar las comas por puntos decimales
            precio = precio.strip().replace(",", ".")
            if "." in precio:
                parte_entera, parte_decimal = precio.split('.') # Separamos entre la parte entera y parte decimal
                # Verificar que la parte decimal no tenga más de 2 dígitos
                if len(parte_decimal) > 2:
                    return False
            
            precio = float(precio)
            # Verificar que el precio no sea muy largo
            if precio > 0 and precio < 100000000:
                return precio
            
            return False
        except ValueError:
            return False

    def validar_cantidad(self, cantidad):
        try:
            cantidad = int(cantidad.strip())
            if cantidad > 0 and cantidad < 100000000:
                return cantidad  
            return False
        except ValueError:
            return False

    def validar_campo_agregar_producto(self, campo, message, max_length=21):
        
        if len(campo.get().strip()) == 0 or len(campo.get().strip()) > max_length:
            notificacion = CTkNotification(master=self.contenedor, state="warning", message=message, side="right_top")
            self.contenedor.after(3000, notificacion.destroy)
            return False
        return True

    def mostrar_notificacion(self, message, tipo="info"):
        notificacion = CTkNotification(master=self.contenedor, state=tipo, message=message, side="right_top")
        self.contenedor.after(3000, notificacion.destroy)

    def enviar_producto_a_bd(self):
        try:
            # Verificar todos los campos, para evitar errores del usuario al ingresar un nuevo producto
            if not self.validar_campo_agregar_producto(self.producto_nombre, "Nombre no válido o muy largo."):
                return

            if not self.validar_campo_agregar_producto(self.producto_marca, "Marca no válida o muy larga."):
                return
                
            if self.producto_categoria.get().strip() == "Elija o escriba una categoría" or len(self.producto_categoria.get().strip()) == 0 or len(self.producto_categoria.get().strip()) > 21:
                self.mostrar_notificacion("Categoría no válida o muy larga", tipo = "warning")
                return

            precio_compra = self.validar_precio(self.producto_precio_compra.get().strip())
            if not precio_compra or len(self.producto_precio_compra.get().strip()) == 0:
                self.mostrar_notificacion("Debes ingresar un precio de compra válido.", tipo = "warning")
                return

            precio_venta = self.validar_precio(self.producto_precio_venta.get().strip())
            if not precio_venta or len(self.producto_precio_venta.get().strip()) == 0:
                self.mostrar_notificacion("Debes ingresar un precio de venta válido.", tipo = "warning")
                return

            cantidad = self.validar_cantidad(self.producto_cantidad.get().strip())
            if not cantidad:
                self.mostrar_notificacion("Debes ingresar una cantidad válida.", tipo = "warning")
                return
            
            fecha_formateada = self.validar_y_convertir_fecha(self.producto_vencimiento.get())
            if not fecha_formateada:
                self.mostrar_notificacion("Debes ingresar una fecha válida.", tipo = "warning")
                
                return

            if self.productos_funciones.subir_producto_a_bd(self.producto_nombre.get(), self.producto_marca.get(), precio_compra, precio_venta, self.producto_categoria.get(), cantidad, fecha_formateada):
                self.mostrar_notificacion("Producto cargado correctamente.")
                self.limpiar_campos()
            
            else:
                self.mostrar_notificacion("Error al cargar el producto, intentelo nuevamente.")

        except Exception as e:
            print(f"Error en la bd: {e}")
        
    def editar_producto(self, procedencia, id_producto):
        try:
            campos_a_actualizar_producto = {}

            # Mensajes de error para los campos de editar producto
            if len(self.producto_nombre.get().strip()) != 0:
                if len(self.producto_nombre.get().strip()) > 21:
                    self.mostrar_notificacion("Nombre muy largo", tipo = "warning")
                    return
                campos_a_actualizar_producto['nombre'] = self.producto_nombre.get().strip()

            if len(self.producto_marca.get().strip()) != 0:
                if len(self.producto_marca.get().strip()) > 21:
                    self.mostrar_notificacion("Marca muy larga", tipo = "warning")
                    return
                campos_a_actualizar_producto['marca'] = self.producto_marca.get().strip()

            if len(self.producto_categoria.get().strip()) != 0:
                if self.producto_categoria.get().strip() != "Elija o escriba una categoría": 
                    if len(self.producto_categoria.get().strip()) > 21:
                        self.mostrar_notificacion("Categoria muy larga", tipo = "warning")
                        return
                    campos_a_actualizar_producto['categoria'] = self.producto_categoria.get().strip()

            if len(self.producto_precio_compra.get().strip()) != 0:
                precio_compra = self.validar_precio(self.producto_precio_compra.get().strip())
                
                if not precio_compra:
                    self.mostrar_notificacion("Debes ingresar un precio de compra válido", tipo = "warning")
                    return
                campos_a_actualizar_producto['precio_compra'] = precio_compra

            if len(self.producto_precio_venta.get().strip()) != 0:
                precio_venta = self.validar_precio(self.producto_precio_venta.get().strip())
                if not precio_venta:
                    self.mostrar_notificacion("Debes ingresar un precio de venta válido", tipo = "warning")
                    return
                campos_a_actualizar_producto['precio_venta'] = precio_venta

            if len(campos_a_actualizar_producto) == 0:
                self.mostrar_notificacion("Debes modificar un campo", tipo = "warning")

                campos_a_actualizar_producto = False
                return

            if campos_a_actualizar_producto:
                conexion = Database()

                partes_sql_producto = []

                # Actualización de la tabla "productos"
                if campos_a_actualizar_producto:
                    for campo in campos_a_actualizar_producto:
                        partes_sql_producto.append(f"{campo} = %s")  # Añadir todos los campos para el sql
                    
                    # Unir las partes y crear la consulta final para la tabla "productos"
                    campos_producto = ", ".join(partes_sql_producto)
                    valores_producto = list(campos_a_actualizar_producto.values())
                    valores_producto.append(id_producto)  # Agrega el ID del producto para la cláusula WHERE
                    
                    sql_producto = f"UPDATE productos SET {campos_producto} WHERE id = %s"
                    conexion.ejecutar_bd(sql_producto, valores_producto, "update")

                    self.mostrar_notificacion("Producto actualizado, redirigiendo...")
                    self.contenedor.after(1000, lambda: self.frame_origen())

            else:
                self.mostrar_notificacion("Debes ingresar al menos un campo para modificar")

        except Exception as e:
            print(f"Error en la bd: {e}")
        
    def editar_lote(self, procedencia, id_producto):
        try:
            campos_a_actualizar_lote = {}

            # Verificar que los campos ingresados sean válidos al editar lote
            if len(self.producto_cantidad.get().strip()) != 0:
                cantidad = self.validar_cantidad(self.producto_cantidad.get().strip())
                if not cantidad:
                    self.mostrar_notificacion("Debes ingresar una cantidad válida", tipo = "warning")
                    return
                campos_a_actualizar_lote['cantidad'] = cantidad

            if len(self.producto_vencimiento.get().strip()) != 0:
                fecha_formateada = self.validar_y_convertir_fecha(self.producto_vencimiento.get())
                if not fecha_formateada:
                    self.mostrar_notificacion("Debes ingresar una fecha válida", tipo = "warning")

                    return
                campos_a_actualizar_lote['fecha_vencimiento'] = fecha_formateada

            if len(campos_a_actualizar_lote) == 0:
                self.mostrar_notificacion("Debes modificar un campo", tipo = "warning")
                campos_a_actualizar_lote = False
                return

            # Actualizar en la bd los campos ingresados
            if campos_a_actualizar_lote:
                conexion = Database()

                partes_sql_lote = []

                # Actualización de la tabla "lotes"
                if campos_a_actualizar_lote:
                    for campo in campos_a_actualizar_lote:
                        partes_sql_lote.append(f"{campo} = %s") 
                    
                    campos_lote = ", ".join(partes_sql_lote)
                    valores_lote = list(campos_a_actualizar_lote.values())
                    valores_lote.append(id_producto)  
                    
                    sql_lote = f"UPDATE lotes SET {campos_lote} WHERE lote = %s"
                    conexion.ejecutar_bd(sql_lote, valores_lote, "update")

                    self.mostrar_notificacion("Lote actualizado, redirigiendo...")
                    self.contenedor.after(1000, lambda: self.frame_origen())
                    
            else:
                self.mostrar_notificacion("Debes ingresar al menos un campo a modificar")

        except Exception as e:
            print(f"Error en la bd: {e}")

    def limpiar_campos(self):
        # Restablece los campos del formulario
        self.producto_nombre.delete(0, 'end')
        self.producto_marca.delete(0, 'end')
        self.producto_categoria.set("Elija o escriba una categoría")
        self.producto_precio_compra.delete(0, 'end')
        self.producto_precio_venta.delete(0, 'end')
        self.producto_cantidad.delete(0, 'end')
        self.producto_vencimiento.delete(0, 'end')