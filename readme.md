# Taller 3 - El pivote

Resolvemos un sistema de 12 ecuaciones con eliminación gaussiana, sin pivoteo y con pivoteo parcial escalado. Comparamos el costo y los resultados.

**1. Autores y asignatura:** Paloma Norambuena y Jeremy Orellana. Computación Numérica (INF-321), Universidad Católica del Maule, sección 2, 2026.

**2. Requisitos:** Python 3.10 o superior, NumPy 2.5.5 y mpmath 1.4.1. Instalar con `pip install -r requirements.txt`.

**3. Ejecución:** Desde la carpeta principal, ejecutar `python src/main.py`. El programa genera los cuatro archivos de `resultados/`.

**4. Estructura:** `datos/` (matriz y vector), `src/` (programa y comprobaciones), `resultados/` (solución, traza, conteo y residuo). En la raíz están `informe.md`, `readme.md`, `requirements.txt` y `.gitignore`.

**5. Resultados:** Solución con pivoteo parcial escalado, con diez dígitos significativos.

| Incógnita | Valor | Incógnita | Valor |
|---|---:|---|---:|
| x1 | 0.7384915627 | x7 | 1.473820592 |
| x2 | -1.205937417 | x8 | -0.03849271640 |
| x3 | 0.004387195200 | x9 | 0.9152648037 |
| x4 | -0.09172645380 | x10 | -2.607139485 |
| x5 | 2.846109372 | x11 | 0.05187362940 |
| x6 | -0.006281540899 | x12 | -1.084937163 |

**Costo:** 1366 flops principales; 1443 con divisiones de selección. **Residuo:** norma infinito inicial `6.09081267902e-10`; después del refinamiento `4.30068236118e-24`.

**6. Archivos generados:** `resultados/solucion.csv`, `resultados/traza_eliminacion.txt`, `resultados/conteo_flops.md` y `resultados/residuo.txt`.

**7. Informe:** Los cálculos y explicaciones están en [informe.md](informe.md).

**8. Uso académico:** Trabajo de Paloma Norambuena y Jeremy Orellana para Computación Numérica, UCM, 2026. Publicado con fines académicos.
