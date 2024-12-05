from config.config import *
from gui.componentes import *
from core.usuarios import *
from core.productos import *
import csv
import json
import openpyxl  # Para exportar a excel
import os  #Para crear carpeta de exportaciones
from openpyxl.styles import Alignment, PatternFill, Font  # Estilos de excel


class Configuracion:
    def __init__(self, contenedor):
        self.contenedor = contenedor
        self.conexion = Database()
        
        # -------------------------------- Configuración de frame --------------------------------
        self.frame_config = ctk.CTkScrollableFrame(master=self.contenedor, fg_color=COLOR_BG)
        self.frame_config.grid(sticky="nsew", padx=0)

        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)
        self.frame_config.grid_rowconfigure(0, weight=1)
        self.frame_config.grid_rowconfigure(2, weight=1)
        self.frame_config.grid_columnconfigure(0, weight=1)
        
        frame_contenido = ctk.CTkFrame(self.frame_config, fg_color=COLOR_BG)
        frame_contenido.grid(row=1, column=0, padx=120, pady=20, sticky="nsew")
        frame_contenido.grid_columnconfigure((0, 1), weight=1)  # Hacer que las columnas se expandan

        
        label_titulo = crear_label(frame_contenido, 
                                    metodo="grid", 
                                    text="Configuración", 
                                    font=("Roboto", 32, "bold"))
        label_titulo.grid(row=0, column=0, columnspan=2, pady=(20, 25), sticky="ew")
        
        
        # -------------------------------- Datos del usuario --------------------------------
        label_titulo = crear_label(frame_contenido, 
                                    metodo="grid", 
                                    text="Datos del usuario", 
                                    font=("Roboto", 24, "bold"))
        label_titulo.grid(row=1, column=0, columnspan=2, pady=0, sticky="ew")
        
        # Nombre
        label_nombre = crear_label(frame_contenido, 
                    text=f" Nombre y apellido", 
                    font=("Roboto", 18, "bold"),
                    metodo="grid", 
                    image=crear_imagen("src/assets/icons/user.png", size=(22, 22))
                    )
        label_nombre.grid(row=2, columnspan=2, pady=(10, 0), sticky="ew")
        
        nombre = crear_info(frame_contenido, 
                             text=f"{Usuario.usuario_actual[0][0].capitalize()} {Usuario.usuario_actual[0][1].capitalize()}",
                             metodo="grid",
                            )
        nombre.grid(row=3, columnspan=2, pady=0, sticky="ew")

        # Correo
        label_correo = crear_label(frame_contenido, 
                    text=f" Correo electrónico", 
                    font=("Roboto", 18, "bold"),
                    metodo="grid", 
                    image=crear_imagen("src/assets/icons/login-mail.png", size=(22, 22))
                    )
        label_correo.grid(row=4, column=0, pady=(15, 0), sticky="ew")
        
        correo = crear_info(frame_contenido, 
                             text=f"{Usuario.usuario_actual[0][4]}",
                             metodo="grid",
                            )
        correo.grid(row=5, column=0, pady=0, padx=(0, 10), sticky="ew")

        # DNI
        label_dni = crear_label(frame_contenido, 
                    text=f" D.N.I", 
                    font=("Roboto", 18, "bold"),
                    metodo="grid",
                    image=crear_imagen("src/assets/icons/id.png", size=(22, 22))
                    )
        label_dni.grid(row=4, column=1, pady=(15, 0), sticky="ew")
        
        dni = crear_info(frame_contenido, 
                             text=f"{Usuario.usuario_actual[0][5]}",
                             metodo="grid",
                            )
        dni.grid(row=5, column=1, pady=0, padx=(10, 0), sticky="ew")
        
        
        # -------------------------------- Restablecer contraseña --------------------------------
        label_correo = crear_label(frame_contenido, 
                                   text=f" Restablecer contraseña",
                                   font=("Roboto", 24, "bold"),
                                   metodo="grid",
                                   )
        label_correo.grid(row=6, columnspan=2, pady=(35, 0), sticky="ew")
        
        
        label_correo = crear_label(frame_contenido, 
                                   text=f" Contraseña actual",
                                   font=("Roboto", 18, "bold"),
                                   metodo="grid",
                                   image=crear_imagen("src/assets/icons/login-password.png", size=(22, 22))
                                   )
        label_correo.grid(row=7, column=0, pady=(10, 0), sticky="ew")
        
        entry_contrasena_actual = crear_entry(frame_contenido, 
                            placeholder_text="**********", 
                            metodo="grid")
        entry_contrasena_actual.grid(row=8, column=0, pady=0, sticky="ew", padx=(0, 10))
        
        
        label_contrasena_nueva = crear_label(frame_contenido, 
                                   text=f" Nueva contraseña",
                                   font=("Roboto", 18, "bold"),
                                   metodo="grid",
                                   image=crear_imagen("src/assets/icons/login-password.png", size=(22, 22))
                                   )
        label_contrasena_nueva.grid(row=7, column=1, pady=(10, 0), sticky="ew")
        
        entry_contrasena_nueva = crear_entry(frame_contenido, 
                            placeholder_text="**********", 
                            metodo="grid")
        entry_contrasena_nueva.grid(row=8, column=1, pady=0, sticky="ew", padx=(10, 0))
        
        
        btn_contrasena = crear_boton(frame_contenido,
                                     metodo="grid", 
                                     text="Actualizar contraseña")
        btn_contrasena.grid(row=9, columnspan=2, pady=(20, 0), sticky="ew")
        
        # -------------------------------- Exportar productos --------------------------------
        label_exportar = crear_label(frame_contenido, 
                                     text="Exportar productos", 
                                     font=("Roboto", 24, "bold"), 
                                     metodo="grid")
        label_exportar.grid(row=12, columnspan=2, pady=(35, 5), sticky="ew")
        
        exportar_optionmenu = crear_optionmenu(
            parent=frame_contenido,
            values=["Seleccione formato", "Excel", "CSV", "JSON"],
            pady=0,
            metodo="grid",
            )
        exportar_optionmenu.grid(row=13, column=0, sticky="ew", padx=(0, 10))
        
        exportar_btn = crear_boton(parent=frame_contenido, 
                                   text="Exportar", 
                                   metodo="grid",
                                   command=lambda: self.exportar_productos(exportar_optionmenu.get())
                                   )
        exportar_btn.grid(row=13, column=1, sticky="ew", padx=(10, 0))
        
        # -------------------------------- Importar productos --------------------------------
        label_importar = crear_label(frame_contenido, 
                                     text="Importar productos", 
                                     font=("Roboto", 24, "bold"), 
                                     metodo="grid")
        label_importar.grid(row=14, columnspan=2, pady=(35, 5), sticky="ew")
        
        importar_optionmenu = crear_optionmenu(
            parent=frame_contenido,
            values=["Seleccione formato", "Excel", "CSV", "JSON"],
            pady=0,
            metodo="grid",
            command=lambda: self.importar_productos(importar_optionmenu.get())
            )
        importar_optionmenu.grid(row=15, column=0, sticky="ew", padx=(0, 10), pady=(0, 20))
        
        importar_btn = crear_boton(parent=frame_contenido, 
                                   text="Importar", 
                                   metodo="grid")
        importar_btn.grid(row=15, column=1, sticky="ew", padx=(10, 0), pady=(0, 20))
    
    # -------------------------------- Exportar --------------------------------
    def exportar_productos(self, formato):
        if formato == "CSV":
            self.exportar_csv()
        elif formato == "JSON":
            self.exportar_json()
        elif formato == "Excel":
            self.exportar_excel()
        else:
            crear_notificacion(self.contenedor, "error", "Seleccione un formato")
    
    def exportar_csv(self):
        productos = self.conexion.ejecutar_bd("SELECT * FROM productos", tipo="select")
        lotes = self.conexion.ejecutar_bd("SELECT * FROM lotes", tipo="select")
        
        os.makedirs("Exportaciones", exist_ok=True)  # Crea carpeta para exportaciones
        
        with open('Exportaciones/productos.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Nombre", "Marca", "Categoría", "Precio de compra", "Precio de venta"])
            for producto in productos:
                writer.writerow(producto)
        
        with open('Exportaciones/lotes.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Lote", "Producto ID", "Cantidad", "Fecha de vencimiento"])
            for lote in lotes:
                writer.writerow(lote)
        
        crear_notificacion(self.contenedor, "info", "Productos exportados a CSV correctamente.")
    
    def exportar_json(self):
        productos_lista = []
        productos = self.conexion.ejecutar_bd("SELECT * FROM productos", tipo="select")
        
        for producto in productos:
            productos_lista.append({
                "ID": producto[0],
                "Nombre": producto[1],
                "Marca": producto[2],
                "Categoría": producto[3],
                "Precio de compra": float(producto[4]),
                "Precio de venta": float(producto[5])
            })
            
        lotes_lista = []
        lotes = self.conexion.ejecutar_bd("SELECT * FROM lotes", tipo="select")
        
        for lote in lotes:
            lotes_lista.append({
                "Lote": lote[0],
                "Producto ID": lote[1],
                "Cantidad": lote[2],
                "Fecha de vencimiento": str(lote[3]),
            })
        
        os.makedirs("Exportaciones", exist_ok=True)  # Crea carpeta para exportaciones
        
        # Guardar en archivo
        with open('Exportaciones/productos.json', 'w', encoding='utf-8') as file:
            json.dump(productos_lista, file, ensure_ascii=False, indent=4)
        
        with open('Exportaciones/lotes.json', 'w', encoding='utf-8') as file:
            json.dump(lotes_lista, file, ensure_ascii=False, indent=4)
        
        crear_notificacion(self.contenedor, "info", "Productos exportados a JSON correctamente.")
    
    def exportar_excel(self):
        try:
            productos = self.conexion.ejecutar_bd("SELECT * FROM productos", tipo="select")
            lotes = self.conexion.ejecutar_bd("SELECT * FROM lotes", tipo="select")

            wb = openpyxl.Workbook()  # Contenedor para generar excel

            # ----------------- Hoja de Productos -----------------
            ws_productos = wb.active
            ws_productos.title = "Productos"

            # Encabezados
            headers_productos = ["ID", "Nombre", "Marca", "Categoría", "Precio de compra", "Precio de venta"]
            ws_productos.append(headers_productos)

            # Agregar datos de productos
            for producto in productos:
                ws_productos.append(producto)

            for col, header in enumerate(headers_productos, start=1):
                # Ajustar ancho de columnas
                max_length = max((len(str(row[col - 1])) for row in productos), default=len(header))
                ancho_ajustado = max(len(header), max_length) + 2
                ws_productos.column_dimensions[openpyxl.utils.get_column_letter(col)].width = ancho_ajustado
                
                # Estilo de los encabezados
                celda = ws_productos.cell(row=1, column=col)
                celda.fill = PatternFill(start_color="0c955a", end_color="0c955a", fill_type="solid")
                celda.font = Font(bold=True, color="FFFFFF")
                celda.alignment = Alignment(horizontal="center", vertical="center")
            
            
            # ----------------- Hoja de Lotes -----------------
            ws_lotes = wb.create_sheet(title="Lotes")

            # Encabezados
            headers_lotes = ["Lote", "Producto ID", "Cantidad", "Fecha de vencimiento"]
            ws_lotes.append(headers_lotes)

            # Agregar datos de lotes
            for lote in lotes:
                ws_lotes.append(lote)
                
            for col, header in enumerate(headers_lotes, start=1):
                # Ajustar ancho de columnas
                max_length = max((len(str(row[col - 1])) for row in lotes), default=len(header))
                ancho_ajustado = max(len(header), max_length) + 2
                ws_lotes.column_dimensions[openpyxl.utils.get_column_letter(col)].width = ancho_ajustado
                
                # Estilo de los encabezados
                celda = ws_lotes.cell(row=1, column=col)
                celda.fill = PatternFill(start_color="0c955a", end_color="0c955a", fill_type="solid")
                celda.font = Font(bold=True, color="FFFFFF")
                celda.alignment = Alignment(horizontal="center", vertical="center")
            
            os.makedirs("Exportaciones", exist_ok=True)  # Crea carpeta para exportaciones
            
            # Guardar archivo
            excel_file = "Exportaciones/productos_y_lotes.xlsx"
            wb.save(excel_file)
            
            crear_notificacion(self.contenedor, "info", "Productos exportados a Excel correctamente.")
        
        except Exception as e:
            print(f"Error al exportar a Excel: {e}")
            crear_notificacion(self.contenedor, "error", "El archivo ya existe.")
        
            
    # -------------------------------- Importar --------------------------------
    def importar_productos(self, formato):
        if formato == "CSV":
            self.importar_csv()
        elif formato == "JSON":
            self.importar_json()
        elif formato == "Excel":
            self.importar_excel()
        else:
            print("Formato no soportado")
    
