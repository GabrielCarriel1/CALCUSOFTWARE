from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sympy as sp
import numpy as np
import customtkinter as ctk

def mostrar_grafica(solucion, condiciones_iniciales, contenedor, variable_x):
    try:
        sol_expr = solucion.rhs if isinstance(solucion, sp.Eq) else solucion
        constantes = [s for s in sol_expr.free_symbols if s != variable_x]

        if constantes and not condiciones_iniciales:
            subs = {c: 1 for c in constantes}
            sol_expr = sol_expr.subs(subs)

            label = ctk.CTkLabel(contenedor, text="⚠ Graficando con valores genéricos: C₁ = 1, C₂ = 1, etc.")
            label.pack(anchor="w", pady=2)

        f = sp.lambdify(variable_x, sol_expr, modules=["numpy", "sympy"])
        x0 = condiciones_iniciales[0] if condiciones_iniciales and len(condiciones_iniciales) >= 1 else 0
        xs = np.linspace(x0 - 5, x0 + 5, 400)
        ys = f(xs)

        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(xs, ys, label="y(x)", color="blue")
        ax.axhline(0, color='gray', linewidth=0.5)
        ax.axvline(0, color='gray', linewidth=0.5)
        ax.set_title("Gráfica de la solución")
        ax.set_xlabel("x")
        ax.set_ylabel("y(x)")
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, contenedor)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(pady=10)
        canvas_widget.pack_configure(anchor="center")  # 👈 centra horizontalmente

    except Exception as e:
        label = ctk.CTkLabel(contenedor, text=f"⚠ No se pudo graficar: {str(e)}")
        label.pack(anchor="w", pady=2)
