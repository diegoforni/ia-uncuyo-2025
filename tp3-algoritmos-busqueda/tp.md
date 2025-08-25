# Trabajo Práctico 3: Búsqueda no informada e informada

Este documento describe las consignas del TP3 y cómo ejecutar los programas provistos para resolverlas.

## FrozenLake

`FrozenLake-v1` es un entorno de cuadrícula donde el agente debe avanzar desde un punto de inicio hasta la meta evitando los agujeros del hielo. Por defecto se dispone de 100 acciones como máximo.

Las acciones disponibles son:

- `0`: mover a la izquierda.
- `1`: mover hacia abajo.
- `2`: mover a la derecha.
- `3`: mover hacia arriba.

El agente percibe su ubicación y si la casilla contiene un agujero o es la meta.

## Exploración del entorno

1. **Instalación y ejecución básica**
   ```python
   import gymnasium as gym
   env = gym.make('FrozenLake-v1', render_mode='human')
   ```
2. **Información del entorno**
   ```python
   print("Número de estados:", env.observation_space.n)
   print("Número de acciones:", env.action_space.n)
   ```
3. **Episodio con acciones aleatorias**
   ```python
   state = env.reset()
   done = truncated = False
   while not (done or truncated):
       action = env.action_space.sample()
       next_state, reward, done, truncated, _ = env.step(action)
       print(f"Acción: {action}, Nuevo estado: {next_state}, Recompensa: {reward}")
   ```
4. **Mapas y parámetros personalizados**
   - `is_slippery`: controla si el agente puede deslizarse (por defecto `True`).
   - Mapas precargados: `gym.make('FrozenLake-v1', map_name="4x4")`
   - Mapas definidos manualmente:
     ```python
     desc = ["SFFF", "FHFH", "FFFH", "HFFG"]
     gym.make('FrozenLake-v1', desc=desc)
     ```
   - Mapas aleatorios:
     ```python
     from gymnasium.envs.toy_text.frozen_lake import generate_random_map
     gym.make('FrozenLake-v1', desc=generate_random_map(size=8))
     ```
   - **Función personalizada** `generate_random_map_custom` (incluida en `code/env_utils.py`) para definir tamaño, probabilidad de celdas transitables y posiciones aleatorias de inicio y objetivo.
5. **Modificar la "vida" del agente**
   ```python
   from gymnasium import wrappers
   nuevo_limite = 10
   env = gym.make('FrozenLake-v1').env
   env = wrappers.TimeLimit(env, nuevo_limite)
   ```

## Búsquedas

1. **Entorno determinista de 100×100**
   ```bash
   python code/busquedas.py --size 100 --p 0.92 --escenario 1 --algoritmo bfs
   ```
   El parámetro `--escenario` determina los costos de las acciones y `--algoritmo` selecciona el método de búsqueda.

2. **Algoritmos disponibles**
   - `random`: búsqueda aleatoria.
   - `bfs`: búsqueda por anchura.
   - `dfs`: búsqueda por profundidad.
   - `dls`: profundidad limitada (`--limite` para 50, 75 o 100).
   - `ucs`: costo uniforme.
   - `astar`: A* con heurística admisible.

   Ejemplos:
   ```bash
   # Escenario 1 - costo uniforme
   python code/busquedas.py --escenario 1 --algoritmo ucs

   # Escenario 2 - costos diferenciados
   python code/busquedas.py --escenario 2 --algoritmo astar
   ```

3. **Impresión de resultados**
   Al finalizar cada ejecución se muestra el mapa generado y la secuencia de estados desde el origen hasta la meta si se encontró solución.

## Evaluación estadística

Ejecutar 30 veces cada algoritmo sobre entornos aleatorios y guardar los resultados:
```bash
python code/evaluacion.py --runs 30 --size 100 --p 0.92 --results results.csv --images images
```
Se generan métricas de estados explorados, acciones, costos y tiempo, además de gráficos de cajas en `images/`.

## Forma de entrega

La carpeta final debe contener:

```
tp3-algoritmos-busqueda/
├── code/
├── images/
├── results.csv
├── tp3-reporte.md
└── tp.md
```

El archivo `tp3-reporte.md` debe incluir el análisis de desempeño junto con los gráficos generados.
