import customtkinter as ctk
import numpy as np
import sympy as sp
from CTkMessagebox import CTkMessagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
class Vector(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="📊 Operaciones con Vectores", font=("Arial", 20)).pack(pady=10)

        # Entradas de vectores
        self.entry_v1 = ctk.CTkEntry(self, placeholder_text="Vector A (Ej: 1, 2, 3)", width=400)
        self.entry_v1.pack(pady=5)

        self.entry_v2 = ctk.CTkEntry(self, placeholder_text="Vector B (Ej: 4, 5, 6)", width=400)
        self.entry_v2.pack(pady=5)

        self.resultado_vectores = ctk.CTkFrame(self)
        self.resultado_vectores.pack(pady=10)

        # Caja de resultados a la izquierda
        self.resultado_frame = ctk.CTkFrame(self.resultado_vectores, width=400)
        self.resultado_frame.pack(side="left", padx=5)
        self.canvas_resultado = None

        # Botonera
        botones = ctk.CTkFrame(self)
        botones.pack(pady=10)

        # Lista de botones (texto, comando)
        boton_textos = [
            ("➕ Sumar", self.sumar),
            ("➖ Restar", self.restar),
            ("📏 Magnitud A", self.magnitud),
            ("⚫ Producto Punto", self.producto_punto),
            ("✖️ Producto Cruzado", self.producto_cruzado),
            ("📐 Ángulo entre vectores", self.angulo_entre_vectores)
        ]

        total = len(boton_textos)
        for i, (texto, comando) in enumerate(boton_textos):
            fila = i // 2
            columna = i % 2

            if total % 2 == 1 and i == total - 1:
                # Último botón en caso impar: centrar usando columnspan=2
                ctk.CTkButton(botones, text=texto, width=180, command=comando).grid(
                    row=fila, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
            else:
                ctk.CTkButton(botones, text=texto, width=180, command=comando).grid(
                    row=fila, column=columna, padx=10, pady=5, sticky="ew")


    def obtener_vectores(self):
        try:
            v1 = np.array([float(x.strip()) for x in self.entry_v1.get().split(",")])
            v2 = np.array([float(x.strip()) for x in self.entry_v2.get().split(",")])
            return v1, v2
        except:
            self.mostrar_error("Error: Ingresa vectores válidos separados por comas.")
            return None, None

    def sumar(self):
        v1, v2 = self.obtener_vectores()
        if v1 is not None and len(v1) == len(v2):
            suma = v1 + v2
            latex_expr = sp.latex(suma)
            self.mostrar_resultado_latex(f"\\text{{Resultado Suma: }}\\quad {latex_expr}")
        else:
            self.mostrar_error("⚠️ Los vectores deben tener la misma dimensión.")

    def restar(self):
        v1, v2 = self.obtener_vectores()
        if v1 is not None and len(v1) == len(v2):
            resta = v1 - v2
            latex_expr = sp.latex(resta)
            self.mostrar_resultado_latex(f"\\text{{Resultado Resta: }}\\quad {latex_expr}")
        else:
            self.mostrar_error("⚠️ Los vectores deben tener la misma dimensión.")

    def magnitud(self):
        try:
            v1 = np.array([float(x.strip()) for x in self.entry_v1.get().split(",")])
            mag = np.linalg.norm(v1)
            latex_expr = sp.latex(mag)
            self.mostrar_resultado_latex(f"\\text{{La magnitud es: }} \\quad {latex_expr}")
        except:
            self.mostrar_error("Error al calcular la magnitud.\n")

    def producto_punto(self):

        v1, v2 = self.obtener_vectores()
        if v1 is not None and len(v1) == len(v2):
            punto = np.dot(v1, v2)
            latex_expr = sp.latex(punto)
            self.mostrar_resultado_latex(f"\\text {{El producto punto es: }}\\quad {latex_expr}")
        else:
            self.mostrar_error("⚠️ Los vectores deben tener la misma dimensión.")

    def producto_cruzado(self):
        v1, v2 = self.obtener_vectores()
        if v1 is not None and len(v1) == 3 and len(v2) == 3:
            cruz = np.cross(v1, v2)
            latex_expr = sp.latex(cruz)
            self.mostrar_resultado_latex(f"\\text {{El punto cruzado es: }}\\quad {latex_expr}")
        else:
            self.mostrar_error("⚠️ Solo se puede calcular producto cruzado entre vectores de 3 dimensiones.")
    
    def angulo_entre_vectores(self):
        v1, v2 = self.obtener_vectores()
        if v1 is not None and len(v1) == len(v2):
            norm1 = np.linalg.norm(v1)
            norm2 = np.linalg.norm(v2)
            if norm1 == 0 or norm2 == 0:
                self.mostrar_error("⚠️ No se puede calcular el ángulo con un vector nulo.")
                return

            cos_theta = np.dot(v1, v2) / (norm1 * norm2)
            cos_theta = np.clip(cos_theta, -1.0, 1.0)  # prevenir errores por redondeo
            angulo_rad = np.arccos(cos_theta)
            angulo_deg = np.degrees(angulo_rad)

            latex_expr = sp.latex(round(angulo_deg, 4))
            if len(v1) == 2:
                self.graficar_vectores_con_angulo(v1, v2, angulo_deg)
            else:
                self.mostrar_resultado_latex(f"\\text{{Ángulo entre los vectores: }}\\quad {latex_expr}^\\circ")

        else:
            self.mostrar_error("⚠️ Los vectores deben tener la misma dimensión.")
    
    def graficar_vectores_con_angulo(self, v1, v2, angulo_deg):
        if hasattr(self, 'canvas_resultado') and self.canvas_resultado:
            self.canvas_resultado.get_tk_widget().destroy()

        fig, ax = plt.subplots(figsize=(4, 4), dpi=100)

        ax.quiver(0, 0, v1[0], v1[1], angles='xy', scale_units='xy', scale=1, color='blue')
        ax.quiver(0, 0, v2[0], v2[1], angles='xy', scale_units='xy', scale=1, color='green')

        # Etiquetas de vectores
        ax.text(v1[0] + 0.1, v1[1] + 0.1, 'A', color='blue', fontsize=12)
        ax.text(v2[0] - 0.2, v2[1] - 0.2, 'B', color='green', fontsize=12)


        # Posición dinámica del texto del ángulo
        pos_x = (v1[0] + v2[0]) / 4
        pos_y = (v1[1] + v2[1]) / 4
        ax.text(pos_x, pos_y, f"{round(angulo_deg, 2)}°", fontsize=12, color='red', ha='center')

        # Ajuste de límites
        max_val = max(np.linalg.norm(v1), np.linalg.norm(v2)) + 1
        ax.set_xlim(-max_val, max_val)
        ax.set_ylim(-max_val, max_val)
        ax.set_aspect('equal')
        ax.grid(True)
        ax.set_title("Ángulo entre vectores")

        self.canvas_resultado = FigureCanvasTkAgg(fig, master=self.resultado_frame)
        self.canvas_resultado.draw()
        self.canvas_resultado.get_tk_widget().pack(padx=10, pady=10)




    def mostrar_error(self, mensaje):
        CTkMessagebox(title="❌ Error", message=mensaje, icon="cancel")
    def mostrar_resultado_latex(self, texto_latex: str):
        """Renderiza un texto en LaTeX en el canvas de resultados."""
        if hasattr(self, 'canvas_resultado') and self.canvas_resultado:
            self.canvas_resultado.get_tk_widget().destroy()

        fig, ax = plt.subplots(figsize=(5, 1.5), dpi=100)
        ax.text(0.5, 0.5, f"${texto_latex}$", fontsize=14, ha="center", va="center")
        ax.axis("off")

        self.canvas_resultado = FigureCanvasTkAgg(fig, master=self.resultado_frame)
        self.canvas_resultado.draw()
        self.canvas_resultado.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)