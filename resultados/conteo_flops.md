# Conteo de operaciones

Convencion: una operacion aritmetica elemental equivale a una flop.

## Sin pivoteo

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
| Sustitucion | 66 | 12 | 66 | 12 | 156 |

Multiplicaciones: 638

Divisiones: 78

Sumas: 66

Restas: 584

Flops principales: 1366

Comparaciones de pivoteo: 0

Intercambios de filas: 0

Comparaciones para escalas: 0

## Pivoteo escalado

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
| Sustitucion | 66 | 12 | 66 | 12 | 156 |

Multiplicaciones: 638

Divisiones: 78

Sumas: 66

Restas: 584

Flops principales: 1366

Comparaciones de pivoteo: 66

Intercambios de filas: 8

Comparaciones para escalas: 144

Divisiones de seleccion: 77

Total aritmetico parcial: 1443

Referencia del enunciado: aproximadamente 1486 flops.

Las comparaciones y los intercambios no se consideran flops. La medicion de crecimiento y el refinamiento se informan por separado.
