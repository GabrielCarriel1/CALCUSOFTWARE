import customtkinter as ctk
import sympy as sp
import re
from CTkMessagebox import CTkMessagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DerivacionIntegracion(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.pack(padx=20, pady=20)

        ctk.CTkLabel(self, text="🧠 Derivación e Integración", font=("Arial", 22)).pack(pady=10)

        self.x, self.y = sp.symbols('x y')

        self.selector = ctk.CTkOptionMenu(self, values=[
            "x^2",
            "sin(x)*cos(x)",
            "exp(x^2)",
            "ln(x^2 + 1)",
            "x^2*sin(x) + cos(x)"
        ], command=self.insertar_ejemplo)
        self.selector.set("Seleccionar ejemplo")
        self.selector.pack(pady=5)

        self.entrada = ctk.CTkEntry(self, width=500, placeholder_text="Ej: x^2 * sin(x) + cos(x)")
        self.entrada.pack(pady=5)

        variable_frame = ctk.CTkFrame(self)
        variable_frame.pack(pady=5)
        ctk.CTkLabel(variable_frame, text="📌 Variable:", font=("Arial", 14)).pack(side="left", padx=5)
        self.var_elegida = ctk.CTkComboBox(variable_frame, values=["x", "y"], width=80)
        self.var_elegida.set("x")
        self.var_elegida.pack(side="left", padx=5)

        limites_frame = ctk.CTkFrame(self)
        limites_frame.pack(pady=5)
        ctk.CTkLabel(limites_frame, text="∫ Límite inferior:", font=("Arial", 13)).pack(side="left", padx=5)
        self.lim_inf = ctk.CTkEntry(limites_frame, width=70, placeholder_text="a")
        self.lim_inf.pack(side="left", padx=5)

        ctk.CTkLabel(limites_frame, text="Límite superior:", font=("Arial", 13)).pack(side="left", padx=5)
        self.lim_sup = ctk.CTkEntry(limites_frame, width=70, placeholder_text="b")
        self.lim_sup.pack(side="left", padx=5)

        self.resultado_frame = ctk.CTkFrame(self, height=100, width=500)
        self.resultado_frame.pack(pady=10)
        self.resultado_frame.pack_propagate(False)
        self.canvas_resultado = None

        btns = ctk.CTkFrame(self)
        btns.pack(pady=10)
        ctk.CTkButton(btns, text="📉 Derivar", command=self.derivar, width=120).pack(side="left", padx=10)
        ctk.CTkButton(btns, text="∫ Integrar", command=self.integrar, width=120).pack(side="left", padx=10)
        ctk.CTkButton(btns, text="🧽 Limpiar", command=self.limpiar, width=120).pack(side="left", padx=10)

    def insertar_ejemplo(self, texto):
        self.entrada.delete(0, "end")
        self.entrada.insert(0, texto)

    def limpiar(self):
        self.entrada.delete(0, "end")
        self.lim_inf.delete(0, "end")
        self.lim_sup.delete(0, "end")
        self.var_elegida.set("x")
        self.selector.set("Seleccionar ejemplo")
        if self.canvas_resultado:
            self.canvas_resultado.get_tk_widget().destroy()
            self.canvas_resultado = None

    def limpiar_entrada(self, texto):
        texto = texto.replace(" ", "")
        reemplazos = {
            "^": "**",
            "sen": "sin",
            "ln": "log",
            "PI": "pi",
            "π": "pi",
            "√": "sqrt"
        }
        for viejo, nuevo in reemplazos.items():
            texto = texto.replace(viejo, nuevo)

        funciones = ['sin', 'cos', 'tan', 'log', 'sqrt', 'exp']
        for func in funciones:
            texto = re.sub(rf'\b{func}([a-zA-Z0-9_]+)', rf'{func}(\1)', texto)

        return texto

    def mostrar_latex(self, expresion_latex):
        if self.canvas_resultado:
            self.canvas_resultado.get_tk_widget().destroy()

        fig, ax = plt.subplots(figsize=(4.5, 0.9), dpi=100)
        ax.text(0.5, 0.5, f"${expresion_latex}$", fontsize=14, ha="center", va="center")
        ax.axis("off")

        self.canvas_resultado = FigureCanvasTkAgg(fig, master=self.resultado_frame)
        self.canvas_resultado.draw()
        self.canvas_resultado.get_tk_widget().pack(fill="both", expand=True)

    def derivar(self):
        expr_str = self.entrada.get()
        var = sp.Symbol(self.var_elegida.get())
        try:
            limpio = self.limpiar_entrada(expr_str)
            expr = sp.sympify(limpio)
            derivada = sp.diff(expr, var)
            latex = sp.latex(sp.Eq(sp.Function('f')(var), derivada))
            self.mostrar_latex(latex)

        except Exception as e:
            CTkMessagebox(title="Error", message=f"No se pudo derivar:\n{e}", icon="cancel")

    def integrar(self):
        expr_str = self.entrada.get()
        var = sp.Symbol(self.var_elegida.get())
        try:
            limpio = self.limpiar_entrada(expr_str)
            expr = sp.sympify(limpio)
            a = self.lim_inf.get().strip()
            b = self.lim_sup.get().strip()

            if a and b:
                a_val = float(sp.sympify(a))
                b_val = float(sp.sympify(b))
                integral_def = sp.integrate(expr, (var, a_val, b_val))
                valor = integral_def.evalf()
                latex = f"\int_{{{a}}}^{{{b}}} {sp.latex(expr)}\,d{var} = {sp.latex(valor)}"
            else:
                integral = sp.integrate(expr, var)
                latex = f"\int {sp.latex(expr)}\,d{var} = {sp.latex(integral)} + C"

            self.mostrar_latex(latex)

        except Exception as e:
            CTkMessagebox(title="Error", message=f"No se pudo integrar:\n{e}", icon="cancel")
