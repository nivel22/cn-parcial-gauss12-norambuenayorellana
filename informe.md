# El pivote: eliminación gaussiana con mínimo costo operacional y máxima exactitud de mantisa

## 1. Identificación

**Universidad:** Universidad Católica del Maule  
**Carrera:** Ingeniería Civil Informática  
**Asignatura:** Computación Numérica (INF-321)  
**Evaluación:** Taller 3 - Prueba Parcial  
**Integrantes:** Paloma Norambuena y Jeremy Orellana  
**Sección:** 2  
**Fecha:** Noviembre de 2026  
**Repositorio:** https://github.com/nivel22/cn-parcial-gauss12-norambuenayorellana

## 2. Planteamiento

El objetivo consiste en resolver un sistema lineal \(Ax=b\) de 12 ecuaciones y 12 incógnitas mediante eliminación gaussiana, minimizando las operaciones aritméticas y controlando los errores de redondeo.

La matriz A es densa, contiene 144 elementos distintos de cero y presenta diferencias importantes entre las magnitudes de sus filas. El pivote inicial es \(a_{11}=1.3407\times10^{-8}\), mientras que otros elementos de la primera columna son considerablemente mayores.

También existe una casi dependencia lineal de la fila 7 respecto de las filas 3 y 5, lo que contribuye al elevado condicionamiento del sistema.

Estas características hacen necesario comparar distintas estrategias de eliminación, porque un algoritmo puede resolver correctamente el sistema y, aun así, perder precisión numérica.

Los valores originales se conservaron completos en `datos/matriz_a.csv` y `datos/vector_b.csv`.

## 3. Estrategia de eliminación

Se implementaron dos versiones de eliminación gaussiana: sin pivoteo y con pivoteo parcial escalado.

En cada paso se calcula un multiplicador:

\[
m_{ik}=\frac{a_{ik}}{a_{kk}}
\]

Posteriormente, los elementos de cada fila se actualizan mediante:

\[
a_{ij}=a_{ij}-m_{ik}a_{kj}
\]

Cada multiplicador se calcula una sola vez por fila y se reutiliza tanto para actualizar la matriz como para modificar el vector b.

Las operaciones comienzan desde la columna siguiente al pivote, evitando volver a calcular elementos que ya fueron anulados.

En el pivoteo parcial escalado se calcula una escala por fila:

\[
s_i=\max_j |a_{ij}|
\]

Luego se selecciona la fila cuyo cociente \(|a_{ik}|/s_i\) sea mayor. Esto permite comparar candidatos considerando sus escalas originales.

La eliminación comprende 11 pasos y anula los 66 elementos bajo la diagonal principal. Finalmente, se utiliza sustitución regresiva.

También se conservan las matrices L y U para reutilizarlas durante el refinamiento iterativo, sin repetir la factorización.

## 4. Conteo de operaciones

El contador implementado registra las sumas, restas, multiplicaciones y divisiones realizadas. Se utiliza una flop por cada operación aritmética elemental.

| Paso | Multiplicaciones | Divisiones | Sumas | Restas | Total |
|---|---:|---:|---:|---:|---:|
| 1 | 132 | 11 | 0 | 132 | 275 |
| 2 | 110 | 10 | 0 | 110 | 230 |
| 3 | 90 | 9 | 0 | 90 | 189 |
| 4 | 72 | 8 | 0 | 72 | 152 |
| 5 | 56 | 7 | 0 | 56 | 119 |
| 6 | 42 | 6 | 0 | 42 | 90 |
| 7 | 30 | 5 | 0 | 30 | 65 |
| 8 | 20 | 4 | 0 | 20 | 44 |
| 9 | 12 | 3 | 0 | 12 | 27 |
| 10 | 6 | 2 | 0 | 6 | 14 |
| 11 | 2 | 1 | 0 | 2 | 5 |
| Sustitución | 66 | 12 | 66 | 12 | 156 |
| **Total** | **638** | **78** | **66** | **584** | **1366** |

El costo principal fue de 1366 flops para ambas estrategias.

El pivoteo escalado requirió adicionalmente 77 divisiones de selección, 66 comparaciones entre candidatos y 144 comparaciones para calcular las escalas. Se registraron también 8 intercambios de filas.

Al incorporar las 77 divisiones, el costo aritmético parcial alcanza 1443 flops.

La referencia del enunciado es aproximadamente 1486 flops. La diferencia es cercana al 2,9 %, dentro de la tolerancia del 10 %.

Las comparaciones e intercambios se contabilizan por separado y no se consideran flops aritméticas. El costo de las verificaciones y del refinamiento se distingue del costo principal de eliminación.

La reducción de trabajo proviene principalmente de reutilizar los multiplicadores y evitar actualizaciones redundantes. No se calcula la inversa de A.

## 5. Análisis de mantisa y pivoteo

Se trabajó con aritmética de doble precisión IEEE 754, que utiliza una precisión significativa de 53 bits.

El pivote inicial \(1.3407\times10^{-8}\) es muy pequeño respecto de otros elementos de su columna. Utilizarlo sin intercambiar filas genera multiplicadores grandes que pueden amplificar errores de redondeo.

Los resultados fueron:

| Indicador | Sin pivoteo | Pivoteo escalado |
|---|---:|---:|
| Multiplicador máximo | \(2.7526\times10^{13}\) | \(2.4656\times10^{10}\) |
| Factor de crecimiento | 2641,22 | 1,7832 |
| Error relativo | \(2.6802\times10^{-10}\) | \(2.3566\times10^{-13}\) |

Para analizar la amplificación potencial de errores, se calculó el logaritmo en base 2 de los multiplicadores máximos:

\[
\log_2(2.7526\times10^{13})\approx44.65
\]

\[
\log_2(2.4656\times10^{10})\approx31.20
\]

La diferencia es de aproximadamente 13,45 bits equivalentes.

Estas cantidades permiten comparar la magnitud potencial de la amplificación del error, pero no representan una medición directa de los bits perdidos por cancelación.

El factor de crecimiento y el error relativo observados muestran que el pivoteo escalado ofrece una solución considerablemente más estable.

Por este motivo, aunque el pivote inicial no sea exactamente cero, resulta numéricamente inadecuado mantenerlo como primera elección.

## 6. Condicionamiento

Se estimó el número de condición mediante NumPy:

\[
\kappa_2(A)\approx3.0847\times10^{13}
\]

En doble precisión se tiene:

\[
\varepsilon\approx2.2204\times10^{-16}
\]

Por lo tanto:

\[
\kappa_2(A)\varepsilon\approx0.0068495
\]

Este producto representa una advertencia sobre la sensibilidad del sistema ante perturbaciones de magnitud comparable al épsilon de máquina. Su orden de magnitud es cercano a \(10^{-2}\), por lo que la cota general no garantiza una precisión elevada.

Sin embargo, los resultados observados fueron considerablemente mejores.

Esto se explica porque el número de condición describe una sensibilidad de peor caso. El comportamiento real depende de las perturbaciones concretas, los datos y el procedimiento utilizado.

Por esta razón, se complementó el análisis de condicionamiento con un cálculo del residuo en precisión extendida y una comparación con una solución de referencia.

## 7. Resultados

La eliminación con pivoteo parcial escalado produjo las siguientes soluciones, acompañadas por una estimación conservadora de sus dígitos significativos correctos.

| Incógnita | Solución reportada | Dígitos correctos |
|---|---:|---:|
| x1 | 0.7384915626999 | 13 |
| x2 | -1.2059374168 | 12 |
| x3 | 0.0043871952 | 10 |
| x4 | -0.0917264538 | 11 |
| x5 | 2.8461093725 | 12 |
| x6 | -0.006281540899 | 10 |
| x7 | 1.4738205916 | 12 |
| x8 | -0.0384927164 | 11 |
| x9 | 0.9152648037 | 12 |
| x10 | -2.6071394852 | 12 |
| x11 | 0.0518736294 | 11 |
| x12