from config.config import *
from gui.componentes import *
from core.productos import *


class Vencimientos:
    def __init__(self, contenedor):
        self.contenedor = contenedor
        self.fecha_actual = datetime.now().date()

        frame_vencimientos = ctk.CTkFrame(self.contenedor, fg_color=COLOR_BG)
        frame_vencimientos.pack(expand=True, fill="x", padx=60)

        # Título
        crear_label(
            frame_vencimientos,
            text="Vencimientos",
            font=("Roboto", 32, "bold"),
            pady=25,
        )

        # Contadores de productos
        frame_contadores = ctk.CTkFrame(frame_vencimientos, fg_color=COLOR_BG)
        frame_contadores.pack(fill="x", pady=(0,20))

        self.contador_vencidos = crear_stat(frame_contadores, "Productos vencidos", "0")
        self.contador_proximos = crear_stat(
            frame_contadores, "Próximos a vencer", "0", padx=10
        )
        self.contador_perdidas = crear_stat(frame_contadores, "Pérdidas", "$0.00")

        crear_label(
            frame_vencimientos,
            text="Productos",
            font=("Roboto", 24, "bold"),
            pady=(20, 0),
        )
        # Búsqueda y filtro
        frame_busqueda = ctk.CTkFrame(frame_vencimientos, fg_color=COLOR_BG)
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
            metodo="pack",
            command=self.evento_buscar,
        )
        boton_buscar.pack(side="right")

        # Dropdown de filtro para seleccionar vencidos o próximos a vencer
        self.filtro_vencimiento = crear_dropdown(
            parent=frame_busqueda,
            values=["Todos", "Próximos a vencer", "Vencidos"],
            pady=0,
            padx=15,
        )

        self.filtro_vencimiento.pack(side="left")

        # Crear las columnas y encabezados
        columnas = (
            "lote",
            "nombre",
            "marca",
            "categoria",
            "precio_compra",
            "precio_venta",
            "cantidad",
            "vencimiento",
        )
        encabezados = [
            "Lote",
            "Nombre",
            "Marca",
            "Categoría",
            "Precio compra",
            "Precio venta",
            "Cantidad",
            "Vencimiento",
        ]

        # Obtenemos los productos y lotes combinados
        lotes = Database()

        self.lotes = lotes.consultar_bd(
            sql="""
                    SELECT 
                        lotes.nombre, 
                        productos.nombre, 
                        productos.marca, 
                        productos.categoria, 
                        productos.precio_compra, 
                        productos.precio_venta, 
                        lotes.cantidad, 
                        lotes.fecha_vencimiento 
                    FROM 
                        lotes
                    JOIN 
                        productos ON lotes.producto_id = productos.id;
                """,
            valores=None,
        )

        self.frame_tabla, self.tree = crear_tabla(
            frame_vencimientos, columnas, encabezados, self.lotes
        )

        self.tree.tag_configure("vencido", background="tomato")
        self.tree.tag_configure("proximo", background="yellow")

        # Aplicar filtro inicial
        self.filtrar(False)

    # Obtener productos con vencimiento a un mes o vencidos
    def obtener_vencimientos(self, busqueda):
        fecha_limite = self.fecha_actual + timedelta(days=30)

        productos_vencidos = []
        proximo_vencimiento = []

        if busqueda is None:
            return productos_vencidos, proximo_vencimiento

        if busqueda is False:
            for producto in self.lotes:
                fecha_vencimiento = producto[7]

                if fecha_vencimiento < self.fecha_actual:
                    productos_vencidos.append(producto)

                elif fecha_vencimiento > fecha_limite:
                    proximo_vencimiento.append(producto)

        else:
            for producto in busqueda:
                # Si el usuario ingresa algo en el buscador se itera ahí
                fecha_vencimiento = producto[7]
                if fecha_vencimiento < self.fecha_actual:
                    productos_vencidos.append(producto)

                elif fecha_vencimiento > fecha_limite:
                    proximo_vencimiento.append(producto)

        return productos_vencidos, proximo_vencimiento

    # Filtrar según un criterio
    def filtrar(self, busqueda):
        fecha_limite = self.fecha_actual + timedelta(days=30)

        # Limpiar la tabla antes de aplicar el filtro
        for item in self.tree.get_children():
            self.tree.delete(item)

        productos_vencidos, proximo_vencimiento = self.obtener_vencimientos(busqueda)

        if not productos_vencidos and not proximo_vencimiento:
            # Añadir mensaje para tabla vacía
            return

        else:
            if (
                self.filtro_vencimiento.get() == "Próximos a vencer"
                or self.filtro_vencimiento.get() == "Todos"
            ):
                for proximo_a_vencer in proximo_vencimiento:
                    self.tree.insert(
                        "", tk.END, values=proximo_a_vencer, tags=("proximo",)
                    )

            if (
                self.filtro_vencimiento.get() == "Vencidos"
                or self.filtro_vencimiento.get() == "Todos"
            ):
                for producto_vencido in productos_vencidos:
                    self.tree.insert(
                        "", tk.END, values=producto_vencido, tags=("vencido",)
                    )

        ajustar_altura_tabla(self.tree, len(self.tree.get_children()))

    # Click en "Buscar" activa el filtrado o busca lo ingresado en el Entry
    def evento_buscar(self):
        # Implementar la logica de busqueda
        if len(self.entry_busqueda.get().strip()) == 0:
            self.filtrar(False)
            return

        busqueda = Database()
        busqueda = busqueda.consultar_bd(
            sql="""
            SELECT 
                lotes.nombre, 
                productos.nombre,
                productos.marca, 
                productos.categoria, 
                productos.precio_compra, 
                productos.precio_venta, 
                lotes.cantidad, 
                lotes.fecha_vencimiento 
            FROM 
                lotes
            JOIN 
                productos ON lotes.producto_id = productos.id
            WHERE 
                productos.nombre LIKE %s 
                OR productos.marca LIKE %s 
                OR productos.categoria LIKE %s
        """,
            valores=("%" + self.entry_busqueda.get().strip() + "%",) * 3,
        )

        self.filtrar(busqueda)