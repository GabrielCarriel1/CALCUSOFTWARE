import customtkinter as ctk
from module_logic.distribuciones import GeneradorDistribuciones
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import tkinter.messagebox as msgbox
import tkinter as tk


class DistribucionesUI(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(1, weight=1)

        self.entrada_frame = ctk.CTkFrame(self)
        self.entrada_frame.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)

        self.resultado_frame = ctk.CTkScrollableFrame(self)
        self.resultado_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.resultado_frame.grid_columnconfigure(0, weight=1)
        self.resultado_frame.grid_rowconfigure(0, weight=1)

        self._crear_entradas()
        self._crear_salida()

        self.canvas_montecarlo = None

    def _toggle_inputs(self):
        estado = "normal" if self.checkbox_congruencial.get() else "disabled"
        for widget in [self.semilla, self.a, self.c, self.m]:
            widget.configure(state=estado)

    def _crear_entradas(self):
        ctk.CTkLabel(self.entrada_frame, text="Método Monte Carlo", font=("Arial", 14, "bold")).pack(pady=(20, 5))

        ctk.CTkButton(self.entrada_frame, text="Estimar Área", command=self.estimar_area_montecarlo).pack(pady=5)

        ctk.CTkLabel(self.entrada_frame, text="Parámetros del Generador", font=("Arial", 16, "bold")).pack(pady=10)
        self.semilla = ctk.CTkEntry(self.entrada_frame, placeholder_text="Semilla", state="disabled")
        self.a = ctk.CTkEntry(self.entrada_frame, placeholder_text="Multiplicador a", state="disabled")
        self.c = ctk.CTkEntry(self.entrada_frame, placeholder_text="Incremento c", state="disabled")
        self.m = ctk.CTkEntry(self.entrada_frame, placeholder_text="Módulo m", state="disabled")
        self.n = ctk.CTkEntry(self.entrada_frame, placeholder_text="Cantidad de números")

        for widget in [self.semilla, self.a, self.c, self.m, self.n]:
            widget.pack(pady=2, fill="x")

        ctk.CTkLabel(self.entrada_frame, text="Distribución", font=("Arial", 14)).pack(pady=(10, 5))
        self.distribucion_selector = ctk.CTkOptionMenu(self.entrada_frame, values=["Uniforme", "Poisson", "Exponencial", "Normal", "Binomial"], command=self._cambiar_distribucion)
        self.distribucion_selector.set("Uniforme")
        self.distribucion_selector.pack(pady=(0, 10), fill="x")

        ctk.CTkLabel(self.entrada_frame, text="Ejemplos", font=("Arial", 14)).pack(pady=(5, 5))
        self.selector_ejemplo = ctk.CTkOptionMenu(self.entrada_frame, values=["Ejemplo 1", "Ejemplo 2"], command=self._cargar_ejemplo)
        self.selector_ejemplo.pack(pady=(0, 10), fill="x")

        self.lambda_poisson = None

        self.checkbox_congruencial = ctk.CTkCheckBox(self.entrada_frame, text="Usar generador congruencial", command=self._toggle_inputs)
        self.checkbox_congruencial.pack(pady=(10, 5))

        self.generar_btn = ctk.CTkButton(self.entrada_frame, text="Generar", command=self.generar_datos)
        self.generar_btn.pack(pady=5)

    def _crear_salida(self):
        self.texto_resultado = ctk.CTkTextbox(self.resultado_frame, font=("Courier", 12), corner_radius=5, height=300)
        self.texto_resultado.pack(expand=True, fill="both")

    def _cargar_ejemplo(self, seleccion):
        ejemplos = {
            "Ejemplo 1": ("7", "5", "3", "16", "20", "Uniforme"),
            "Ejemplo 2": ("1", "7", "0", "31", "15", "Poisson")
        }
        if seleccion in ejemplos:
            vals = ejemplos[seleccion]
            for entry, val in zip([self.semilla, self.a, self.c, self.m, self.n], vals[:-1]):
                entry.configure(state="normal")
                entry.delete(0, 'end')
                entry.insert(0, val)
            self.distribucion_selector.set(vals[-1])
            if not self.checkbox_congruencial.get():
                for entry in [self.semilla, self.a, self.c, self.m]:
                    entry.configure(state="disabled")

    def _cambiar_distribucion(self, seleccion):
        if self.lambda_poisson:
            self.lambda_poisson.destroy()
            self.lambda_poisson = None
        if seleccion == "Poisson":
            self.lambda_poisson = ctk.CTkEntry(self.entrada_frame, placeholder_text="λ (solo Poisson)")
            self.lambda_poisson.pack(pady=2, fill="x")

    def estimar_area_montecarlo(self):
        try:
            n = int(self.n.get())
            x_vals = np.random.rand(n)
            y_vals = np.random.rand(n)
            y_x2 = x_vals ** 2
            y_sqrt = np.sqrt(x_vals)

            interiores_ambas = np.logical_and(y_vals >= y_x2, y_vals <= y_sqrt)
            area_ambas = np.sum(interiores_ambas) / n

            self.texto_resultado.delete("0.0", "end")
            self.texto_resultado.insert("end", f"Resumen estimaci\u00f3n Monte Carlo:\n")
            self.texto_resultado.insert("end", f"- Total de puntos: {n}\n")
            self.texto_resultado.insert("end", f"- Puntos entre x\u00b2 y \u221ax: {np.sum(interiores_ambas)}\n")
            self.texto_resultado.insert("end", f"- \u00c1rea estimada (entre): {area_ambas:.5f}\n\n")

            self.texto_resultado.insert("end", f"{'n°':<5}{'x':<10}{'y':<10}{'Dentro (x² < y < √x)':<25}\n")
            self.texto_resultado.insert("end", "="*50 + "\n")
            for i in range(n):
                self.texto_resultado.insert("end", f"{i+1:<5}{x_vals[i]:<10.4f}{y_vals[i]:<10.4f}{int(interiores_ambas[i]):<25}\n")

            if hasattr(self, "canvas_montecarlo") and self.canvas_montecarlo is not None:
                self.canvas_montecarlo.get_tk_widget().destroy()

            fig, ax = plt.subplots(figsize=(6, 5))
            ax.plot(np.sort(x_vals), np.sort(y_x2), label="f(x)=x²", linewidth=2)
            ax.plot(np.sort(x_vals), np.sort(y_sqrt), label="f(x)=√x", linestyle="--", linewidth=2)
            ax.scatter(x_vals[interiores_ambas], y_vals[interiores_ambas], s=15, label="Dentro ambas")
            ax.scatter(x_vals[~interiores_ambas], y_vals[~interiores_ambas], s=15, label="Fuera")
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.legend(frameon=True, loc="upper right")
            ax.grid(True, linestyle=":", alpha=0.6)
            ax.set_title("Monte Carlo - Área entre x² y √x", fontsize=12)

            self.canvas_montecarlo = FigureCanvasTkAgg(fig, master=self.resultado_frame)
            self.canvas_montecarlo.draw()
            self.canvas_montecarlo.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            msgbox.showerror("Error en Monte Carlo", f"Ocurrió un error: {e}")


    def generar_datos(self):
        try:
            usar_congruencial = self.checkbox_congruencial.get()
            n = int(self.n.get())
            distribucion = self.distribucion_selector.get()

            if usar_congruencial:
                semilla = int(self.semilla.get())
                a = int(self.a.get())
                c = int(self.c.get())
                m = int(self.m.get())
                gen = GeneradorDistribuciones(semilla, a, c, m, n)
                x_vals, u_vals = gen.generar_congruencial()
            else:
                u_vals = np.random.rand(n).tolist()
                x_vals = list(range(n))
                gen = GeneradorDistribuciones(0, 0, 0, 1, n)  # Dummy gen para funciones

            if distribucion == "Uniforme":
                transformados = u_vals
            elif distribucion == "Poisson":
                lam = float(self.lambda_poisson.get()) if self.lambda_poisson and self.lambda_poisson.get() else 4.0
                transformados = gen.aplicar_poisson(u_vals, lam)
            elif distribucion == "Exponencial":
                transformados = gen.aplicar_exponencial(u_vals)
            elif distribucion == "Normal":
                transformados = gen.aplicar_normal(u_vals)
            elif distribucion == "Binomial":
                transformados = gen.aplicar_binomial(u_vals, n=10, p=0.5)  # puedes parametrizar esto luego
            else:
                raise ValueError("Distribución no soportada.")

            tabla = gen.construir_tabla(x_vals, u_vals, transformados)

            self.texto_resultado.delete("0.0", "end")
            self.texto_resultado.insert("end", f"{'n':<5}{'Xn':<10}{'Un':<15}{'f(Un)':<15}{'X^2':<15}{'√X²':<10}\n")
            self.texto_resultado.insert("end", "="*70 + "\n")
            for fila in tabla:
                self.texto_resultado.insert("end", f"{fila['n']:<5}{fila['Xn']:<10}{fila['Un']:<15.6f}{fila['f(Un)']:<15.6f}{fila['X²']:<15.6f}{fila['√X²']:<10.6f}\n")

        except Exception as e:
            msgbox.showerror("Error al generar datos", f"Ocurrió un error: {e}")
