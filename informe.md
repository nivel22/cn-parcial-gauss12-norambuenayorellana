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

En este trabajo resolvemos un sistema de 12 ecuaciones con 12 incógnitas ($Ax=b$) usando eliminación gaussiana. La idea es hacer la menor cantidad posible de operaciones y obtener resultados precisos.

La matriz A es densa, con sus 144 elementos distintos de cero. Sus coeficientes presentan diferencias importantes de magnitud y el primer pivote es $a_{11}=1.3407\times10^{-8}$. Esto puede generar multiplicadores muy grandes y aumentar los errores de redondeo.

Además, la fila 7 presenta una casi dependencia lineal respecto de las filas 3 y 5, lo que contribuye al elevado condicionamiento del sistema.

Comparamos el método sin pivoteo con el pivoteo parcial escalado para ver cuánto cuesta cada uno y qué tan precisos son los resultados.

Guardamos los 144 valores de A y los 12 de b completos, sin cortar cifras, en la carpeta `datos/`.

## 3. Estrategia de eliminación

Se implementaron dos ejecuciones del mismo algoritmo: una sin pivoteo y otra con pivoteo parcial escalado.

En cada paso k se calcula el multiplicador:

$$
m_{ik}=\frac{a_{ik}}{a_{kk}}
$$

Posteriormente se actualizan los elementos mediante:

$$
a_{ij}=a_{ij}-m_{ik}a_{kj}
$$

Calculamos cada multiplicador una sola vez por fila y lo usamos para actualizar la matriz y el vector b.

Para ahorrar operaciones, no volvemos a calcular los valores que ya quedaron en cero.

En el pivoteo parcial escalado se calcula primero la escala de cada fila:

$$
s_i=\max_j |a_{ij}|
$$

La fila pivote se selecciona considerando el mayor cociente $|a_{ik}|/s_i$. Así podemos comparar mejor las filas, aunque tengan valores de tamaños muy distintos.

Se realizaron 11 pasos de eliminación, anulando los 66 elementos bajo la diagonal principal. Finalmente, se utilizó sustitución regresiva para obtener las incógnitas.

También se almacenaron las matrices L y U, junto con las permutaciones, para reutilizarlas durante el refinamiento iterativo sin efectuar otra factorización.

## 4. Conteo de operaciones

Se implementó un contador que registra multiplicaciones, divisiones, sumas y restas. La convención utilizada es una flop por cada operación aritmética elemental.

El conteo obtenido para los 11 pasos de eliminación y la sustitución regresiva fue:

| Paso | Mult. | Div. | Sumas | Restas | Total |
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

El costo principal fue de **1366 flops** para ambas estrategias.

El pivoteo parcial escalado agregó 77 divisiones para seleccionar los pivotes, 66 comparaciones entre candidatos, 144 comparaciones para calcular las escalas y 8 intercambios de filas.

Al sumar las divisiones de selección, el total aritmético parcial fue de 1443 flops. Las comparaciones e intercambios se informaron por separado y no se contabilizaron como flops aritméticas.

La referencia del enunciado es aproximadamente 1486 flops. La diferencia respecto de las 1443 contabilizadas es cercana al 2,9 %, dentro del margen permitido del 10 %.

El conteo de 1443 no incluye los cálculos auxiliares de diagnóstico ni el costo adicional del refinamiento, que se efectuó con precisión extendida.

Ahorramos operaciones porque reutilizamos los multiplicadores, evitamos cálculos repetidos y no usamos la matriz inversa.

## 5. Análisis de mantisa y pivoteo

Se utilizó aritmética IEEE 754 de doble precisión, cuya precisión significativa es de 53 bits.

El primer pivote, $1.3407\times10^{-8}$, es muy pequeño frente a otros elementos de su columna. Utilizarlo directamente genera multiplicadores elevados, capaces de amplificar los errores de redondeo.

Los resultados de ambas ejecuciones fueron:

| Indicador | Sin pivoteo | Pivoteo escalado |
|---|---:|---:|
| Multiplicador máximo | $2.7526\times10^{13}$ | $2.4656\times10^{9}$ |
| Factor de crecimiento | 2641,22 | 1,7832 |
| Error relativo | $2.0802\times10^{-10}$ | $2.3566\times10^{-13}$ |

Para expresar la magnitud de los multiplicadores en términos de bits equivalentes de amplificación potencial, se calculó:

$$
\log_2(2.7526\times10^{13})\approx44.65
$$

$$
\log_2(2.4656\times10^{9})\approx31.20
$$

La diferencia fue aproximadamente 13,45 bits equivalentes.

Estas cantidades no representan una medición directa de bits efectivamente perdidos por cancelación. Indican la diferencia de magnitud entre los multiplicadores y su posible efecto sobre la propagación de errores.

En operaciones de resta entre valores cercanos puede producirse cancelación, disminuyendo la cantidad de cifras significativas confiables. Los multiplicadores grandes aumentan el riesgo de amplificar errores previos.

El factor de crecimiento disminuyó de 2641,22 a 1,7832 con pivoteo escalado, mientras que el error relativo se redujo aproximadamente tres órdenes de magnitud.

Por eso no conviene usar el primer pivote sin cambiar las filas, aunque su valor no sea cero.

## 6. Condicionamiento

Se calculó el número de condición de la matriz en norma 2 mediante NumPy:

$$
\kappa_2(A)\approx3.0847\times10^{13}
$$

Para aritmética de doble precisión, el épsilon de máquina es:

$$
\varepsilon\approx2.2204\times10^{-16}
$$

El producto obtenido fue:

$$
\kappa_2(A)\varepsilon\approx0.0068495
$$

Este valor indica una sensibilidad elevada frente a perturbaciones. Una estimación de error de ese orden no permitiría garantizar dos dígitos significativos correctos en el peor caso.

Sin embargo, los errores observados en las ejecuciones fueron considerablemente menores.

Esto pasa porque el número de condición muestra lo que podría ocurrir en un caso muy desfavorable, pero el error real depende de lo que sucede en cada cálculo.

Por este motivo, el condicionamiento se complementó con el residuo calculado en precisión extendida, una solución de referencia de alta precisión y un refinamiento iterativo.

## 7. Resultados

La eliminación con pivoteo parcial escalado produjo las siguientes soluciones en doble precisión.

Se presentan los valores calculados y la cantidad conservadora de dígitos significativos correctos estimada respecto de una referencia de 60 dígitos obtenida con `mpmath`.

| Incógnita | Solución calculada | Dígitos correctos |
|---|---:|---:|
| x1 | 0.7384915626999453 | 13 |
| x2 | -1.2059374167993293 | 12 |
| x3 | 0.00438719520036459 | 10 |
| x4 | -0.09172645380023377 | 11 |
| x5 | 2.846109372499657 | 12 |
| x6 | -0.006281540899463979 | 10 |
| x7 | 1.4738205916004574 | 12 |
| x8 | -0.038492716399937434 | 11 |
| x9 | 0.9152648036998292 | 12 |
| x10 | -2.607139485200364 | 12 |
| x11 | 0.05187362939993543 | 11 |
| x12 | -1.0849371625003397 | 12 |

Los valores mostrados corresponden a las soluciones calculadas, no a una afirmación de que todas sus cifras sean correctas. La tercera columna indica cuántos dígitos significativos se consideran defendibles según la comparación individual.

Las 12 incógnitas alcanzaron al menos 10 dígitos correctos, superando el mínimo de 8 exigido por la rúbrica.

El archivo `resultados/solucion.csv` también contiene los valores refinados. Estos se presentan por separado porque se obtuvieron utilizando precisión extendida.

## 8. Verificación

Se calculó el residuo del sistema mediante:

$$
r=b-Ax
$$

Para evitar que el propio cálculo del residuo introdujera errores importantes, se utilizó `mpmath` con 60 dígitos de precisión, considerando los datos decimales originales.

La norma infinito inicial fue:

$$
\|r\|_\infty\approx6.09081267902\times10^{-10}
$$

Posteriormente se realizó una pasada de refinamiento iterativo reutilizando los factores L y U obtenidos durante la eliminación.

Se resolvió el sistema de corrección:

$$
LU\delta x=Pr
$$

Y se actualizó la solución mediante:

$$
x_{\text{nuevo}}=x+\delta x
$$

Los resultados fueron:

| Indicador | Antes | Después |
|---|---:|---:|
| Norma infinito del residuo | $6.0908\times10^{-10}$ | $4.3007\times10^{-24}$ |
| Error relativo | $2.3566\times10^{-13}$ | $6.1840\times10^{-26}$ |

El refinamiento mejoró tanto el residuo como el error relativo.

La mejora se obtuvo calculando el residuo y la corrección mediante precisión extendida. Por lo tanto, no corresponde atribuir estos niveles de precisión exclusivamente a la eliminación original en doble precisión.

Además, se contrastó la solución con `numpy.linalg.solve`, obteniéndose una diferencia absoluta máxima aproximada de:

$$
5.44\times10^{-14}
$$

Usamos esta biblioteca solo para comparar resultados, no para reemplazar el método de eliminación gaussiana del programa.

## 9. Conclusiones

Se consiguió triangularizar la matriz de 12 por 12 mediante 11 pasos, anulando los 66 elementos bajo la diagonal principal y reutilizando los multiplicadores para evitar cálculos redundantes.

La eliminación sin pivoteo y con pivoteo escalado presentaron el mismo costo aritmético principal de 1366 flops. Sin embargo, el pivoteo escalado agregó operaciones de selección e intercambios de filas que mejoraron considerablemente la estabilidad numérica.

El error relativo se redujo desde aproximadamente $2.08\times10^{-10}$ hasta $2.36\times10^{-13}$, mientras que el factor de crecimiento disminuyó de 2641,22 a 1,7832.

La ejecución de una pasada de refinamiento iterativo permitió mejorar aún más la solución, reutilizando la factorización original.

Para un sistema de tamaño $n=1000$, sería recomendable utilizar operaciones matriciales optimizadas y bibliotecas numéricas eficientes, manteniendo un análisis del costo, la memoria y la estabilidad. La eliminación gaussiana presenta un costo de orden cúbico respecto del tamaño del sistema.

En conclusión, el pivoteo parcial escalado resultó una estrategia adecuada para este caso porque permitió mejorar la exactitud a cambio de un sobrecosto limitado de selección.

## 10. Reproducibilidad

El proyecto fue desarrollado y comprobado con:

- Python 3.14.0.
- NumPy 2.5.5.
- mpmath 1.4.1.
- Visual Studio Code.

Las dependencias están especificadas en `requirements.txt`.

Para instalarlas desde la raíz del repositorio:

```bash
pip install -r requirements.txt
```

Para ejecutar el programa:

```bash
python src/main.py
```

La ejecución genera automáticamente los siguientes archivos:

- `resultados/solucion.csv`
- `resultados/traza_eliminacion.txt`
- `resultados/conteo_flops.md`
- `resultados/residuo.txt`

También probamos el programa desde una copia nueva del repositorio. Instalamos las dependencias y lo ejecutamos sin cambiar el código.

**Fuentes consultadas:** Enunciado oficial de la Prueba Parcial 3 de Computación Numérica (INF-321), Universidad Católica del Maule; documentación de Python, NumPy y mpmath.

**Declaración de uso de inteligencia artificial:** Se utilizó ChatGPT como herramienta de apoyo para resolver dudas puntuales, revisar aspectos de redacción y documentación, y consultar posibles soluciones a dificultades técnicas durante el desarrollo.
