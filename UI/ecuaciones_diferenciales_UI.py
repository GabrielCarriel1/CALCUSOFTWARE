import customtkinter as ctk
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from CTkMessagebox import CTkMessagebox

from module_logic.ecuaciones_diferenciales import EcuacionesDiferenciales
from module_logic.gestor_resultados import ResultadosEDOManager
from module_logic.minimos_cuadrados import MinimosCuadrados
from module_logic.graficasEDO import mostrar_grafica
from utils.utils_labels import guardar_resultado_metodo 

class EcuacionesDiferencialesUI(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.solver = EcuacionesDiferenciales()
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.tabs_config = {
            "Euler": ["x + y", "x * y", "x**2 - y"],
            "RK4": ["x + y", "y - x**2 + 1"],
            "Heun": ["x + y", "x * y", "x**2 - y"],
        }

        for nombre_tab, ejemplos in self.tabs_config.items():
            tab = self.tabview.add(f"Método de {nombre_tab}")
            tab.grid_rowconfigure(0, weight=1)
            tab.grid_columnconfigure(0, weight=1)
            scroll = ctk.CTkScrollableFrame(tab)
            scroll.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            setattr(self, f"scroll_{nombre_tab.lower()}", scroll)

            self.crear_ui_metodo_numerico(
                scroll,
                nombre_func_entry=f"entry_funcion_f_{nombre_tab.lower()}",
                nombre_ejemplo_var=f"ejemplo_var_{nombre_tab.lower()}",
                lista_ejemplos=ejemplos,
                cargar_ejemplo_callback=lambda n=nombre_tab.lower(): self.cargar_ejemplo_generico(
                    var_attr=f"ejemplo_var_{n}", entry_attr=f"entry_funcion_f_{n}"
                ),
                aplicar_callback=lambda n=nombre_tab.lower(), m=nombre_tab.lower(): self.lg_metodo_generico(n, m),
                destino=nombre_tab.lower()
            )

        self._crear_tab_analitica()
        self._crear_tab_minimos()
        self._crear_tab_taylor2()
        self._crear_tab_comparativa()
        self.pestana_actual = self.tabview.get()
        self._verificar_cambio_pestana()
        

    def crear_ui_metodo_numerico(self, frame_scroll, nombre_func_entry, nombre_ejemplo_var, lista_ejemplos,
                                 cargar_ejemplo_callback, aplicar_callback, destino):
        frame = frame_scroll

        ecuacion_frame = ctk.CTkFrame(frame)
        ecuacion_frame.pack(fill="x", padx=10, pady=10)
        ecuacion_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(ecuacion_frame, text="Ingrese y' = f(x, y)", font=("Arial", 14)).grid(row=0, column=0, padx=5, pady=5)
        entry_func = ctk.CTkEntry(ecuacion_frame, placeholder_text="Ej: x + y")
        entry_func.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        setattr(self, nombre_func_entry, entry_func)

        ejemplo_var = ctk.StringVar(value=lista_ejemplos[0])
        setattr(self, nombre_ejemplo_var, ejemplo_var)

        menu = ctk.CTkOptionMenu(ecuacion_frame, variable=ejemplo_var, values=lista_ejemplos)
        menu.grid(row=0, column=2, padx=5, pady=5)
        ctk.CTkButton(ecuacion_frame, text="Cargar Ejemplo", command=cargar_ejemplo_callback).grid(row=0, column=3, padx=5)

        datos_frame = ctk.CTkFrame(frame)
        datos_frame.pack(fill="x", padx=10, pady=5)
        self._crear_entrada(datos_frame, "(x₀) Inicial", 0, 0, f"{destino}_x0")
        self._crear_entrada(datos_frame, "(y₀) Inicial", 0, 2, f"{destino}_y0")
        self._crear_entrada(datos_frame, "(h) Tamaño", 0, 4, f"{destino}_h")
        self._crear_entrada(datos_frame, "(n) Numero de pasos", 0, 6, f"{destino}_n")

        ctk.CTkButton(frame, text=f"Aplicar {destino.upper()}", command=aplicar_callback).pack(padx=10, pady=5)

        resultado_final = ctk.CTkLabel(frame, text="", font=("Arial", 14))
        resultado_final.pack(padx=10, pady=(0, 10), anchor="w")
        setattr(self, f"resultado_final_{destino}", resultado_final)

        style = ttk.Style()
        style.configure(f"{destino}.Treeview", font=("Arial", 12), rowheight=28)
        style.configure(f"{destino}.Treeview.Heading", font=("Arial", 13, "bold"))

        treeview_frame = ctk.CTkFrame(frame)
        treeview_frame.pack(fill="both", expand=True, padx=10, pady=5)
        tree = ttk.Treeview(treeview_frame, columns=("Paso", "x", "y"), show="headings", height=10, style=f"{destino}.Treeview")
        for col in ("Paso", "x", "y"):
            tree.heading(col, text=col)
            tree.column(col, width=100 if col != "Paso" else 50, anchor="center")
        tree.pack(fill="both", expand=True)
        setattr(self, f"tree_{destino}", tree)



    def lg_metodo_generico(self, destino, metodo):
        resultado_final = getattr(self, f"resultado_final_{destino}")
        tree = getattr(self, f"tree_{destino}")
        scroll = getattr(self, f"scroll_{destino}")
        entry_func = getattr(self, f"entry_funcion_f_{destino}")

        resultado_final.configure(text="")
        for item in tree.get_children():
            tree.delete(item)

        try:
            f_str = entry_func.get().strip()
            if not f_str:
                CTkMessagebox(title="Error", message="❌ Ingrese la función f(x, y).", icon="cancel")
                return
            if "=" in f_str:
                CTkMessagebox(title="Advertencia", message="⚠ Ingrese solo el lado derecho de la ecuación.", icon="warning")
                return

            x0 = float(getattr(self, f"{destino}_x0").get().strip())
            y0 = float(getattr(self, f"{destino}_y0").get().strip())
            h = float(getattr(self, f"{destino}_h").get().strip())
            n = int(getattr(self, f"{destino}_n").get().strip())

            if h == 0:
                CTkMessagebox(title="Error", message="❌ h no puede ser 0.", icon="cancel")
                return
            if n <= 0:
                CTkMessagebox(title="Error", message="❌ El número de pasos debe ser mayor que 0.", icon="cancel")
                return
        except Exception as e:
            CTkMessagebox(title="Error", message=f"❌ Error en entradas: {e}", icon="cancel")
            return

        self.aplicar_metodo_generico(f_str, x0, y0, h, n, metodo, destino)

    def aplicar_metodo_generico(self, f_str, x0, y0, h, n, metodo, destino):
        try:
            f_expr = sp.sympify(f_str)
            f = sp.lambdify(("x", "y"), f_expr, modules=["math", "sympy"])

            xs, ys = [x0], [y0]
            for _ in range(n):
                xi, yi = xs[-1], ys[-1]
                if metodo == "euler":
                    yi_new = yi + h * f(xi, yi)
                elif metodo == "rk4":
                    k1 = h * f(xi, yi)
                    k2 = h * f(xi + h / 2, yi + k1 / 2)
                    k3 = h * f(xi + h / 2, yi + k2 / 2)
                    k4 = h * f(xi + h, yi + k3)
                    yi_new = yi + (k1 + 2 * k2 + 2 * k3 + k4) / 6
                elif metodo == "heun":
                    y_pred = yi + h * f(xi, yi)
                    yi_new = yi + h * (f(xi, yi) + f(xi + h, y_pred)) / 2
                else:
                    CTkMessagebox(title="Error", message=f"❌ Método {metodo} no implementado.", icon="cancel")
                    return

                xs.append(xi + h)
                ys.append(yi_new)

            tree = getattr(self, f"tree_{destino}")
            for i, (x_val, y_val) in enumerate(zip(xs, ys)):
                tree.insert("", "end", values=(i, f"{x_val:.5f}", f"{y_val:.5f}"))

            resultado_label = getattr(self, f"resultado_final_{destino}")
            resultado_label.configure(text=f"🔎 y({xs[-1]:.3f}) ≈ {ys[-1]:.5f}")

            fig, ax = plt.subplots(figsize=(6, 3))
            ax.plot(xs, ys, marker="o", linestyle="--", label=metodo.upper())
            ax.set_title(f"Aproximación con {metodo.upper()}")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.grid(True)
            ax.legend()

            canvas_attr = f"{destino}_canvas"
            if hasattr(self, canvas_attr):
                getattr(self, canvas_attr).get_tk_widget().destroy()

            canvas = FigureCanvasTkAgg(fig, getattr(self, f"scroll_{destino}"))
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)
            setattr(self, canvas_attr, canvas)

            guardar_resultado_metodo(metodo.upper(), f_str, x0, y0, xs[-1], n, xs, ys)

        except Exception as e:
            CTkMessagebox(title="Error de ejecución", message=f"❌ Error durante cálculo: {e}", icon="cancel")


    def _crear_tab_taylor2(self):
        tab = self.tabview.add("Método de Taylor 2")
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        frame = ctk.CTkScrollableFrame(tab)
        frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.scroll_taylor2 = frame

        # ===== Título =====
        ctk.CTkLabel(frame, text="Método de Taylor 2º Orden", font=("Arial", 18, "bold")).pack(pady=(5, 15))

        # ===== Frame de entradas principales =====
        entradas_frame = ctk.CTkFrame(frame)
        entradas_frame.pack(padx=10, pady=10, fill="x")
        entradas_frame.grid_columnconfigure((0, 2, 4, 6), weight=0)
        entradas_frame.grid_columnconfigure((1, 3, 5, 7), weight=1)

        self._crear_entrada(entradas_frame, "x₀", 0, 0, "entry_x0_taylor")
        self._crear_entrada(entradas_frame, "y₀", 0, 2, "entry_y0_taylor")
        self._crear_entrada(entradas_frame, "x final (xf)", 0, 4, "entry_xf_taylor")
        self._crear_entrada(entradas_frame, "n pasos", 0, 6, "entry_n_taylor")

        # ===== Función f(x, y) =====
        ctk.CTkLabel(frame, text="f(x, y) = y'").pack(anchor="w", padx=20)
        self.entry_funcion_f_taylor = ctk.CTkEntry(frame, placeholder_text="Ej: x + y")
        self.entry_funcion_f_taylor.pack(fill="x", padx=20, pady=5)

        # ===== Derivada f'(x, y) con botón =====
        derivada_frame = ctk.CTkFrame(frame)
        derivada_frame.pack(fill="x", padx=20, pady=5)
        derivada_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(derivada_frame, text="f'(x, y):").grid(row=0, column=0, sticky="w", padx=5)
        self.entry_funcion_df_taylor = ctk.CTkEntry(derivada_frame, placeholder_text="Derivada total")
        self.entry_funcion_df_taylor.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(derivada_frame, text="📐 Calcular f'(x, y)", command=self.calcular_derivada_total_taylor).grid(row=0, column=2, padx=5)

        # ===== Ejemplos y botón aplicar =====
        ejemplos_frame = ctk.CTkFrame(frame)
        ejemplos_frame.pack(pady=10)

        self.ejemplos_taylor2 = [
            "x + y", "x * y", "x**2 - y", "sin(x) + y", "x**2 + y**2"
        ]
        self.ejemplo_var_taylor2 = ctk.StringVar(value=self.ejemplos_taylor2[0])
        ejemplo_menu = ctk.CTkOptionMenu(ejemplos_frame, variable=self.ejemplo_var_taylor2, values=self.ejemplos_taylor2)
        ejemplo_menu.pack(side="left", padx=5)
        ctk.CTkButton(ejemplos_frame, text="📥 Cargar Ejemplo", command=self.cargar_ejemplo_taylor2).pack(side="left", padx=5)

        ctk.CTkButton(frame, text="✅ Aplicar Taylor 2º Orden", command=self.lg_metodo_taylor2).pack(pady=10)

        # ===== Resultado final =====
        self.resultado_final_taylor2 = ctk.CTkLabel(frame, text="", font=("Arial", 14))
        self.resultado_final_taylor2.pack(pady=(0, 10), anchor="w", padx=20)

        # ===== Tabla de resultados =====
        self.treeview_frame_taylor2 = ctk.CTkFrame(frame)
        self.treeview_frame_taylor2.pack(fill="both", expand=True, padx=10, pady=5)

        style = ttk.Style()
        style.configure("Taylor2.Treeview", font=("Arial", 12), rowheight=28)
        style.configure("Taylor2.Treeview.Heading", font=("Arial", 13, "bold"))

        self.tree_taylor2 = ttk.Treeview(
            self.treeview_frame_taylor2,
            columns=("Paso", "x", "y"),
            show="headings",
            height=10,
            style="Taylor2.Treeview"
        )
        self.tree_taylor2.heading("Paso", text="Paso")
        self.tree_taylor2.heading("x", text="x")
        self.tree_taylor2.heading("y", text="y")
        self.tree_taylor2.column("Paso", width=50, anchor="center")
        self.tree_taylor2.column("x", width=100, anchor="center")
        self.tree_taylor2.column("y", width=100, anchor="center")
        self.tree_taylor2.pack(fill="both", expand=True)

        # ===== Gráfico =====
        self.frame_grafico_taylor2 = ctk.CTkFrame(frame)
        self.frame_grafico_taylor2.pack(fill="both", expand=True, padx=10, pady=10)



    
    def cargar_ejemplo_taylor2(self):
        ejemplo = self.ejemplo_var_taylor2.get()
        self.entry_funcion_f_taylor.delete(0, "end")
        self.entry_funcion_f_taylor.insert(0, ejemplo)

        derivadas = {
            "x + y": "1 + x + y",
            "x * y": "y + x*y",
            "x**2 - y": "2*x - x**2 + y",
            "sin(x) + y": "cos(x) + sin(x) + y",
            "x**2 + y**2": "2*x + 2*y*(x**2 + y**2)"
        }
        self.entry_funcion_df_taylor.delete(0, "end")
        self.entry_funcion_df_taylor.insert(0, derivadas.get(ejemplo, ""))


    def calcular_derivada_total_taylor(self):
        x, y = sp.symbols('x y')
        f_str = self.entry_funcion_f_taylor.get().strip()

        if not f_str:
            CTkMessagebox(title="Error", message="❌ Ingrese primero f(x, y)", icon="cancel")
            return

        try:
            f_expr = sp.sympify(f_str)
            df_dx = sp.diff(f_expr, x)
            df_dy = sp.diff(f_expr, y)
            total = df_dx + df_dy * f_expr
            self.entry_funcion_df_taylor.delete(0, "end")
            self.entry_funcion_df_taylor.insert(0, str(total))
            CTkMessagebox(title="Éxito", message="✅ Derivada total calculada.", icon="check")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"❌ Error al calcular f'(x, y): {e}", icon="cancel")


    def lg_metodo_taylor2(self):
        self.resultado_final_taylor2.configure(text="")
        for item in self.tree_taylor2.get_children():
            self.tree_taylor2.delete(item)

        try:
            f_str = self.entry_funcion_f_taylor.get().strip()
            df_str = self.entry_funcion_df_taylor.get().strip()
            x0 = float(self.entry_x0_taylor.get().strip())
            y0 = float(self.entry_y0_taylor.get().strip())
            xf = float(self.entry_xf_taylor.get().strip())
            n = int(self.entry_n_taylor.get().strip())

            if not f_str or not df_str:
                CTkMessagebox(title="Error", message="❌ Ingrese f(x,y) y f'(x,y).", icon="cancel")
                return
            if n <= 0 or x0 == xf:
                CTkMessagebox(title="Error", message="❌ Verifique que n > 0 y x₀ ≠ xf.", icon="cancel")
                return

        except ValueError as e:
            CTkMessagebox(title="Error", message=f"❌ Valores inválidos: {e}", icon="cancel")
            return

        try:
            resultado = self.solver.metodo_taylor_segundo_orden(f_str, df_str, x0, y0, xf, n)
            if not resultado["exito"]:
                CTkMessagebox(title="Error", message=resultado.get("mensaje", "Error al resolver."), icon="cancel")
                return
        except Exception as e:
            CTkMessagebox(title="Error", message=f"❌ Excepción durante cálculo: {e}", icon="cancel")
            return

        xs, ys = resultado["xs"], resultado["ys"]
        for i, (x, y) in enumerate(zip(xs, ys)):
            self.tree_taylor2.insert("", "end", values=(i, f"{x:.5f}", f"{y:.5f}"))

        self.resultado_final_taylor2.configure(
            text=f"🔎 Resultado final: y({xs[-1]:.3f}) ≈ {ys[-1]:.5f}"
        )

        for widget in self.frame_grafico_taylor2.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(xs, ys, marker="o", linestyle="--", label="Taylor 2º Orden")
        ax.set_title("Aproximación con Taylor de Segundo Orden")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, self.frame_grafico_taylor2)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        guardar_resultado_metodo("Taylor2", f_str, x0, y0, xf, n, xs, ys)



    def _crear_tab_analitica(self):
        self.tab_analitica = self.tabview.add("Solución Analítica")
        self.tab_analitica.grid_rowconfigure(0, weight=1)
        self.tab_analitica.grid_columnconfigure(0, weight=1)

        self.scroll_analitica = ctk.CTkScrollableFrame(self.tab_analitica)
        self.scroll_analitica.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # === Título ===
        ctk.CTkLabel(self.scroll_analitica, text="Solución Analítica de EDO", font=("Arial", 18, "bold")).pack(pady=(5, 15))

        # === Frame de condiciones iniciales ===
        ci_frame = ctk.CTkFrame(self.scroll_analitica)
        ci_frame.pack(fill="x", padx=20, pady=5)
        ci_frame.grid_columnconfigure((1, 2, 3), weight=1)

        ctk.CTkLabel(ci_frame, text="Condiciones iniciales (opcionales):", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_x0 = ctk.CTkEntry(ci_frame, placeholder_text="x₀", width=80)
        self.entry_x0.grid(row=0, column=1, padx=5, pady=5)
        self.entry_y0 = ctk.CTkEntry(ci_frame, placeholder_text="y(x₀)", width=80)
        self.entry_y0.grid(row=0, column=2, padx=5, pady=5)
        self.entry_dy0 = ctk.CTkEntry(ci_frame, placeholder_text="y'(x₀)", width=80)
        self.entry_dy0.grid(row=0, column=3, padx=5, pady=5)

        # === Ecuación de entrada ===
        entrada_frame = ctk.CTkFrame(self.scroll_analitica)
        entrada_frame.pack(fill="x", padx=20, pady=10)
        entrada_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(entrada_frame, text="Ecuación diferencial:", font=("Arial", 14)).grid(row=0, column=0, padx=5, pady=5)
        self.entry_ecuacion = ctk.CTkEntry(entrada_frame, placeholder_text="Ej: y'' + 2*y' + y = 0")
        self.entry_ecuacion.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # === Botones principales ===
        botones_frame = ctk.CTkFrame(self.scroll_analitica)
        botones_frame.pack(padx=20, pady=5)

        ctk.CTkButton(botones_frame, text="✅ Resolver Analíticamente", command=self.resolver_analitica).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(botones_frame, text="🧹 Limpiar", command=self.limpiar_analitica).pack(side="left", padx=5, pady=5)

        # === Resultado ===
        self.resultado_scroll = ctk.CTkScrollableFrame(self.scroll_analitica, width=600, height=250)
        self.resultado_scroll.pack(fill="both", expand=True, padx=20, pady=10)

        # === Ejemplos ===
        ejemplos_frame = ctk.CTkFrame(self.scroll_analitica)
        ejemplos_frame.pack(fill="x", padx=20, pady=(5, 15))

        ctk.CTkLabel(ejemplos_frame, text="Ejemplos:", font=("Arial", 12)).pack(side="left", padx=5)
        self.ejemplos = [
            "y' + y = x", "y'' + y = 0", "y'' + 2*y' + y = 0",
            "y' + 2*x*y = x", "y'' + 4*y = 0", "y' = y/x", "y' = y**2"
        ]
        self.ejemplo_var = ctk.StringVar(value=self.ejemplos[0])
        ejemplo_menu = ctk.CTkOptionMenu(ejemplos_frame, variable=self.ejemplo_var, values=self.ejemplos)
        ejemplo_menu.pack(side="left", padx=5)
        ctk.CTkButton(ejemplos_frame, text="📥 Cargar Ejemplo", command=self.cargar_ejemplo_analitico).pack(side="left", padx=5)


    def resolver_analitica(self):
        ecuacion_str = self.entry_ecuacion.get().strip()
        if not ecuacion_str:
            CTkMessagebox(title="Error", message="❌ Ingrese una ecuación diferencial.", icon="cancel")
            return

        condiciones_iniciales = self._obtener_condiciones_iniciales()
        for widget in self.resultado_scroll.winfo_children():
            widget.destroy()

        try:
            resultado = self.solver.resolver_analitica(ecuacion_str, condiciones_iniciales)

            if resultado["exito"]:
                sol = resultado["solucion"]
                expr = sol.rhs if isinstance(sol, sp.Eq) else sol
                expr = expr.xreplace({n: sp.Float(n.evalf(3)) for n in expr.atoms(sp.Float)})
                latex_sol = f"\\text{{Solución: }} y(x) = {sp.latex(expr)}"

                fig, ax = plt.subplots(figsize=(6, 1.5))
                ax.text(0.5, 0.5, f"${latex_sol}$", fontsize=13, ha="center", va="center")
                ax.axis("off")

                canvas = FigureCanvasTkAgg(fig, self.resultado_scroll)
                canvas_widget = canvas.get_tk_widget()
                canvas.draw()
                canvas_widget.pack(pady=15)

                # Centrado visual del canvas
                canvas_widget.pack_configure(anchor="center")

                # Línea divisoria o espacio
                ctk.CTkLabel(self.resultado_scroll, text="").pack(pady=5)  # Espaciador opcional

                # Botón centrado
                ctk.CTkButton(
                    self.resultado_scroll,
                    text="📈 Mostrar gráfica",
                    command=lambda: mostrar_grafica(sol, condiciones_iniciales, self.resultado_scroll, self.solver.x)
                ).pack(pady=10, anchor="center")

            else:
                CTkMessagebox(title="Sin solución", message=resultado.get("mensaje", "No se pudo resolver."), icon="warning")

        except Exception as e:
            CTkMessagebox(title="Error inesperado", message=str(e), icon="cancel")

    def cargar_ejemplo_analitico(self):
        ejemplo = self.ejemplo_var.get()
        self.entry_ecuacion.delete(0, "end")
        self.entry_ecuacion.insert(0, ejemplo)
        self.entry_x0.delete(0, "end")
        self.entry_y0.delete(0, "end")
        self.entry_dy0.delete(0, "end")

    def limpiar_analitica(self):
        self.entry_ecuacion.delete(0, "end")
        self.entry_x0.delete(0, "end")
        self.entry_y0.delete(0, "end")
        self.entry_dy0.delete(0, "end")
        for widget in self.resultado_scroll.winfo_children():
            widget.destroy()

    def _obtener_condiciones_iniciales(self):
        try:
            x0_str = self.entry_x0.get().strip()
            y0_str = self.entry_y0.get().strip()
            dy0_str = self.entry_dy0.get().strip()
            condiciones = []

            if x0_str and y0_str:
                x0 = float(x0_str)
                y0 = float(y0_str)
                condiciones = [x0, y0]
                if dy0_str:
                    dy0 = float(dy0_str)
                    condiciones.append(dy0)
            return condiciones if condiciones else None
        except ValueError:
            CTkMessagebox(title="Error", message="Condiciones iniciales no válidas. Use solo números.", icon="cancel")
            return None

    def _crear_tab_minimos(self):
        self.tab_minimos = self.tabview.add("Mínimos Cuadrados")
        self.tab_minimos.grid_rowconfigure(0, weight=1)
        self.tab_minimos.grid_columnconfigure(0, weight=1)

        self.scroll_minimos = ctk.CTkScrollableFrame(self.tab_minimos)
        self.scroll_minimos.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        ctk.CTkLabel(self.scroll_minimos, text="Selecciona un método numérico:", font=("Arial", 13)).pack(pady=5)

        self.opcion_metodo = ctk.StringVar()
        self.menu_minimos = ctk.CTkOptionMenu(self.scroll_minimos, variable=self.opcion_metodo, values=[""])
        self.menu_minimos.pack(pady=5)

        ctk.CTkButton(self.scroll_minimos, text="Aplicar Ajuste Lineal", command=self.aplicar_minimos_cuadrados).pack(pady=10)

        self.resultado_minimos = ctk.CTkTextbox(self.scroll_minimos, height=200)
        self.resultado_minimos.pack(fill="both", expand=True, padx=10, pady=10)

        self.frame_grafico_minimos = ctk.CTkFrame(self.scroll_minimos)
        self.frame_grafico_minimos.pack(fill="both", expand=True, padx=10, pady=10)

    def aplicar_minimos_cuadrados(self):
        self.resultado_minimos.delete("0.0", "end")
        metodo = self.opcion_metodo.get()
        datos = ResultadosEDOManager.filtrar_por_metodo(metodo)

        if not datos:
            CTkMessagebox(title="Error", message="❌ No hay datos disponibles para ese método.", icon="cancel")
            return

        try:
            resultado = MinimosCuadrados.ajustar_lineal(datos[-1]["xs"], datos[-1]["ys"])
        except Exception as e:
            CTkMessagebox(title="Error", message=f"❌ Error en ajuste lineal: {e}", icon="cancel")
            return

        self.resultado_minimos.insert("end", f"Ajuste lineal: y = {resultado['a']:.4f}x + {resultado['b']:.4f}\n")

        for widget in self.frame_grafico_minimos.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(resultado["xs"], resultado["ys_originales"], 'o', label=metodo)
        ax.plot(resultado["xs"], resultado["ys_ajustados"], 'r--', label="Ajuste Lineal")
        ax.set_title("Mínimos Cuadrados")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, self.frame_grafico_minimos)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def actualizar_menu_metodos_minimos(self):
        metodos = list(set(r["metodo"] for r in ResultadosEDOManager.obtener_todos()))
        if metodos:
            self.opcion_metodo.set(metodos[0])
            self.menu_minimos.configure(values=metodos)
    
    def _crear_tab_comparativa(self):
        self.tab_comparativa = self.tabview.add("Comparativa de Métodos")
        self.tab_comparativa.grid_rowconfigure(0, weight=1)
        self.tab_comparativa.grid_columnconfigure(0, weight=1)

        self.scroll_comparativa = ctk.CTkScrollableFrame(self.tab_comparativa)
        self.scroll_comparativa.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        ctk.CTkLabel(self.scroll_comparativa, text="Seleccione los métodos para comparar:", font=("Arial", 14)).pack(pady=5)

        self.frame_checkboxes = ctk.CTkFrame(self.scroll_comparativa)
        self.frame_checkboxes.pack(fill="x", padx=10, pady=5)
        self.checkboxes_metodos = []
        self.var_checkboxes = []

        ctk.CTkButton(self.scroll_comparativa, text="Comparar Métodos", command=self.comparar_metodos).pack(pady=10)

        self.resultado_comparativa = ctk.CTkTextbox(self.scroll_comparativa, height=200)
        self.resultado_comparativa.pack(fill="both", expand=True, padx=10, pady=10)

        self.frame_grafico_comparativa = ctk.CTkFrame(self.scroll_comparativa)
        self.frame_grafico_comparativa.pack(fill="both", expand=True, padx=10, pady=10)

    def actualizar_checkboxes_comparativa(self):
        for cb in self.checkboxes_metodos:
            cb.destroy()
        self.checkboxes_metodos.clear()
        self.var_checkboxes.clear()

        metodos_unicos = list(set(r["metodo"] for r in ResultadosEDOManager.obtener_todos()))

        for metodo in metodos_unicos:
            var = ctk.BooleanVar()
            cb = ctk.CTkCheckBox(self.frame_checkboxes, text=metodo, variable=var)
            cb.pack(anchor="w", padx=20)
            self.checkboxes_metodos.append(cb)
            self.var_checkboxes.append((metodo, var))

    def comparar_metodos(self):
        self.resultado_comparativa.delete("0.0", "end")
        seleccionados = [met for met, var in self.var_checkboxes if var.get()]

        if not seleccionados:
            CTkMessagebox(title="Advertencia", message="❌ Selecciona al menos un método para comparar.", icon="warning")
            return

        resultados = []
        for metodo in seleccionados:
            datos = ResultadosEDOManager.filtrar_por_metodo(metodo)
            if datos:
                resultados.append(datos[-1])

        if not resultados:
            CTkMessagebox(title="Advertencia", message="❌ No hay datos disponibles para los métodos seleccionados.", icon="warning")
            return

        max_pasos = max(len(r["xs"]) for r in resultados)
        encabezado = "Paso\t" + "\t".join(r["metodo"] for r in resultados) + "\n"
        self.resultado_comparativa.insert("end", encabezado)
        self.resultado_comparativa.insert("end", "-" * len(encabezado) + "\n")

        for i in range(max_pasos):
            fila = f"{i}\t"
            for r in resultados:
                if i < len(r["ys"]):
                    fila += f"{r['ys'][i]:.4f}\t"
                else:
                    fila += "----\t"
            self.resultado_comparativa.insert("end", fila + "\n")

        for widget in self.frame_grafico_comparativa.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 3))
        for r in resultados:
            ax.plot(r["xs"], r["ys"], marker="o", linestyle="--", label=r["metodo"])

        ax.set_title("Comparativa de Métodos")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, self.frame_grafico_comparativa)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def _crear_entrada(self, parent, texto, row, col, attr_name):
        ctk.CTkLabel(parent, text=texto).grid(row=row, column=col, padx=5)
        entry = ctk.CTkEntry(parent, width=80)
        entry.grid(row=row, column=col + 1, padx=5)
        setattr(self, attr_name, entry)

    def cargar_ejemplo_generico(self, var_attr: str, entry_attr: str):
        ejemplo = getattr(self, var_attr).get()
        entry = getattr(self, entry_attr)
        entry.delete(0, "end")
        entry.insert(0, ejemplo)

    def _verificar_cambio_pestana(self):
        seleccion = self.tabview.get()
        if seleccion != self.pestana_actual:
            self.pestana_actual = seleccion
            self._al_cambiar_pestana(seleccion)
        self.after(200, self._verificar_cambio_pestana)

    def _al_cambiar_pestana(self, nombre_tab):
        if nombre_tab == "Mínimos Cuadrados":
            self.actualizar_menu_metodos_minimos()
        elif nombre_tab == "Comparativa de Métodos":
            self.actualizar_checkboxes_comparativa()


