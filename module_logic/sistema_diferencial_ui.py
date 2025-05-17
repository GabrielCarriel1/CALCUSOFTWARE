import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from CTkMessagebox import CTkMessagebox

class SistemaDiferencialUI(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(1, weight=1)

        self.entrada_frame = ctk.CTkFrame(self)
        self.entrada_frame.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)

        self.resultado_frame = ctk.CTkFrame(self)
        self.resultado_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.resultado_frame.grid_rowconfigure((0, 1), weight=1)
        self.resultado_frame.grid_columnconfigure(0, weight=1)

        self._crear_entradas()
        self._crear_salidas()

    def _crear_entradas(self):
        ctk.CTkLabel(self.entrada_frame, text="Sistema de ecuaciones", font=("Arial", 16, "bold")).pack(anchor="w", pady=(0, 10))

        self.ejemplo_selector = ctk.CTkOptionMenu(self.entrada_frame, values=["Ejemplo 1", "Ejemplo 2"], command=self._cargar_ejemplo)
        self.ejemplo_selector.pack(fill="x", pady=(0, 10))

        ecuacion_frame1 = ctk.CTkFrame(self.entrada_frame)
        ecuacion_frame1.pack(fill="x", pady=2)
        ctk.CTkLabel(ecuacion_frame1, text="dx/dt =").pack(side="left")
        self.ecuacion1 = ctk.CTkEntry(ecuacion_frame1)
        self.ecuacion1.pack(side="left", fill="x", expand=True)

        ecuacion_frame2 = ctk.CTkFrame(self.entrada_frame)
        ecuacion_frame2.pack(fill="x", pady=2)
        ctk.CTkLabel(ecuacion_frame2, text="dy/dt =").pack(side="left")
        self.ecuacion2 = ctk.CTkEntry(ecuacion_frame2)
        self.ecuacion2.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(self.entrada_frame, text="Condiciones iniciales", font=("Arial", 14, "bold")).pack(anchor="w", pady=(10, 5))
        self.x0_entry = ctk.CTkEntry(self.entrada_frame, placeholder_text="x(0)", width=100)
        self.y0_entry = ctk.CTkEntry(self.entrada_frame, placeholder_text="y(0)", width=100)
        self.x0_entry.pack(pady=2)
        self.y0_entry.pack(pady=2)

        ctk.CTkLabel(self.entrada_frame, text="Parámetros de integración", font=("Arial", 14, "bold")).pack(anchor="w", pady=(10, 5))
        self.tiempo_total = ctk.CTkEntry(self.entrada_frame, placeholder_text="Tiempo total", width=100)
        self.paso = ctk.CTkEntry(self.entrada_frame, placeholder_text="Paso h", width=100)
        self.tiempo_total.pack(pady=2)
        self.paso.pack(pady=2)

        ctk.CTkLabel(self.entrada_frame, text="Método numérico", font=("Arial", 14, "bold")).pack(anchor="w", pady=(10, 5))
        self.metodo_selector = ctk.CTkOptionMenu(self.entrada_frame, values=["Ninguno", "Euler", "Runge-Kutta 4", "Analítico"])
        self.metodo_selector.set("Ninguno")
        self.metodo_selector.pack(fill="x", pady=(0, 10))

        self.btn_resolver = ctk.CTkButton(self.entrada_frame, text="Resolver", command=self.resolver_sistema)
        self.btn_resolver.pack(pady=(10, 0))

        self.resultado_texto = ctk.CTkTextbox(self.entrada_frame, height=180, corner_radius=5)
        self.resultado_texto.pack(fill="x", pady=(10, 0))

    def _crear_salidas(self):
        self.canvas_frame = ctk.CTkFrame(self.resultado_frame)
        self.canvas_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 5))

        self.tabla_texto = ctk.CTkTextbox(self.resultado_frame, height=160, corner_radius=5, font=("Courier", 12))
        self.tabla_texto.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.tabla_texto.configure(wrap="none")

    def _cargar_ejemplo(self, seleccion):
        if seleccion == "Ejemplo 1":
            self.ecuacion1.delete(0, "end")
            self.ecuacion1.insert(0, "0.3*x + 0.1*y")
            self.ecuacion2.delete(0, "end")
            self.ecuacion2.insert(0, "0.02*x - 0.05*y")
            self.x0_entry.delete(0, "end")
            self.x0_entry.insert(0, "10")
            self.y0_entry.delete(0, "end")
            self.y0_entry.insert(0, "5")
            self.tiempo_total.delete(0, "end")
            self.tiempo_total.insert(0, "20")
            self.paso.delete(0, "end")
            self.paso.insert(0, "1")
        elif seleccion == "Ejemplo 2":
            self.ecuacion1.delete(0, "end")
            self.ecuacion1.insert(0, "-0.1*x + 0.2*y")
            self.ecuacion2.delete(0, "end")
            self.ecuacion2.insert(0, "-0.3*x - 0.4*y")
            self.x0_entry.delete(0, "end")
            self.x0_entry.insert(0, "8")
            self.y0_entry.delete(0, "end")
            self.y0_entry.insert(0, "4")
            self.tiempo_total.delete(0, "end")
            self.tiempo_total.insert(0, "15")
            self.paso.delete(0, "end")
            self.paso.insert(0, "0.5")

    def _validar_entradas(self):
        campos = [self.ecuacion1.get(), self.ecuacion2.get(), self.x0_entry.get(), self.y0_entry.get(), self.tiempo_total.get(), self.paso.get()]
        if any(not campo.strip() for campo in campos):
            raise ValueError("Todos los campos deben estar completos.")
        float(self.x0_entry.get())
        float(self.y0_entry.get())
        float(self.tiempo_total.get())
        float(self.paso.get())

    def resolver_sistema(self):
        try:
            self._validar_entradas()
            f1 = self.ecuacion1.get().strip()
            f2 = self.ecuacion2.get().strip()
            dxdt = lambda x, y: eval(f1)
            dydt = lambda x, y: eval(f2)

            x0 = float(self.x0_entry.get())
            y0 = float(self.y0_entry.get())
            T = float(self.tiempo_total.get())
            h = float(self.paso.get())
            metodo = self.metodo_selector.get()
            if metodo == "Ninguno":
                raise ValueError("Por favor selecciona un método para continuar.")

            t_vals = np.arange(0, T + h, h)
            x_vals = [x0]
            y_vals = [y0]

            for i in range(1, len(t_vals)):
                x_prev = x_vals[-1]
                y_prev = y_vals[-1]

                if metodo == "Euler":
                    x_next = x_prev + h * dxdt(x_prev, y_prev)
                    y_next = y_prev + h * dydt(x_prev, y_prev)

                elif metodo == "Runge-Kutta 4":
                    k1x = h * dxdt(x_prev, y_prev)
                    k1y = h * dydt(x_prev, y_prev)

                    k2x = h * dxdt(x_prev + k1x/2, y_prev + k1y/2)
                    k2y = h * dydt(x_prev + k1x/2, y_prev + k1y/2)

                    k3x = h * dxdt(x_prev + k2x/2, y_prev + k2y/2)
                    k3y = h * dydt(x_prev + k2x/2, y_prev + k2y/2)

                    k4x = h * dxdt(x_prev + k3x, y_prev + k3y)
                    k4y = h * dydt(x_prev + k3x, y_prev + k3y)

                    x_next = x_prev + (k1x + 2*k2x + 2*k3x + k4x) / 6
                    y_next = y_prev + (k1y + 2*k2y + 2*k3y + k4y) / 6

                elif metodo == "Analítico":
                    try:
                        from scipy.linalg import expm
                        def coef(eq_str):
                            eq_str = eq_str.replace(" ", "").replace("-", "+-")
                            terms = eq_str.split("+")
                            ax = ay = 0
                            for term in terms:
                                if "*x" in term:
                                    ax = float(term.replace("*x", ""))
                                elif "*y" in term:
                                    ay = float(term.replace("*y", ""))
                            return ax, ay

                        a, b = coef(f1)
                        c, d = coef(f2)
                        A = np.array([[a, b], [c, d]])
                        t_vals = np.arange(0, T + h, h)
                        x_vals = []
                        y_vals = []
                        x0_vec = np.array([[x0], [y0]])
                        for t in t_vals:
                            try:
                                exp_At = expm(A * t)
                                sol = np.dot(exp_At, x0_vec)
                                x_vals.append(sol[0, 0])
                                y_vals.append(sol[1, 0])
                            except Exception as e:
                                raise ValueError(f"No se pudo calcular exp(At) en t={t}: {e}")
                    except ImportError:
                        CTkMessagebox(title="Requiere scipy", message="El método analítico requiere 'scipy'. Por favor instálalo para continuar.", icon="warning")
                        raise ImportError("El método analítico requiere 'scipy'. Por favor instálalo para continuar.")
                else:
                    raise ValueError("Método no soportado.")

                if metodo in ("Euler", "Runge-Kutta 4"):
                  x_vals.append(x_next)
                  y_vals.append(y_next)

            self._graficar(t_vals, x_vals, y_vals)
            self._mostrar_tabla(t_vals, x_vals, y_vals)
            self._mostrar_valores_vectores(f1, f2)

        except Exception as e:
            CTkMessagebox(title="Error", message=str(e), icon="cancel")

    def _graficar(self, t, x, y):
        # Comparación visual si se selecciona Runge-Kutta 4
        metodo = self.metodo_selector.get()
        mostrar_comparacion = metodo == "Runge-Kutta 4"
        fig, ax = plt.subplots(figsize=(5, 3))
        if mostrar_comparacion:
            f1 = self.ecuacion1.get().strip()
            f2 = self.ecuacion2.get().strip()
            dxdt = lambda x, y: eval(f1)
            dydt = lambda x, y: eval(f2)
            h = float(self.paso.get())
            T = float(self.tiempo_total.get())
            x0 = float(self.x0_entry.get())
            y0 = float(self.y0_entry.get())
            t_vals = np.arange(0, T + h, h)
            x_euler = [x0]
            y_euler = [y0]
            for i in range(1, len(t_vals)):
                x_prev = x_euler[-1]
                y_prev = y_euler[-1]
                x_next = x_prev + h * dxdt(x_prev, y_prev)
                y_next = y_prev + h * dydt(x_prev, y_prev)
                x_euler.append(x_next)
                y_euler.append(y_next)
            ax.plot(t, x_euler, label="x(t) - Euler", linestyle="--")
            ax.plot(t, y_euler, label="y(t) - Euler", linestyle="--")
        ax.plot(t, x, label="x(t)", marker="o")
        ax.plot(t, y, label="y(t)", marker="s")
        ax.set_title(f"Solución del Sistema - Método: {metodo}")
        ax.set_xlabel("t")
        ax.set_ylabel("x(t), y(t)")
        ax.grid(True)
        ax.text(0.99, 0.01, f"Método: {metodo}Paso h: {self.paso.get()}T: {self.tiempo_total.get()}",
                transform=ax.transAxes, fontsize=8, va='bottom', ha='right',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f0f0', edgecolor='gray'))
        ax.legend()

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def _mostrar_tabla(self, t, x, y):
        self.tabla_texto.delete("0.0", "end")
        self.tabla_texto.insert("end", f"{'t':<10}{'x(t)':<15}{'y(t)':<15}\n")
        self.tabla_texto.insert("end", "="*40 + "\n")
        for i in range(len(t)):
            self.tabla_texto.insert("end", f"{t[i]:<10.4f}{x[i]:<15.6f}{y[i]:<15.6f}\n")

    def _mostrar_valores_vectores(self, f1_str, f2_str):
        try:
            def coef(eq_str):
                eq_str = eq_str.replace(" ", "").replace("-", "+-")
                terms = eq_str.split("+")
                ax = ay = 0
                for term in terms:
                    if "*x" in term:
                        ax = float(term.replace("*x", ""))
                    elif "*y" in term:
                        ay = float(term.replace("*y", ""))
                return ax, ay

            a, b = coef(f1_str)
            c, d = coef(f2_str)
            A = np.array([[a, b], [c, d]])
            vals, vecs = np.linalg.eig(A)

            self.resultado_texto.delete("0.0", "end")
            for i, val in enumerate(vals):
                self.resultado_texto.insert("end", f"λ = {val:.6f}\nVector: {vecs[:,i]}\n")
        except Exception as e:
            self.resultado_texto.insert("end", f"❌ Error al calcular autovalores: {e}\n")
