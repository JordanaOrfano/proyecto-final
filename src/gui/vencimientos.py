from config.config import *
from gui.componentes import *

class Vencimientos:
    def __init__(self, contenedor):
        self.contenedor = contenedor

        # Frame principal
        frame_bg = ctk.CTkFrame(master=self.contenedor, fg_color=COLOR_BG)
        frame_bg.pack(expand=True, fill="both", padx=0)

        frame_vencimientos = ctk.CTkFrame(frame_bg, fg_color=COLOR_BG)
        frame_vencimientos.pack(expand=True, fill="x", padx=60)

        # Título
        crear_label(
            frame_vencimientos,
            text="Vencimientos",
            font=("Roboto", 32, "bold"),
            pady=(0, 25)
        )
        
        # Contadores de productos
        frame_contadores = ctk.CTkFrame(frame_vencimientos, fg_color=COLOR_BG)
        frame_contadores.pack(fill="x", pady=(0,20))

        self.contador_vencidos = crear_stat(frame_contadores, "Productos vencidos", "0")
        self.contador_proximos = crear_stat(frame_contadores, "Próximos a vencer", "0", padx=10)
        self.contador_perdidas = crear_stat(frame_contadores, "Pérdidas", "$0.00")

        crear_label(
            frame_vencimientos,
            text="Productos",
            font=("Roboto", 24, "bold"),
            pady=(20,0)
        )
        # Búsqueda y filtro
        frame_busqueda = ctk.CTkFrame(frame_vencimientos, fg_color=COLOR_BG)
        frame_busqueda.pack(fill="x", pady=(10,0))

        entry_busqueda = crear_entry(
            parent=frame_busqueda,
            placeholder_text="Buscar por nombre, marca o categoría",
            fill="x",
            padx=0,
            pady=0,
            metodo="pack"
        )
        entry_busqueda.pack(side="left", expand=True, fill="x")

        boton_buscar = crear_boton(
            parent=frame_busqueda,
            text="Buscar",
            width=100,
            padx=0,
            pady=0,
            metodo="pack"
        )
        boton_buscar.pack(side="right")

        # Dropdown de filtro para seleccionar vencidos o próximos a vencer
        filtro_vencimiento = crear_dropdown(
            parent=frame_busqueda,
            values=["Todos", "Próximos a vencer", "Vencidos"],
            pady=0,
            padx=15,
        )
        filtro_vencimiento.pack(side="left")
        filtro_vencimiento.bind("<<ComboboxSelected>>", lambda event: self.filtrar_por_fecha(filtro_vencimiento.get()))

        # Datos de ejemplo
        self.datos = [
            (1, "Producto 1", "Marca A", "Categoría A", "$10.00", "$15.00", "100", "2024-11-03"),
            (2, "Producto 2", "Marca B", "Categoría B", "$20.00", "$30.00", "50", "2024-10-20"),
            (3, "Producto 3", "Marca C", "Categoría C", "$15.00", "$25.00", "70", "2024-12-01"),
            (4, "Producto 4", "Marca D", "Categoría D", "$12.00", "$18.00", "30", "2025-12-26"),
            (5, "Producto 5", "Marca E", "Categoría E", "$16.00", "$18.00", "30", "2024-11-26"),
        ]
        
        # Crear la tabla
        columnas = ("lote", "nombre", "marca", "categoria", "precio_compra", "precio_venta", "cantidad", "vencimiento")
        encabezados = ["Lote", "Nombre", "Marca", "Categoría", "Precio compra", "Precio venta", "Cantidad", "Vencimiento"]
        self.frame_tabla, self.tree = crear_tabla(frame_vencimientos, columnas, encabezados, self.datos)

        # Aplicar filtro inicial
        self.filtrar_por_fecha("Todos")

        # Actualizar contadores iniciales
        self.actualizar_contadores()

    def actualizar_contadores(self):
        vencidos = 0
        proximos = 0
        perdidas = 0.0
        fecha_actual = datetime.now().date()

        for dato in self.datos:
            lote, nombre, marca, categoria, precio_compra, precio_venta, cantidad, fecha_vencimiento_str = dato
            fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, "%Y-%m-%d").date()
            precio_compra = float(precio_compra.replace("$", ""))
            cantidad = int(cantidad)

            if fecha_vencimiento < fecha_actual:
                vencidos += 1
                perdidas += precio_compra * cantidad
            elif (fecha_vencimiento - fecha_actual).days <= 30:
                proximos += 1

        self.contador_vencidos.configure(text=f"Productos vencidos\n{vencidos}")
        self.contador_proximos.configure(text=f"Próximos a vencer\n{proximos}")
        self.contador_perdidas.configure(text=f"Pérdidas\n${perdidas:.2f}")

    def filtrar_por_fecha(self, filtro):
        fecha_actual = datetime.now().date()
        fecha_limite = fecha_actual + timedelta(days=30)

        # Limpiar la tabla antes de aplicar el filtro
        for item in self.tree.get_children():
            self.tree.delete(item)

        for dato in self.datos:
            lote, nombre, marca, categoria, precio_compra, precio_venta, cantidad, fecha_vencimiento_str = dato
            fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, "%Y-%m-%d").date()

            # Asegurarnos de que solo se muestren productos con fecha de vencimiento dentro de los próximos 30 días o vencidos
            if fecha_vencimiento > fecha_limite:
                continue  # Saltar productos con vencimiento mayor a 30 días

            # Determinar si el producto debe mostrarse según el filtro
            mostrar = False
            if filtro == "Todos":
                mostrar = True
            elif filtro == "Vencidos" and fecha_vencimiento < fecha_actual:
                mostrar = True
            elif filtro == "Próximos a vencer (1 mes)" and fecha_actual <= fecha_vencimiento <= fecha_limite:
                mostrar = True

            if mostrar:
                tag = "vencido" if fecha_vencimiento < fecha_actual else "proximo"
                self.tree.insert("", tk.END, values=dato, tags=(tag,))

        # Ajuste de estilo para vencidos y próximos a vencer
        self.tree.tag_configure("vencido", background="tomato")
        self.tree.tag_configure("proximo", background="white")

        # Ajustar la altura de la tabla después de aplicar el filtro
        ajustar_altura_tabla(self.tree, len(self.tree.get_children()))