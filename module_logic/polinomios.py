import re
import numpy as np
import customtkinter as ctk
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from CTkMessagebox import CTkMessagebox


class Polinomios(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        

        ctk.CTkLabel(self, text="📐 Operaciones con Polinomios", font=("Arial", 20)).pack(pady=10)
        contenedor = ctk.CTkFrame(self)
        contenedor.pack(expand=True, fill="both", padx=20, pady=20)

        self.var_x = sp.Symbol('x')

        # Entradas
        self.entry_p1 = ctk.CTkEntry(contenedor, placeholder_text="Polinomio A (Ejemplo: x^2 - 3x + 2)", width=400)
        self.entry_p1.pack(pady=5)

        self.entry_p2 = ctk.CTkEntry(contenedor, placeholder_text="Polinomio B (opcional)", width=400)
        self.entry_p2.pack(pady=5)

        eval_frame = ctk.CTkFrame(contenedor)
        eval_frame.pack(pady=5)
        ctk.CTkLabel(eval_frame, text="📍 Evaluar A en x =", font=("Arial", 14)).pack(side="left", padx=5)
        self.entry_eval = ctk.CTkEntry(eval_frame, width=80, placeholder_text="Ej: 2")
        self.entry_eval.pack(side="left", padx=5)

        # Scrollable panel
        self.scrollable_panel = ctk.CTkScrollableFrame(contenedor)
        self.scrollable_panel.pack(expand=True, fill="both", padx=10, pady=10)

        # Contenedor horizontal para resultados y gráfica
        self.resultado_grafica_frame = ctk.CTkFrame(self.scrollable_panel)
        self.resultado_grafica_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Caja de resultados a la izquierda
        self.resultado_frame = ctk.CTkFrame(self.resultado_grafica_frame, width=400)
        self.resultado_frame.pack(side="left", fill="both", expand=True, padx=5)
        self.canvas_resultado = None

        # Frame de gráfica a la derecha
        self.graph_frame = ctk.CTkFrame(self.resultado_grafica_frame, width=400)
        self.graph_frame.pack(side="left", fill="both", expand=True, padx=5)
        self.canvas = None


        # Botonera justo debajo del resultado
        botones = ctk.CTkFrame(self.scrollable_panel)
        botones.pack(pady=5, fill="x")

        fila1 = ctk.CTkFrame(botones)
        fila1.pack(pady=5, fill="x", padx=20)
        ctk.CTkButton(fila1, text="➕ Sumar", command=self.sumar).pack(side="left", expand=True, fill="x", padx=10)
        ctk.CTkButton(fila1, text="✖️ Multiplicar", command=self.multiplicar).pack(side="left", expand=True, fill="x", padx=10)

        fila2 = ctk.CTkFrame(botones)
        fila2.pack(pady=5, fill="x", padx=20)
        ctk.CTkButton(fila2, text="📉 Derivar A", command=self.derivar).pack(side="left", expand=True, fill="x", padx=10)
        ctk.CTkButton(fila2, text="∫ Integrar A", command=self.integrar).pack(side="left", expand=True, fill="x", padx=10)

        fila3 = ctk.CTkFrame(botones)
        fila3.pack(pady=5, fill="x", padx=20)
        ctk.CTkButton(fila3, text="📍 Evaluar A", command=self.evaluar).pack(side="left", expand=True, fill="x", padx=10)
        ctk.CTkButton(fila3, text="📊 Graficar A", command=self.graficar).pack(side="left", expand=True, fill="x", padx=10)


    def parsear(self, texto):
        try:
            texto = texto.replace("^", "**")
            texto = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', texto)
            texto = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', texto)
            return parse_expr(texto, evaluate=False)
        except:
            self.mostrar_error("❌ Error al interpretar el Polinomio, revisa la sintaxis.")
            return None

    def obtener_polinomios(self):
        if hasattr(self, 'canvas_resultado') and self.canvas_resultado:
            self.canvas_resultado.get_tk_widget().destroy()

        p1_texto = self.entry_p1.get().strip()
        p2_texto = self.entry_p2.get().strip()
        p1 = self.parsear(p1_texto) if p1_texto else None
        p2 = self.parsear(p2_texto) if p2_texto else None
        return p1, p2


    def sumar(self):
        p1, p2 = self.obtener_polinomios()
        if p1 and p2:
            suma = sp.expand(p1 + p2)
            latex_expr = sp.latex(suma)
            self.mostrar_resultado_latex(f"\\text{{Resultado: }}\\quad {latex_expr}")
        else:
            self.mostrar_error("⚠️ Se necesitan dos polinomios válidos para sumar.")


    def multiplicar(self):
        p1, p2 = self.obtener_polinomios()
        if p1 and p2:
            producto = sp.expand(p1 * p2)
            latex_expr = sp.latex(producto)
            self.mostrar_resultado_latex(f"\\text{{Producto: }}\\quad {latex_expr}")
        else:
            self.mostrar_error("⚠️ Se necesitan dos polinomios válidos para multiplicar.")


    def derivar(self):
        p1, _ = self.obtener_polinomios()
        if p1:
            derivada = sp.diff(p1, self.var_x)
            self.resultado.insert("0.0", f"📉 Derivada:\n{sp.pretty(derivada)}\n")
        else: 
            self.mostrar_error("Error al Derivar")
    def integrar(self):
        p1, _ = self.obtener_polinomios()
        if p1:
            integral = sp.integrate(p1, self.var_x)
            self.resultado.insert("0.0", f"∫ Integral:\n{sp.pretty(integral)} + C\n")
        else:
            self.mostrar_error("Error al integrar")

    def evaluar(self):
        p1, _ = self.obtener_polinomios()
        if p1:
            try:
                x_val = float(self.entry_eval.get().strip())
                valor = p1.subs(self.var_x, x_val).evalf()
                self.mostrar_resultado_latex( f"📍 A({x_val}) = {valor}")
            except:
                self.mostrar_error("⚠️ Ingresa un número válido para evaluar.")

    def graficar(self):
        p1, _ = self.obtener_polinomios()
        if p1:
            try:
                if hasattr(self, "canvas") and self.canvas:
                    self.canvas.get_tk_widget().destroy()

                f_lambd = sp.lambdify(self.var_x, p1, modules=["numpy"])
                x_vals = np.linspace(-10, 10, 400)
                y_vals = f_lambd(x_vals)

                fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
                ax.plot(x_vals, y_vals, label=f"A(x) = {sp.sstr(p1).replace('**','^')}", color="blue")

                punto_x = self.entry_eval.get().strip()
                if punto_x:
                    try:
                        x_num = float(punto_x)
                        y_num = f_lambd(x_num)
                        ax.plot(x_num, y_num, 'ro', label=f"A({x_num}) = {round(y_num, 2)}")
                        ax.annotate(f"({x_num}, {round(y_num, 2)})", (x_num, y_num),
                                    textcoords="offset points", xytext=(0, 10), ha='center',
                                    fontsize=9, color='red')
                    except:
                        self.mostrar_error("⚠️ Punto inválido para graficar.")

                ax.axhline(0, color='gray', lw=0.5)
                ax.axvline(0, color='gray', lw=0.5)
                ax.grid(True)
                ax.set_title("Gráfica de A(x)")
                ax.legend()

                # 🎯 Aquí aseguramos que solo se actualice la gráfica
                self.canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
                self.canvas.draw()
                self.canvas.get_tk_widget().pack(fill="both", expand=True)

            except Exception as e:
                self.mostrar_error("❌ Error al graficar.")

                
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
