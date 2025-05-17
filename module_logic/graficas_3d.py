import customtkinter as ctk
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from CTkMessagebox import CTkMessagebox
import re
from pathlib import Path

class Graficas3D(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="📈 Gráficas 3D", font=("Arial", 22)).pack(pady=10)

        self.selector = ctk.CTkOptionMenu(self, values=[
            "x^2 + y^2",
            "sin(x)*cos(y)",
            "√(x^2 + y^2)",
            "exp(-x^2 - y^2)",
            "ln(x^2 + y^2)"
        ], command=self.insertar_ejemplo)
        self.selector.set("Seleccionar ejemplo")
        self.selector.pack(pady=5)

        self.entrada_funcion = ctk.CTkEntry(self, width=500, placeholder_text="f(x, y) = x^2 + y^2")
        self.entrada_funcion.pack(pady=5)

        rango_frame = ctk.CTkFrame(self)
        rango_frame.pack(pady=5)

        self.xmin = self._crear_entrada_rango(rango_frame, "x min", -5, 0)
        self.xmax = self._crear_entrada_rango(rango_frame, "x max", 5, 1)
        self.ymin = self._crear_entrada_rango(rango_frame, "y min", -5, 2)
        self.ymax = self._crear_entrada_rango(rango_frame, "y max", 5, 3)

        resolucion_frame = ctk.CTkFrame(self)
        resolucion_frame.pack(pady=5)
        ctk.CTkLabel(resolucion_frame, text="Resolución de malla:").pack(side="left")
        self.resolucion_selector = ctk.CTkOptionMenu(resolucion_frame, values=["Baja", "Media", "Alta"])
        self.resolucion_selector.set("Media")
        self.resolucion_selector.pack(side="left", padx=5)

        boton_frame = ctk.CTkFrame(self)
        boton_frame.pack(pady=10)
        ctk.CTkButton(boton_frame, text="Graficar 3D", command=self.graficar_funcion).pack(side="left", padx=5)
        ctk.CTkButton(boton_frame, text="Guardar imagen", command=self.guardar_imagen).pack(side="left", padx=5)
        ctk.CTkButton(boton_frame, text="Animar", command=self.animar_rotacion).pack(side="left", padx=5)
        ctk.CTkButton(boton_frame, text="Limpiar", command=self.limpiar_todo).pack(side="left", padx=5)

        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.pack(expand=True, fill="both", pady=5)

        self.fig = None
        self.ax = None

    def insertar_ejemplo(self, texto):
        self.entrada_funcion.delete(0, "end")
        self.entrada_funcion.insert(0, texto)

    def _crear_entrada_rango(self, frame, label_text, default_value, column):
        ctk.CTkLabel(frame, text=label_text).grid(row=0, column=column)
        entry = ctk.CTkEntry(frame, width=80)
        entry.insert(0, str(default_value))
        entry.grid(row=1, column=column, padx=5)
        return entry

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
            x, y = sp.symbols('x y')
            texto_raw = self.entrada_funcion.get()
            texto_limpio = self.preprocesar_entrada(texto_raw)
            expr = sp.sympify(texto_limpio)
            f = sp.lambdify((x, y), expr, modules=["numpy"])

            xmin = float(self.xmin.get())
            xmax = float(self.xmax.get())
            ymin = float(self.ymin.get())
            ymax = float(self.ymax.get())

            if xmin >= xmax or ymin >= ymax:
                self.mostrar_error("Rangos inválidos.")

            resolucion = self.resolucion_selector.get()
            puntos = {"Baja": 30, "Media": 60, "Alta": 100}[resolucion]

            X, Y = np.meshgrid(np.linspace(xmin, xmax, puntos), np.linspace(ymin, ymax, puntos))
            Z = f(X, Y)

            Z = np.array(Z, dtype=np.complex128)
            Z = np.where(np.isreal(Z), Z.real, np.nan)
            mask = np.isfinite(Z)
            if not np.any(mask):
               self.mostrar_error("La función devuelve valores no válidos en el dominio dado.")

            self.fig = plt.figure(figsize=(8, 6))
            self.ax = self.fig.add_subplot(111, projection='3d')
            self.ax.plot_surface(X, Y, Z, cmap='viridis')
            self.ax.set_title("Gráfica 3D")

            canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            self.mostrar_error("Ocurrio un error al graficar, datos invalidos.")

    def guardar_imagen(self):
        if self.fig:
            output_path = Path.home() / "Downloads" / "grafica3D.png"
            self.fig.savefig(output_path)
            CTkMessagebox(title="Guardado", message=f"Imagen guardada en:\n{output_path}", icon="check")

    def animar_rotacion(self):
        if not self.fig or not self.ax:
            CTkMessagebox(title="Error", message="Primero genera una gráfica.", icon="cancel")
            return

        def update(angle):
            self.ax.view_init(elev=30, azim=angle)
            self.fig.canvas.draw()

        anim = FuncAnimation(self.fig, update, frames=np.arange(0, 360, 2), interval=50)
        self.fig.canvas.draw()

    def limpiar_todo(self):
        self.entrada_funcion.delete(0, "end")
        self.xmin.delete(0, "end")
        self.xmax.delete(0, "end")
        self.ymin.delete(0, "end")
        self.ymax.delete(0, "end")
        self.xmin.insert(0, "-5")
        self.xmax.insert(0, "5")
        self.ymin.insert(0, "-5")
        self.ymax.insert(0, "5")
        self.selector.set("Seleccionar ejemplo")
        self.resolucion_selector.set("Media")
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        self.fig = None
        self.ax = None
    def mostrar_error(self, mensaje):
            CTkMessagebox(title="❌ Error", message=mensaje, icon="cancel")