import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import numpy as np
import random
import tkinter as tk

class MatricesPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.filas = 3
        self.columnas = 3
        self.inputs_A = []
        self.inputs_B = []

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(expand=True, fill="both", padx=10, pady=10)

        self.tab_operaciones = self.tabview.add("🧮 Operaciones")
      

        self.init_operaciones()

    def pedir_valor(self, mensaje, titulo):
        top = ctk.CTkToplevel(self)
        top.title(titulo)
        top.geometry("300x150")
        ctk.CTkLabel(top, text=mensaje, font=("Arial", 14)).pack(pady=10)
        entrada = ctk.CTkEntry(top)
        entrada.pack(pady=5)

        resultado = {"valor": None}

        def aceptar():
            resultado["valor"] = entrada.get()
            top.destroy()

        ctk.CTkButton(top, text="Aceptar", command=aceptar).pack(pady=10)
        top.grab_set()
        top.wait_window()
        return resultado["valor"]

    def init_operaciones(self):

        frame_base = self.tab_operaciones

        # === CANVAS + SCROLLBAR ===
        canvas = tk.Canvas(frame_base, background="#2b2b2b", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_base, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # === CONTENIDO PRINCIPAL ===
        self.scroll_content = ctk.CTkFrame(canvas)
        canvas_window = canvas.create_window((0, 0), window=self.scroll_content, anchor="nw")

        def ajustar_scroll(e):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.scroll_content.bind("<Configure>", ajustar_scroll)

        def expandir_canvas(e):
            canvas.itemconfig(canvas_window, width=e.width)

        canvas.bind("<Configure>", expandir_canvas)

        # === CONTENIDO ===
        ctk.CTkLabel(self.scroll_content, text="Operaciones con Matrices", font=("Arial", 20)).pack(pady=10)

        # Restricción de tamaño
        self.filas_A_valor = self.columnas_A_valor = 3
        self.filas_B_valor = self.columnas_B_valor = 3
        LIMITE_MAX = 5
        LIMITE_MIN = 1

        def limitar_dim(v):
            return max(LIMITE_MIN, min(LIMITE_MAX, v))

        # Dimensiones
        for letra in ["A", "B"]:
            frame_dim = ctk.CTkFrame(self.scroll_content)
            frame_dim.pack(pady=5)
            ctk.CTkLabel(frame_dim, text=f"📘 Matriz {letra}").grid(row=0, column=0)
            for k, tipo in enumerate(["filas", "columnas"]):
                idx = 1 + k * 4
                ctk.CTkLabel(frame_dim, text=f"{tipo.capitalize()}:").grid(row=0, column=idx)
                lbl = ctk.CTkLabel(frame_dim, text="3", width=40)
                lbl.grid(row=0, column=idx + 1)
                setattr(self, f"label_{tipo}_{letra}", lbl)
                ctk.CTkButton(frame_dim, text="-", width=30,
                            command=lambda l=letra, t=tipo: self.cambiar_dim(l, t, -1)).grid(row=0, column=idx + 2)
                ctk.CTkButton(frame_dim, text="+", width=30,
                            command=lambda l=letra, t=tipo: self.cambiar_dim(l, t, 1)).grid(row=0, column=idx + 3)

        # Botones y operaciones
        ctk.CTkButton(self.scroll_content, text="LIMPIAR TABLAS", command=self.crear_tablas).pack(pady=5)

        btns = ctk.CTkFrame(self.scroll_content)
        btns.pack(pady=5)
        for name in [("Ceros", "zeros"), ("Unos", "ones"), ("Aleatorios", "rand")]:
            ctk.CTkButton(btns, text=name[0], command=lambda t=name[1]: self.rellenar(t)).pack(side="left", padx=5)

        # Matrices
        contenedor_matrices = ctk.CTkFrame(self.scroll_content)
        contenedor_matrices.pack(pady=10)

        ctk.CTkLabel(contenedor_matrices, text="Matriz A", font=("Arial", 16)).grid(row=0, column=0, padx=20)
        ctk.CTkLabel(contenedor_matrices, text="Matriz B", font=("Arial", 16)).grid(row=0, column=1, padx=20)

        self.matriz_A = ctk.CTkFrame(contenedor_matrices)
        self.matriz_A.grid(row=1, column=0, padx=20)
        self.matriz_B = ctk.CTkFrame(contenedor_matrices)
        self.matriz_B.grid(row=1, column=1, padx=20)

        self.operacion = ctk.CTkComboBox(self.scroll_content, values=[
            "Suma (A + B)", "Resta (A - B)", "Multiplicación (A * B)",
            "Inversa de A", "Determinante de A", "Transpuesta de A", "Valores propios de A",
            "Inversa de B", "Determinante de B", "Transpuesta de B", "Valores propios de B",
            "A * escalar", "B * escalar", "A^n", "B^n", "Traza de A", "Traza de B", "Norma de A", "Norma de B"
        ])
        self.operacion.set("Suma (A + B)")
        self.operacion.pack(pady=10)

        ctk.CTkButton(self.scroll_content, text="Calcular", command=self.calcular).pack(pady=5)
        ctk.CTkLabel(self.scroll_content, text="RESULTADO DE LA OPERACIÓN:", font=("Arial", 16)).pack()
        self.resultado_frame = ctk.CTkFrame(self.scroll_content)
        self.resultado_frame.pack()
        self.resumen_operacion = ctk.CTkLabel(self.scroll_content, text="", font=("Arial", 14), text_color="gray")
        self.resumen_operacion.pack(pady=(5, 10))

        self.crear_tablas()


    def actualizar_dim(self):
        try:
            self.filas = int(self.entry_filas.get())
            self.columnas = int(self.entry_columnas.get())
            if self.filas <= 0 or self.columnas <= 0:
                raise ValueError("Debe ingresar valores positivos.")
            self.crear_tablas()
        except Exception as e:
            CTkMessagebox(title="Error", message=str(e), icon="cancel")

    def crear_tablas(self):
        try:
            filas_A = self.filas_A_valor
            cols_A = self.columnas_A_valor
            filas_B = self.filas_B_valor
            cols_B = self.columnas_B_valor


            if min(filas_A, cols_A, filas_B, cols_B) <= 0:
                raise ValueError("Todas las dimensiones deben ser mayores a 0.")

            for w in self.matriz_A.winfo_children(): w.destroy()
            for w in self.matriz_B.winfo_children(): w.destroy()
            self.inputs_A, self.inputs_B = [], []

            for i in range(filas_A):
                fila_A = []
                for j in range(cols_A):
                    a = ctk.CTkEntry(self.matriz_A, width=60)
                    a.grid(row=i, column=j, padx=2, pady=2)
                    a.insert(0, "0")
                    fila_A.append(a)
                self.inputs_A.append(fila_A)

            for i in range(filas_B):
                fila_B = []
                for j in range(cols_B):
                    b = ctk.CTkEntry(self.matriz_B, width=60)
                    b.grid(row=i, column=j, padx=2, pady=2)
                    b.insert(0, "0")
                    fila_B.append(b)
                self.inputs_B.append(fila_B)

        except Exception as e:
            CTkMessagebox(title="Error", message=str(e), icon="cancel")


    def rellenar(self, tipo):
        for tabla in [self.inputs_A, self.inputs_B]:
            for fila in tabla:
                for celda in fila:
                    val = {"zeros": 0, "ones": 1, "rand": random.randint(1, 30)}[tipo]
                    celda.delete(0, "end")
                    celda.insert(0, str(val))

    def leer_matriz(self, inputs, nombre):
        matriz = []
        for i, fila in enumerate(inputs):
            fila_valores = []
            for j, celda in enumerate(fila):
                val = celda.get()
                if not val.strip():
                    raise ValueError(f"{nombre}[{i+1},{j+1}] vacío.")
                try:
                    fila_valores.append(float(val))
                except:
                    raise ValueError(f"{nombre}[{i+1},{j+1}] inválido.")
            matriz.append(fila_valores)
        return np.array(matriz)

    def mostrar_resultado(self, matriz):
        for w in self.resultado_frame.winfo_children(): w.destroy()
        matriz = np.atleast_2d(matriz)
        for i in range(matriz.shape[0]):
            for j in range(matriz.shape[1]):
                r = ctk.CTkEntry(self.resultado_frame, width=60)
                r.grid(row=i, column=j, padx=2, pady=2)
                r.insert(0, str(round(matriz[i][j], 3)))
                r.configure(state="disabled")

    def calcular(self):
        try:
            A = self.leer_matriz(self.inputs_A, "A")
            op = self.operacion.get()
            if "B" in op:
                B = self.leer_matriz(self.inputs_B, "B")

            if op == "Suma (A + B)":
                if A.shape != B.shape:
                    raise ValueError("A y B deben tener el mismo tamaño.")
                resultado = A + B
            elif op == "Resta (A - B)":
                if A.shape != B.shape:
                    raise ValueError("A y B deben tener el mismo tamaño.")
                resultado = A - B
            elif op == "Multiplicación (A * B)":
                if A.shape[1] != B.shape[0]:
                    raise ValueError("Columnas de A deben coincidir con filas de B.")
                resultado = A @ B
            elif op == "Inversa de A":
                if A.shape[0] != A.shape[1]:
                    raise ValueError("A debe ser cuadrada.")
                if np.linalg.det(A) == 0:
                    raise ValueError("A no tiene inversa.")
                resultado = np.linalg.inv(A)
            elif op == "Determinante de A":
                if A.shape[0] != A.shape[1]:
                    raise ValueError("A debe ser cuadrada.")
                resultado = [[np.linalg.det(A)]]
            elif op == "Transpuesta de A":
                resultado = A.T
            elif op == "Valores propios de A":
                if A.shape[0] != A.shape[1]:
                    raise ValueError("A debe ser cuadrada.")
                resultado = [[val] for val in np.linalg.eigvals(A)]
            elif op == "Inversa de B":
                B = self.leer_matriz(self.inputs_B, "B")
                resultado = self.operar_matriz(B, "inversa", "B")
            elif op == "Determinante de B":
                B = self.leer_matriz(self.inputs_B, "B")
                resultado = self.operar_matriz(B, "determinante", "B")
            elif op == "Transpuesta de B":
                B = self.leer_matriz(self.inputs_B, "B")
                resultado = self.operar_matriz(B, "transpuesta", "B")
            elif op == "Valores propios de B":
                B = self.leer_matriz(self.inputs_B, "B")
                resultado = self.operar_matriz(B, "valores_propios", "B")
            elif op == "A * escalar":
                resultado = self.escalar_o_potencia(A, "escalar", "A")
            elif op == "B * escalar":
                B = self.leer_matriz(self.inputs_B, "B")
                resultado = self.escalar_o_potencia(B, "escalar", "B")
            elif op == "A^n":
                resultado = self.escalar_o_potencia(A, "potencia", "A")
            elif op == "B^n":
                B = self.leer_matriz(self.inputs_B, "B")
                resultado = self.escalar_o_potencia(B, "potencia", "B")
            elif op == "Traza de A":
                resultado = self.operar_matriz(A, "traza", "A")
            elif op == "Traza de B":
                B = self.leer_matriz(self.inputs_B, "B")
                resultado = self.operar_matriz(B, "traza", "B")
            elif op == "Norma de A":
                resultado = self.operar_matriz(A, "norma", "A")
            elif op == "Norma de B":
                B = self.leer_matriz(self.inputs_B, "B")
                resultado = self.operar_matriz(B, "norma", "B")

            else:
                raise ValueError("Operación no reconocida.")

            self.mostrar_resultado(resultado)
            self.resumen_operacion.configure(text=f"✅ Operación realizada: {op}")

        except Exception as e:
            CTkMessagebox(title="Error", message=str(e), icon="cancel")
            self.resumen_operacion.configure(text=f"❌ Error: {str(e)}")

    def escalar_o_potencia(self, matriz, tipo, nombre):
        if tipo == "escalar":
            escalar = self.pedir_valor("Introduce el escalar", f"{nombre} * escalar")
            if escalar is None or escalar.strip() == "":
                raise ValueError("Operación cancelada.")
            try:
                escalar = float(escalar)
            except ValueError:
                raise ValueError("El escalar debe ser un número válido.")
            return escalar * matriz

        elif tipo == "potencia":
            if matriz.shape[0] != matriz.shape[1]:
                raise ValueError(f"{nombre} debe ser cuadrada para elevarla a una potencia.")
            potencia = self.pedir_valor("Introduce el exponente entero", f"{nombre} ^ n")
            if potencia is None or potencia.strip() == "":
                raise ValueError("Operación cancelada.")
            try:
                potencia = int(potencia)
            except ValueError:
                raise ValueError("El exponente debe ser un número entero.")
            return np.linalg.matrix_power(matriz, potencia)

        else:
            raise ValueError("Tipo de operación inválida.")


    def operar_matriz(self, matriz, op, nombre):
        if op == "inversa":
            if matriz.shape[0] != matriz.shape[1]:
                raise ValueError(f"{nombre} debe ser cuadrada.")
            if np.linalg.det(matriz) == 0:
                raise ValueError(f"{nombre} no tiene inversa.")
            return np.linalg.inv(matriz)
        elif op == "determinante":
            if matriz.shape[0] != matriz.shape[1]:
                raise ValueError(f"{nombre} debe ser cuadrada.")
            return [[np.linalg.det(matriz)]]
        elif op == "transpuesta":
            return matriz.T
        elif op == "valores_propios":
            if matriz.shape[0] != matriz.shape[1]:
                raise ValueError(f"{nombre} debe ser cuadrada.")
            return [[val] for val in np.linalg.eigvals(matriz)]
        elif op == "traza":
            if matriz.shape[0] != matriz.shape[1]:
                raise ValueError(f"{nombre} debe ser cuadrada.")
            return [[np.trace(matriz)]]
        elif op == "norma":
            return [[np.linalg.norm(matriz)]]
        else:
            raise ValueError("Operación no soportada.")


    def cambiar_dim(self, matriz, tipo, cambio):
        LIMITE_MAX = 5
        LIMITE_MIN = 1

        if matriz == "A":
            if tipo == "filas":
                nueva = self.filas_A_valor + cambio
                if LIMITE_MIN <= nueva <= LIMITE_MAX:
                    self.filas_A_valor = nueva
                    self.label_filas_A.configure(text=str(nueva))
            elif tipo == "columnas":
                nueva = self.columnas_A_valor + cambio
                if LIMITE_MIN <= nueva <= LIMITE_MAX:
                    self.columnas_A_valor = nueva
                    self.label_columnas_A.configure(text=str(nueva))

        elif matriz == "B":
            if tipo == "filas":
                nueva = self.filas_B_valor + cambio
                if LIMITE_MIN <= nueva <= LIMITE_MAX:
                    self.filas_B_valor = nueva
                    self.label_filas_B.configure(text=str(nueva))
            elif tipo == "columnas":
                nueva = self.columnas_B_valor + cambio
                if LIMITE_MIN <= nueva <= LIMITE_MAX:
                    self.columnas_B_valor = nueva
                    self.label_columnas_B.configure(text=str(nueva))

        self.crear_tablas()
    
    
