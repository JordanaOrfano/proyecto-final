from core.usuarios import *
from config.config import *
from gui.componentes import *


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, frame_cambiar):
        super().__init__(master)

        # Guardamos la función para cambiar de frame
        self.frame_cambiar = frame_cambiar
        
        frameFondo = ctk.CTkFrame(master=self, fg_color=COLOR_BG)
        frameFondo.pack(expand=True, fill="both")

        # Frame izquierdo con imagen
        imgFrame = ctk.CTkFrame(
            master=frameFondo, width=1000, fg_color=COLOR_BG)
        imgFrame.pack(side="left", fill="y")

        # Cargar imagen y ajustarla con CTkImage
        self.image_original = Image.open("src/assets/bg.png")
        self.image_ctk = ctk.CTkImage(self.image_original, size=(
            imgFrame.winfo_width(), imgFrame.winfo_height()))

        # Label con la imagen redimensionable
        self.image_label = ctk.CTkLabel(
            imgFrame, text="", image=self.image_ctk)
        self.image_label.pack(expand=True, fill="both")

        # Redimensionar la imagen al cambiar el tamaño de imgFrame
        imgFrame.bind("<Configure>", self.resize_image)

        # Botón en el frame izquierdo
        self.login_button = crear_boton(
            imgFrame, text="", fill="x", width=470)

        # Frame derecho con formulario de login
        frameLogin = ctk.CTkFrame(master=frameFondo, fg_color=COLOR_BG)
        frameLogin.pack(expand=True, fill="x", padx=110)

        crear_label(
            frameLogin, text="¡Bienvenido a StockUp!", font=("Roboto", 32, "bold"), pady=(0, 30), anchor="center"
        )

        crear_label(frameLogin, text=" Correo electrónico", font=("Roboto", 18, "bold"), pady=(10, 0), padx=0,
                    image=crear_imagen(
                        "src/assets/icons/login-mail.png", size=(22, 22))
                    )

        self.usuario_correo = crear_entry(
            frameLogin, placeholder_text="Correo electrónico", pady=0, fill="x")

        crear_label(frameLogin, text=" Contraseña", font=("Roboto", 18, "bold"), pady=(10, 0), padx=0,
                    image=crear_imagen(
                        "src/assets/icons/login-password.png", size=(22, 22))
                    )

        self.__usuario_contrasena = crear_entry(
            frameLogin, placeholder_text="**********", show="*", pady=0, fill="x")

        frame_botones = ctk.CTkFrame(frameLogin)
        frame_botones.pack(pady=20, fill="x")
        
        self.login_button = crear_boton(
            frame_botones,
            text="Iniciar sesión",
            command=lambda: self.login(frameFondo),
            fill="x",
            metodo="grid"
        )
        self.login_button.pack(side="left", fill="x", expand=True, padx=(0, 5))

        # Botón de manual
        self.manual_button = crear_boton(
            frame_botones, 
            text="",
            command=self.abrir_manual,
            width=20,
            metodo="grid",
            image=crear_imagen("src/assets/icons/book.png", size=(22, 22))
        )
        self.manual_button.pack(side="right", padx=0)
        
        crear_label(frameLogin, text="¿Tenés alguna duda o consulta? Contactanos por mail a horizonweb@gmail.com", anchor="center", font=("Roboto", 16, "bold"), pady=30)
        
    def resize_image(self, event):
        # Ajusta la imagen al tamaño actual de imgFrame
        nuevo_width = event.width
        nuevo_height = event.height
        self.image_ctk.configure(size=(nuevo_width, nuevo_height))

    def mostrar_notificacion(self, frame, mensaje):
        notificacion = CTkNotification(master=frame, state="info", message=mensaje, side="right_bottom")
        frame.after(3000, notificacion.destroy)

    def login(self, frame):
        if not self.usuario_correo.get().strip() or len(self.usuario_correo.get().strip()) < 6:
            self.mostrar_notificacion(frame, "Debes ingresar un correo válido.")
            return
        
        if not self.__usuario_contrasena.get() or len(self.__usuario_contrasena.get()) < 8:
            self.mostrar_notificacion(frame, "Debes ingresar una contraseña válida")
            return

        logear_usuario = Usuario(
            self.usuario_correo.get(), self.__usuario_contrasena.get()
        )

        # Verificar usuario
        if not logear_usuario.verificar_usuario(
            self.usuario_correo.get(), self.__usuario_contrasena.get()
        ):
            self.mostrar_notificacion(frame, "Usuario o contraseña incorrecto")
            return

        self.mostrar_notificacion(frame, "Sesión iniciada con éxito, redirigiendo...")
        frame.after(10, lambda: self.frame_cambiar("inicio"))

    def abrir_manual(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Manual de Usuario")
        popup.geometry("600x400")
        popup.resizable(False, False)
        popup.attributes("-topmost", True)  # Forzar que esté siempre al frente
        centrar_ventana(popup, 600, 400)

        manual_fondo = ctk.CTkScrollableFrame(master=popup)
        manual_fondo.pack(expand=True, fill="both", padx=0)
        
        manual_frame = ctk.CTkFrame(master=manual_fondo)
        manual_frame.pack(expand=True, fill="both", padx=30)
        
        crear_label(manual_frame, text="Manual de Usuario", font=("Roboto", 24, "bold"), anchor="center", pady=20, padx=0)
        crear_texto(manual_frame, "Bienvenido al Sistema de Gestión de Supermercado StockUp! Este manual te guiará paso a paso sobre cómo usar el sistema para administrar productos, registrar ventas y acceder a las estadísticas clave. A continuación, encontrarás instrucciones sobre cómo comenzar y cómo utilizar las funcionalidades principales del sistema.")
        
        crear_label(manual_frame, text="Funcionalidades Principales", font=("Roboto", 16, "bold"), anchor="w", pady=(10, 0), justify="left", padx=0)
        crear_texto(manual_frame, text="El sistema te permite gestionar tanto los productos en inventario como las ventas realizadas, todo a través de una interfaz fácil de usar. Si eres administrador, podrás realizar todas las acciones disponibles, mientras que los empleados tienen permisos limitados.\n\nLa gestión de productos te permite registrar nuevos artículos en el sistema, donde puedes ingresar detalles como el nombre del producto, la marca, la categoría, los precios de compra y venta, la cantidad disponible en stock y la fecha de vencimiento. Además, puedes editar o eliminar productos cuando sea necesario.")
        
        crear_label(manual_frame, text="Roles y permisos", font=("Roboto", 16, "bold"), anchor="w", pady=(10, 0), justify="left", padx=0)
        crear_texto(manual_frame, text="Existen dos tipos de usuarios: Administrador y Empleado.\n\nAdministrador: tiene acceso completo al sistema, incluyendo la capacidad de crear y gestionar cuentas de empleados, visualizar estadísticas completas y eliminar productos.\n\nEmpleados: pueden registrar ventas y gestionar el stock de productos, pero no tienen acceso a la configuración de roles ni a las estadísticas avanzadas.")
        
        crear_label(manual_frame, text="Ventas y estadísticas", font=("Roboto", 16, "bold"), anchor="w", pady=(10, 0), justify="left", padx=0)
        crear_texto(manual_frame, text="El sistema también permite registrar ventas de manera detallada, indicando qué productos se han vendido y en qué cantidades. Esto facilita el control sobre el inventario y proporciona información precisa para las estadísticas del negocio.\n\nAdemás, las estadísticas del sistema te permiten visualizar información clave que puede ayudarte a tomar decisiones informadas sobre tu negocio. Puedes consultar la ganancia total, pérdidas, ventas mensuales y por empleado. Estas estadísticas se muestran de forma clara, lo que te permite obtener una visión general del desempeño de tu negocio.")
        
        crear_label(manual_frame, text="Uso del sistema", font=("Roboto", 16, "bold"), anchor="w", pady=(10, 0), justify="left", padx=0)
        crear_texto(manual_frame, text="Para utilizar el sistema, primero debes iniciar sesión con tus credenciales. Si eres un administrador, el usuario y la contraseña predeterminados son ambos 'administrador'. Los empleados deberán ingresar las credenciales proporcionadas por el administrador.\n\nUna vez que inicies sesión, podrás acceder al menú principal, desde donde podrás gestionar los productos, registrar ventas y, si eres administrador, gestionar los usuarios y ver las estadísticas. Si eres un empleado, tus opciones estarán limitadas a la gestión de productos y el registro de ventas.\n\nCuando termines de usar el sistema, puedes cerrar sesión para volver a la pantalla de inicio de sesión.")
        
        crear_label(manual_frame, text="Autores", font=("Roboto", 16, "bold"), anchor="w", pady=(10, 0), justify="left", padx=0)
        crear_texto(manual_frame, pady=(0, 20), text="Este proyecto fue desarrollado por Jordana Orfano y Fernando Hidalgo, quienes han trabajado juntos para crear una herramienta eficiente y fácil de usar para la gestión de supermercados. Si tienes alguna pregunta o sugerencia, no dudes en contactarnos a través de GitHub o por correo electrónico.")
        
        