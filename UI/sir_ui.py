import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from module_logic.modelo_sir import ModeloSIR


class ModeloSIR_UI(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  # lado izquierdo fijo
        self.grid_columnconfigure(1, weight=1)  # lado derecho expandible

        # === Sección izquierda (Entradas + Ejemplos) ===
        self.izquierda = ctk.CTkFrame(self)
        self.izquierda.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        self.entries = {}
        for label, clave in [
            ("Población Total (N)", "N"),
            ("Infectados Iniciales (I₀)", "I0"),
            ("Tasa de Infección β", "beta"),
            ("Tasa de Recuperación γ", "gamma"),
            ("Días a Simular", "dias")
        ]:
            frame = ctk.CTkFrame(self.izquierda)
            frame.pack(pady=5, padx=5, fill="x")
            ctk.CTkLabel(frame, text=label, width=180).pack(side="left")
            entry = ctk.CTkEntry(frame)
            entry.pack(side="left", fill="x", expand=True)
            self.entries[clave] = entry

        # === Menú de ejemplos ===
        self.ejemplos_sir = {
            "Ejemplo 1: Brote leve": {"N": 100000, "I0": 1, "beta": 0.1, "gamma": 0.2, "dias": 365},
            "Ejemplo 2: Brote moderado": {"N": 34000, "I0": 5, "beta": 0.3, "gamma": 0.1, "dias": 365*2},
            "Ejemplo 3: Contagio rápido": {"N": 445500, "I0": 10, "beta": 0.5, "gamma": 0.1, "dias": 600}
        }

        self.ejemplo_var = ctk.StringVar(value="Ejemplo 1: Brote leve")
        ejemplo_frame = ctk.CTkFrame(self.izquierda)
        ejemplo_frame.pack(pady=10, fill="x", padx=5)

        ctk.CTkLabel(ejemplo_frame, text="Ejemplos:").pack(side="left", padx=(0, 5))
        self.ejemplo_menu = ctk.CTkOptionMenu(
            ejemplo_frame,
            variable=self.ejemplo_var,
            values=list(self.ejemplos_sir.keys())
        )
        self.ejemplo_menu.pack(side="left", padx=5)

        ctk.CTkButton(ejemplo_frame, text="📥 Cargar Ejemplo", command=self.cargar_ejemplo).pack(side="left", padx=5)

        # === Botón de simulación ===
        ctk.CTkButton(self.izquierda, text="▶ Simular", command=self.simular).pack(pady=10, padx=5)

        # === Sección derecha (Gráfica + conclusión) ===
        self.derecha = ctk.CTkFrame(self)
        self.derecha.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.derecha.grid_rowconfigure(0, weight=1)  # Gráfica
        self.derecha.grid_rowconfigure(1, weight=1)  # Conclusión
        self.derecha.grid_columnconfigure(0, weight=1)

        # Mitad superior: gráfica
        self.frame_grafico = ctk.CTkFrame(self.derecha)
        self.frame_grafico.grid(row=0, column=0, sticky="nsew", padx=5, pady=(5, 2))

        # Mitad inferior: conclusión
        self.resultado_conclusion = ctk.CTkTextbox(self.derecha)
        self.resultado_conclusion.grid(row=1, column=0, sticky="nsew", padx=5, pady=(2, 5))

    def cargar_ejemplo(self):
        seleccion = self.ejemplo_var.get()
        if seleccion in self.ejemplos_sir:
            ejemplo = self.ejemplos_sir[seleccion]
            for clave, valor in ejemplo.items():
                self.entries[clave].delete(0, "end")
                self.entries[clave].insert(0, str(valor))

    def simular(self):
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        try:
            N = int(self.entries["N"].get())
            I0 = int(self.entries["I0"].get())
            beta = float(self.entries["beta"].get())
            gamma = float(self.entries["gamma"].get())
            dias = int(self.entries["dias"].get())

            if N <= 0:
                raise ValueError("Población total debe ser mayor a 0.")
            if I0 < 0 or I0 > N:
                raise ValueError("Infectados iniciales deben estar entre 0 y N.")
            if beta <= 0 or gamma <= 0:
                raise ValueError("Tasas β y γ deben ser mayores a 0.")
            if dias <= 0:
                raise ValueError("Días debe ser mayor a 0.")

        except ValueError as e:
            ctk.CTkLabel(self.frame_grafico, text=f"❌ Error: {e}").pack()
            return

        modelo = ModeloSIR(N, I0, beta, gamma, dias)
        t, S, I, R = modelo.resolver()

        R0 = beta / gamma
        pico_infeccion = max(I)
        dia_pico = list(I).index(pico_infeccion)

        # Gráfica
        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.plot(t, S, label="Susceptibles")
        ax.plot(t, I, label="Infectados")
        ax.plot(t, R, label="Recuperados")
        ax.axvline(x=dia_pico, color='gray', linestyle='--', alpha=0.6)
        ax.annotate(f"Pico día {dia_pico}", xy=(dia_pico, pico_infeccion),
                    xytext=(dia_pico + 3, pico_infeccion),
                    arrowprops=dict(arrowstyle='->'), fontsize=9)

        ax.set_title("Modelo Epidemiológico SIR")
        ax.set_xlabel("Días")
        ax.set_ylabel("Personas")
        ax.grid(True)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Mostrar conclusión
        self.resultado_conclusion.delete("0.0", "end")
        conclusion = self.interpretar_resultado(R0, I, S, R, dias, dia_pico, pico_infeccion)
        self.resultado_conclusion.insert("end", conclusion)

    def interpretar_resultado(self, R0, I, S, R, dias, dia_pico, pico_infeccion):
        if R0 < 1:
            estado_R0 = "🟢 La epidemia tenderá a desaparecer con el tiempo."
        elif R0 == 1:
            estado_R0 = "🟡 La epidemia se mantendrá estable (endémica)."
        else:
            estado_R0 = "🔴 La epidemia crecerá inicialmente y puede volverse un brote importante."

        conclusion = (
            f"📊 Conclusión del modelo SIR:\n"
            f"- R₀ (número básico de reproducción) = {R0:.2f}\n"
            f"  {estado_R0}\n"
            f"- La epidemia alcanza su punto máximo de infectados el día {dia_pico}.\n"
            f"- En ese momento, aproximadamente {int(pico_infeccion)} personas están infectadas.\n"
            f"- Al final de los {dias} días, {int(R[-1])} personas se habrán recuperado.\n"
            f"- El número de susceptibles disminuirá a {int(S[-1])} personas.\n"
        )
        return conclusion
