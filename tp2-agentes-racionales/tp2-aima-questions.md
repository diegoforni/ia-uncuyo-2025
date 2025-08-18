## 2.10 Consider a modified version of the vacuum environment in Exercise 2.8, in which the agent is penalized one point for each movement.

**a. Can a simple reflex agent be perfectly rational for this environment? Explain.**

No, un agente reflexivo simple no puede ser perfectamente racional, ya que no tiene memoria. Por lo tanto, no puede recordar la cantidad de pasos realizados para minimizarlos.

**b. What about a reflex agent with state? Design such an agent.**

Un agente reflexivo con estado puede acercarse más al objetivo. Sería similar al agente reflexivo simple, pero incorporando memoria para no pasar dos veces por la misma celda.

**c. How do your answers to a and b change if the agent’s percepts give it the clean/dirty status of every square in the environment?**

Si el agente tiene acceso a esa información, podemos diseñar agentes con un rendimiento significativamente mejor, con o sin memoria. Igualmente, se podría buscar el camino más corto que limpie todas las celdas.

---

## 2.11 Consider a modified version of the vacuum environment in Exercise 2.8, in which the geography of the environment—its extent, boundaries, and obstacles—is unknown, as is the initial dirt configuration. (The agent can go Up and Down as well as Left and Right.)

**a. Can a simple reflex agent be perfectly rational for this environment? Explain.**

Sí, un agente reflexivo simple puede ser perfectamente racional en este entorno, ya que su objetivo será limpiar la mayor cantidad posible de celdas, y eso es lo que intentará hacer, sin importar los obstáculos.

**b. Can a simple reflex agent with a randomized agent function outperform a simple reflex agent?**

Sí, un agente aleatorio, con la semilla correcta, puede resolver el problema de manera óptima en ciertos casos.

**c. Can you design an environment in which your randomized agent will perform poorly? Show your results.**

Un entorno muy grande en el que la suciedad se encuentre en los bordes. En este caso, la probabilidad de que el agente llegue hasta los bordes para limpiar sería cercana a cero.

**d. Can a reflex agent with state outperform a simple reflex agent? Can you design a rational agent of this type?**

Si el agente tuviera memoria, podría evitar pasar dos veces por la misma celda y también recordar obstáculos y los bordes del entorno. Esto mejoraría significativamente su rendimiento, convirtiéndolo en un agente racional más eficiente.
