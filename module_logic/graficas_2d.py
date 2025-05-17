import customtkinter as ctk
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from CTkMessagebox import CTkMessagebox
import re
from pathlib import Path
class Graficas2D(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="📊 Gráficas 2D Avanzadas", font=("Arial", 22)).pack(pady=10)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(expand=True, fill="both", padx=10, pady=10)
        self.tab_graficas = self.tabview.add("Gráficas 2D")

        self.configurar_tab_graficas()

    def configurar_tab_graficas(self):
        ctk.CTkLabel(self.tab_graficas, text="Funciones f(x), separadas por coma").pack(pady=5)

        selector_frame = ctk.CTkFrame(self.tab_graficas)
        selector_frame.pack(pady=5)

        self.example_selector = ctk.CTkOptionMenu(selector_frame, values=[
            "x^2 + 2*x + 1",
            "sen(x) + x^2",
            "√x",
            "ln(x)",
            "sin(x), cos(x), x/5"
        ], command=self.insertar_ejemplo)
        self.example_selector.set("Seleccionar ejemplo")
        self.example_selector.pack()

        self.entry_funcion = ctk.CTkEntry(self.tab_graficas, width=400)
        self.entry_funcion.pack(pady=5)

        rango_frame = ctk.CTkFrame(self.tab_graficas)
        rango_frame.pack(pady=5)

        ctk.CTkLabel(rango_frame, text="x min:").grid(row=0, column=0)
        self.xmin = ctk.CTkEntry(rango_frame, width=80)
        self.xmin.insert(0, "-10")
        self.xmin.grid(row=0, column=1, padx=5)

        ctk.CTkLabel(rango_frame, text="x max:").grid(row=0, column=2)
        self.xmax = ctk.CTkEntry(rango_frame, width=80)
        self.xmax.insert(0, "10")
        self.xmax.grid(row=0, column=3, padx=5)

        opciones_frame = ctk.CTkFrame(self.tab_graficas)
        opciones_frame.pack(pady=5)

        self.ver_derivada = ctk.CTkCheckBox(opciones_frame, text="Mostrar derivada")
        self.ver_integral = ctk.CTkCheckBox(opciones_frame, text="Mostrar integral definida")
        self.ver_derivada.grid(row=0, column=0, padx=10)
        self.ver_integral.grid(row=0, column=1, padx=10)

        boton_frame = ctk.CTkFrame(self.tab_graficas)
        boton_frame.pack(pady=10)
        ctk.CTkButton(boton_frame, text="Graficar", command=self.graficar_funcion).pack(side="left", padx=5)
        ctk.CTkButton(boton_frame, text="Guardar como PNG", command=self.guardar_imagen).pack(side="left", padx=5)
        ctk.CTkButton(boton_frame, text="Limpiar", command=self.limpiar_todo).pack(side="left", padx=5)

        self.canvas_frame = ctk.CTkFrame(self.tab_graficas)
        self.canvas_frame.pack(expand=True, fill="both", pady=5)

        self.fig = None

    def insertar_ejemplo(self, texto):
        self.entry_funcion.delete(0, "end")
        self.entry_funcion.insert(0, texto)

    def preprocesar_entrada(self, texto):
        reemplazos = {
            "^": "**",
            "sen": "sin",
            "√": "sqrt",
            "ln": "log",
            "PI": "pi",
            "π": "pi"
        }
        for viejo, nuevo in reemplazos.items():
            texto = texto.replace(viejo, nuevo)

        funciones = ['sin', 'cos', 'tan', 'log', 'sqrt', 'exp']
        for func in funciones:
            texto = re.sub(rf'\b{func}([a-zA-Z0-9_]+)', rf'{func}(\1)', texto)

        return texto

    def graficar_funcion(self):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        try:
            x = sp.Symbol('x')
            texto_raw = self.entry_funcion.get()
            texto_limpio = self.preprocesar_entrada(texto_raw)
            funciones = [sp.sympify(f.strip()) for f in texto_limpio.split(',') if f.strip()]

            if not funciones:
                raise ValueError("No se ingresaron funciones válidas.")

            xmin = float(self.xmin.get())
            xmax = float(self.xmax.get())
            if xmin >= xmax:
                raise ValueError("x min debe ser menor que x max.")

            x_vals = np.linspace(xmin, xmax, 500)
            self.fig, ax = plt.subplots(figsize=(7, 5), dpi=120)

            for expr in funciones:
                try:
                    f = sp.lambdify(x, expr, modules=["numpy"])
                    y_vals = f(x_vals)
                    y_vals = np.array(y_vals, dtype=np.complex128)
                    y_vals = np.where(np.isreal(y_vals), y_vals.real, np.nan)
                    mask = np.isfinite(y_vals)

                    if not np.any(mask):
                        raise ValueError("Resultado indefinido o complejo en el rango seleccionado.")

                    ax.plot(x_vals[mask], y_vals[mask], label=f"y = {expr}")

                    if self.ver_derivada.get():
                        f_prime = sp.diff(expr, x)
                        f_prime_lambdified = sp.lambdify(x, f_prime, modules=["numpy"])
                        y_prime = f_prime_lambdified(x_vals)
                        y_prime = np.array(y_prime, dtype=np.complex128)
                        y_prime = np.where(np.isreal(y_prime), y_prime.real, np.nan)
                        mask_prime = np.isfinite(y_prime)
                        ax.plot(x_vals[mask_prime], y_prime[mask_prime], linestyle='--', label=f"y' = {f_prime}")

                    if self.ver_integral.get():
                        area = sp.integrate(expr, (x, xmin, xmax))
                        ax.text(0.5, 0.95, f"\u222B f(x) dx = {round(float(area), 4)}", transform=ax.transAxes, ha='center', fontsize=10)

                except Exception as sub_e:
                    ax.text(0.5, 0.5, f"Error en f(x) = {expr}\n{sub_e}", transform=ax.transAxes, ha='center', va='center', fontsize=10, color='red')

            ax.set_title("Gráfica de funciones")
            ax.grid(True, linestyle='--', linewidth=0.5)
            ax.legend()

            canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            toolbar = NavigationToolbar2Tk(canvas, self.canvas_frame)
            toolbar.update()
            toolbar.pack(side="bottom", fill="x")

        except Exception as e:
            CTkMessagebox(title="Error de sintaxis", message=f"No se pudo interpretar una o más funciones:\n{e}", icon="cancel")

    def guardar_imagen(self):
        if self.fig:
            output_path = Path.home() / "Downloads" / "grafica3D.png"
            self.fig.savefig(output_path)
            CTkMessagebox(title="Guardado", message=f"Imagen guardada en:\n{output_path}", icon="check")
           
    def limpiar_todo(self):
        self.entry_funcion.delete(0, "end")
        self.xmin.delete(0, "end")
        self.xmax.delete(0, "end")
        self.xmin.insert(0, "-10")
        self.xmax.insert(0, "10")
        self.ver_derivada.deselect()
        self.ver_integral.deselect() 
        self.example_selector.set("Seleccionar ejemplo")
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        self.fig = None
