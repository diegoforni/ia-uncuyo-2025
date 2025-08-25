# Informe de desempeño

Se ejecutaron 30 instancias en mapas aleatorios de 20×20 con probabilidad de
0.92 de celdas transitables. Para cada entorno se corrieron los ocho
algoritmos (`RANDOM`, `BFS`, `DFS`, `DLS50`, `DLS75`, `DLS100`, `UCS` y `A*`)
en **dos escenarios de costos**: uniforme y con penalización vertical. En total
se obtuvieron 480 ejecuciones.

Las métricas registradas (estados explorados, cantidad de acciones, costo y
tiempo) se resumen en el archivo `results.csv`, que incluye una columna
`scenario` para identificar el modelo de costos utilizado. A partir de este
archivo pueden generarse gráficas localmente.

De forma general, los métodos informados (`UCS` y `A*`) presentaron menor
costo y tiempo medio en ambos escenarios, mientras que la búsqueda aleatoria
resultó la menos eficiente.
