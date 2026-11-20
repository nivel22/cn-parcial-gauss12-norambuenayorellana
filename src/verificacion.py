
import csv
import mpmath as mp


def leer_datos():
    mp.mp.dps = 60

    matriz = []
    vector = []

    with open("datos/matriz_a.csv", "r") as archivo:
        lector = csv.reader(archivo)

        for fila in lector:
            valores = []
            for numero in fila:
                valores.append(mp.mpf(numero))
            matriz.append(valores)

    with open("datos/vector_b.csv", "r") as archivo:
        lector = csv.reader(archivo)

        for fila in lector:
            vector.append(mp.mpf(fila[0]))

    return mp.matrix(matriz), mp.matrix(vector)


def calcular_residuo(matriz, vector, solucion):
    n = len(solucion)
    residuo = []

    for i in range(n):
        suma = mp.mpf("0")

        for j in range(n):
            suma += matriz[i, j] * mp.mpf(str(solucion[j]))

        residuo.append(vector[i] - suma)

    norma = max(abs(valor) for valor in residuo)

    return residuo, norma


def solucion_referencia(matriz, vector):
    return mp.lu_solve(matriz, vector)


def error_relativo(solucion, referencia):
    error_maximo = mp.mpf("0")
    valor_maximo = mp.mpf("0")

    for i in range(len(solucion)):
        valor = mp.mpf(str(solucion[i]))
        error = abs(valor - referencia[i])

        if error > error_maximo:
            error_maximo = error

        if abs(referencia[i]) > valor_maximo:
            valor_maximo = abs(referencia[i])

    return error_maximo / valor_maximo


def refinamiento_iterativo(matriz, vector, solucion, l, u, permutacion):
    n = len(solucion)

    residuo, norma_antes = calcular_residuo(
        matriz, vector, solucion
    )

    # Aplicar permutacion
    r = []

    for i in range(n):
        r.append(residuo[permutacion[i]])

    # Sustitucion hacia adelante
    y = [mp.mpf("0")] * n

    for i in range(n):
        suma = mp.mpf("0")

        for j in range(i):
            suma += mp.mpf(str(l[i][j])) * y[j]

        y[i] = r[i] - suma

    # Sustitucion regresiva
    correccion = [mp.mpf("0")] * n

    for i in range(n - 1, -1, -1):
        suma = mp.mpf("0")

        for j in range(i + 1, n):
            suma += mp.mpf(str(u[i][j])) * correccion[j]

        correccion[i] = (
            y[i] - suma
        ) / mp.mpf(str(u[i][i]))

    # Actualizar solucion
    solucion_nueva = []

    for i in range(n):
        valor = mp.mpf(str(solucion[i]))
        solucion_nueva.append(valor + correccion[i])

    residuo_nuevo, norma_despues = calcular_residuo(
        matriz, vector, solucion_nueva
    )

    return solucion_nueva, norma_antes, norma_despues
