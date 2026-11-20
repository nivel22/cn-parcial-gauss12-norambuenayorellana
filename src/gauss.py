
import numpy as np
from conteo import Contador


def eliminacion_gaussiana(matriz, vector, pivoteo=False, guardar_factores=False):
    n = len(vector)
    a = matriz.copy()
    b = vector.copy()

    contador = Contador()
    contador.divisiones_pivoteo = 0

    traza = []
    max_multiplicador = 0

    l = np.eye(n)
    permutacion = list(range(n))

    max_inicial = 0

    for i in range(n):
        for j in range(n):
            if abs(a[i][j]) > max_inicial:
                max_inicial = abs(a[i][j])

    max_durante = max_inicial

    escalas = []

    if pivoteo:
        for i in range(n):
            mayor = 0

            for j in range(n):
                contador.comparaciones_escalas += 1

                if abs(a[i][j]) > mayor:
                    mayor = abs(a[i][j])

            escalas.append(mayor)

    # Eliminacion gaussiana
    for k in range(n - 1):
        contador.nuevo_paso()

        if pivoteo:
            fila_pivote = k
            mayor = abs(a[k][k]) / escalas[k]
            contador.divisiones_pivoteo += 1

            for i in range(k + 1, n):
                valor = abs(a[i][k]) / escalas[i]
                contador.divisiones_pivoteo += 1
                contador.contar_comparacion()

                if valor > mayor:
                    mayor = valor
                    fila_pivote = i

            if fila_pivote != k:
                a[[k, fila_pivote]] = a[[fila_pivote, k]]
                b[k], b[fila_pivote] = b[fila_pivote], b[k]

                escalas[k], escalas[fila_pivote] = (
                    escalas[fila_pivote], escalas[k]
                )

                permutacion[k], permutacion[fila_pivote] = (
                    permutacion[fila_pivote], permutacion[k]
                )

                for j in range(k):
                    l[k][j], l[fila_pivote][j] = (
                        l[fila_pivote][j], l[k][j]
                    )

                contador.contar_intercambio()

        if a[k][k] == 0:
            raise ValueError("Pivote igual a cero")

        for i in range(k + 1, n):
            factor = a[i][k] / a[k][k]
            contador.registrar("division")

            l[i][k] = factor

            if abs(factor) > max_multiplicador:
                max_multiplicador = abs(factor)

            for j in range(k + 1, n):
                producto = factor * a[k][j]
                a[i][j] = a[i][j] - producto

                contador.registrar("multiplicacion")
                contador.registrar("resta")

                if abs(a[i][j]) > max_durante:
                    max_durante = abs(a[i][j])

            producto = factor * b[k]
            b[i] = b[i] - producto

            contador.registrar("multiplicacion")
            contador.registrar("resta")

            a[i][k] = 0.0

        traza.append(a.copy())

    # Sustitucion regresiva
    contador.nuevo_paso()
    solucion = [0.0] * n

    for i in range(n - 1, -1, -1):
        suma = 0.0

        for j in range(i + 1, n):
            producto = a[i][j] * solucion[j]
            suma = suma + producto

            contador.registrar("multiplicacion")
            contador.registrar("suma")

        solucion[i] = (b[i] - suma) / a[i][i]

        contador.registrar("resta")
        contador.registrar("division")

    crecimiento = max_durante / max_inicial

    resultado = (
        solucion, contador, traza,
        max_multiplicador, crecimiento
    )

    if guardar_factores:
        return resultado + (l, a, permutacion)

    return resultado
