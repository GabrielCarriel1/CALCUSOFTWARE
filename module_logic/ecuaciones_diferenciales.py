import sympy as sp
from sympy import Function, Eq, Derivative, dsolve, classify_ode, checkodesol
from typing import Dict, Any, Optional, List, Union
import re
import numpy as np
class EcuacionesDiferenciales:
    def __init__(self) -> None:
        self.x: sp.Symbol = sp.Symbol('x')
        self.y: sp.Function = Function('y')(self.x)
        self.dy: sp.Expr = Derivative(self.y, self.x)
        self.d2y: sp.Expr = Derivative(self.y, self.x, 2)

    def clasificar_edo(self, ecuacion: Eq) -> Dict[str, Any]:
        tipos = classify_ode(ecuacion, self.y)
        orden = self._determinar_orden(ecuacion)
        return {
            "tipos": tipos,
            "orden": orden,
            "lineal": any(t.startswith('1st_linear') or 'linear' in t for t in tipos),
            "separable": 'separable' in tipos,
            "exacta": '1st_exact' in tipos,
            "homogenea": any('homogeneous' in t for t in tipos),
            "coef_constantes": any('constant_coeff' in t for t in tipos),
            "bernoulli": 'Bernoulli' in tipos,
            "riccati": any('Riccati' in t for t in tipos),
            "resoluble_analitica": bool(tipos)
        }

    def formatear_solucion(self, solucion: Union[sp.Eq, sp.Expr]) -> Dict[str, str]:
        sol_expr = solucion.rhs if isinstance(solucion, sp.Eq) else solucion
        latex_sol = sp.latex(sol_expr).replace('C1', 'C_1').replace('C2', 'C_2')
        unicode_sol = str(sol_expr).replace('exp', 'e^').replace('C1', 'C₁').replace('**', '^')
        return {
            "latex": f"y(x) = {latex_sol}",
            "unicode": f"y(x) = {unicode_sol}",
            "original": str(solucion)
        }

    def _determinar_orden(self, ecuacion: Eq) -> int:
        eq_str = str(ecuacion)
        for i in range(1, 11):
            if f"Derivative(y(x), x, {i})" in eq_str or f"diff(y(x), x, {i})" in eq_str:
                return i
        return 1

    def procesar_entrada(self, entrada_str: str) -> Eq:
        entrada_str = normalizar_entrada_usuario(entrada_str)
        entrada = re.sub(r"y('+)", lambda m: f"Derivative(y(x), x, {len(m.group(1))})", entrada_str)
        entrada = re.sub(r'\by\b(?!\()', 'y(x)', entrada)
        partes = entrada.split('=')
        if len(partes) != 2:
            raise ValueError("La ecuación debe incluir un signo '='")
        contexto = {
            'x': self.x, 'y': sp.Function('y'),
            'Derivative': Derivative, 'sin': sp.sin, 'cos': sp.cos,
            'exp': sp.exp, 'log': sp.log, 'sqrt': sp.sqrt,
            'pi': sp.pi, 'E': sp.E
        }
        lhs = sp.sympify(partes[0].strip(), locals=contexto)
        rhs = sp.sympify(partes[1].strip(), locals=contexto)
        return sp.Eq(lhs, rhs)

    def resolver_analitica(self, ecuacion_str: str, condiciones_iniciales: Optional[List[float]] = None) -> Dict[str, Any]:
        try:
            ecuacion = self.procesar_entrada(ecuacion_str)
            ecuacion = sp.simplify(ecuacion)
            ecuacion = ecuacion.xreplace({n: sp.Rational(n) for n in ecuacion.atoms(sp.Float)})
            clasif = self.clasificar_edo(ecuacion)

            if not clasif['resoluble_analitica']:
                return {
                    'exito': False,
                    'clasificacion': clasif,
                    'mensaje': 'No resoluble analíticamente',
                }

            if condiciones_iniciales:
                orden = clasif['orden']
                if len(condiciones_iniciales) < 2:
                    return {
                        'exito': False,
                        'clasificacion': clasif,
                        'mensaje': 'Condiciones iniciales insuficientes para el orden de la EDO.'
                    }

                x0 = condiciones_iniciales[0]
                ics = {Derivative(self.y, self.x, i).subs(self.x, x0): val for i, val in enumerate(condiciones_iniciales[1:])}
                solucion = dsolve(ecuacion, self.y, ics=ics)
            else:
                solucion = dsolve(ecuacion, self.y)

            verif, err = checkodesol(ecuacion, solucion)

            return {
                'exito': True,
                'solucion': solucion,
                'verificacion': verif,
                'error_verificacion': err,
                'clasificacion': clasif,
                'metodo': self._describir_metodo(clasif)
            }

        except Exception as e:
            return {
                'exito': False,
                'mensaje': 'Error al intentar resolver analíticamente.',
                'error': str(e)
            }

    def _describir_metodo(self, clasif: Dict[str, Any]) -> str:
        tipos = clasif.get('tipos', [])
        prioridad = [
            ('Bernoulli', 'Ecuación de Bernoulli'),
            ('Riccati', 'Ecuación de Riccati'),
            ('1st_exact', 'Ecuación exacta de primer orden'),
            ('separable', 'Separación de variables'),
            ('1st_linear', 'Ecuación lineal de primer orden'),
            ('nth_linear_constant_coeff_homogeneous', 'EDO lineal homogénea con coeficientes constantes'),
            ('nth_linear_constant_coeff_undetermined_coefficients', 'Coeficientes indeterminados'),
            ('nth_linear_constant_coeff_variation_of_parameters', 'Variación de parámetros'),
            ('homogeneous', 'Ecuación homogénea'),
        ]
        for clave, descripcion in prioridad:
            if any(clave in t for t in tipos):
                return descripcion
        return "Método general analítico"

    def metodo_heun(self, f_str, x0, y0, xf, n):
        import sympy as sp
        try:
            f_expr = sp.sympify(f_str)
            f = sp.lambdify(("x", "y"), f_expr, modules=["math", "sympy"])
            h = (xf - x0) / n

            xs, ys = [x0], [y0]
            for _ in range(n):
                xi, yi = xs[-1], ys[-1]
                y_pred = yi + h * f(xi, yi)
                xi1 = xi + h
                y_corr = yi + (h / 2) * (f(xi, yi) + f(xi1, y_pred))
                xs.append(xi1)
                ys.append(y_corr)

            return {
                "exito": True,
                "xs": xs,
                "ys": ys
            }
        except Exception as e:
            return {
                "exito": False,
                "mensaje": str(e)
            }


    def metodo_taylor_segundo_orden(self, f_str, df_str, x0, y0, xf, n):
        try:
            if n <= 0 or x0 == xf:
                return {"exito": False, "mensaje": "Parámetros inválidos: n debe ser > 0 y x₀ ≠ x final."}

            x, y = sp.symbols('x y')
            f_expr = sp.sympify(f_str)
            df_expr = sp.sympify(df_str)

            # Usar numpy para mayor compatibilidad y manejo de errores numéricos
            f = sp.lambdify((x, y), f_expr, modules=["numpy"])
            df = sp.lambdify((x, y), df_expr, modules=["numpy"])

            h = (xf - x0) / n
            xs = [x0]
            ys = [y0]

            for _ in range(n):
                xi, yi = xs[-1], ys[-1]
                try:
                    f_val = f(xi, yi)
                    df_val = df(xi, yi)
                    y_next = yi + h * f_val + (h ** 2 / 2) * df_val

                    if not np.isfinite(y_next):
                        return {"exito": False, "mensaje": f"Resultado inválido (NaN o inf) en x = {xi:.4f}"}

                    xs.append(xi + h)
                    ys.append(y_next)
                except Exception as e:
                    return {"exito": False, "mensaje": f"Error en paso con x = {xi:.4f}: {str(e)}"}

            return {"exito": True, "xs": xs, "ys": ys}

        except Exception as e:
            return {"exito": False, "mensaje": str(e)}

def normalizar_entrada_usuario(entrada: str) -> str:
    entrada = entrada.replace(" ", "")
    entrada = re.sub(r"(?<!\w)y''", "Derivative(y(x),x,2)", entrada)
    entrada = re.sub(r"(?<!\w)y'", "Derivative(y(x),x)", entrada)
    entrada = re.sub(r"d\^2y/dx\^2", "Derivative(y(x),x,2)", entrada)
    entrada = re.sub(r"dy/dx", "Derivative(y(x),x)", entrada)
    entrada = re.sub(r"d³y/dx³", "Derivative(y(x),x,3)", entrada)
    entrada = re.sub(r"d\^3y/dx\^3", "Derivative(y(x),x,3)", entrada)
    entrada = entrada.replace("sen", "sin").replace("tg", "tan").replace("ln", "log")
    entrada = re.sub(r"\by\b(?!\()", "y(x)", entrada)
    return entrada
