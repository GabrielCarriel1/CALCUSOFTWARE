import customtkinter as ctk
from module_logic.gestor_resultados import ResultadosEDOManager
def mostrar_label(contenedor, texto: str):
    """Agrega texto al contenedor (textbox o frame) de forma inteligente."""
    if isinstance(contenedor, ctk.CTkTextbox):
        contenedor.insert("end", texto + "\n")
    else:
        label = ctk.CTkLabel(contenedor, text=texto, anchor="w", justify="left")
        label.pack(anchor="w", pady=2)

def guardar_resultado_metodo(nombre_metodo, f_str, x0, y0, xf, n, xs, ys, **extras):
        entrada = {
            "metodo": nombre_metodo,
            "funcion": f_str,
            "x0": x0,
            "y0": y0,
            "xf": xf,
            "n": n,
            "xs": xs,
            "ys": ys,
        }
        entrada.update(extras)
        ResultadosEDOManager.agregar(entrada)