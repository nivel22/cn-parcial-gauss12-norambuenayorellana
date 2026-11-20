
import csv
import os
import numpy as np
import mpmath as mp

from gauss import eliminacion_gaussiana
from verificacion import (
    leer_datos,
    calcular_residuo,
    solucion_referencia,
    error_relativo,
    refinamiento_iterativo
)


def contar_digitos(valor, referencia):
    if referencia == 0:
        return 0

    error = abs((mp.mpf(str(valor)) - referencia) / referencia)

    if error == 0:
        return 60

    return max(0, int(mp.floor(-mp.log10(error))))


def guardar_solucion(solucion, refinada, referencia):
    with open("resultados/solucion.csv", "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)

        escritor.writerow([
            "Incognita",
            "Solucion_pivoteo",
            "Digitos_correctos",
            "Solucion_refinada",
            "Digitos_refinados"
        ])

        for i in range(12):
            digitos = contar_digitos(solucion[i], referencia[i])
            digitos_ref = contar_digitos(refinada[i], referencia[i])

            escritor.writerow([
                f"x{i + 1}",
                mp.nstr(mp.mpf(str(solucion[i])), 17),
                digitos,
                mp.nstr(refinada[i], 35),
                digitos_ref
            ])


def guardar_traza(sin_pivoteo, con_pivoteo):
    with open("resultados/traza_eliminacion.txt", "w", encoding="utf-8") as archivo:
        for nombre, resultado in [
            ("SIN PIVOTEO", sin_pivoteo),
            ("PIVOTEO ESCALADO", con_pivoteo)
        ]:
            archivo.write(nombre + "\n\n")

            traza = resultado[2]

            for k in range(len(traza)):
                archivo.write(f"PASO {k + 1}\n")

                matriz = traza[k]

                for fila in matriz:
                    valores = []

                    for numero in fila:
                        valores.append(f"{numero:.17e}")

                    archivo.write("  ".join(valores) + "\n")

                archivo.write("\n")


def guardar_conteo(sin_pivoteo, con_pivoteo):
    with open("resultados/conteo_flops.md", "w", encoding="utf-8") as archivo:
        archivo.write("# Conteo de operaciones\n\n")
        archivo.write("Convencion: una operacion aritmetica elemental equivale a una flop.\n\n")

        for nombre, resultado in [
            ("Sin pivoteo", sin_pivoteo),
            ("Pivoteo escalado", con_pivoteo)
        ]:
            contador = resultado[1]

            archivo.write(f"## {nombre}\n\n")
            archivo.write("| Paso | Mult. | Div. | Sumas | Restas | Total |\n")
            archivo.write("|---|---:|---:|---:|---:|---:|\n")

            for i in range(len(contador.pasos)):
                paso = contador.pasos[i]

                mult = paso["multiplicaciones"]
                div = paso["divisiones"]
                sumas = paso["sumas"]
                restas = paso["restas"]

                total = mult + div + sumas + restas

                if i < 11:
                    nombre_paso = str(i + 1)
                else:
                    nombre_paso = "Sustitucion"

                archivo.write(
                    f"| {nombre_paso} | {mult} | {div} | "
                    f"{sumas} | {restas} | {total} |\n"
                )

            archivo.write("\n")
            archivo.write(f"Multiplicaciones: {contador.multiplicaciones}\n\n")
            archivo.write(f"Divisiones: {contador.divisiones}\n\n")
            archivo.write(f"Sumas: {contador.sumas}\n\n")
            archivo.write(f"Restas: {contador.restas}\n\n")
            archivo.write(f"Flops principales: {contador.total_flops()}\n\n")
            archivo.write(f"Comparaciones de pivoteo: {contador.comparaciones}\n\n")
            archivo.write(f"Intercambios de filas: {contador.intercambios}\n\n")
            archivo.write(f"Comparaciones para escalas: {contador.comparaciones_escalas}\n\n")

            if nombre == "Pivoteo escalado":
                divisiones = contador.divisiones_pivoteo
                total = contador.total_flops() + divisiones

                archivo.write(f"Divisiones de seleccion: {divisiones}\n\n")
                archivo.write(f"Total aritmetico parcial: {total}\n\n")

        archivo.write("Referencia del enunciado: aproximadamente 1486 flops.\n\n")
        archivo.write(
            "Las comparaciones y los intercambios no se consideran flops. "
            "La medicion de crecimiento y el refinamiento se informan por separado.\n"
        )


def guardar_residuo(matriz, vector, solucion, refinada, referencia):
    residuo_antes, norma_antes = calcular_residuo(
        matriz, vector, solucion
    )

    residuo_despues, norma_despues = calcular_residuo(
        matriz, vector, refinada
    )

    error_antes = error_relativo(solucion, referencia)
    error_despues = error_relativo(refinada, referencia)

    with open("resultados/residuo.txt", "w", encoding="utf-8") as archivo:
        archivo.write("RESIDUO ANTES DEL REFINAMIENTO\n\n")

        for i in range(12):
            archivo.write(f"r{i + 1} = {mp.nstr(residuo_antes[i], 20)}\n")

        archivo.write(f"\nNorma infinito: {mp.nstr(norma_antes, 20)}\n")
        archivo.write(f"Error relativo: {mp.nstr(error_antes, 20)}\n\n")

        archivo.write("RESIDUO DESPUES DEL REFINAMIENTO\n\n")

        for i in range(12):
            archivo.write(f"r{i + 1} = {mp.nstr(residuo_despues[i], 20)}\n")

        archivo.write(f"\nNorma infinito: {mp.nstr(norma_despues, 20)}\n")
        archivo.write(f"Error relativo: {mp.nstr(error_despues, 20)}\n")


def main():
    os.makedirs("resultados", exist_ok=True)

    a = np.loadtxt("datos/matriz_a.csv", delimiter=",")
    b = np.loadtxt("datos/vector_b.csv", delimiter=",")

    matriz, vector = leer_datos()
    referencia = solucion_referencia(matriz, vector)

    sin_pivoteo = eliminacion_gaussiana(a, b, False)
    con_pivoteo = eliminacion_gaussiana(a, b, True, True)

    solucion, contador, traza, multiplicador, crecimiento, l, u, p = con_pivoteo

    refinada, norma_antes, norma_despues = refinamiento_iterativo(
        matriz, vector, solucion, l, u, p
    )

    condicion = np.linalg.cond(a)
    epsilon = np.finfo(float).eps

    guardar_solucion(solucion, refinada, referencia)
    guardar_traza(sin_pivoteo, con_pivoteo)
    guardar_conteo(sin_pivoteo, con_pivoteo)
    guardar_residuo(matriz, vector, solucion, refinada, referencia)

    print("COMPARACION DE METODOS")

    for nombre, resultado in [
        ("Sin pivoteo", sin_pivoteo),
        ("Pivoteo escalado", con_pivoteo)
    ]:
        x, c, t, m, g = resultado[:5]

        print()
        print(nombre)
        print("Flops principales:", c.total_flops())
        print("Multiplicador maximo:", m)
        print("Factor de crecimiento:", g)
        print("Error relativo:", mp.nstr(error_relativo(x, referencia), 12))

    print()
    print("CONDICIONAMIENTO")
    print("Numero de condicion:", condicion)
    print("Cota de error:", condicion * epsilon)

    x_numpy = np.linalg.solve(a, b)
    diferencia = np.max(np.abs(np.array(solucion) - x_numpy))
    print("Error maximo frente a NumPy:", diferencia)

    print()
    print("BITS EQUIVALENTES DEL MULTIPLICADOR")
    print("Sin pivoteo:", np.log2(sin_pivoteo[3]))
    print("Pivoteo escalado:", np.log2(con_pivoteo[3]))
    print("Estas cifras no miden bits realmente perdidos.")

    print()
    print("REFINAMIENTO ITERATIVO")
    print("Residuo antes:", mp.nstr(norma_antes, 12))
    print("Residuo despues:", mp.nstr(norma_despues, 12))
    print("Error antes:", mp.nstr(error_relativo(solucion, referencia), 12))
    print("Error despues:", mp.nstr(error_relativo(refinada, referencia), 12))

    print()
    print("DIGITOS CORRECTOS")
    print("Variable | Pivoteo | Refinamiento")

    for i in range(12):
        d1 = contar_digitos(solucion[i], referencia[i])
        d2 = contar_digitos(refinada[i], referencia[i])

        print(f"x{i + 1} | {d1} | {d2}")

    print()
    print("ARCHIVOS GENERADOS")
    print("resultados/solucion.csv")
    print("resultados/traza_eliminacion.txt")
    print("resultados/conteo_flops.md")
    print("resultados/residuo.txt")


if __name__ == "__main__":
    main()
