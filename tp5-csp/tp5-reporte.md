# TP5 - Constraint Satisfaction Problems (CSP) para N-Reinas

## Implementación de Algoritmos

### 1. Backtracking con Least Constraining Value (LCV)
- **Descripción**: Implementación básica de backtracking que asigna reinas columna por columna. Usa LCV para ordenar las filas posibles por el menor impacto potencial en futuras columnas (contando conflictos estimados con dominios estáticos).
- **Código**: `backtracking.py`
- **Características**:
  - Asignación secuencial de columnas.
  - Verificación de consistencia con `is_safe` (restricciones de fila y diagonal).
  - LCV: Ordena filas por `count_conflicts(row)`, que estima restricciones futuras.
  - Sin propagación de restricciones ni MRV.

### 2. CSP con Forward Checking, MRV y LCV
- **Descripción**: Modelo CSP completo con variables (columnas), dominios (filas posibles) y restricciones (no ataque). Incluye forward checking para actualizar dominios, MRV para seleccionar variables y LCV para ordenar valores.
- **Código**: `csp_nqueens.py`
- **Características**:
  - **MRV**: Selecciona la columna no asignada con dominio más pequeño.
  - **LCV**: Ordena filas por menor restricción futura (usando dominios dinámicos).
  - **Forward Checking**: Elimina valores conflictivos de dominios futuros al asignar, restaurándolos en backtracking.
  - Detección de inconsistencias: Falla si un dominio queda vacío.

## Comparación de Tiempos y Eficiencia

Se ejecutaron 30 semillas (1-30) para n=4, 8, 10. Ambos algoritmos encontraron soluciones en 100% de los casos.

### Tiempos Promedio (s) y Desviación Estándar
- **Backtracking (LCV)**:
  - n=4: 0.0001 ± 0.0000
  - n=8: 0.0306 ± 0.0014
  - n=10: 0.8506 ± 0.0114
- **CSP (Forward Checking + MRV + LCV)**:
  - n=4: 0.0001 ± 0.0000
  - n=8: 0.0112 ± 0.0002
  - n=10: 0.5124 ± 0.0249

El CSP es más rápido y eficiente, especialmente para n mayor, debido a pruning con forward checking y selección inteligente con MRV.

### Nodos Explorados Promedio
- **Backtracking (LCV)**:
  - n=4: 60
  - n=8: 15720
  - n=10: 348150
- **CSP (Forward Checking + MRV + LCV)**:
  - n=4: 16
  - n=8: 1995
  - n=10: 76018

El CSP explora menos nodos gracias a la reducción de dominios.

## Comparación con tp4-busquedas-locales

Las métricas no son equivalentes:
- **tp5 (Nodos Explorados)**: Número de asignaciones probadas en backtracking (intentos de colocar reina en fila/columna).
- **tp4 (Estados Explorados)**: Número de evaluaciones de la función heurística `h_attacking_pairs` (fitness de tableros).

tp5 mide expansiones en el árbol de búsqueda (con restricciones directas), mientras tp4 mide evaluaciones de heurística en búsquedas locales. No se pueden comparar directamente, ya que tp5 no usa h y tp4 no cuenta asignaciones.

## Gráficos de Boxplots

Los boxplots muestran la distribución de tiempos y nodos explorados (ver `boxplots.png`):
- **Tiempos**: CSP tiene menor variabilidad y tiempos más bajos.
- **Nodos**: CSP explora consistentemente menos nodos.

![Boxplots](boxplots.png)

## Conclusión

El CSP con heurísticas es superior para N-Reinas, reduciendo espacio de búsqueda. Las métricas difieren de tp4, enfocándose en diferentes aspectos de eficiencia.
