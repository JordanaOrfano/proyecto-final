from config.config import *
from gui.componentes import *
from core.usuarios import *


class Configuracion:
    def __init__(self, contenedor):
        self.contenedor = contenedor

        # -------------------------------- Configuración de frame --------------------------------
        frame_config = ctk.CTkScrollableFrame(master=self.contenedor, fg_color=COLOR_BG)
        frame_config.grid(sticky="nsew", padx=0)

        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)
        frame_config.grid_rowconfigure(0, weight=1)
        frame_config.grid_rowconfigure(2, weight=1)
        frame_config.grid_columnconfigure(0, weight=1)
        
        frame_contenido = ctk.CTkFrame(frame_config, fg_color=COLOR_BG)
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
        
        
        # -------------------------------- Reestablecer contraseña --------------------------------
        label_correo = crear_label(frame_contenido, 
                                   text=f"Reestablecer contraseña",
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
        
        
        # -------------------------------- Tema --------------------------------
        label_tema = crear_label(frame_contenido, 
                                 text="Tema", 
                                 font=("Roboto", 24, "bold"), 
                                 metodo="grid")
        label_tema.grid(row=10, columnspan=2, sticky="ew", pady=(35, 5))
        
        tema_optionmenu = crear_optionmenu(
            parent=frame_contenido,
            values=["Claro", "Oscuro"],
            metodo="grid",)
        tema_optionmenu.grid(row=11, columnspan=2, sticky="ew")
        
        
        # -------------------------------- Exportar productos --------------------------------
        label_exportar = crear_label(frame_contenido, 
                                     text="Exportar productos", 
                                     font=("Roboto", 24, "bold"), 
                                     metodo="grid")
        label_exportar.grid(row=12, columnspan=2, pady=(35, 5), sticky="ew")
        
        exportar_optionmenu = crear_optionmenu(
            parent=frame_contenido,
            values=["Seleccione formato", "CSV", "PDF", "JSON"],
            pady=0,
            metodo="grid",
            )
        exportar_optionmenu.grid(row=13, column=0, sticky="ew", padx=(0, 10))
        
        exportar_btn = crear_boton(parent=frame_contenido, 
                                   text="Exportar", 
                                   metodo="grid")
        exportar_btn.grid(row=13, column=1, sticky="ew", padx=(10, 0))
