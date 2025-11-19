from exceptions import *
import time
import math
import re

class MatrixOperations:
    def __init__(self):
        self.console_messages = []
        self.steps = []
    
    def log(self, message, level="INFO"):
        """Agrega un mensaje a la consola integrada (para depuración)"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {level}: {message}"
        self.console_messages.append(formatted_message)
    
    def add_step(self, description, matrix=None, highlighted_cells=None, step_type="operation"):
        """
        Agrega un paso visual con soporte para resaltar celdas.
        """
        step = {
            "description": description,
            "matrix": [row[:] for row in matrix] if matrix else None,
            "highlighted_cells": highlighted_cells or [],
            "type": step_type,
            "timestamp": time.strftime("%H:%M:%S")
        }
        self.steps.append(step)
        self.log(description)
    
    def clear_log(self):
        """Limpia los mensajes de la consola"""
        self.console_messages = []
        self.steps = []
    
    def get_console_output(self):
        """Retorna todos los mensajes de consola para la interfaz"""
        return "\n".join(self.console_messages)
    
    def get_steps(self):
        """Retorna los pasos visuales"""
        return self.steps.copy()

    def evaluate_expression(self, expression):
        """Evalúa expresiones matemáticas con constantes y operaciones"""
        if not expression.strip():
            return 0.0
            
        expr = expression.lower()
        expr = expr.replace('pi', str(math.pi))
        expr = expr.replace('e', str(math.e))
        expr = expr.replace('^', '**')
        
        # Patrón más seguro para expresiones matemáticas
        safe_pattern = r'^[0-9+\-*/().\s]+$'
        if not re.match(safe_pattern, expr.replace('**', '')):
            raise InvalidExpressionError(expression, "caracteres no permitidos")
        
        try:
            result = eval(expr)
            return float(result)
        except Exception as e:
            raise InvalidExpressionError(expression, str(e))

    def validate_dimensions_for_addition(self, matrices):
        """Valida que todas las matrices tengan las mismas dimensiones para suma/resta"""
        if not matrices:
            raise OperationNotPossibleError("operar con matrices", "no hay matrices ingresadas")
        
        rows, cols = len(matrices[0]), len(matrices[0][0])
        for i, matrix in enumerate(matrices):
            if len(matrix) != rows or len(matrix[0]) != cols:
                raise DimensionError(
                    "operar con matrices", 
                    f"dimensiones {rows}x{cols}", 
                    f"dimensiones {len(matrix)}x{len(matrix[0])} en matriz {i+1}"
                )

    def validate_dimensions_for_multiplication(self, matrix1, matrix2):
        """Valida dimensiones para multiplicación"""
        if len(matrix1[0]) != len(matrix2):
            raise DimensionError(
                "multiplicar matrices",
                f"que las columnas de la primera ({len(matrix1[0])}) igualen las filas de la segunda ({len(matrix2)})"
            )

    def add_matrices(self, matrices):
        """Suma múltiples matrices"""
        self.clear_log()
        self.add_step("=== INICIANDO SUMA DE MATRICES ===")
        
        self.validate_dimensions_for_addition(matrices)
        self.add_step("✓ Validación de dimensiones exitosa")
        
        rows, cols = len(matrices[0]), len(matrices[0][0])
        result = [[0.0 for _ in range(cols)] for _ in range(rows)]
        
        for i in range(rows):
            for j in range(cols):
                total = 0.0
                for k, matrix in enumerate(matrices):
                    total += matrix[i][j]
                result[i][j] = total
        
        self.add_step("✓ Suma completada exitosamente", result, [], "result")
        return result

    def subtract_matrices(self, matrices):
        """Resta múltiples matrices"""
        self.clear_log()
        self.add_step("=== INICIANDO RESTA DE MATRICES ===")
        
        self.validate_dimensions_for_addition(matrices)
        self.add_step("✓ Validación de dimensiones exitosa")
        
        rows, cols = len(matrices[0]), len(matrices[0][0])
        result = [[0.0 for _ in range(cols)] for _ in range(rows)]
        
        for i in range(rows):
            for j in range(cols):
                total = matrices[0][i][j]
                for k in range(1, len(matrices)):
                    total -= matrices[k][i][j]
                result[i][j] = total
        
        self.add_step("✓ Resta completada exitosamente", result, [], "result")
        return result

    def multiply_matrices(self, matrix1, matrix2):
        """Multiplica dos matrices"""
        self.clear_log()
        self.add_step("=== INICIANDO MULTIPLICACIÓN DE MATRICES ===")
        
        self.validate_dimensions_for_multiplication(matrix1, matrix2)
        self.add_step("✓ Validación de dimensiones exitosa")
        
        rows1, cols1 = len(matrix1), len(matrix1[0])
        rows2, cols2 = len(matrix2), len(matrix2[0])
        result = [[0.0 for _ in range(cols2)] for _ in range(rows1)]
        
        for i in range(rows1):
            for j in range(cols2):
                subtotal = 0.0
                for k in range(cols1):
                    subtotal += matrix1[i][k] * matrix2[k][j]
                result[i][j] = subtotal
        
        self.add_step("✓ Multiplicación completada exitosamente", result, [], "result")
        return result

    def divide_matrices(self, matrix1, matrix2):
        """Divide matriz1 entre matriz2 (matriz1 × matriz2⁻¹)"""
        self.clear_log()
        self.add_step("=== INICIANDO DIVISIÓN DE MATRICES ===")
        
        if len(matrix2) != len(matrix2[0]):
            raise OperationNotPossibleError("dividir matrices", "la matriz divisor debe ser cuadrada")
        
        self.add_step("Paso 1: Calculando inversa de la matriz B")
        inverse_matrix2, _ = self.inverse(matrix2)
        self.add_step("✓ Inversa de B calculada", inverse_matrix2, [], "intermediate")
        
        self.add_step("Paso 2: Multiplicando A × B⁻¹")
        result = self.multiply_matrices(matrix1, inverse_matrix2)
        self.add_step("✓ División completada exitosamente", result, [], "result")
        return result

    def transpose(self, matrix):
        """Calcula la transpuesta de una matriz"""
        self.clear_log()
        self.add_step("=== INICIANDO CÁLCULO DE TRANSPUESTA ===")
        
        rows, cols = len(matrix), len(matrix[0])
        result = [[0.0 for _ in range(rows)] for _ in range(cols)]
        
        for i in range(rows):
            for j in range(cols):
                result[j][i] = matrix[i][j]
        
        self.add_step("✓ Transpuesta calculada exitosamente", result, [], "result")
        return result

    def determinant(self, matrix):
        """Calcula el determinante de una matriz cuadrada"""
        self.clear_log()
        self.add_step("=== INICIANDO CÁLCULO DE DETERMINANTE ===")
        
        n = len(matrix)
        if n == 0:
            raise MatrixError("Matriz vacía")
        if len(matrix[0]) != n:
            raise MatrixError("El determinante solo se puede calcular para matrices cuadradas")
        
        det = self._determinant_recursive(matrix)
        self.add_step(f"✓ Determinante calculado: {det:.6f}", None, [], "result")
        return det

    def _determinant_recursive(self, matrix):
        """Calcula el determinante recursivamente"""
        n = len(matrix)
        
        # Caso base: matriz 1x1
        if n == 1:
            return matrix[0][0]
        
        # Caso base: matriz 2x2
        if n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        
        det = 0.0
        for j in range(n):
            # Crear submatriz (menor)
            minor = []
            for i in range(1, n):
                row = []
                for k in range(n):
                    if k != j:
                        row.append(matrix[i][k])
                minor.append(row)
            
            # Calcular cofactor y sumar al determinante
            cofactor = ((-1) ** j) * matrix[0][j] * self._determinant_recursive(minor)
            det += cofactor
        
        return det

    def gaussian_elimination(self, matrix):
        """Aplica eliminación gaussiana a una matriz"""
        self.clear_log()
        self.add_step("=== INICIANDO ELIMINACIÓN GAUSSIANA ===")
        
        if not matrix or not matrix[0]:
            raise MatrixError("Matriz vacía")
        
        mat = [row[:] for row in matrix]
        rows, cols = len(mat), len(mat[0])
        
        pivot_row = 0
        for pivot_col in range(min(rows, cols)):
            # Encontrar pivote
            max_row = pivot_row
            for row in range(pivot_row + 1, rows):
                if abs(mat[row][pivot_col]) > abs(mat[max_row][pivot_col]):
                    max_row = row
            
            # Si encontramos un pivote no cero
            if abs(mat[max_row][pivot_col]) > 1e-10:
                # Intercambiar filas si es necesario
                if max_row != pivot_row:
                    mat[pivot_row], mat[max_row] = mat[max_row], mat[pivot_row]
                    self.add_step(f"Intercambiando fila {pivot_row + 1} con fila {max_row + 1}", 
                                [row[:] for row in mat], 
                                [{"row": pivot_row, "col": pivot_col, "role": "pivot"},
                                 {"row": max_row, "col": pivot_col, "role": "pivot"}], 
                                "step")
                
                # Normalizar fila pivote
                pivot_val = mat[pivot_row][pivot_col]
                if abs(pivot_val - 1.0) > 1e-10:
                    for j in range(pivot_col, cols):
                        mat[pivot_row][j] /= pivot_val
                    self.add_step(f"Normalizando fila {pivot_row + 1}", 
                                [row[:] for row in mat], 
                                [{"row": pivot_row, "col": j, "role": "write"} for j in range(pivot_col, cols)], 
                                "step")
                
                # Eliminar en otras filas
                for i in range(pivot_row + 1, rows):
                    factor = mat[i][pivot_col]
                    if abs(factor) > 1e-10:
                        for j in range(pivot_col, cols):
                            mat[i][j] -= factor * mat[pivot_row][j]
                        self.add_step(f"Eliminando en fila {i + 1} usando fila {pivot_row + 1}", 
                                    [row[:] for row in mat], 
                                    [{"row": i, "col": j, "role": "write"} for j in range(pivot_col, cols)], 
                                    "step")
                
                pivot_row += 1
        
        self.add_step("✓ Eliminación gaussiana completada", mat, [], "result")
        return mat

    def gauss_jordan(self, matrix):
        """Aplica eliminación de Gauss-Jordan a una matriz"""
        self.clear_log()
        self.add_step("=== INICIANDO ELIMINACIÓN GAUSS-JORDAN ===")
        
        if not matrix or not matrix[0]:
            raise MatrixError("Matriz vacía")
        
        mat = [row[:] for row in matrix]
        rows, cols = len(mat), len(mat[0])
        
        pivot_row = 0
        for pivot_col in range(min(rows, cols)):
            # Encontrar pivote
            max_row = pivot_row
            for row in range(pivot_row + 1, rows):
                if abs(mat[row][pivot_col]) > abs(mat[max_row][pivot_col]):
                    max_row = row
            
            if abs(mat[max_row][pivot_col]) > 1e-10:
                # Intercambiar filas
                if max_row != pivot_row:
                    mat[pivot_row], mat[max_row] = mat[max_row], mat[pivot_row]
                
                # Normalizar fila pivote
                pivot_val = mat[pivot_row][pivot_col]
                for j in range(pivot_col, cols):
                    mat[pivot_row][j] /= pivot_val
                
                # Eliminar en otras filas
                for i in range(rows):
                    if i != pivot_row and abs(mat[i][pivot_col]) > 1e-10:
                        factor = mat[i][pivot_col]
                        for j in range(pivot_col, cols):
                            mat[i][j] -= factor * mat[pivot_row][j]
                
                pivot_row += 1
        
        self.add_step("✓ Eliminación Gauss-Jordan completada", mat, [], "result")
        return mat

    def inverse(self, matrix):
        """Calcula la inversa de una matriz cuadrada"""
        self.clear_log()
        self.add_step("=== INICIANDO CÁLCULO DE MATRIZ INVERSA ===")
        
        n = len(matrix)
        if n == 0 or len(matrix[0]) != n:
            raise OperationNotPossibleError("calcular la inversa", "la matriz debe ser cuadrada")
        
        # Calcular determinante para verificar si es singular
        det = self.determinant(matrix)
        if abs(det) < 1e-10:
            raise SingularMatrixError()
        
        self.add_step(f"Determinante: {det:.6f} (matriz no singular)")
        
        # Crear matriz aumentada [A|I]
        augmented = []
        for i in range(n):
            row = matrix[i][:] + [1.0 if j == i else 0.0 for j in range(n)]
            augmented.append(row)
        
        self.add_step("Matriz aumentada [A|I] creada", augmented, [], "intermediate")
        
        # Aplicar Gauss-Jordan a la matriz aumentada
        result = self.gauss_jordan(augmented)
        
        # Extraer la inversa (últimas n columnas)
        inverse_mat = []
        for i in range(n):
            inverse_mat.append(result[i][n:])
        
        self.add_step("✓ Matriz inversa calculada", inverse_mat, [], "result")
        return inverse_mat, det
