class MatrixError(Exception):
    """Excepción base para errores de matrices"""
    pass

class DimensionError(MatrixError):
    """Error cuando las dimensiones no son compatibles"""
    def __init__(self, operation, required=None, actual=None):
        message = f"No se puede realizar {operation}"
        if required and actual:
            message += f". Se requieren {required}, pero se tienen {actual}"
        super().__init__(message)

class SingularMatrixError(MatrixError):
    """Error cuando la matriz es singular"""
    def __init__(self):
        super().__init__("La matriz es singular y no tiene inversa")

class OperationNotPossibleError(MatrixError):
    """Error cuando una operación no es posible"""
    def __init__(self, operation, reason):
        super().__init__(f"No se puede {operation}: {reason}")

class DivisionByZeroMatrixError(MatrixError):
    """Error cuando se intenta dividir por una matriz singular"""
    def __init__(self):
        super().__init__("No se puede dividir: la matriz divisor es singular")

class InvalidExpressionError(MatrixError):
    """Error cuando una expresión matemática es inválida"""
    def __init__(self, expression, reason):
        super().__init__(f"Expresión inválida '{expression}': {reason}")