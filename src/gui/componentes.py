from config.config import *
from core.productos import *

def crear_boton(
    parent, text, command=None, fill="none", fg_color=COLOR_PRIMARIO, font=("Roboto", 16, "bold"), padx=50, width=350, pady=20, metodo="pack", **kwargs,
):
    boton = ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=width,
        height=45,
        corner_radius=8,
        font=font,
        compound="left",
        fg_color=fg_color,
        hover_color=COLOR_PRIMARIO_HOVER,
        **kwargs,
    )
    
    if metodo == "grid":
        pass
    else:
        boton.pack(pady=pady, padx=padx, fill=fill,)

    return boton


def crear_boton_sideframe(parent, text, command=None, pady=5, selected=False, **kwargs):
    boton = ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=210,
        height=40,
        corner_radius=8,
        font=("Roboto", 15, "bold"),
        hover=False,
        compound="left",
        fg_color=COLOR_PRIMARIO_HOVER if selected else COLOR_PRIMARIO,
        text_color=COLOR_BG,
        anchor="w",
        **kwargs,
    )
    boton.pack(pady=pady, padx=30, fill="x")

    return boton


def crear_imagen(route, size=(20, 20)):
    return ctk.CTkImage(Image.open(route), size=size)


def crear_entry(
    parent, metodo="pack", placeholder_text="", padx=0, fill="none", pady=10, **kwargs
):
    entry = ctk.CTkEntry(
        parent,
        placeholder_text=placeholder_text,
        height=45,
        corner_radius=8,
        font=("Roboto", 14),
        border_color=COLOR_PRIMARIO,
        **kwargs,
    )
    
    if metodo == "grid":
        pass
    else:
        entry.pack(pady=pady, padx=padx, fill=fill)

    return entry


def crear_label(parent, metodo="pack", text="", pady=10, anchor="w", padx=0, text_color=COLOR_PRIMARIO, font=("Roboto", 14), **kwargs):
    label = ctk.CTkLabel(
        parent,
        text=text,
        height=40,
        wraplength=500,
        anchor=anchor,
        corner_radius=8,
        font=font,
        text_color=text_color,
        compound="left",
        **kwargs,
    )
    
    if metodo == "grid":
        pass
    else:
        label.pack(pady=pady, padx=padx, fill="x")

    return label


def crear_stat(parent, titulo, contador, padx=0, image=None, **kwargs):
    label_stat = ctk.CTkLabel(
        parent,
        text=f"{titulo} | {contador}",
        height=40,
        width=150,
        anchor="center",
        compound="left",
        corner_radius=8,
        font=("Roboto", 18, "bold"),
        text_color=COLOR_BG,
        fg_color=COLOR_PRIMARIO,
        image=image,
    )
    label_stat.pack(side="left", expand=True, fill="x", padx=padx, pady=0, ipady=20, ipadx=0)

    return label_stat

def crear_info(parent, text, command=None, fill="none", padx=50, width=350, pady=20, metodo="pack", **kwargs):
        info = ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=width,
        height=45,
        corner_radius=8,
        font=("Roboto", 15),
        fg_color="white",
        hover=False,
        border_width=2,
        border_color=COLOR_PRIMARIO,
        text_color="black",
    )
    
        if metodo == "grid":
            pass
        else:
            info.pack(pady=pady, padx=padx, fill=fill)

        return info

def crear_dropdown(parent, values=[], metodo="pack", pady=10, padx=0, width=200, **kwargs):
    dropdown = ctk.CTkComboBox(
            parent,
            height=45,
            width=width,
            corner_radius=8,
            font=("Roboto", 14),
            border_color=COLOR_PRIMARIO,
            button_color=COLOR_PRIMARIO,
            button_hover_color=COLOR_PRIMARIO_HOVER,
            dropdown_fg_color=COLOR_BG,
            dropdown_hover_color=COLOR_PRIMARIO,
            values=values,
        )
    
    if metodo == "grid":
        pass
    else:
        dropdown.pack(pady=pady, padx=padx, fill="x")
    
    return dropdown

def crear_optionmenu(parent, values=[], pady=10, padx=0, width=200, metodo="pack", **kwargs):
    dropdown = ctk.CTkOptionMenu(
            parent,
            height=45,
            width=width,
            corner_radius=8,
            font=("Roboto", 14),
            fg_color=COLOR_PRIMARIO,
            button_color=COLOR_PRIMARIO_HOVER,
            values=values,
            dropdown_fg_color=COLOR_BG,
            dropdown_hover_color=COLOR_PRIMARIO,
        )

    if metodo == "grid":
        pass
    else:
        dropdown.pack(pady=pady, padx=padx, fill="x")
    
    return dropdown

def crear_tabla(parent, columnas, encabezados, lotes, pady=20, menu = None, frame_origen = None):
    configurar_estilo_tabla()

    # Frame de la tabla
    frame_tabla = ctk.CTkFrame(parent, fg_color=COLOR_BG)
    frame_tabla.pack(fill="both", padx=0, pady=pady)

    # Crear el Treeview
    tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", style="Treeview")

    # Configuración de encabezados
    for col, encabezado in zip(columnas, encabezados):
        tree.heading(col, text=encabezado)
        
        # Ajuste de ancho de columnas
        if col in ("lote", "id"):
            width = 40
        elif col == "cantidad":
            width = 80
        elif col == "nombre":
            width = 140
        else:
            width = 120
        
        tree.column(col, anchor="center", width=width, minwidth=width)
   
    for lote in lotes:
        tree.insert("", tk.END, values=lote)

    # Scrollbar
    scrollbar = ctk.CTkScrollbar(frame_tabla, 
                                 orientation="vertical", 
                                 command=tree.yview, 
                                 button_color=COLOR_PRIMARIO, 
                                 button_hover_color=COLOR_PRIMARIO_HOVER)
    
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Desactivar ajuste de ancho de columnas
    tree.bind('<Motion>', 'break')

    tree.pack(fill="both", expand=True)
    ajustar_altura_tabla(tree, len(lotes))

    # Crear el menú contextual
    menu_contextual = Menu(tree, tearoff=0, 
                           background="white", 
                           borderwidth=0, 
                           font=("Roboto", 10), 
                           selectcolor=COLOR_PRIMARIO_HOVER, 
                           activebackground=COLOR_PRIMARIO_HOVER,
                           activeborderwidth=0,
                           )
    
    if menu == "productos":
        menu_contextual.add_command(label="Agregar al carrito", command=lambda: MenuTablas().agregar_a_carrito(tree))
        menu_contextual.add_command(label="Editar Producto", command=lambda: MenuTablas(parent).editar_producto(tree, frame_origen))
        menu_contextual.add_command(label="Eliminar producto", command=lambda: MenuTablas().eliminar_producto(tree, frame_tabla))
    
    if menu == "lotes":
        menu_contextual.add_command(label="Editar Lote", command=lambda: MenuTablas(parent).editar_lote(tree, frame_origen))
        menu_contextual.add_command(label="Eliminar lote", command=lambda: MenuTablas().eliminar_lote(tree, frame_tabla))
        
    
    # Función para mostrar el menú en clic derecho
    def mostrar_menu(event):
        item = tree.identify_row(event.y)
        if item:
            tree.selection_set(item)  # Selecciona la fila donde se hizo clic derecho
            menu_contextual.post(event.x_root, event.y_root)  # Muestra el menú en la posición del cursor

    # Asociar el menú de clic derecho
    tree.bind("<Button-3>", mostrar_menu)

    return frame_tabla, tree

def configurar_estilo_tabla():
    style = ttk.Style()
    style.theme_use("default")

    style.configure("Treeview.Heading", 
                    background=COLOR_PRIMARIO,
                    font=("Roboto", 11, "bold"),
                    foreground="white",
                    relief="flat",
                    padding=5,
                    )
    style.map("Treeview.Heading",
                background=[('active', COLOR_PRIMARIO_HOVER)])

    style.configure("Treeview", 
                    background="white",
                    fieldbackground=COLOR_BG,
                    foreground="black",
                    rowheight=35,
                    borderwidth=0) 
    style.map("Treeview",
                background=[('selected', COLOR_PRIMARIO_HOVER)])


class MenuTablas:    
    def __init__(self, frame = None):
        self.db = Database()
        self.frame = frame
        

    def agregar_a_carrito(self, tree):
        item = tree.selection()[0]
        valores = tree.item(item, "values")
        # Código para agregar el producto al carrito, FALTA

        CTkAlert(
            state="info",
            title="Agregar al producto",
            body_text=f"Producto {valores[1]} agregado.",
            btn1="Ok",
        )

    def editar_producto(self, tree, frame_origen):
        item = tree.selection()[0]
        valores = tree.item(item, "values")  # obtiene los valores de la fila

        # Eliminar todos los elementos que están en pantalla
        for elemento in self.frame.winfo_children():
            elemento.destroy()

        from gui.agregar_producto import CrearProducto
        CrearProducto(contenedor = self.frame, frame_origen = frame_origen, procedencia = "tabla_producto", valor = valores)
        
    def editar_lote(self, tree, frame_origen):
        item = tree.selection()[0]
        valores = tree.item(item, "values") 
    
        # Eliminar todos los elementos que están en pantalla
        for elemento in self.frame.winfo_children():
            elemento.destroy()

        from gui.agregar_producto import CrearProducto
        CrearProducto(contenedor = self.frame, frame_origen = frame_origen, procedencia = "tabla_lote", valor = valores)

    def eliminar_producto(self, tree, frame):
        item = tree.selection()[0]
        valores = tree.item(item, "values")  # Obtiene los valores de la fila
        producto_id = valores[0]
        
        respuesta = CTkAlert(
            state="warning",
            title="Eliminar producto",
            body_text=f"¿Desea eliminar el producto '{valores[1]}'? Esta acción no se puede deshacer.",
            btn1="Eliminar",
            btn2="Cancelar",
        )

        if respuesta.get() == "Eliminar":
            try:
                # Eliminar lotes asociados al producto
                self.db.ejecutar_bd(
                    "DELETE FROM lotes WHERE producto_id = %s",
                    (producto_id,),
                    tipo="delete"
                )
                # Eliminar producto
                self.db.ejecutar_bd(
                    "DELETE FROM productos WHERE id = %s",
                    (producto_id,),
                    tipo="delete"
                )

                # Eliminar la fila en la interfaz
                tree.delete(item)

                notificacion = CTkNotification(
                    master=frame, 
                    state="info", 
                    message=f"'{valores[1]}' eliminado.", 
                    side="right_bottom"
                )
                frame.after(3000, notificacion.destroy)
                
            except Exception as error:
                print(f"Error al eliminar producto: {error}")
    
    
    def eliminar_lote(self, tree, frame):
        item = tree.selection()[0]
        valores = tree.item(item, "values")
        
        lote = valores[0]
        producto_id = valores[1]

        # Confirmación antes de eliminar
        respuesta = CTkAlert(
            state="warning",
            title="Eliminar lote",
            body_text=f"¿Desea eliminar el lote {valores[0]} de '{valores[2]}'? Esta acción no se puede deshacer.",
            btn1="Eliminar",
            btn2="Cancelar",
        )

        if respuesta.get() == "Eliminar":
            try:
                # Eliminar lote de la base de datos
                self.db.ejecutar_bd(
                    "DELETE FROM lotes WHERE lote = %s",
                    (lote,),
                    tipo="delete"
                )
                
                # Verificar si el producto tiene otros lotes asociados
                resultado = self.db.ejecutar_bd(
                    "SELECT COUNT(*) FROM lotes WHERE producto_id = %s",
                    (producto_id,),
                    tipo="select"
                )

                # Si no hay más lotes, eliminar el producto
                if resultado[0][0] == 0:
                    self.db.ejecutar_bd(
                        "DELETE FROM productos WHERE id = %s",
                        (producto_id,),
                        tipo="delete"
                    )

                # Eliminar la fila en la interfaz
                tree.delete(item)

                notificacion = CTkNotification(
                    master=frame, 
                    state="info", 
                    message=f"Lote {valores[0]} de '{valores[2]}' eliminado.", 
                    side="right_bottom"
                )
                frame.after(3000, notificacion.destroy)
                
            except Exception as error:
                print(f"Error al eliminar lote: {error}")
