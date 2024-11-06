import customtkinter as ctk
from config.config import *
from PIL import Image


def crear_boton(
    parent, text, command=None, fill="none", padx=50, width=350, pady=20, metodo="grid", **kwargs,
):
    boton = ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=width,
        height=45,
        corner_radius=8,
        font=("Roboto", 16, "bold"),
        compound="right",
        fg_color=COLOR_PRIMARIO,
        hover_color=COLOR_PRIMARIO_HOVER,
        **kwargs,
    )
    
    if metodo == "grid":
        pass
    else:
        boton.pack(pady=pady, padx=padx, fill=fill
        )

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
    parent, metodo="grid", placeholder_text="", padx=0, fill="none", pady=10, **kwargs
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


def crear_stat(parent, titulo, contador, padx=0, **kwargs):
    label_stat = ctk.CTkLabel(
        parent,
        text=f"{titulo}\n{contador}",
        height=40,
        width=150,
        anchor="center",
        compound="left",
        corner_radius=8,
        font=("Roboto", 18, "bold"),
        text_color=COLOR_BG,
        fg_color=COLOR_PRIMARIO,
    )
    label_stat.pack(side="left", expand=True, fill="x", padx=padx, pady=0, ipady=20, ipadx=20)

    return label_stat

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
            values=values,
        )
    
    if metodo == "grid":
        pass
    else:
        dropdown.pack(pady=pady, padx=padx, fill="x")
    
    return dropdown

def crear_tabla(parent, columnas, encabezados, datos):
    configurar_estilo_tabla()

    # Frame de la tabla
    frame_tabla = ctk.CTkFrame(parent, fg_color=COLOR_BG)
    frame_tabla.pack(fill="both", padx=0, pady=20)

    # Crear el Treeview
    tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", style="Treeview")

    # Configuración de encabezados
    for col, encabezado in zip(columnas, encabezados):
        tree.heading(col, text=encabezado)
        width = 50 if col == "lote" else 80 if col == "cantidad" else 120  # Ajuste de ancho
        tree.column(col, anchor="center", width=width, minwidth=width)

    # Insertar datos
    for dato in datos:
        tree.insert("", tk.END, values=dato)

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
    ajustar_altura_tabla(tree, len(datos))

    return frame_tabla, tree


def ajustar_altura_tabla(tree, cantidad_productos):
    max_filas = 10  # Establecer un límite máximo para la altura
    if cantidad_productos == 0:
        tree.configure(height=1)  # Si no hay productos, mostrar solo una fila
    else:
        tree.configure(height=min(max_filas, cantidad_productos))  # Ajustar según la cantidad de productos

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
                    borderwidth=0)  # No border for Treeview
    style.map("Treeview",
                background=[('selected', COLOR_PRIMARIO_HOVER)])
