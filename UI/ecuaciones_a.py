import customtkinter as ctk
import sympy as sp
import matplotlib.pyplot as plt
from utils.utils_labels import mostrar_label, guardar_resultado_metodo
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from module_logic.ecuaciones_diferenciales import EcuacionesDiferenciales
from module_logic.graficasEDO import mostrar_grafica
from module_logic.gestor_resultados import ResultadosEDOManager
from module_logic.minimos_cuadrados import MinimosCuadrados
from tkinter import ttk

class EcuacionesDiferencialesUI(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.solver = EcuacionesDiferenciales()

        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.tab_analitica = self.tabview.add("Solución Analítica")

        self.tab_analitica.grid_rowconfigure(0, weight=1)
        self.tab_analitica.grid_columnconfigure(0, weight=1)

        self.scroll_analitica = ctk.CTkScrollableFrame(self.tab_analitica)
        self.scroll_analitica.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        #PESTAÑAS DE LOS METODOS NUMERICOS

        #Metodo de euler
        self.tab_numerico = self.tabview.add("Método de Euler")
        self.tab_numerico.grid_rowconfigure(0, weight=1)
        self.tab_numerico.grid_columnconfigure(0, weight=1)

        self.scroll_numerico = ctk.CTkScrollableFrame(self.tab_numerico)
        self.scroll_numerico.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        #Metodo de RK4
        self.tab_rk4 = self.tabview.add("Método RK4")
        self.tab_rk4.grid_rowconfigure(0, weight=1)
        self.tab_rk4.grid_columnconfigure(0, weight=1)

        self.scroll_rk4 = ctk.CTkScrollableFrame(self.tab_rk4)
        self.scroll_rk4.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        #Metodo de Heun
        self.tab_heun = self.tabview.add("Método de Heun")
        self.tab_heun.grid_rowconfigure(0, weight=1)
        self.tab_heun.grid_columnconfigure(0, weight=1)

        self.scroll_heun = ctk.CTkScrollableFrame(self.tab_heun)
        self.scroll_heun.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        #Metodo de taylor 2da orden
        self.tab_taylor2 = self.tabview.add("Método de Taylor 2º Orden")
        self.tab_taylor2.grid_rowconfigure(0, weight=1)
        self.tab_taylor2.grid_columnconfigure(0, weight=1)

        self.scroll_taylor2 = ctk.CTkScrollableFrame(self.tab_taylor2)
        self.scroll_taylor2.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        #Metodo minimos cuadrados
        self.tab_minimos = self.tabview.add("Mínimos Cuadrados")
        self.tab_minimos.grid_rowconfigure(0, weight=1)
        self.tab_minimos.grid_columnconfigure(0, weight=1)

        self.scroll_minimos = ctk.CTkScrollableFrame(self.tab_minimos)
        self.scroll_minimos.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.pestana_actual = self.tabview.get()
        self._verificar_cambio_pestana()

        #Comparativa
        self.tab_comparativa = self.tabview.add("Comparativa de Métodos")
        self.tab_comparativa.grid_rowconfigure(0, weight=1)
        self.tab_comparativa.grid_columnconfigure(0, weight=1)
        self.scroll_comparativa = ctk.CTkScrollableFrame(self.tab_comparativa)
        self.scroll_comparativa.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.checkboxes_metodos = []
        self.var_checkboxes = []

        self.pestana_actual = self.tabview.get()
        self.tabview._seguro_anterior = self.pestana_actual
        self._verificar_cambio_pestana()



        self.UI_metodo_comparativa()
        self.UI_metodo_minimos()
        self.UI_metodo_taylor2()
        self.UI_metodo_heun()
        self.UI_metodo_rk4()
        self.UI_metodo_euler()
        self._setup_tab_analitica()

    def _setup_tab_analitica(self):
        ci_frame = ctk.CTkFrame(self.scroll_analitica)
        ci_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(ci_frame, text="Condiciones iniciales (opcional):", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.entry_x0 = ctk.CTkEntry(ci_frame, placeholder_text="x₀", width=80)
        self.entry_x0.grid(row=0, column=1, padx=5, pady=5)
        self.entry_y0 = ctk.CTkEntry(ci_frame, placeholder_text="y(x₀)", width=80)
        self.entry_y0.grid(row=0, column=2, padx=5, pady=5)
        self.entry_dy0 = ctk.CTkEntry(ci_frame, placeholder_text="y'(x₀)", width=80)
        self.entry_dy0.grid(row=0, column=3, padx=5, pady=5)

        entrada_frame = ctk.CTkFrame(self.scroll_analitica)
        entrada_frame.pack(fill="x", padx=10, pady=10)
        entrada_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(entrada_frame, text="Ingrese la ecuación diferencial:", font=("Arial", 14)).grid(row=0, column=0, padx=5, pady=5)
        self.entry_ecuacion = ctk.CTkEntry(entrada_frame, placeholder_text="Ej: y'' + 2*y' + y = 0")
        self.entry_ecuacion.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        teclado_frame = ctk.CTkFrame(self.scroll_analitica)
        teclado_frame.pack(fill="x", padx=10, pady=5)
        teclado_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        botones_simbolos = [
            ("y'", "y'"), ("y''", "y''"), ("dy/dx", "dy/dx"), ("d²y/dx²", "d^2y/dx^2"), ("=", "="),
            ("e^x", "exp(x)"), ("ln(x)", "log(x)"), ("sin(x)", "sin(x)"), ("cos(x)", "cos(x)"), ("^", "^"),
            ("(", "("), (")", ")"), ("+", "+"), ("-", "-"), ("*", "*")
        ]
        for i, (texto, insertar) in enumerate(botones_simbolos):
            boton = ctk.CTkButton(teclado_frame, text=texto, width=40, command=lambda s=insertar: self._insertar_simbolo(s))
            boton.grid(row=i // 5, column=i % 5, padx=3, pady=3)

        botones_frame = ctk.CTkFrame(self.scroll_analitica)
        botones_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(botones_frame, text="Resolver Analíticamente", command=self.resolver_analitica).grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkButton(botones_frame, text="Limpiar", command=self.limpiar_analitica).grid(row=0, column=3, padx=5, pady=5)

        resultado_frame = ctk.CTkFrame(self.scroll_analitica)
        resultado_frame.pack(fill="both", expand=True, padx=10, pady=5)
        ctk.CTkLabel(resultado_frame, text="Resultado:", font=("Arial", 14)).pack(anchor="w", padx=5, pady=5)
        self.resultado_scroll = ctk.CTkScrollableFrame(resultado_frame, width=600, height=250)
        self.resultado_scroll.pack(fill="both", expand=True, padx=5, pady=5)

        ejemplos_frame = ctk.CTkFrame(self.scroll_analitica)
        ejemplos_frame.pack(fill="x", padx=10, pady=(5, 15))
        ejemplos_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(ejemplos_frame, text="Ejemplos:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.ejemplos = [
            "y' + y = x", "y'' + y = 0", "y'' + 2*y' + y = 0",
            "y' + 2*x*y = x", "y'' + 4*y = 0", "y' = y/x", "y' = y²"
        ]
        self.ejemplo_var = ctk.StringVar(value=self.ejemplos[0])
        ejemplo_dropdown = ctk.CTkOptionMenu(ejemplos_frame, variable=self.ejemplo_var, values=self.ejemplos)
        ejemplo_dropdown.grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkButton(ejemplos_frame, text="Cargar Ejemplo", command=self.cargar_ejemplo).grid(row=0, column=2, padx=5, pady=5)


    def _insertar_simbolo(self, texto: str):
        """Inserta el texto dado en la posición actual del cursor del campo de ecuación."""
        self.entry_ecuacion.insert(self.entry_ecuacion.index("insert"), texto)
    
    
    def resolver_analitica(self):
        """Resuelve la ecuación diferencial analíticamente y muestra resultado + gráfico"""
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        import matplotlib.pyplot as plt

        ecuacion_str = self.entry_ecuacion.get().strip()
        if not ecuacion_str:
            mostrar_label(self.resultado_scroll, "Por favor, ingrese una ecuación diferencial.")
            return

        condiciones_iniciales = self._obtener_condiciones_iniciales()

        # Limpiar contenido anterior
        for widget in self.resultado_scroll.winfo_children():
            widget.destroy()

        try:
            resultado = self.solver.resolver_analitica(ecuacion_str, condiciones_iniciales)

            if resultado["exito"]:
                clasificacion = resultado["clasificacion"]
                metodo = resultado.get("metodo", "Método no identificado")
                orden = clasificacion.get("orden", "?")

                mostrar_label(self.resultado_scroll,f"✅ La ecuación fue resuelta analíticamente.")
                mostrar_label(self.resultado_scroll,f"➡️ Tipo identificado: {metodo} | Orden: {orden}")
                mostrar_label(self.resultado_scroll,f"🛠 Método aplicado: {metodo}")

                sol = resultado["solucion"]
                expr = sol.rhs if isinstance(sol, sp.Eq) else sol
                expr = expr.xreplace({
                    n: sp.Float(n.evalf(3)) for n in expr.atoms(sp.Float)
                })

                latex_sol = f"\\text{{Soluci\u00f3n: }} y(x) = {sp.latex(expr)}"
                fig, ax = plt.subplots(figsize=(6, 1.5))
                ax.text(0.5, 0.5, f"${latex_sol}$", fontsize=12, ha="center", va="center")
                ax.axis('off')
                canvas = FigureCanvasTkAgg(fig, self.resultado_scroll)
                canvas.draw()
                canvas.get_tk_widget().pack(pady=10)

                boton_graf = ctk.CTkButton(
                    self.resultado_scroll,
                    text="\ud83d\udcc8 Mostrar gr\u00e1fica de la soluci\u00f3n",
                     command=lambda: mostrar_grafica(sol, condiciones_iniciales, self.resultado_scroll, self.solver.x)
                )
                boton_graf.pack(pady=10)

            else:
                mostrar_label(self.resultado_scroll,"❌ No se pudo resolver analíticamente.")
                mostrar_label(self.resultado_scroll,f"📌 Motivo: {resultado.get('mensaje', 'Desconocido')}.")

                if "error" in resultado:
                    mostrar_label(self.resultado_scroll,f"⚠ Detalle técnico: {resultado['error']}")

                mostrar_label("💡 Sugerencia: Verifique si la ecuación puede simplificarse o considere métodos numéricos.")

        except Exception as e:
            mostrar_label(f"Error inesperado: {str(e)}")

    def UI_metodo_euler(self):
        frame = self.scroll_numerico

        # Entrada de función f(x, y)
        ecuacion_frame = ctk.CTkFrame(frame)
        ecuacion_frame.pack(fill="x", padx=10, pady=10)
        ecuacion_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(ecuacion_frame, text="Ingrese la ecuación y' = f(x, y)", font=("Arial", 14)).grid(row=0, column=0, padx=5, pady=5)
        self.entry_funcion_f = ctk.CTkEntry(ecuacion_frame, placeholder_text="Ej: x + y")
        self.entry_funcion_f.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Menú de ejemplos y botón
        self.ejemplos_euler = ["x + y", "x * y", "x**2 - y", "sin(x) + y"]
        self.ejemplo_var_euler = ctk.StringVar(value=self.ejemplos_euler[0])
        ejemplo_menu = ctk.CTkOptionMenu(ecuacion_frame, variable=self.ejemplo_var_euler, values=self.ejemplos_euler)
        ejemplo_menu.grid(row=0, column=2, padx=5, pady=5)
        ctk.CTkButton(ecuacion_frame, text="Cargar Ejemplo", command=self.cargar_ejemplo_euler).grid(row=0, column=3, padx=5, pady=5)

        # Entradas numéricas
        datos_frame = ctk.CTkFrame(frame)
        datos_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(datos_frame, text="x₀ inicial").grid(row=0, column=0, padx=5)
        self.entry_x0_num = ctk.CTkEntry(datos_frame, width=80)
        self.entry_x0_num.grid(row=0, column=1, padx=5)

        ctk.CTkLabel(datos_frame, text="y₀ inicial").grid(row=0, column=2, padx=5)
        self.entry_y0_num = ctk.CTkEntry(datos_frame, width=80)
        self.entry_y0_num.grid(row=0, column=3, padx=5)

        ctk.CTkLabel(datos_frame, text="Tamaño de paso (h)").grid(row=0, column=4, padx=5)
        self.entry_h = ctk.CTkEntry(datos_frame, width=80)
        self.entry_h.grid(row=0, column=5, padx=5)

        ctk.CTkLabel(datos_frame, text="Número de Pasos (n)").grid(row=0, column=6, padx=5)
        self.entry_n = ctk.CTkEntry(datos_frame, width=80)
        self.entry_n.grid(row=0, column=7, padx=5)

        # Botón para resolver
        boton_frame = ctk.CTkFrame(frame)
        boton_frame.pack(padx=10, pady=5)
        ctk.CTkButton(boton_frame, text="Aplicar Método de Euler", command=self.lg_metodo_euler).pack(padx=5, pady=5)

        # Mensaje de estado
        self.mensaje_estado = ctk.CTkLabel(frame, text="", font=("Arial", 13), text_color="red")
        self.mensaje_estado.pack(pady=(0, 5), padx=10, anchor="w")

        # Resultado final
        self.resultado_final_label = ctk.CTkLabel(frame, text="", font=("Arial", 14))
        self.resultado_final_label.pack(padx=10, pady=(0, 10), anchor="w")

        # Estilo tabla
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Arial", 12)) 
        style.configure("Custom.Treeview.Heading", font=("Arial", 13, "bold"))

        # Tabla visual
        self.treeview_frame = ctk.CTkFrame(frame)
        self.treeview_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(self.treeview_frame, columns=("Paso", "x", "y"), show="headings", height=10, style="Custom.Treeview")
        self.tree.heading("Paso", text="Paso")
        self.tree.heading("x", text="x")
        self.tree.heading("y", text="y")

        self.tree.column("Paso", width=50, anchor="center")
        self.tree.column("x", width=100, anchor="center")
        self.tree.column("y", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True)

    def lg_metodo_euler(self):
        self.mensaje_estado.configure(text="")
        self.resultado_final_label.configure(text="")

        # Validación de función f(x, y)
        f_str = self.entry_funcion_f.get().strip()
        if not f_str:
            self.mostrar_mensaje_estado("❌ Ingrese la función f(x, y).", tipo="error", destino="euler")
            return
        if "=" in f_str:
            self.mostrar_mensaje_estado("⚠ Ingrese solo el lado derecho de la ecuación. Ejemplo: x + y", tipo="advertencia", destino="euler")
            return

        # Validación de entradas numéricas
        try:
            x0 = float(self.entry_x0_num.get().strip())
            y0 = float(self.entry_y0_num.get().strip())
            h = float(self.entry_h.get().strip())
            n = int(self.entry_n.get().strip())

            if n <= 0:
                self.mostrar_mensaje_estado("❌ El número de pasos debe ser mayor que cero.", tipo="error", destino="euler")
                return
            if h == 0:
                self.mostrar_mensaje_estado("❌ El tamaño de paso h no puede ser cero.", tipo="error", destino="euler")
                return

            xf = x0 + h * n
        except ValueError:
            self.mostrar_mensaje_estado("❌ Error en los valores numéricos.", tipo="error", destino="euler")
            return

        # Interpretar función f(x, y)
        try:
            f_expr = sp.sympify(f_str)
            f_func = sp.lambdify(("x", "y"), f_expr, modules=["math", "sympy"])
        except Exception as e:
            self.mostrar_mensaje_estado(f"❌ Error al interpretar f(x, y): {str(e)}", tipo="error", destino="euler")
            return

        # Método de Euler
        try:
            xs = [x0]
            ys = [y0]

            for _ in range(n):
                xi = xs[-1]
                yi = ys[-1]
                yi_new = yi + h * f_func(xi, yi)
                xs.append(xi + h)
                ys.append(yi_new)

            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insertar resultados
            for i, (x_val, y_val) in enumerate(zip(xs, ys)):
                self.tree.insert("", "end", values=(i, f"{x_val:.3f}", f"{y_val:.3f}"))

            self.resultado_final_label.configure(text=f"🔎 Resultado final: y({xs[-1]:.3f}) ≈ {ys[-1]:.5f}")

            # Gráfica
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.plot(xs, ys, marker="o", linestyle="--", label="Euler")
            ax.set_title("Aproximación con Euler")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.grid(True)
            ax.legend()

            if hasattr(self, "euler_canvas"):
                self.euler_canvas.get_tk_widget().destroy()

            self.euler_canvas = FigureCanvasTkAgg(fig, self.scroll_numerico)
            self.euler_canvas.draw()
            self.euler_canvas.get_tk_widget().pack(pady=10)

            guardar_resultado_metodo("Euler", f_str, x0, y0, xf, n, xs, ys)

        except Exception as e:
            self.mostrar_mensaje_estado(f"❌ Error durante el cálculo: {str(e)}", tipo="error", destino="euler")

    
    def UI_metodo_rk4(self):
        frame = self.scroll_rk4  

        # Entrada de ecuación
        ecuacion_frame = ctk.CTkFrame(frame)
        ecuacion_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(ecuacion_frame, text="Ingrese la ecuación y' = f(x, y)", font=("Arial", 14)).grid(row=0, column=0, padx=5, pady=5)
        self.entry_funcion_f_rk = ctk.CTkEntry(ecuacion_frame, placeholder_text="Ej: x + y")
        self.entry_funcion_f_rk.grid(row=0, column=1, padx=5, pady=5)

        self.ejemplos_rk4 = ["x + y", "y - x**2 + 1", "x * y", "sin(x) + y"]
        self.ejemplo_var_rk4 = ctk.StringVar(value=self.ejemplos_rk4[0])
        ejemplo_menu = ctk.CTkOptionMenu(ecuacion_frame, variable=self.ejemplo_var_rk4, values=self.ejemplos_rk4)
        ejemplo_menu.grid(row=0, column=2, padx=5, pady=5)
        ctk.CTkButton(ecuacion_frame, text="Cargar Ejemplo", command=self.cargar_ejemplo_rk4).grid(row=0, column=3, padx=5, pady=5)

        # Entradas numéricas
        datos_frame = ctk.CTkFrame(frame)
        datos_frame.pack(fill="x", padx=10, pady=5)

        self._crear_entrada(datos_frame, "x₀ inicial", 0, 0, "entry_x0_rk")
        self._crear_entrada(datos_frame, "y₀ inicial", 0, 2, "entry_y0_rk")
        self._crear_entrada(datos_frame, "Tamaño de paso (h)", 0, 4, "entry_h_rk")
        self._crear_entrada(datos_frame, "Número de pasos (n)", 0, 6, "entry_n_rk")

        # Botón
        boton_frame = ctk.CTkFrame(frame)
        boton_frame.pack(padx=10, pady=5)
        ctk.CTkButton(boton_frame, text="Aplicar Runge-Kutta 4", command=self.lg_metodo_rk4).pack(padx=5, pady=5)

        # Mensaje de estado
        self.mensaje_estado_rk4 = ctk.CTkLabel(frame, text="", font=("Arial", 13), text_color="red")
        self.mensaje_estado_rk4.pack(pady=(0, 5), padx=10, anchor="w")

        # Resultado final
        self.resultado_final_rk4 = ctk.CTkLabel(frame, text="", font=("Arial", 14))
        self.resultado_final_rk4.pack(padx=10, pady=(0, 10), anchor="w")

        # Estilo tabla
        style = ttk.Style()
        style.configure("RK4.Treeview", font=("Arial", 12), rowheight=28)
        style.configure("RK4.Treeview.Heading", font=("Arial", 13, "bold"))

        # Tabla
        self.treeview_frame_rk4 = ctk.CTkFrame(frame)
        self.treeview_frame_rk4.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree_rk4 = ttk.Treeview(self.treeview_frame_rk4, columns=("Paso", "x", "y"), show="headings", height=10, style="RK4.Treeview")
        self.tree_rk4.heading("Paso", text="Paso")
        self.tree_rk4.heading("x", text="x")
        self.tree_rk4.heading("y", text="y")
        self.tree_rk4.column("Paso", width=50, anchor="center")
        self.tree_rk4.column("x", width=100, anchor="center")
        self.tree_rk4.column("y", width=100, anchor="center")
        self.tree_rk4.pack(fill="both", expand=True)


    def lg_metodo_rk4(self):
        self.mensaje_estado_rk4.configure(text="")
        self.resultado_final_rk4.configure(text="")
        for item in self.tree_rk4.get_children():
            self.tree_rk4.delete(item)

        try:
            f_str = self.entry_funcion_f.get().strip()
            if not f_str:
                self.mostrar_mensaje_estado("❌ Ingrese la función f(x, y).", tipo="error", destino="rk4")
                return
            if "=" in f_str:
                self.mostrar_mensaje_estado("⚠ Ingrese solo el lado derecho de la ecuación. Ejemplo: x + y", tipo="advertencia", destino="rk4")
                return 

            x0 = float(self.entry_x0_rk.get().strip())
            y0 = float(self.entry_y0_rk.get().strip())
            h = float(self.entry_h_rk.get().strip())
            n = int(self.entry_n_rk.get().strip())

            if h == 0:
                self.mostrar_mensaje_estado("❌ h no puede ser 0", tipo="error", destino="rk4")
                return  

            if n <= 0:
                self.mostrar_mensaje_estado("❌ n no puede ser menor o igual a 0", tipo="error", destino="rk4")
                return  

            xf = x0 + h * n
        except Exception as e:
            self.mensaje_estado_rk4.configure(text=str(e))
            return

        try:
            f_expr = sp.sympify(f_str)
            f = sp.lambdify(("x", "y"), f_expr, modules=["math", "sympy"])
        except Exception as e:
            self.mensaje_estado_rk4.configure(text=f"❌ Error en función f(x, y): {str(e)}")
            return

        try:
            xs, ys = [x0], [y0]
            for _ in range(n):
                xi, yi = xs[-1], ys[-1]
                k1 = h * f(xi, yi)
                k2 = h * f(xi + h / 2, yi + k1 / 2)
                k3 = h * f(xi + h / 2, yi + k2 / 2)
                k4 = h * f(xi + h, yi + k3)
                yi_new = yi + (k1 + 2 * k2 + 2 * k3 + k4) / 6
                xs.append(xi + h)
                ys.append(yi_new)

            for i, (x_val, y_val) in enumerate(zip(xs, ys)):
                self.tree_rk4.insert("", "end", values=(i, f"{x_val:.5f}", f"{y_val:.5f}"))

            self.resultado_final_rk4.configure(
                text=f"🔎 Resultado final: y({xs[-1]:.3f}) ≈ {ys[-1]:.5f}"
            )

            if hasattr(self, "rk4_canvas"):
                self.rk4_canvas.get_tk_widget().destroy()

            fig, ax = plt.subplots(figsize=(6, 3))
            ax.plot(xs, ys, marker="o", linestyle="--", label="RK4")
            ax.set_title("Aproximación con Runge-Kutta 4")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.grid(True)
            ax.legend()
            self.rk4_canvas = FigureCanvasTkAgg(fig, self.scroll_rk4)
            self.rk4_canvas.draw()
            self.rk4_canvas.get_tk_widget().pack(pady=10)

            guardar_resultado_metodo("RK4", f_str, x0, y0, xs[-1], n, xs, ys)

        except Exception as e:
            self.mensaje_estado_rk4.configure(text=f"❌ Error durante el cálculo: {str(e)}")


    def UI_metodo_heun(self):
        frame = self.scroll_heun

        ecuacion_frame = ctk.CTkFrame(frame)
        ecuacion_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(ecuacion_frame, text="Ingrese y' = f(x, y)", font=("Arial", 14)).grid(row=0, column=0, padx=5)
        self.entry_funcion_f_heun = ctk.CTkEntry(ecuacion_frame, placeholder_text="Ej: x + y")
        self.entry_funcion_f_heun.grid(row=0, column=1, padx=5, pady=5)

        self.ejemplos_heun = ["x + y", "x * y", "x**2 - y"]
        self.ejemplo_var_heun = ctk.StringVar(value=self.ejemplos_heun[0])
        ejemplo_menu = ctk.CTkOptionMenu(ecuacion_frame, variable=self.ejemplo_var_heun, values=self.ejemplos_heun)
        ejemplo_menu.grid(row=0, column=2, padx=5)
        ctk.CTkButton(ecuacion_frame, text="Cargar Ejemplo", command=self.cargar_ejemplo_heun).grid(row=0, column=3, padx=5)

        datos_frame = ctk.CTkFrame(frame)
        datos_frame.pack(fill="x", padx=10, pady=5)
        self._crear_entrada(datos_frame, "x₀ inicial", 0, 0, "entry_x0_heun")
        self._crear_entrada(datos_frame, "y₀ inicial", 0, 2, "entry_y0_heun")
        self._crear_entrada(datos_frame, "x tamaño (h)", 0, 4, "entry_xf_heun")
        self._crear_entrada(datos_frame, "n pasos", 0, 6, "entry_n_heun")

        boton_frame = ctk.CTkFrame(frame)
        boton_frame.pack(padx=10, pady=5)
        ctk.CTkButton(boton_frame, text="Aplicar Método de Heun", command=self.lg_metodo_heun).pack()

        # Mensaje de estado
        self.mensaje_estado_heun = ctk.CTkLabel(frame, text="", font=("Arial", 13), text_color="red")
        self.mensaje_estado_heun.pack(pady=(0, 5), padx=10, anchor="w")

        # Resultado final
        self.resultado_final_heun = ctk.CTkLabel(frame, text="", font=("Arial", 14))
        self.resultado_final_heun.pack(padx=10, pady=(0, 10), anchor="w")

        # Estilo y tabla
        style = ttk.Style()
        style.configure("Heun.Treeview", font=("Arial", 12), rowheight=28)
        style.configure("Heun.Treeview.Heading", font=("Arial", 13, "bold"))

        self.treeview_frame_heun = ctk.CTkFrame(frame)
        self.treeview_frame_heun.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree_heun = ttk.Treeview(self.treeview_frame_heun, columns=("Paso", "x", "y"), show="headings", height=10, style="Heun.Treeview")
        self.tree_heun.heading("Paso", text="Paso")
        self.tree_heun.heading("x", text="x")
        self.tree_heun.heading("y", text="y")
        self.tree_heun.column("Paso", width=50, anchor="center")
        self.tree_heun.column("x", width=100, anchor="center")
        self.tree_heun.column("y", width=100, anchor="center")
        self.tree_heun.pack(fill="both", expand=True)


    
    def lg_metodo_heun(self):
        self.mensaje_estado_heun.configure(text="")
        self.resultado_final_heun.configure(text="")
        for item in self.tree_heun.get_children():
            self.tree_heun.delete(item)

        try:
            f_str = self.entry_funcion_f_heun.get().strip()
            if not f_str:
                self.mensaje_estado_heun.configure(text="❌ Ingrese la función f(x, y).")
                return
            if "=" in f_str:
                self.mensaje_estado_heun.configure(text="⚠ Ingrese solo el lado derecho de la ecuación. Ejemplo: x + y")
                return

            x0 = float(self.entry_x0_heun.get().strip())
            y0 = float(self.entry_y0_heun.get().strip())
            xf = float(self.entry_xf_heun.get().strip())
            n = int(self.entry_n_heun.get().strip())

            if n <= 0:
                self.mensaje_estado_heun.configure(text="❌ El número de pasos debe ser mayor que cero.")
                return
            if x0 == xf:
                self.mensaje_estado_heun.configure(text="❌ x₀ y x final no pueden ser iguales.")
                return

        except ValueError as e:
            self.mensaje_estado_heun.configure(text=f"❌ Error en valores: {str(e)}")
            return

        try:
            resultado = self.solver.metodo_heun(f_str, x0, y0, xf, n)
            if not resultado["exito"]:
                self.mensaje_estado_heun.configure(text=f"❌ Error al aplicar Heun: {resultado['mensaje']}")
                return
        except Exception as e:
            self.mensaje_estado_heun.configure(text=f"❌ Excepción durante el cálculo: {str(e)}")
            return

        xs = resultado["xs"]
        ys = resultado["ys"]

        for i, (x, y) in enumerate(zip(xs, ys)):
            self.tree_heun.insert("", "end", values=(i, f"{x:.5f}", f"{y:.5f}"))

        self.resultado_final_heun.configure(
            text=f"🔎 Resultado final: y({xs[-1]:.3f}) ≈ {ys[-1]:.5f}"
        )

        if hasattr(self, "heun_canvas"):
            self.heun_canvas.get_tk_widget().destroy()

        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(xs, ys, marker="o", linestyle="--", label="Heun")
        ax.set_title("Aproximación con Método de Heun")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True)
        ax.legend()

        self.heun_canvas = FigureCanvasTkAgg(fig, self.scroll_heun)
        self.heun_canvas.draw()
        self.heun_canvas.get_tk_widget().pack(pady=10)

        guardar_resultado_metodo("Heun (Euler mejorado)", f_str, x0, y0, xf, n, xs, ys)



    def UI_metodo_taylor2(self):
        frame = self.scroll_taylor2

        # Entradas
        self._crear_entrada(frame, "x₀ Inicial", 0, 0, "entry_x0_taylor")
        self._crear_entrada(frame, "y₀ Inicial", 0, 2, "entry_y0_taylor")
        self._crear_entrada(frame, "x tamaño (h)", 0, 4, "entry_xf_taylor")
        self._crear_entrada(frame, "n pasos", 0, 6, "entry_n_taylor")

        ctk.CTkLabel(frame, text="f(x, y) = y'").grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        self.entry_funcion_f_taylor = ctk.CTkEntry(frame, width=400)
        self.entry_funcion_f_taylor.grid(row=1, column=2, columnspan=4, padx=10, pady=5, sticky="ew")

        df_frame = ctk.CTkFrame(frame)
        df_frame.grid(row=2, column=0, columnspan=6, padx=10, pady=5, sticky="ew")
        df_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(df_frame, text="f'(x, y)").grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.entry_funcion_df_taylor = ctk.CTkEntry(df_frame, placeholder_text="f'(x, y)")
        self.entry_funcion_df_taylor.grid(row=0, column=1, padx=(0, 5), sticky="ew")
        ctk.CTkButton(df_frame, text="Calcular f'(x, y)", command=self.calcular_derivada_total_taylor).grid(row=0, column=2)

        self.ejemplos_taylor2 = ["x + y", "x * y", "x**2 - y"]
        self.ejemplo_var_taylor2 = ctk.StringVar(value=self.ejemplos_taylor2[0])
        ctk.CTkLabel(frame, text="Ejemplos").grid(row=3, column=0, padx=5, pady=5)
        ejemplo_menu = ctk.CTkOptionMenu(frame, variable=self.ejemplo_var_taylor2, values=self.ejemplos_taylor2)
        ejemplo_menu.grid(row=3, column=1, columnspan=2, padx=5, pady=5)
        ctk.CTkButton(frame, text="Cargar Ejemplo", command=self.cargar_ejemplo_taylor2).grid(row=3, column=3, columnspan=2, padx=5, pady=5)

        ctk.CTkButton(frame, text="Aplicar Método de Taylor 2°", command=self.lg_metodo_taylor2).grid(row=4, column=0, columnspan=6, pady=10)

        # Mensaje de estado y resultado
        self.mensaje_estado_taylor2 = ctk.CTkLabel(frame, text="", font=("Arial", 13), text_color="red")
        self.mensaje_estado_taylor2.grid(row=5, column=0, columnspan=6, sticky="w", padx=10)

        self.resultado_final_taylor2 = ctk.CTkLabel(frame, text="", font=("Arial", 14))
        self.resultado_final_taylor2.grid(row=6, column=0, columnspan=6, sticky="w", padx=10, pady=(0, 10))

        # Tabla
        style = ttk.Style()
        style.configure("Taylor2.Treeview", font=("Arial", 12), rowheight=28)
        style.configure("Taylor2.Treeview.Heading", font=("Arial", 13, "bold"))

        self.treeview_frame_taylor2 = ctk.CTkFrame(frame)
        self.treeview_frame_taylor2.grid(row=7, column=0, columnspan=6, padx=10, pady=5, sticky="nsew")

        self.tree_taylor2 = ttk.Treeview(self.treeview_frame_taylor2, columns=("Paso", "x", "y"), show="headings", height=10, style="Taylor2.Treeview")
        self.tree_taylor2.heading("Paso", text="Paso")
        self.tree_taylor2.heading("x", text="x")
        self.tree_taylor2.heading("y", text="y")
        self.tree_taylor2.column("Paso", width=50, anchor="center")
        self.tree_taylor2.column("x", width=100, anchor="center")
        self.tree_taylor2.column("y", width=100, anchor="center")
        self.tree_taylor2.pack(fill="both", expand=True)

        self.frame_grafico_taylor2 = ctk.CTkFrame(frame)
        self.frame_grafico_taylor2.grid(row=8, column=0, columnspan=6, sticky="nsew", padx=10, pady=10)

        frame.grid_rowconfigure(8, weight=1)
        frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

    
    def lg_metodo_taylor2(self):
        self.mensaje_estado_taylor2.configure(text="")
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
                self.mostrar_mensaje_estado("❌ Ingrese ambas funciones: f(x,y) y f'(x,y)", tipo="error", destino="taylor2")
                return
            if n <= 0 or x0 == xf:
                self.mostrar_mensaje_estado("❌ Verifique que n > 0 y x₀ ≠ x final.", tipo="error", destino="taylor2")
                return

        except ValueError as e:
            self.mostrar_mensaje_estado(f"❌ Error en valores: {str(e)}", tipo="error", destino="taylor2")
            return

        try:
            resultado = self.solver.metodo_taylor_segundo_orden(f_str, df_str, x0, y0, xf, n)
            if not resultado["exito"]:
                self.mostrar_mensaje_estado(f"❌ Error al aplicar Taylor 2° orden: {resultado['mensaje']}", tipo="error", destino="taylor2")
                return
        except Exception as e:
            self.mostrar_mensaje_estado(f"❌ Excepción durante cálculo: {str(e)}", tipo="error", destino="taylor2")
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



    def UI_metodo_minimos(self):
        frame = self.scroll_minimos

        ctk.CTkLabel(frame, text="Selecciona un método numérico").pack(pady=5)
        
        self.metodos_disponibles = [r["metodo"] for r in ResultadosEDOManager.obtener_todos()]
        self.opcion_metodo = ctk.StringVar()
        self.menu_minimos = ctk.CTkOptionMenu(frame, variable=self.opcion_metodo, values=list(set(self.metodos_disponibles)))
        self.menu_minimos.pack(pady=5)

        
        ctk.CTkButton(frame, text="Aplicar Ajuste Lineal", command=self.aplicar_minimos_cuadrados).pack(pady=10)

        self.resultado_minimos = ctk.CTkTextbox(frame, height=200)
        self.resultado_minimos.pack(fill="both", expand=True, padx=10, pady=10)

        self.frame_grafico_minimos = ctk.CTkFrame(frame)
        self.frame_grafico_minimos.pack(fill="both", expand=True, padx=10, pady=10)

    def aplicar_minimos_cuadrados(self):
        self.resultado_minimos.delete("0.0", "end")
        metodo = self.opcion_metodo.get()
        datos = ResultadosEDOManager.filtrar_por_metodo(metodo)

        if not datos:
            self.resultado_minimos.insert("end", "❌ No hay datos para ese método.")
            return

        resultado = MinimosCuadrados.ajustar_lineal(datos[-1]["xs"], datos[-1]["ys"])

        self.resultado_minimos.insert("end", f"Ajuste lineal: y = {resultado['a']:.4f}x + {resultado['b']:.4f}\n")

        # Limpiar gráfico anterior
        for widget in self.frame_grafico_minimos.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(resultado["xs"], resultado["ys_originales"], 'o', label= metodo)
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

    def on_tab_changed(self, event):
        tab_name = self.tabview.get()
        if tab_name == "Mínimos Cuadrados":
            self.actualizar_menu_metodos_minimos()

    def UI_metodo_comparativa(self):
        frame = self.scroll_comparativa

        ctk.CTkLabel(frame, text="Seleccione los métodos para comparar", font=("Arial", 14)).pack(pady=5)

        self.checkboxes_metodos = []
        self.var_checkboxes = []

        # Área para checkboxes (rellenado dinámico)
        self.frame_checkboxes = ctk.CTkFrame(frame)
        self.frame_checkboxes.pack(fill="x", padx=10, pady=5)

        # Botón para lanzar comparación
        ctk.CTkButton(frame, text="Comparar Métodos", command=self.comparar_metodos).pack(pady=10)

        # Área de resultados (tabla)
        self.resultado_comparativa = ctk.CTkTextbox(frame, height=200)
        self.resultado_comparativa.pack(fill="both", expand=True, padx=10, pady=10)

        # Área de gráfica
        self.frame_grafico_comparativa = ctk.CTkFrame(frame)
        self.frame_grafico_comparativa.pack(fill="both", expand=True, padx=10, pady=10)

    def comparar_metodos(self):
        self.resultado_comparativa.delete("0.0", "end")

        seleccionados = [met for met, var in self.var_checkboxes if var.get()]
        if not seleccionados:
            self.resultado_comparativa.insert("end", "❌ Selecciona al menos un método.")
            return

        resultados = []
        for metodo in seleccionados:
            datos = ResultadosEDOManager.filtrar_por_metodo(metodo)
            if datos:
                resultados.append(datos[-1])  # último resultado de ese método

        if not resultados:
            self.resultado_comparativa.insert("end", "❌ No hay datos disponibles para mostrar.")
            return

        # Determinar el número máximo de pasos
        max_pasos = max(len(r["xs"]) for r in resultados)

        # Encabezado
        encabezado = "Paso\t" + "\t".join(f"{r['metodo']}" for r in resultados) + "\n"
        self.resultado_comparativa.insert("end", encabezado)
        self.resultado_comparativa.insert("end", "-" * len(encabezado) + "\n")

        # Construir filas paso a paso
        for i in range(max_pasos):
            fila = f"{i}\t"
            for r in resultados:
                if i < len(r["ys"]):
                    fila += f"{r['ys'][i]:.4f}\t"
                else:
                    fila += "----\t"
            self.resultado_comparativa.insert("end", fila + "\n")

        # Gráfica
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


    def actualizar_checkboxes_comparativa(self):
        # Elimina checkboxes previos
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




    def _crear_entrada(self, parent, texto, row, col, attr_name):
        ctk.CTkLabel(parent, text=texto).grid(row=row, column=col, padx=5)
        entry = ctk.CTkEntry(parent, width=80)
        entry.grid(row=row, column=col + 1, padx=5)
        setattr(self, attr_name, entry)
    

    def cargar_ejemplo_taylor2(self):
        ejemplo = self.ejemplo_var_taylor2.get()
        self.entry_funcion_f_taylor.delete(0, "end")
        self.entry_funcion_f_taylor.insert(0, ejemplo)

    def cargar_ejemplo_heun(self):
        ejemplo = self.ejemplo_var_heun.get()
        self.entry_funcion_f_heun.delete(0, "end")
        self.entry_funcion_f_heun.insert(0, ejemplo)


    def cargar_ejemplo_euler(self):
        ejemplo = self.ejemplo_var_euler.get()
        self.entry_funcion_f.delete(0, "end")
        self.entry_funcion_f.insert(0, ejemplo)

    def cargar_ejemplo(self):
        """Carga un ejemplo seleccionado"""
        ejemplo = self.ejemplo_var.get()
        self.entry_ecuacion.delete(0, "end")
        self.entry_ecuacion.insert(0, ejemplo)
        
        # Limpiar condiciones iniciales
        self.entry_x0.delete(0, "end")
        self.entry_y0.delete(0, "end")
        self.entry_dy0.delete(0, "end")
        
    
    def limpiar_analitica(self):
        """Limpia los campos y resultados de la pestaña analítica"""
        self.entry_ecuacion.delete(0, "end")
        self.entry_x0.delete(0, "end")
        self.entry_y0.delete(0, "end")
        self.entry_dy0.delete(0, "end")

        for widget in self.resultado_scroll.winfo_children():
            widget.destroy()

    
    def _obtener_condiciones_iniciales(self):
        """Obtiene las condiciones iniciales de los campos de entrada"""
        condiciones = []
        
        try:
            x0_str = self.entry_x0.get().strip()
            y0_str = self.entry_y0.get().strip()
            dy0_str = self.entry_dy0.get().strip()
            
            if x0_str and y0_str:
                x0 = float(x0_str) if x0_str else None
                y0 = float(y0_str) if y0_str else None
                
                condiciones = [x0, y0]
                
                if dy0_str:
                    dy0 = float(dy0_str)
                    condiciones.append(dy0)
            
            return condiciones if condiciones else None
        
        except ValueError:
            self.mostrar_error("Error en las condiciones iniciales. Use valores numéricos.")
            return None
    
    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error"""
        for widget in self.resultado_scroll.winfo_children():
            widget.destroy()
        mostrar_label(f"❌ Error: {mensaje}")
    
    def cargar_ejemplo_rk4(self):
        ejemplo = self.ejemplo_var_rk4.get()
        self.entry_funcion_f_rk.delete(0, "end")
        self.entry_funcion_f_rk.insert(0, ejemplo)

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

    def mostrar_mensaje_estado(self, mensaje, tipo="error", destino="euler"):
        colores = {
            "error": "red",
            "advertencia": "#FFD700",
            "info": "white"
        }
        color = colores.get(tipo, "red")

        if destino == "euler" and hasattr(self, "mensaje_estado"):
            self.mensaje_estado.configure(text=mensaje, text_color=color)
        elif destino == "rk4" and hasattr(self, "mensaje_estado_rk4"):
            self.mensaje_estado_rk4.configure(text=mensaje, text_color=color)
        elif destino == "heun" and hasattr(self, "mensaje_estado_heun"):
            self.mensaje_estado_heun.configure(text=mensaje, text_color=color)
        elif destino == "taylor2" and hasattr(self, "mensaje_estado_taylor2"):
            self.mensaje_estado_taylor2.configure(text=mensaje, text_color=color)
        else:
            print(f"[Mensaje {tipo.upper()}] {mensaje}")

    def calcular_derivada_total_taylor(self):
        x, y = sp.symbols('x y')
        f_str = self.entry_funcion_f_taylor.get().strip()

        if not f_str:
            self.mostrar_mensaje_estado("❌ Ingrese primero f(x, y)", tipo="error", destino="taylor2")
            return

        try:
            f_expr = sp.sympify(f_str)
            df_dx = sp.diff(f_expr, x)
            df_dy = sp.diff(f_expr, y)
            total = df_dx + df_dy * f_expr
            self.entry_funcion_df_taylor.delete(0, "end")
            self.entry_funcion_df_taylor.insert(0, str(total))
            self.mostrar_mensaje_estado("✅ Derivada total calculada exitosamente.", tipo="info", destino="taylor2")
        except Exception as e:
            self.mostrar_mensaje_estado(f"❌ Error al calcular f'(x, y): {str(e)}", tipo="error", destino="taylor2")

