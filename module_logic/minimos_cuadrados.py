import numpy as np
from typing import List

class MinimosCuadrados:
    @staticmethod
    def ajustar_lineal(xs: List[float], ys: List[float]):
        xs = np.array(xs)
        ys = np.array(ys)
        
        # Cálculo de coeficientes a (pendiente) y b (intersección)
        A = np.vstack([xs, np.ones(len(xs))]).T
        a, b = np.linalg.lstsq(A, ys, rcond=None)[0]
        
        ys_ajustados = a * xs + b
        return {
            "a": a,
            "b": b,
            "ys_ajustados": ys_ajustados,
            "xs": xs,
            "ys_originales": ys
        }
