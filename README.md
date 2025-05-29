
GESTION DE CENTRO DE VOTACIÓN

Este proyecto tiene como objetivo principal llevar un registro completo para ayudar a la administración de un centro de votación, se encuentra desarrollado en Python integrando una interfaz gráfica construida gracias a tkinter. Optimiza correctamente los datos, como los de votantes a sus puestos asignados, como a los jurados; la estadística y los gráficos se encuentran bien detallados.
Como requisito número 1 debes tener descargado Python en tu dispositivo (se recomienda la versión 3.6). Ya instalado puedes empezar a instalar dependencias. Tkinter viene normalmente ya incluida en el paquete de Python para Windows/macOS, en caso de que no tengas ese sistema debes entrar a tu terminal ingresar un código para instalarlo internamente.
Continuando con la descarga de Pandas que se usa para el análisis de datos, debes abrir tu terminal y colocar lo siguiente: ‘pip install pandas’, así ya obtendrías pandas en tu modelo Python. Siguiendo con matplotlib que se utiliza para la creación de gráficas, debes poner lo siguiente en tu terminal: ‘pip install matplotlib’, logrando descargar exitosamente la independencia.
Para mayor comodidad y no descargar uno por uno puedes sencillamente colocar esto en tu terminal: ‘pip install pandas matplotlib’, se descargan las dos dependencias sin ningún inconveniente.

Ejecutar Aplicación

Para ejecutar la aplicación debes seguir una serie de pasos detalladamente:
1.	Debes ingresar los datos de entrada que son el número de salones, número de mesas por salón y número de jurados por mesa, luego ingresas números enteros de los datos que desees poner.
2.	Haz clic en “Generar Centro de Votación”, a lo que inmediatamente la interfaz agregar los salones que ingresaste, los botones de las mesas y los de los jurados
3.	Debes registrar un jurado dando clic en el botón de “Jurados”, se abrirá una ventana en la que debes ingresar los datos como el Nombre, Cédula, Teléfono y Dirección en los campos que se indican.
4.	Haz clic en el botón “Guardar” e inmediatamente debe aparecer un mensaje mostrando que fue exitoso. 
5.	En la interfaz principal, haz clic en el botón “Cargar Votantes”, se abre una ventana para seleccionar el archivo csv con el nombre de ‘votantes.cv’, y recibirás un mensaje de confirmación.
6.	Puedes realizar búsqueda de votantes como la búsqueda de jurados, debes ingresar la cédula en números enteros y te aparecerán los datos.
7.	Debes registrar la asistencia de los votantes que asistieron, en la interfaz principal deber dar clic al botón “Registrar Asistencia”, se abre una ventana en la que debes ingresar la cédula del votante, el salón, la mesa y la hora de asistencia, claramente la cédula, la mesa y el salón deben coincidir con los votantes cargados.
8.	En la interfaz principal haz clic en “Cargar Resultados CSV”, se abre una ventana para seleccionar el archivo csv que tiene como nombre ‘resultados.csv’, se confirma la carga de los datos.
9.	Haz clic en botón “Resumen Estadístico”, aparece un mensaje de todos los jurados por salón/mesa, votantes por salón, asistencia, y las respuestas de votación.
10.	Luego das clic en el botón “Generar Gráficos”, se abre una ventana con las opciones de gráfico que desees ver.
11.	Por último, haz clic en el botón “Guardar Centro de Votación” se guardarán automáticamente en un archivo llamado ‘CentrodeVotacion.csv’ en la misma carpeta donde ejecutas la aplicación y recibirás un mensaje de confirmación al finalizar la carga.


