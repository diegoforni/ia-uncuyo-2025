# Informe de desempeño

Se ejecutaron 30 instancias en mapas aleatorios de 20×20 con probabilidad de
0.92 de celdas transitables. Se evaluaron los algoritmos `RANDOM`, `BFS`,
`DFS`, `DLS50`, `DLS75`, `DLS100`, `UCS` y `A*`.

Las métricas registradas (estados explorados, cantidad de acciones, costo y tiempo) se resumen en el archivo `results.csv`. A partir de este archivo pueden generarse gráficas localmente.

De forma general, los métodos informados (`UCS` y `A*`) presentaron menor
costo y tiempo medio, mientras que la búsqueda aleatoria resultó la menos
eficiente.
