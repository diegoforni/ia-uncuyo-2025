# TP5 - Constraint Satisfaction Problems (CSP) para N-Reinas

## 1. Formulación CSP para Sudoku

El Sudoku se puede formular como un problema de satisfacción de restricciones (CSP) de la siguiente manera:

### Variables
- **Variables**: \( c_{i,j} \) para \( i = 1, \dots, 9 \) y \( j = 1, \dots, 9 \), donde cada variable representa el valor en la celda de la fila \( i \) y columna \( j \) del tablero de Sudoku.

### Dominio
- **Dominio**: Cada variable \( c_{i,j} \) tiene un dominio de valores posibles: \( \{1, 2, 3, 4, 5, 6, 7, 8, 9\} \).

### Restricciones
Las restricciones del Sudoku clásico son:
- **Restricciones de fila**: Para cada fila \( i \), todas las variables \( c_{i,1}, c_{i,2}, \dots, c_{i,9} \) deben tener valores distintos.
- **Restricciones de columna**: Para cada columna \( j \), todas las variables \( c_{1,j}, c_{2,j}, \dots, c_{9,j} \) deben tener valores distintos.
- **Restricciones de bloque**: Para cada bloque 3x3 (definido por \( b_r = \lfloor (i-1)/3 \rfloor + 1 \) y \( b_c = \lfloor (j-1)/3 \rfloor + 1 \)), todas las variables en ese bloque deben tener valores distintos.

Estas restricciones aseguran que el tablero resultante sea una solución válida de Sudoku.

## 2. Consistencia de arcos (AC-3) en el mapa de Australia

Demostrar que AC-3 detecta la inconsistencia de la asignación parcial \(\text{WA}=\text{red},\, \text{V}=\text{blue}\) en el problema de coloreo del mapa de Australia (AIMA Fig. 6.1).

### Variables, dominios y vecinos
- Variables: \(\{\text{WA}, \text{NT}, \text{SA}, \text{Q}, \text{NSW}, \text{V}, \text{T}\}\)
- Dominio inicial: \(D(X)=\{\text{red},\text{green},\text{blue}\}\) para todas, salvo las asignadas.
- Restricciones: desigualdad para pares de regiones adyacentes.
- Vecindad (aristas):
  - WA: NT, SA
  - NT: WA, SA, Q
  - SA: WA, NT, Q, NSW, V
  - Q: NT, SA, NSW
  - NSW: Q, SA, V
  - V: SA, NSW
  - T: (sin vecinos)

Asignación parcial: \(D(\text{WA})=\{\text{red}\}\), \(D(\text{V})=\{\text{blue}\}\) y las demás con \(\{\text{red},\text{green},\text{blue}\}\).

### Ejecución de AC-3 (resumen de podas)
Partimos con la cola de arcos salientes de las variables asignadas: \((\text{WA},\text{NT}), (\text{WA},\text{SA}), (\text{V},\text{SA}), (\text{V},\text{NSW})\), etc. Aplicamos REVISE y reinsertamos arcos cuando un dominio cambia.

1) Propagación desde WA=red:
  - \(D(\text{NT}) \leftarrow D(\text{NT})\\\{\text{red}\} = \{\text{green},\text{blue}\}\)
  - \(D(\text{SA}) \leftarrow D(\text{SA})\\\{\text{red}\} = \{\text{green},\text{blue}\}\)

2) Propagación desde V=blue:
  - \(D(\text{NSW}) \leftarrow D(\text{NSW})\\\{\text{blue}\} = \{\text{red},\text{green}\}\)
  - \(D(\text{SA}) \leftarrow D(\text{SA})\\\{\text{blue}\} = \{\text{green}\}\)  (SA queda singleton)

3) Propagación desde SA=green (nuevo singleton):
  - \(D(\text{NT}) \leftarrow D(\text{NT})\\\{\text{green}\} = \{\text{blue}\}\)
  - \(D(\text{Q}) \leftarrow D(\text{Q})\\\{\text{green}\} = \{\text{red},\text{blue}\}\)
  - \(D(\text{NSW}) \leftarrow D(\text{NSW})\\\{\text{green}\} = \{\text{red}\}\)

4) Propagación desde NT=blue (nuevo singleton):
  - \(D(\text{Q}) \leftarrow D(\text{Q})\\\{\text{blue}\} = \{\text{red}\}\)

5) Propagación entre Q y NSW:
  - Con \(D(\text{Q})=\{\text{red}\}\) y \(D(\text{NSW})=\{\text{red}\}\), la restricción \(\text{Q} \neq \text{NSW}\) obliga a podar \(\text{red}\) en al menos uno. Al revisar el arco \((\text{Q},\text{NSW})\) o \((\text{NSW},\text{Q})\), uno de los dominios queda vacío.
  - Por ejemplo, al revisar \((\text{Q},\text{NSW})\): \(D(\text{NSW}) \leftarrow D(\text{NSW})\\\{\text{red}\} = \varnothing\).

Como \(D(\text{NSW})=\varnothing\), AC-3 detecta inconsistencia y se detiene. Intuitivamente: la asignación \(\text{WA}=\text{red}\) fuerza \(\text{SA}=\text{green}\), lo que fuerza \(\text{NT}=\text{blue}\) y \(\text{Q}=\text{red}\); a la vez, \(\text{V}=\text{blue}\) fuerza \(\text{NSW}=\text{red}\), dejando a NSW sin color distinto de sus vecinos (Q=red, SA=green, V=blue).

## 3. Complejidad de AC-3 en CSP estructurado como árbol

En un CSP estructurado como árbol, donde el grafo de restricciones forma un árbol (cualquier dos variables están relacionadas por a lo sumo un camino), la complejidad en el peor caso de AC-3 es \(O(c \cdot d)\). Esto se debe a que chequear la consistencia de un arco (es decir, revisar si un par de variables es consistente bajo la restricción) toma tiempo \(O(d)\), donde \(d\) es el tamaño del dominio, y dado que hay \(c\) restricciones (arcos) en el grafo, el algoritmo debe procesar cada una de ellas, resultando en una complejidad total de \(O(c \cdot d)\).

Esto es fácil de deducir tratando el árbol como una lista (y ese es el peor caso del árbol), ya que en una estructura lineal, el algoritmo procesa cada arco una vez, y la verificación de consistencia por arco es \(O(d)\), llevando a \(O(c \cdot d)\) en total.

Por qué no se reencolan arcos en un árbol
- No hay ciclos: entre dos variables hay un único camino, de modo que la información (podas de dominio) fluye en una sola dirección a lo largo del árbol.
- Si se enraiza el árbol y se procesa de hojas→raíz, cada REVISE(Xi, Xj) solo puede reducir el dominio “hacia arriba”. Como los dominios solo disminuyen (monotonía) y no existe un camino alternativo que haga que un recorte vuelva a impactar arcos ya verificados, ningún arco necesita reinsertarse.
- Intuitivamente, el peor caso equivale a una lista: se recorre cada arco una sola vez en el sentido hoja→raíz, sin reencolados adicionales.

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
