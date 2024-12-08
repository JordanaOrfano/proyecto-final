from config.config import *
from gui.componentes import *
from core.productos import *


class Vencimientos:
    def __init__(self, contenedor):
        self.contenedor = contenedor
        self.fecha_actual = datetime.now().date()
        self.fecha_limite = self.fecha_actual + timedelta(days=30)
        self.productos = Productos()
        

        frame_vencimientos = ctk.CTkFrame(self.contenedor, fg_color=COLOR_BG)
        frame_vencimientos.pack(expand=True, fill="x", padx=40)

        # Título
        crear_label(
            frame_vencimientos,
            text="Vencimientos",
            font=("Roboto", 32, "bold"),
            pady=(10, 25),
        )

        # Contadores de productos
        frame_contadores = ctk.CTkFrame(frame_vencimientos, fg_color=COLOR_BG)
        frame_contadores.pack(fill="x", pady=(0, 20))

        self.contador_vencidos = crear_stat(frame_contadores, " Productos vencidos", "0", image=crear_imagen("src/assets/icons/alarm.png", size=(40, 40)))
        self.contador_proximos = crear_stat(frame_contadores, " Próximos a vencer", "0", padx=10, image=crear_imagen("src/assets/icons/calendar-exclamation.png", size=(40, 40)))
        self.contador_perdidas = crear_stat(frame_contadores, " Pérdidas", "$0.00", image=crear_imagen("src/assets/icons/cash-off.png", size=(40, 40)))

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
        self.filtro_vencimiento = crear_optionmenu(
            parent=frame_busqueda,
            values=["Todos", "Próximos a vencer", "Vencidos"],
            pady=0,
            padx=15,
        )

        self.filtro_vencimiento.pack(side="left")

        # Crear las columnas y encabezados
        columnas = [
            "lote",
            "nombre",
            "marca",
            "categoria",
            "precio_compra",
            "precio_venta",
            "cantidad",
            "vencimiento",
        ]
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
        self.conexion = Database()
        # lotes = self.conexion.ejecutar_bd(
        #     sql="""
        #             SELECT 
        #                 lotes.lote, 
        #                 productos.nombre, 
        #                 productos.marca, 
        #                 productos.categoria, 
        #                 productos.precio_compra, 
        #                 productos.precio_venta, 
        #                 lotes.cantidad, 
        #                 lotes.fecha_vencimiento 
        #             FROM 
        #                 lotes
        #             JOIN 
        #                 productos ON lotes.producto_id = productos.id
        #             ORDER BY productos.nombre, lotes.fecha_vencimiento;
        #         """,
        #     valores=None,
        # )

        lotes = self.conexion.ejecutar_bd(
        sql="""
            SELECT 
                lotes.lote, 
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
                productos.mostrar = 1 AND lotes.cantidad > 0
            ORDER BY 
                productos.nombre, lotes.fecha_vencimiento;
        """,
        valores=None,
        )


        # Transformamos a una lista
        lotes_lista = []

        for fila in lotes:
            lotes_lista.append(list(fila))

        self.lotes = lotes_lista

        self.frame_tabla, self.tree = crear_tabla(
            frame_vencimientos, columnas, encabezados, self.lotes
        )

        self.tree.tag_configure("vencido", background="tomato")
        self.tree.tag_configure("proximo", background="#FFEAAE")

        # Actualizar contadores
        self.actualizar_contadores()

        # Aplicar filtro inicial
        self.filtrar(False)

    # Obtener productos con vencimiento a un mes o vencidos
    def obtener_vencimientos(self, busqueda):
        productos_vencidos = []
        proximo_vencimiento = []

        def formatear_fecha(fecha_vencimiento):
            # Comprobar si es un datetime
            if isinstance(fecha_vencimiento, str):
                fecha_objeto = datetime.strptime(fecha_vencimiento, "%d/%m/%Y").date()
            elif isinstance(fecha_vencimiento, datetime):
                fecha_objeto = fecha_vencimiento.date()
            else:
                fecha_objeto = fecha_vencimiento

            return fecha_objeto

        # No encuentra ningun producto que coincida con la búsqueda
        if busqueda is None:
            return productos_vencidos, proximo_vencimiento

        # No procesa la búsqueda porque el Entry está vacío
        if busqueda is False:
            for producto in self.lotes:
                fecha_vencimiento = producto[7]
                fecha_objeto = formatear_fecha(fecha_vencimiento)

                fecha_formateada = fecha_objeto.strftime("%d/%m/%Y")
                producto[7] = fecha_formateada

                # Si la fecha es anterior a la fecha actual, está vencido
                if fecha_objeto < self.fecha_actual:
                    productos_vencidos.append(producto)

                # Si la fecha es mayor que la fecha límite, es un próximo vencimiento
                elif self.fecha_actual <= fecha_objeto <= self.fecha_limite:
                    proximo_vencimiento.append(producto)

        else:

            busqueda_lista = []
            for fila in busqueda:
                busqueda_lista.append(list(fila))

            for producto in busqueda_lista:
                fecha_vencimiento = producto[7]
                fecha_objeto = formatear_fecha(fecha_vencimiento)

                fecha_formateada = fecha_objeto.strftime("%d/%m/%Y")
                producto[7] = fecha_formateada

                if fecha_objeto < self.fecha_actual:
                    productos_vencidos.append(producto)

                # si fecha_objeto es menor a fecha_limite y mayor a fecha_actual
                elif fecha_objeto <= self.fecha_limite and fecha_objeto >= self.fecha_actual:
                    proximo_vencimiento.append(producto)

        return productos_vencidos, proximo_vencimiento

    def actualizar_contadores(self):
        # perdidas = self.conexion.ejecutar_bd(
        #     """
        # SELECT SUM(productos.precio_compra * lotes.cantidad) AS perdidas
        # FROM 
        #     lotes 
        # JOIN 
        #     productos ON lotes.producto_id = productos.id
        # WHERE 
        #     lotes.fecha_vencimiento < CURRENT_DATE;""",
        #     None,
        # )
        perdidas = self.conexion.ejecutar_bd(
        """
        SELECT SUM(productos.precio_compra * lotes.cantidad) AS perdidas
        FROM 
            lotes 
        JOIN 
            productos ON lotes.producto_id = productos.id
        WHERE 
            lotes.fecha_vencimiento < CURRENT_DATE 
            AND productos.mostrar = 1 
            AND lotes.cantidad > 0;
        """,
        None,
        )


        productos_vencidos, proximo_vencimiento = self.obtener_vencimientos(False)

        if perdidas and perdidas[0][0] is not None:
            perdidas = round(perdidas[0][0])

        else:
            perdidas = 0

        self.contador_vencidos.configure(
            text=f" Productos vencidos | {len(productos_vencidos)}"
        )
        self.contador_proximos.configure(
            text=f" Próximos a vencer | {len(proximo_vencimiento)}"
        )
        self.contador_perdidas.configure(text=f" Pérdidas | ${perdidas}")

    # Filtrar según un criterio
    def filtrar(self, busqueda):
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
        
        if len(self.entry_busqueda.get().strip()) == 0:
            # Si no hay un criterio de búsqueda, filtrar con todos los productos
            self.filtrar(False)
        else:
            busqueda = self.conexion.ejecutar_bd(
            sql="""
                SELECT 
                    lotes.lote, 
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
                    (lotes.lote LIKE %s OR
                    productos.nombre LIKE %s OR 
                    productos.marca LIKE %s OR 
                    productos.categoria LIKE %s)
                    AND productos.mostrar = 1 AND lotes.cantidad > 0
                ORDER BY 
                    productos.nombre, lotes.fecha_vencimiento;
            """,
            valores=("%" + self.entry_busqueda.get().strip() + "%",) * 4,
            )
            self.filtrar(busqueda)

        #     busqueda = self.conexion.ejecutar_bd(
        #     sql="""
        #     SELECT 
        #         lotes.lote, 
        #         productos.nombre,
        #         productos.marca, 
        #         productos.categoria, 
        #         productos.precio_compra, 
        #         productos.precio_venta, 
        #         lotes.cantidad, 
        #         lotes.fecha_vencimiento 
        #     FROM 
        #         lotes
        #     JOIN 
        #         productos ON lotes.producto_id = productos.id
        #     WHERE 
        #         lotes.lote LIKE %s OR
        #         productos.nombre LIKE %s 
        #         OR productos.marca LIKE %s 
        #         OR productos.categoria LIKE %s
        #     ORDER BY productos.nombre, lotes.fecha_vencimiento;
        # """,
        #     valores=("%" + self.entry_busqueda.get().strip() + "%",) * 4,
        # )
        
