import customtkinter as ctk
from module_logic.matrices import MatricesPage
from module_logic.graficas_2d import Graficas2D
from module_logic.vectores import Vector
from module_logic.polinomios import Polinomios
from module_logic.graficas_3d import Graficas3D
from module_logic.calculo import DerivacionIntegracion
from UI.ecuaciones_diferenciales_UI import EcuacionesDiferencialesUI
from UI.sir_ui import ModeloSIR_UI
from module_logic.sistema_diferencial_ui import SistemaDiferencialUI
from UI.distribuciones_ui import DistribucionesUI
from PIL import Image

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora")
        self.centrar_ventana(1000, 700)
        self.resizable(True, True)

        # ------ ESTRUCTURA GENERAL DE LA VENTANA ------
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.main_content = ctk.CTkFrame(self)
        self.main_content.pack(side="right", fill="both", expand=True)

        self.toggle_btn = ctk.CTkButton(self, text="☰", width=30, height=30, command=self.toggle_sidebar)
        self.toggle_btn.place(x=10, y=10)
        self.toggle_btn.lift()  


        self.menu_visible = True 


        self.current_page = None

       # BOTONES DE LA PARTE LATERAL
        self.logo_image = ctk.CTkImage(light_image=Image.open("assets/unemi.png"), size=(100, 100))
        ctk.CTkLabel(self.sidebar, image=self.logo_image, text="", fg_color="transparent", bg_color="transparent").pack(pady=(10, 0))



        ctk.CTkLabel(self.sidebar, text=" UNEMI ", font=("Arial", 20, "bold")).pack(pady=20)

        self.btn_inicio = ctk.CTkButton(self.sidebar, text="🏠 Inicio", command=self.mostrar_inicio)
        self.btn_inicio.pack(pady=5, fill="x", padx=10)

        self.btn_matrices = ctk.CTkButton(self.sidebar, text="🧮 Matrices", command=self.mostrar_matrices)
        self.btn_matrices.pack(pady=5, fill="x", padx=10)

        self.btn_polinomios = ctk.CTkButton(self.sidebar, text="📐 Polinomios ", command=self.mostrar_polinomios)
        self.btn_polinomios.pack(pady=5, fill="x", padx=10)

        self.btn_vectores = ctk.CTkButton(self.sidebar, text="🧮 Vectores", command=self.mostrar_vectores)
        self.btn_vectores.pack(pady=5, fill="x", padx=10)


        self.btn_graficas2d = ctk.CTkButton(self.sidebar, text="📈 Gráficas 2D", command=self.mostrar_grafica_2D)
        self.btn_graficas2d.pack(pady=5, fill="x", padx=10)

        self.btn_graficas3d = ctk.CTkButton(self.sidebar, text="📊 Gráficas 3D", command=self.mostrar_grafica_3D)
        self.btn_graficas3d.pack(pady=5, fill="x", padx=10)

        self.btn_calculo = ctk.CTkButton(self.sidebar, text="🔣 Derivación e Integración", command=self.mostrar_calculo)
        self.btn_calculo.pack(pady=5, fill="x", padx=10)

        self.btn_EDO = ctk.CTkButton(self.sidebar, text="🔣 Ecuaciones Diferenciales", command=self.mostrar_edo)
        self.btn_EDO.pack(pady=5, fill="x", padx=10)

        self.btn_sir = ctk.CTkButton(self.sidebar, text="🧬 Modelo SIR", command=self.mostrar_sir)
        self.btn_sir.pack(pady=5, fill="x", padx=10)

        self.btn_sistema = ctk.CTkButton(self.sidebar, text="📘 Sistema de EDOs", command=self.mostrar_sistema)
        self.btn_sistema.pack(pady=5, fill="x", padx=10)

        self.btn_distribuciones = ctk.CTkButton(self.sidebar, text="📊 Distribuciones", command=self.mostrar_distribuciones)
        self.btn_distribuciones.pack(pady=5, fill="x", padx=10)

        self.btn_acerca = ctk.CTkButton(self.sidebar, text="ℹ️ Acerca de", command=self.mostrar_acerca_de)
        self.btn_acerca.pack(pady=5, fill="x", padx=10)

        #MUESTRO EL INICIO
        self.mostrar_inicio()



    def limpiar_main(self):
        if self.current_page:
            self.current_page.destroy()
            self.current_page = None

    def centrar_ventana(self, ancho=1000, alto=700):
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = int((pantalla_ancho - ancho) / 2)
        y = int((pantalla_alto - alto) / 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")


    def mostrar_inicio(self):
        self.limpiar_main()
        self.current_page = ctk.CTkFrame(self.main_content)
        self.current_page.pack(expand=True, fill="both")
        
        titulo = ctk.CTkLabel(self.current_page, text="CALCU-SOFTWARE", font=("Arial", 24))
        titulo.pack(pady=30)
        logo_path = "assets/unemi.png"  
        self.logo_image = ctk.CTkImage(light_image=Image.open(logo_path), size=(100, 100))
        ctk.CTkLabel(self.current_page, image=self.logo_image, text="", fg_color="transparent", bg_color="transparent").pack(pady=(10, 0))

        scrollable_frame = ctk.CTkScrollableFrame(self.current_page)
        scrollable_frame.pack(expand=True, fill="both", padx=20, pady=10)

        # Frame interno para centrar los botones
        cards_frame = ctk.CTkFrame(scrollable_frame)
        cards_frame.pack(anchor="center", pady=10)

        # Lista de botones con texto y función asociada
        botones = [
            ("🧮 Matrices", self.mostrar_matrices),
            ("📐 Polinomios", self.mostrar_polinomios),
            ("🧮 Vectores", self.mostrar_vectores),
            ("📈 Gráficas 2D", self.mostrar_grafica_2D),
            ("📊 Gráficas 3D", self.mostrar_grafica_3D),
            ("🔣 Derivación e Integración", self.mostrar_calculo),
            ("🔣 Ecuaciones Diferenciales", self.mostrar_edo),
            ("🧬 Modelo SIR", self.mostrar_sir),
            ("📘 Sistema de EDOs", self.mostrar_sistema),
            ("📊 Distribuciones", self.mostrar_distribuciones),
            ("ℹ️  Acerca de.", self.mostrar_acerca_de),
        ]

        # Mostrar los botones en 4 columnas por fila
        for idx, (texto, comando) in enumerate(botones):
            fila = idx // 4
            col = idx % 3
            ctk.CTkButton(cards_frame, text=texto, width=200, height=100, command=comando).grid(row=fila, column=col, padx=15, pady=10)


    def mostrar_matrices(self):
        self.limpiar_main()
        self.current_page = MatricesPage(self.main_content)
        self.current_page.pack(fill="both", expand=True)

    def mostrar_polinomios(self):
        self.limpiar_main()
        self.current_page = Polinomios(self.main_content)
        self.current_page.pack(fill="both", expand=True)

    def mostrar_vectores(self):
        self.limpiar_main()
        self.current_page = Vector(self.main_content)
        self.current_page.pack(fill="both", expand=True)
    
    def mostrar_grafica_2D(self):
        self.limpiar_main()
        self.current_page = Graficas2D(self.main_content)
        self.current_page.pack(fill="both", expand=True)
    
    def mostrar_grafica_3D(self):
        self.limpiar_main()
        self.current_page = Graficas3D(self.main_content)
        self.current_page.pack(fill="both", expand=True)
    
    def mostrar_calculo(self):
        self.limpiar_main()
        self.current_page = DerivacionIntegracion(self.main_content)
        self.current_page.pack(fill="both", expand=True)

    def mostrar_edo(self):
        self.limpiar_main()
        self.current_page = EcuacionesDiferencialesUI(self.main_content)
        self.current_page.pack(fill="both", expand=True)


    def mostrar_acerca_de(self):
        self.limpiar_main()
        self.current_page = ctk.CTkFrame(self.main_content)
        self.current_page.pack(expand=True, fill="both")

        ctk.CTkLabel(self.current_page, text="ℹ️ Acerca de esta aplicación", font=("Arial", 24)).pack(pady=20)
        texto = (
            "CALCULADORA CIENTÍFICA\n"
            "Desarrollado por: GABRIEL CARRIEL\n"
            "Carrera: Ingeniería en Software \n"
            "Semestre: 6to semestre\n"
            "Materia: Modelos Matemáticos y Simulación\n"
            "Año académico : 2025\n"
            "Profesor: ISIDRO FABRICIO MORALES TORRES\n"
            "Tecnologías: Python + CustomTkinter + NumPy + Matplotlib\n"
            
        )
        ctk.CTkLabel(self.current_page, text=texto, font=("Arial", 16), justify="left").pack(pady=10, padx=20)

    def toggle_sidebar(self):
        if self.menu_visible:
            self.sidebar.pack_forget()
            self.menu_visible = False
            self.toggle_btn.configure(text="→")
        else:
            self.sidebar.pack(side="left", fill="y")
            self.menu_visible = True
            self.toggle_btn.configure(text="☰")
    def mostrar_sir(self):
        self.limpiar_main()
        self.current_page = ModeloSIR_UI(self.main_content)
        self.current_page.pack(fill="both", expand=True)

    def mostrar_sistema(self):
        self.limpiar_main()
        self.current_page = SistemaDiferencialUI(self.main_content)
        self.current_page.pack(fill="both", expand=True)

    def mostrar_distribuciones(self):
        self.limpiar_main()
        self.current_page = DistribucionesUI(self.main_content)
        self.current_page.pack(fill="both", expand=True)
