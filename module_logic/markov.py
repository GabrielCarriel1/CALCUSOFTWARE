import numpy as np

def calcular_estados_markov(matriz, vector_inicial, pasos):
    """
    Calcula la evolución de una cadena de Markov dado un vector inicial y una matriz de transición.
    :param matriz: Matriz de transición (n x n)
    :param vector_inicial: Vector de estado inicial (1 x n)
    :param pasos: Número de pasos a simular
    :return: Lista de vectores de estado en cada paso
    """
    historial = [vector_inicial]
    actual = vector_inicial

    for _ in range(pasos):
        siguiente = np.dot(actual, matriz)
        historial.append(siguiente)
        actual = siguiente

    return np.array(historial)

def calcular_estado_estable(matriz, tol=1e-6, max_iter=1000):
    """
    Calcula el estado estable de una matriz de transición de Markov (si existe).
    :param matriz: Matriz de transición (n x n)
    :param tol: Tolerancia para convergencia
    :param max_iter: Máximo de iteraciones
    :return: Vector de estado estable o None si no converge
    """
    n = matriz.shape[0]
    vector = np.ones(n) / n
    for _ in range(max_iter):
        nuevo_vector = np.dot(vector, matriz)
        if np.allclose(nuevo_vector, vector, atol=tol):
            return nuevo_vector
        vector = nuevo_vector
    return None
