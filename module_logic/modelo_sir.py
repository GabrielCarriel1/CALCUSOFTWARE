# module_logic/modelo_sir.py
import numpy as np
from scipy.integrate import odeint

class ModeloSIR:
    def __init__(self, N, I0, beta, gamma, dias):
        self.N = N
        self.I0 = I0
        self.S0 = N - I0
        self.R0 = 0
        self.beta = beta
        self.gamma = gamma
        self.dias = dias

    def resolver(self):
        def ecuaciones(y, t, beta, gamma):
            S, I, R = y
            dSdt = -beta * S * I / self.N
            dIdt = beta * S * I / self.N - gamma * I
            dRdt = gamma * I
            return dSdt, dIdt, dRdt

        y0 = self.S0, self.I0, self.R0
        t = np.linspace(0, self.dias, self.dias + 1)
        resultado = odeint(ecuaciones, y0, t, args=(self.beta, self.gamma))
        S, I, R = resultado.T
        return t, S, I, R
