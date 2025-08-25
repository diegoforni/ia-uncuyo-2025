Trabajo Práctico 3: Algoritmos de Búsqueda

Este directorio reúne los materiales necesarios para resolver el TP3 del curso.

Instalación de dependencias

Posicionarse en la carpeta del proyecto:

cd tp3-algoritmos-busqueda


Ejecutar el script de instalación:

./install.sh


El script crea un entorno virtual en .venv e instala las dependencias listadas en requirements.txt.

Ejecución de los problemas

Los programas se ubicarán en la carpeta code. A continuación se indican los comandos previstos para ejecutar cada problema del trabajo.

1. Exploración del entorno
python code/exploracion_entorno.py

2. Búsquedas

El archivo code/busquedas.py permitirá resolver los distintos algoritmos solicitados. Ejemplos:

# Escenario 1 - costo uniforme
python code/busquedas.py --escenario 1 --algoritmo bfs

# Escenario 2 - costos diferenciados
python code/busquedas.py --escenario 2 --algoritmo astar


Nota: la función dls de búsqueda en profundidad limitada fue corregida para
evitar ciclos mediante un conjunto de estados visitados.

3. Evaluación estadística

Para repetir las ejecuciones en entornos aleatorios y generar los resultados:

# Ejecución completa (puede demorar varios minutos)
python code/evaluacion.py --runs 30 --size 100 --p 0.92

# Prueba rápida sobre mapas más pequeños
python code/evaluacion.py --runs 30 --size 20 --p 0.92


El script ejecuta los dos escenarios de costos (uniforme y diferenciado),
por lo que genera 480 registros: 30 entornos × 8 algoritmos × 2 escenarios.
Los resultados numéricos, con la columna adicional scenario, se almacenarán en results.csv y las gráficas podrán generarse en la carpeta images/ (no versionadas).

4. Análisis

El informe final se redactará en tp3-reporte.md tomando como base los resultados obtenidos.

Estructura esperada
tp3-algoritmos-busqueda/
├── code/
├── images/
├── install.sh
├── requirements.txt
├── results.csv
└── tp3-reporte.md


Cada subcarpeta se poblará a medida que se desarrollen los ejercicios.