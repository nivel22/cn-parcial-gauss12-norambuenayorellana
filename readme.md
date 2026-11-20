# Taller 3 - El pivote

Este proyecto resuelve 12 ecuaciones usando eliminación gaussiana. Comparamos el método sin pivoteo con el pivoteo parcial escalado. También contamos las operaciones y comprobamos los resultados.

## 1. Autores

- Paloma Norambuena
- Jeremy Orellana

**Asignatura:** Computación Numérica (INF-321)  
**Universidad:** Universidad Católica del Maule  
**Sección:** 2  
**Año:** 2026

## 2. Requisitos

- Python 3.14.0.
- NumPy 2.5.5.
- mpmath 1.4.1.

Instalar las dependencias desde la carpeta principal:

```bash
pip install -r requirements.txt
```

## 3. Ejecución

Ejecutar desde la raíz del repositorio:

```bash
python src/main.py
```

El programa resuelve el sistema y guarda cuatro archivos en la carpeta `resultados/`.

## 4. Estructura del proyecto

```text
datos/
  matriz_a.csv
  vector_b.csv
src/
  gauss.py
  conteo.py
  verificacion.py
  main.py
resultados/
  solucion.csv
  traza_eliminacion.txt
  conteo_flops.md
  residuo.txt
informe.md
readme.md
requirements.txt
.gitignore
```

## 5. Resultados

Estos son los resultados con pivoteo parcial escalado, escritos con diez dígitos significativos.

| Incógnita | Valor |
|---|---:|
| x1 | 0.7384915627 |
| x2 | -1.205937417 |
| x3 | 0.004387195200 |
| x4 | -0.09172645380 |
| x5 | 2.846109372 |
| x6 | -0.006281540899 |
| x7 | 1.473820592 |
| x8 | -0.03849271640 |
| x9 | 0.9152648037 |
| x10 | -2.607139485 |
| x11 | 0.05187362940 |
| x12 | -1.084937163 |

**Costo principal:** 1366 flops.

**Costo aritmético parcial con selección escalada:** 1443 flops.

**Norma infinito del residuo inicial:** 6.09081267902 × 10⁻¹⁰.

**Norma infinito después del refinamiento:** 4.30068236118 × 10⁻²⁴.

## 6. Archivos generados

- `solucion.csv`: incógnitas originales, refinadas y dígitos correctos estimados.
- `traza_eliminacion.txt`: once pasos de eliminación por cada estrategia.
- `conteo_flops.md`: desglose de operaciones aritméticas y costo del pivoteo.
- `residuo.txt`: residuos y errores antes y después del refinamiento.

## 7. Informe técnico

La explicación de los cálculos y las pruebas está en [informe.md](informe.md).

## 8. Uso académico

Proyecto desarrollado por Paloma Norambuena y Jeremy Orellana para la evaluación de Computación Numérica de la Universidad Católica del Maule, 2026. Su contenido se publica con fines académicos.