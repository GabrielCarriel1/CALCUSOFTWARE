import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from CTkMessagebox import CTkMessagebox
import networkx as nx
from module_logic.markov import calcular_estados_markov, calcular_estado_estable

class MarkovUI(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#101117")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.label_titulo = ctk.CTkLabel(self, text="Cadenas de Markov (n x n)", font=("Arial", 18, "bold"))
        self.label_titulo.grid(row=0, column=0, columnspan=2, pady=10)

        # Lado izquierdo: entradas
        self.panel_izquierdo = ctk.CTkFrame(self)
        self.panel_izquierdo.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.label_n = ctk.CTkLabel(self.panel_izquierdo, text="Número de estados (n):")
        self.label_n.grid(row=0, column=0, padx=5, pady=5)
        self.entry_n = ctk.CTkEntry(self.panel_izquierdo, width=60)
        self.entry_n.grid(row=0, column=1, padx=5, pady=5)

        self.button_generar = ctk.CTkButton(self.panel_izquierdo, text="Generar matriz", command=self.generar_matriz)
        self.button_generar.grid(row=0, column=2, padx=10)

        self.frame_matriz = ctk.CTkFrame(self.panel_izquierdo)
        self.frame_matriz.grid(row=1, column=0, columnspan=3, pady=10)

        self.entry_pasos = ctk.CTkEntry(self.panel_izquierdo, placeholder_text="Nro. pasos", width=150)
        self.entry_pasos.grid(row=2, column=0, columnspan=2, pady=5)

        self.boton_calcular = ctk.CTkButton(self.panel_izquierdo, text="Calcular evolución", command=self.calcular)
        self.boton_calcular.grid(row=3, column=0, columnspan=3, pady=5)

        self.entries = []

        # Lado derecho: resultados y gráfico
        self.panel_derecho = ctk.CTkFrame(self)
        self.panel_derecho.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.text_resultado = ctk.CTkTextbox(self.panel_derecho, height=200)
        self.text_resultado.pack(pady=5, fill="x", padx=10)

        self.frame_grafico = ctk.CTkFrame(self.panel_derecho)
        self.frame_grafico.pack(pady=5, fill="both", expand=True)

    def generar_matriz(self):
        for widget in self.frame_matriz.winfo_children():
            widget.destroy()
        self.entries.clear()

        try:
            n = int(self.entry_n.get())
            if n <= 0 or n > 5:
                CTkMessagebox(title="Error", message="El número de estados debe estar entre 1 y 5.")
                return
        except ValueError:
            CTkMessagebox(title="Error", message="Ingrese un valor entero válido para n.")
            return

        for i in range(n):
            row = []
            for j in range(n):
                entry = ctk.CTkEntry(self.frame_matriz, width=60)
                entry.grid(row=i, column=j, padx=2, pady=2)
                row.append(entry)
            self.entries.append(row)

        self.vector_inicial_entries = []
        ctk.CTkLabel(self.frame_matriz, text="Vector inicial:").grid(row=n, column=0, columnspan=n, pady=5)
        for j in range(n):
            entry = ctk.CTkEntry(self.frame_matriz, width=60)
            entry.grid(row=n+1, column=j, padx=2, pady=2)
            self.vector_inicial_entries.append(entry)


    def calcular(self):
        try:
            n = int(self.entry_n.get())
            pasos = int(self.entry_pasos.get())
            if pasos <= 0:
                CTkMessagebox(title="Error", message="El número de pasos debe ser mayor que 0.")
                return
        except ValueError:
            CTkMessagebox(title="Error", message="Ingrese valores enteros válidos para n y pasos.")
            return

        matriz = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                val = self.entries[i][j].get().replace(",", ".")  # reemplaza coma por punto
                try:
                    matriz[i, j] = float(val)
                except ValueError:
                    CTkMessagebox(title="Error", message=f"Valor inválido en la celda ({i+1}, {j+1})")
                    return

        # Verificar que cada fila sume 1
        for i in range(n):
            if not np.isclose(np.sum(matriz[i]), 1.0):
                CTkMessagebox(title="Error", message=f"La fila {i+1} de la matriz no suma 1.")
                return

        # Leer vector inicial
        vector = []
        for j, e in enumerate(self.vector_inicial_entries):
            val = e.get().replace(",", ".")
            try:
                vector.append(float(val))
            except ValueError:
                CTkMessagebox(title="Error", message=f"Valor inválido en el vector inicial, posición {j+1}")
                return

        vector = np.array(vector)

        if len(vector) != n:
            CTkMessagebox(title="Error", message="El vector inicial debe tener longitud igual a n.")
            return

        if not np.isclose(np.sum(vector), 1.0):
            CTkMessagebox(title="Error", message="El vector inicial debe sumar 1.")
            return

        try:
            historial = calcular_estados_markov(matriz, vector, pasos)
            estacionario = calcular_estado_estable(matriz)
            self.mostrar_diagrama_transicion(matriz)

            self.text_resultado.delete("0.0", "end")
            for i, v in enumerate(historial):
                self.text_resultado.insert("end", f"Paso {i}: {np.round(v, 4)}\n")

            if estacionario is not None:
                self.text_resultado.insert("end", f"\nEstado estable: {np.round(estacionario, 4)}")
            else:
                self.text_resultado.insert("end", "\nNo converge a un estado estable.")

            self.mostrar_grafico(historial)

        except Exception as e:
            CTkMessagebox(title="Error", message=f"Ocurrió un error: {str(e)}")


    def mostrar_diagrama_transicion(self, matriz):
        import matplotlib.pyplot as plt
        import networkx as nx
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        fig, ax = plt.subplots(figsize=(6, 3))
        G = nx.DiGraph()

        n = matriz.shape[0]
        for i in range(n):
            for j in range(n):
                prob = matriz[i, j]
                if prob > 0:
                    G.add_edge(f"{i+1}", f"{j+1}", weight=prob)

        # Posiciones horizontales lineales
        pos = {f"{i+1}": (i, 0) for i in range(n)}

        # Dibujar nodos
        nx.draw_networkx_nodes(G, pos, node_size=600, node_color="lightgreen", ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=10, font_color="black", ax=ax)

        # Dibujar aristas (con bucles)
        nx.draw_networkx_edges(G, pos, arrows=True, connectionstyle="arc3,rad=0.2", ax=ax)

        # Etiquetas de transiciones
        edge_labels = {(u, v): f"{d['weight']:.2f}" for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9, label_pos=0.5, ax=ax)

        ax.set_title("Diagrama de transición (estilo horizontal)")
        ax.axis("off")
        plt.tight_layout()

        # Mostrar en ventana emergente
        ventana = ctk.CTkToplevel(self)
        ventana.title("Diagrama de transición")
        ventana.geometry("700x400")
        canvas = FigureCanvasTkAgg(fig, master=ventana)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)



    def mostrar_grafico(self, historial):
        for w in self.frame_grafico.winfo_children():
            w.destroy()

        historial = np.array(historial)
        fig, ax = plt.subplots(figsize=(6, 3))
        for i in range(historial.shape[1]):
            ax.plot(range(len(historial)), historial[:, i], marker='o', label=f"Estado {i+1}")

        ax.set_xlabel("Paso")
        ax.set_ylabel("Probabilidad")
        ax.set_title("Evolución de estados")
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)