import numpy as np
from scipy.stats import poisson
class GeneradorDistribuciones:
    def __init__(self, semilla, a, c, m, n):
        self.semilla = semilla
        self.a = a
        self.c = c
        self.m = m
        self.n = n

    def generar_congruencial(self):
        valores = []
        normalizados = []

        x = self.semilla
        for _ in range(self.n):
            x = (self.a * x + self.c) % self.m
            valores.append(x)
            normalizados.append(x / self.m)

        return valores, normalizados

    def aplicar_poisson(self, uniformes, lam=4):

        return poisson.ppf(uniformes, mu=lam).astype(int)

    def aplicar_exponencial(self, uniformes, lambd=1.0):
        return -np.log(1 - np.array(uniformes)) / lambd

    def construir_tabla(self, valores, normalizados, transformados):
        tabla = []
        for i in range(len(valores)):
            x = transformados[i]
            tabla.append({
                "n": i+1,
                "Xn": valores[i],
                "Un": normalizados[i],
                "f(Un)": x,
                "X²": x**2,
                "√X²": np.sqrt(x**2)
            })
        return tabla


    def aplicar_normal(self, u_vals):
        import math
        normales = []
        for i in range(0, len(u_vals) - 1, 2):
            u1 = u_vals[i]
            u2 = u_vals[i + 1]
            z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
            z1 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
            normales.extend([z0, z1])
        if len(normales) < len(u_vals):
            normales.append(normales[-1])  # Padding en caso de número impar
        return normales[:len(u_vals)]

    def aplicar_binomial(self, u_vals, n=10, p=0.5):
        import random
        resultados = []
        for _ in u_vals:
            count = sum(1 if random.random() < p else 0 for _ in range(n))
            resultados.append(count)
        return resultados
