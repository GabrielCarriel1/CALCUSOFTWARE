class ResultadosEDOManager:
    _resultados = []

    @classmethod
    def agregar(cls, resultado: dict):
        cls._resultados.append(resultado)

    @classmethod
    def obtener_todos(cls):
        return cls._resultados

    @classmethod
    def filtrar_por_metodo(cls, metodo):
        return [r for r in cls._resultados if r["metodo"] == metodo]
