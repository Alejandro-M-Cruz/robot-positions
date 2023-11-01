# robot-positions

## Cómo probar el código
Es necesario contar con una versíon reciente de Python (>=3.11) y con la librería matplotlib, que puede ser instalada desde la consola de comandos:\
\
`pip install matplotlib` \
\
Una vez instalado lo necesario, el código puede ejecutarse en cualquier entorno que permita la visualización de gráficos, como Visual Studio o PyCharm, o con el siguiente comando:\
\
`python main.py`\
\
Al ejecutarlo, se crearán 5 ficheros. *linear_speeds.txt* y *angular_speeds.txt* corresponden a los valores de velocidad lineal y angular calculados
a partir de las posiciones leídas del fichero *Path_SRA2223.txt*. Los tres restantes contienen las posiciones que conforman la trayectoria del robot reconstruida a partir de la posición y ángulo iniciales y las
velocidades lineales y angulares, introduciendo o no el error gaussiano artificial. Se imprimirá también por consola la información más relevante sobre los errores cometidos al estimar dichas posiciones, como se puede observar a continuación:

```
---------------Error with no artificial error---------------
Max error: 1.3902191258184728e-13
Average error: 4.825982154435232e-14
------------------------------------------------------------

---------------Error with linear speed error----------------
Max error: 0.03397165158272581
Average error: 0.023605237710064224
------------------------------------------------------------

---------------Error with angular speed error---------------
Max error: 0.022994814978083346
Average error: 0.013443016577788059
------------------------------------------------------------

-------------------Error with both errors-------------------
Max error: 0.04552709558024713
Average error: 0.03329355861181914
------------------------------------------------------------
```

Además, aparecerán varias gráficas. Para cada una de las estimaciones anteriormente descritas, se mostrarán dos gráficas. La primera de ellas es una visualización de la trayectoria del robot en los ejes x e y, mientras que la segunda representa la variación del error
de dicha estimación en comparación a los valores reales leídos del fichero.\
\
![image](https://github.com/Alejandro-M-Cruz/robot-positions/assets/113340373/38a68fc6-d7f0-47f5-8020-3392239f2bb4)
\
![image](https://github.com/Alejandro-M-Cruz/robot-positions/assets/113340373/4373839e-186f-4d7d-889a-49070596b81b)
\
![image](https://github.com/Alejandro-M-Cruz/robot-positions/assets/113340373/c97f488c-6e4c-4f73-9cb6-8dcb40f3c4da)
\
![image](https://github.com/Alejandro-M-Cruz/robot-positions/assets/113340373/60885170-2886-43db-85ef-b1aebb4885a3)
\
![image](https://github.com/Alejandro-M-Cruz/robot-positions/assets/113340373/27c3c067-935a-46c2-ad72-f94ca576205d)
\
![image](https://github.com/Alejandro-M-Cruz/robot-positions/assets/113340373/422d703b-949a-4abb-a386-f182d4043b10)
\
![image](https://github.com/Alejandro-M-Cruz/robot-positions/assets/113340373/dcdac1fc-182b-4a89-9879-b1d04176d218)
\
![image](https://github.com/Alejandro-M-Cruz/robot-positions/assets/113340373/e3d62be7-3fe3-4a52-ba77-0826ad5322ad)
\
![image](https://github.com/Alejandro-M-Cruz/robot-positions/assets/113340373/fa176337-547d-45aa-a6b8-d3f424d09333)

