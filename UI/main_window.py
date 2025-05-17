import customtkinter as ctk
from PIL import Image
import sys
import os

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

# === Función para rutas de recursos ===
def recurso_relativo(ruta):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, ruta)

# === Clase principal ===
class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora")
        self.centrar_ventana(1000, 700)
        self.resizable(True, True)

        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.main_content = ctk.CTkFrame(self)
        self.main_content.pack(side="right", fill="both", expand=True)

        self.toggle_btn = ctk.CTkButton(self, text="☰", width=30, height=30, command=self.toggle_sidebar)
        self.toggle_btn.place(x=10, y=10)
        self.toggle_btn.lift()

        self.menu_visible = True
        self.current_page = None

        # === Cargar y mostrar imagen del logo UNEMI ===
        logo_path = recurso_relativo("assets/unemi.png")
        self.logo_image_sidebar = ctk.CTkImage(light_image=Image.open(logo_path), size=(100, 100))
        ctk.CTkLabel(self.sidebar, image=self.logo_image_sidebar, text="", fg_color="transparent").pack(pady=5)

        ctk.CTkLabel(self.sidebar, text=" UNEMI ", font=("Arial", 20, "bold")).pack(pady=(0, 10))

        botones = [
            ("🏠 Inicio", self.mostrar_inicio),
            ("🧲 Matrices", self.mostrar_matrices),
            ("🖐 Polinomios", self.mostrar_polinomios),
            ("🧲 Vectores", self.mostrar_vectores),
            ("\ud83d\udcc8 Gráficas 2D", self.mostrar_grafica_2D),
            ("\ud83d\udcca Gráficas 3D", self.mostrar_grafica_3D),
            ("\ud83d\udd23 Derivación e Integración", self.mostrar_calculo),
            ("\ud83d\udd23 Ecuaciones Diferenciales", self.mostrar_edo),
            ("\ud83e\uddec Modelo SIR", self.mostrar_sir),
            ("\ud83d\udcd8 Sistema de EDOs", self.mostrar_sistema),
            ("\ud83d\udcca Distribuciones", self.mostrar_distribuciones),
            ("ℹ️ Acerca de", self.mostrar_acerca_de),
        ]

        for texto, comando in botones:
            ctk.CTkButton(self.sidebar, text=texto, command=comando).pack(pady=5, fill="x", padx=10)

        self.mostrar_inicio()

    def centrar_ventana(self, ancho=1000, alto=700):
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = int((pantalla_ancho - ancho) / 2)
        y = int((pantalla_alto - alto) / 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def limpiar_main(self):
        if self.current_page:
            self.current_page.destroy()
            self.current_page = None

    def toggle_sidebar(self):
        if self.menu_visible:
            self.sidebar.pack_forget()
            self.menu_visible = False
            self.toggle_btn.configure(text="→")
        else:
            self.sidebar.pack(side="left", fill="y")
            self.menu_visible = True
            self.toggle_btn.configure(text="☰")

    def mostrar_inicio(self):
        self.limpiar_main()
        self.current_page = ctk.CTkFrame(self.main_content)
        self.current_page.pack(expand=True, fill="both")

        ctk.CTkLabel(self.current_page, text="CALCU-SOFTWARE", font=("Arial", 24)).pack(pady=30)

        # Mostrar el logo otra vez en la pantalla de inicio
        logo_path = recurso_relativo("assets/unemi.png")
        self.logo_image_inicio = ctk.CTkImage(light_image=Image.open(logo_path), size=(100, 100))
        ctk.CTkLabel(self.current_page, image=self.logo_image_inicio, text="", fg_color="transparent").pack(pady=(10, 0))

        scrollable_frame = ctk.CTkScrollableFrame(self.current_page)
        scrollable_frame.pack(expand=True, fill="both", padx=20, pady=10)

        cards_frame = ctk.CTkFrame(scrollable_frame)
        cards_frame.pack(anchor="center", pady=10)

        botones_inicio = [
            ("\ud83e\uddf2 Matrices", self.mostrar_matrices),
            ("\ud83d\udd90 Polinomios", self.mostrar_polinomios),
            ("\ud83e\uddf2 Vectores", self.mostrar_vectores),
            ("\ud83d\udcc8 Gráficas 2D", self.mostrar_grafica_2D),
            ("\ud83d\udcca Gráficas 3D", self.mostrar_grafica_3D),
            ("\ud83d\udd23 Derivación e Integración", self.mostrar_calculo),
            ("\ud83d\udd23 Ecuaciones Diferenciales", self.mostrar_edo),
            ("\ud83e\uddec Modelo SIR", self.mostrar_sir),
            ("\ud83d\udcd8 Sistema de EDOs", self.mostrar_sistema),
            ("\ud83d\udcca Distribuciones", self.mostrar_distribuciones),
            ("ℹ️ Acerca de", self.mostrar_acerca_de),
        ]

        for idx, (texto, comando) in enumerate(botones_inicio):
            fila = idx // 3
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

    def mostrar_acerca_de(self):
        self.limpiar_main()
        self.current_page = ctk.CTkFrame(self.main_content, corner_radius=20)
        self.current_page.pack(expand=True, fill="both", padx=40, pady=30)

        titulo_font = ("Arial Rounded MT Bold", 28)
        texto_font = ("Segoe UI", 16)

        self.current_page.configure(fg_color="#2b2b2b")

        ctk.CTkLabel(self.current_page, text="ℹ️ Acerca de esta aplicación", font=titulo_font, text_color="#ffffff").pack(pady=(20, 10))

        info = [
            ("Aplicación:", "CALCULADORA CIENTÍFICA"),
            ("Autor:", "GABRIEL CARRIEL"),
            ("Carrera:", "Ingeniería en Software"),
            ("Semestre:", "6to semestre"),
            ("Materia:", "Modelos Matemáticos y Simulación"),
            ("Año académico:", "2025"),
            ("Profesor:", "ISIDRO FABRICIO MORALES TORRES"),
            ("Tecnologías:", "Python, CustomTkinter, NumPy, Matplotlib"),
        ]

        for etiqueta, valor in info:
            texto = f"{etiqueta} {valor}"
            ctk.CTkLabel(self.current_page, text=texto, font=texto_font, text_color="#ffffff", anchor="w", justify="left").pack(fill="x", padx=30, pady=3)

        ctk.CTkLabel(self.current_page, text="© 2025 - by Gabrielz", font=("Segoe UI", 12), text_color="#aaaaaa").pack(side="bottom", pady=15)