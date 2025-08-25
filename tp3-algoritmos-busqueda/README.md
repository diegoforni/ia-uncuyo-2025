# Trabajo Práctico 3: Algoritmos de Búsqueda

Este directorio reúne los materiales necesarios para resolver el TP3 del curso.

## Instalación de dependencias

1. Posicionarse en la carpeta del proyecto:
   ```bash
   cd tp3-algoritmos-busqueda
   ```
2. Ejecutar el script de instalación:
   ```bash
   ./install.sh
   ```
   El script crea un entorno virtual en `.venv` e instala las dependencias listadas en `requirements.txt`.

## Ejecución de los problemas

Los programas se ubicarán en la carpeta `code`. A continuación se indican los comandos previstos para ejecutar cada problema del trabajo.

### 1. Exploración del entorno

```bash
python code/exploracion_entorno.py
```

### 2. Búsquedas

El archivo `code/busquedas.py` permitirá resolver los distintos algoritmos solicitados. Ejemplos:

```bash
# Escenario 1 - costo uniforme
python code/busquedas.py --escenario 1 --algoritmo bfs

# Escenario 2 - costos diferenciados
python code/busquedas.py --escenario 2 --algoritmo astar
```

### 3. Evaluación estadística

Para repetir las ejecuciones en entornos aleatorios y generar los resultados:

```bash
python code/evaluacion.py --runs 30 --size 100 --p 0.92
```

Los resultados numéricos se almacenarán en `results.csv` y las gráficas se guardarán en `images/`.

### 4. Análisis

El informe final se redactará en `tp3-reporte.md` tomando como base los resultados obtenidos.

## Estructura esperada

```
tp3-algoritmos-busqueda/
├── code/
├── images/
├── install.sh
├── requirements.txt
├── results.csv
└── tp3-reporte.md
```

Cada subcarpeta se poblará a medida que se desarrollen los ejercicios.

