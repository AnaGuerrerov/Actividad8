
#ACTIVIDAD 8, ANA SOFÍA GUERRERO
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os

 #Realizo estos dos diccionarios vacíos para las estadisiticas
jurados_salon = {}
jurados_mesa = {}
votantes_salon = {}
asistencia_salon = {}
resumen_votos = {}


#Creo una diccionario vacío de resultados para cargar resultados csv
resultados = []
#Creo un conjunto vacio de cédulas de votantes y jurados, para agregar datos, y que no se puedan repetir
cedula_votantes=set()
cedula_jurados=set()

#Creo una lista donde guardará la asistencia 
Asistencia_Vo= []

#Lista donde se almacenarán los votantes
votantes = []
#Creo una lista vacia para agregar datos 
mesajurados = []

def Cargar_Votantes():
    #Esto me permite abrir una ventana para poder seleccionar el archivo, solo se muestran los archivos con extensión .csv
    Archivoscsv = filedialog.askopenfilename(title="Seleccione el archido de votantes.", filetypes=[("Archivos CSV", "*.csv")])
    
    if not Archivoscsv:
        messagebox.showerror("Error", "No se ha seleccionado ningún archivo.")
        return
    #Uso try para que me muestre el error al instante
    try:
        #Aquí se abre y se lee el archivo CSV
        with open(Archivoscsv) as archivotantes:

            lector_csv = csv.reader(archivotantes)

            #Salta el encabezado para leer el dato de una vez en el CSV
            next(lector_csv, None) 

            #Agreg un votantes.clear para poder limpiar los vontantes anteriores si ya estaban 
            votantes.clear()
            #Añado un cedula_votantes.clear para limpiar las cédulas anteriores
            cedula_votantes.clear()
            
            for datocsv in lector_csv:
                #si la longitud de los datos CSV es mayor o igual a 4, se asegura de que tenga los 4 elementos, se espera que cada votante tenga 4 datos
                if len(datocsv)>=4:
                    #debo guardar el dato [1] el cual es la posición 2 d la lista y esta es la cédula
                    Cedula= datocsv[1]

                    #Aquí debo validar si la cédula del votane ya existe
                    if Cedula in cedula_votantes:
                        messagebox.showerror("Error", f"La cédula {Cedula}ya esta registrada, intenta con otra cédula")
                        #Agrego continue para que detecte el error y siga leyendo las filas, sin alterar los datos
                        continue
                    #Debo agregar la cédula si no existe, se agrega con .add al conjunto(set) llamado cedula_votantes
                    cedula_votantes.add(Cedula)

                    #Recorre en el archivo CSV los datos que son, nombre, cédula, salón y mesa, con una lista empezando desde 0
                    #y se le agregan los datos a la lista vacía de votantes

                    votantes.append({"nombre": datocsv[0],"cedula": datocsv[1],"salon": datocsv[2],"mesa":datocsv[3]})

        #Se usa para que el usuario se entere de que fueron cargados exitosamente            
        messagebox.showinfo("Éxito", "Los Votantes han sido cargados correctamente.")

    #Except para indicar el error que hay si no se cumple
    except Exception as e:
        messagebox.showerror("Error", f"No se ha podido cargar el archivo:\n{e}")

#Defino el botón de buscar el Votante
def Buscar_votante():

    #Uso try para que me muestre el error al instante
    try:
        #donde la Cédula del votante es igual a la entrada del bloque
        cedula = EntryVotante.get() 
        
        #Si no ingresa un número de cedula le muestra el error
        if not cedula:

            messagebox.showerror("Error", "Debe ingresar un número de cédula.")

            return
        
        #Aquí realizo un ciclo for para verificar si la cedula que ingresaron es la misma del archivo de un votante, donde "votantes" es el archivo csv
        encontrado=False
        for Votante in votantes:

            #si la cédula de un votante que esta en el archivo es igual a la cedula que ingresaron
            if Votante["cedula"] == cedula:
                #Se muestra un mensaje que si exise, donde muestra los datos que se encuentran en el archivo
                messagebox.showinfo("El Votante si existe",f"Nombre: {Votante['nombre']}\nCédula: {Votante['cedula']}\nSalon: {Votante['salon']}\nMesa: {Votante['mesa']}")
                
                #podemos colocar un True para mostrar que se encontro y asi un error si este no ha sido encontrado.
                encontrado=True 
                #Aquí rompemos el ciclo una vez se haya encontrado el votante
                break  

        if not encontrado:
            messagebox.showinfo("No encontrado", "No se encontró ningún votante con esa cédula.")

    #Esto lo muestra en el caso de que en el archivo no se encuentre
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al buscar al votante: {e}")


#----------------------Interfaz Asistencia------------------
def votantes_asistencia ():
    Ventana = tk.Toplevel()
    Ventana.title("Registro de Asistencia")
    Ventana.geometry("250x200")

    tk.Label(Ventana, text="Cédula del Votante").grid(row=0, column=1)
    Entrycedula = tk.Entry(Ventana)
    Entrycedula.grid(row=1, column=1)

    tk.Label(Ventana, text="Salón").grid(row=2, column=1, padx=100)
    Entrysalon = tk.Entry(Ventana)
    Entrysalon.grid(row=3, column=1)

    tk.Label(Ventana, text="Mesa").grid(row=4, column=1)
    Entrymesa = tk.Entry(Ventana)
    Entrymesa.grid(row=5, column=1)

    tk.Label(Ventana, text="Hora (HH:MM)").grid(row=6, column=1)
    Entryhora = tk.Entry(Ventana)
    Entryhora.grid(row=7, column=1)

    BotonGuardar = tk.Button(Ventana, text="Registrar", command=lambda: Asistencia(Entrycedula, Entrysalon, Entrymesa, Entryhora))
    BotonGuardar.grid(row=9, column=1)
#------------------------------------------------------------------

def asistencia_registrada (cedula,salon,mesa):
    #Sirve para verificiar si el archivo 'asistencia.csv' existe
    if not os.path.exists("asistencia.csv"):
        #si el archivo no existe devuelve false. lo que quiere decir que la cédula no ha sido registrada aún
        return False 

    #Se abre el archivo asistencias.csv para leerlo 'r' 
    with open("asistencia.csv", "r", newline="") as archivo:

        #Se utiliza csv.DictReader que convierte cada fila, para leerla columna por columna
        reader = csv.DictReader(archivo)

        #Ciclo for para que recorra cada fila en este caso lector
        for lector in reader:
            #Con la condición if compara si cada fila corresponde a lo ingresado
            if lector["cedula"] == cedula and lector["salon"] == salon and lector["mesa"] == mesa:
                #Si las tres condiciones son ciertas, quiere decir que ya fue registrada
                return True 
    #Si después de todo da como resultado que no, se return false 
    return False  

#Para Verificar si ya esta registrado en la asistencia
def Asistencia(Entrycedula,Entrysalon,Entrymesa,Entryhora):
    #defino cada campo de entrada como un elemento
    cedula = Entrycedula.get().strip()
    salon = Entrysalon.get().strip()
    mesa = Entrymesa.get().strip()
    hora = Entryhora.get().strip()

    #Debo verificar si no hay un dato completo y asi indique que debe completar los campos
    if not cedula or not salon or not mesa or not hora:

        messagebox.showerror("Error", "Debe completar todos los campos")
        #Para detener la función en caso de que hayan campos vacíos
        return
    
    #Verifico que en las entradas de cedula, salon y mesa deben ser número enteros
    if not Números_Enteros (cedula,salon,mesa):
        messagebox.showerror("Error","Debe Ingresar números enteros positivos")
        #Detiene la función en caso de que encuentre un error
        return

    #Verifico que la hora 17:00 no puede ser registrado en caso de que la registren muestra un mensaje
    if hora == "17:00":
        messagebox.showerror("Error", "No se puede registrar asistencia a las 17:00.")
     #Detiene la función en caso de que pongan la hora 17:00
        return
    
    # if ":" no in hora es si no ponen la hora en el formato de ':'y el len que es la longitud de hora que debe ser de 5
    #tomando en cuenta los ':', si no es igual a 5, muestra el mensaje
    if ":" not in hora or len(hora) != 5:
      
      #Para poder dar un error en caso de que no pongan la hora en el formato correcto (HH:MM)
      messagebox.showerror("Error", "La hora debe estar en formato HH:MM")

     #Detiene la función en caso de que pongan un formato incorrecto
      return
    
    #Inicia en false ya que no se ha encontrado el dato aún
    encontrado = False

    #votantes es una lista que esta con los datos de estos
    for votante in votantes: 
        #Si la cédula que ingreso es igual a la cédula se encuentra 
        if votante["cedula"] == cedula:
            #Si se encuentra la cédula del votante igual a la del archivo
            encontrado = True
            if not  votante["salon"] == salon:
                messagebox.showerror("Error","Debes Ingresar el Salón correcto")
                #Para detener la función en caso que el salón no exista
                return
            if not votante["mesa"] == mesa:
                messagebox.showerror("Error", "Debes Ingresar una Mesa correcta")
                #Para detener la función en caso que la mesa no exista
                return
            break
    #en el caso en el que no la hayan registrado aún aparece un mensaje
    if not encontrado:
        messagebox.showerror("Error", "La cédula no está registrada.")
        return
    

     # Aquí se hace la validación de asistencia repetida, si ya estan registradas muestra el mensaje
    if asistencia_registrada(cedula, salon, mesa):
        messagebox.showerror("Error", "Esta asistencia ya fue registrada.")
        #Se detiene la función en caso de que ya este registrada
        return
    
    #Se crea esta lista con los datos en orden
    registro=[salon,mesa,cedula,hora]

    #Agregamos los datos de registro en la lista vacía 
    Asistencia_Vo.append(registro)

    #Asume que el encabezado debe estar, por lo tanto true
    encabezado = True
    try:
        #Se intenta abrir el archivo en modo lectura 'r'
        with open("asistencia.csv", "r", newline="") as archivoleer:
            #lee la primera línea que es el encabezado con las columnas

            primera_linea = archivoleer.readline()
            if primera_linea.strip():
                #una vez que el encabezado ya esta escrito, para evitar escribir el encabezado de nuevo
                encabezado = False
    #En caso de que el archivo no exista 
    except FileNotFoundError:
        #para indicar que sí se debe escribir el encabezado
        encabezado = True

    try:
        #Se abre el archivo, en 'a' que es agregar
        with open("asistencia.csv", "a", newline="") as archivo:
            writer = csv.writer(archivo)
            #si el encabezado es igual True, se escribe la primera fila con los nombres de las columnas
            if encabezado:
                writer.writerow(["salon", "mesa","cedula", "hora"])
            #se hace uso del registro que es una lista con los datos registrados
            writer.writerow(registro)

        messagebox.showinfo("Éxito", "Asistencia registrada correctamente.")

    except Exception as ex:
        messagebox.showerror("Error", f"No se pudo guardar la asistencia: {ex}")

#Defino el botón de cargar resulados csv
def Cargar_Resultados():

    #Esto me permite abrir una ventana para poder seleccionar el archivo, solo se muestran los archivos con extensión .csv
    archivocsv = filedialog.askopenfilename(title="Seleccione el archivo de resultados.", filetypes=[("Archivos CSV", "*.csv")])
    
    if not archivocsv:
        messagebox.showerror("Error", "No se ha seleccionado ningún archivo")
        return
    #Uso try para que me muestre el error al instante
    try:
        #Se abre el archivo en modo lectura, csv.DictReader lee el archivo CSV para los encabezados 
        with open(archivocsv, encoding="utf-8") as archivo_resultados:
            lector_csv = csv.DictReader(archivo_resultados)

            # el encabezado debe ser de ese orden, p{i} señala el número que esta en el archivo csv, de p1 a p9
            encabezados= ["salon", "mesa", "tarjeton"] + [f"p{i}" for i in range(1, 10)]

            #fieldnames contiene una lista con los nombres de las columnas del archivo
            #Verifica si no son iguales a los encabezados
            if lector_csv.fieldnames != encabezados:

                #muestra un mensaje si no se encontraron los encabazados 
                messagebox.showerror("Error",f"Encabezados incorrectos.\nSe esperaban:\n{encabezados}\n"f"Se encontraron:\n{lector_csv.fieldnames}")
                #Detiene la función si son incorrectos
                return
            
            # Limpia la lista de resultados
            resultados.clear()  
            #El ciclo for es para recorrer cada f en el archivo csv, para agregarla a la lista resultados
            for f in lector_csv:
                resultados.append(f)
                
        #Cuando se carguen todas la filas muestra un mensaje e indica la longitud de los datos usando 'len'
        messagebox.showinfo("Éxito", f"Se cargaron {len(resultados)} resultados correctamente.")
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")


#Debo poner estos parámetros que son las listas con los datos de los votantes y jurados
def resumen_estadistico(mesajurados, votantes, Asistencia_Vo, resultados):
    #Hago un try para que me detecte errores
    try:

       #Establezco este contador en 0 para contar el total de las mesas
        totalmesas_registradas= 0 
        #-----------Total de jurados por salón y por mesa--------------------
        #'salones' es el salón actual que se está procesando, y ese salón es una lista de mesas
        #para i que empieza en 1, recorre la lista mesajurados, y enumerate es la secuencia que se lleva en los ()
        for i, salones in  enumerate(mesajurados, 1): 
            
            #Aquí se inicia otro contado y se sumará todos los jurados encontrados en el salón actual 
            salontotaljurados = 0

            #Hago otro ciclo for para recorrer ahora las mesas, 'm' es el valor que inicia en 1, almacena el número de la mesa actual
            #'mesa' contiene los datos de la mesa actual, en la estructura mesajurados
            for m, mesas in enumerate(salones, 1):
                # Aquí se calcula cuántos jurados hay en mesas, len(mesas) da la cantidad de jurados para una mesa en especifico
                num_juradosmesa = len(mesas)
                #Esta línea suma el número de jurados encontrados en la mesa actual (num_juradosmesa) al total acumulado para el salón actual.
                salontotaljurados += num_juradosmesa
                #Aquí guarda en el diccionario jurados_mesa cuántos jurados tiene esa mesa
                jurados_mesa[f"Salón {i}, Mesa {m}"] = num_juradosmesa
                # Esto cuenta todas las mesas que se han regitrado en mesajurados, sin importar si tienen jurados o no
                totalmesas_registradas+= 1 
                #Aquí guarda el número total de jurados encontrados en el salón actual en el diccionario jurados_salon
            jurados_salon[f"Salón {i}"] = salontotaljurados
        

        #------------Total de votantes por salón-------------
        #Se crea un DataFrame a partir de la lista 'votantes'
        df_votantes = pd.DataFrame(votantes)
        #En esta condición verificamos si hay votantes, .shape nos da sus dimensiones en forma de tupla (x,y)
        #pone como condición si hay más de 0 filas, o si ya hay alguien regisrado
        if df_votantes.shape[0] > 0:
            # Intenta convertir la columna 'salon' a números
            # 'errors='coerce'' convier un valor que no sea numérico a NaN que es (Not a Number)
            #['salon_num'] crea una nueva columna con este nombre. Si ya existe, se sobrescribirá en el df
            df_votantes['salon_num'] = df_votantes['salon'].apply(lambda x: pd.to_numeric(x, errors='coerce'))
            #Elimina los valores faltantes , especificando loq ue debe eliminar con 'subset'
            df_votantes = df_votantes.dropna(subset=['salon_num'])
            #Vuelve los valores de la columna números enteros
            df_votantes['salon_num'] = df_votantes['salon_num'].astype(int)
            #Cuenta las veces que aparecen los datos
            conteo_votantes = df_votantes['salon_num'].value_counts()

            #Realizo un ciclo for para verificar los salones, el +1 es para que genere rango de (1, al número de salones) 
            #len(mesajurados) da la longitud de salones y se crea una secuencia del 1 hasta el total de salones
            for i in range(1, len(mesajurados) + 1):
                #aquí realiza una etiqueta en donde i sera el número de salones
                saloninfo = f"Salón {i}"
                #votantes_salon[salon_key] es cómo cada salón ()"Salón 1", "Salón 2") obtenga su recuento de votantes 
                # y se almacena en el diccionario votantes_salon, si 'i' existe da el número, si no existe da 0
                votantes_salon[saloninfo] = conteo_votantes.get(i, 0)
        #si no hay votantes
        else:
            for i in range(1, len(mesajurados) + 1):
                #se le asigan un valor al diccionario de 0
                votantes_salon[f"Salón {i}"] = 0

        # ---------Porcentaje de mesas completas--------------

        # total_mesas ahora usa 'total_mesas_registradas' que es la cuenta de las sublistas
        total_mesas = totalmesas_registradas
        #sum() cuenta los  elementos que cumplen una función, el 1 es un contador
        # el if len es para verificar si en la longitud de mesas hay un jurado
        mesas_completas = sum(1 for salon_data in mesajurados for mesas in salon_data if len(mesas) > 0)
        #verifica si el total de mesas es mayor y para no dividir entre 0 s pone un else para que ponga el dato en 0
        porcentaje_completas = (mesas_completas / total_mesas * 100) if total_mesas > 0 else 0
        

        #-------Asistencia por salón----------------------
        
        #Realizo un ciclo for para verificar los salones, el +1 es para que genere rango de (1, al número de salones) 
        #len(mesajurados) da la longitud de salones y se crea una secuencia del 1 hasta el total de salones
        for i in range(1, len(mesajurados) + 1):
            #se le asigan un valor al diccionario de 0
            asistencia_salon[f"Salón {i}"] = 0

        # Aquí se verifica si la lista 'Asistencia_Vo' (registros de asistencia) tiene datos
        if Asistencia_Vo:
           
            try:
                #Se creaun DataFrame a partir de los datos de asistencia y se define las columnas 
                df_asistencia = pd.DataFrame(Asistencia_Vo, columns=['salon_col', 'mesa', 'cedula', 'hora'])
                # Se convierte la columna 'salon_col' a números. Si un valor no es numérico marca'errors='coerce' y  lo convierte a NaN (Not a Number)
                df_asistencia['salon_num'] = pd.to_numeric(df_asistencia['salon_col'], errors='coerce')
                #Elimanamos los datos NaN
                df_asistencia = df_asistencia.dropna(subset=['salon_num'])
                #Se convierte la columna 'salon_num' a números enteros
                df_asistencia['salon_num'] = df_asistencia['salon_num'].astype(int)

                #Aquí se cuenta cuántas veces aparece cada número de salón válido.
                conteo_asistencia = df_asistencia['salon_num'].value_counts()


                #Ccilo for para recorrer los resultados de conteo de asistencia, en donde 'salon_num' es el número de salón y 'cantidad' es su conteo
                #.items()para recorrer tanto la clave como el valor 
                for salon_num, cantidad in conteo_asistencia.items():

                    #Donde esta clave sea la etiqueta del salon_num en entero
                    saloninfo= f"Salón {int(salon_num)}"

                    #Si la clave saloninfo ya existe en el diccionario
                    if saloninfo in asistencia_salon:
                        #En el diccionario de asistencia encuentre la entra para la clave
                        asistencia_salon[saloninfo] = cantidad

            except Exception as e:
                messagebox.showerror("Error",f"procesando asistencia con DataFrame: {e}") 

                #Se recorre el registro de la lista 
                for registro in Asistencia_Vo:
                    try:
                        #Para verificar que no este vacío
                        if len(registro) >= 1:
                            #Aquí se convierte el primer elemento del 'registro' a un número entero.
                            salon_num = int(registro[0])
                            saloninfo = f"Salón {salon_num}"
                            # Se verifica si este salón ya esta tenemos en el contador 'asistencia_salon'
                            if saloninfo in asistencia_salon:
                                #Si ya existe, le sumamos 1 al conteo
                                asistencia_salon[saloninfo] += 1

                    except (ValueError, IndexError):
                        continue

        #-------Resumen de votaciones----------

        #Se inicia si 'resultados' no está vacío
        if resultados:
            #Aquí se convierte los resultados a un DataFrame
            df_resultados = pd.DataFrame(resultados)
            #se recorre cada columna
            for columna in df_resultados.columns:
                #Si la columna empeiza por 'p', que son las preguntas 
                if columna.startswith('p'):
                    #Se cuenta cuántas veces aparece cada respuesta en la columna
                    conteo_colum = df_resultados[columna].value_counts()
                    #conteo_column.items() da esto (índice, valor)
                    # el for index, count in, es el que los "recibe" y los separa.
                    conteo_dict = {str(index): count for index, count in conteo_colum.items()}
                    #Se guarda el conteo de la pregunta en el resumen de votos que e el diccionario
                    resumen_votos[columna] = conteo_dict

        # mensaje de resumen
        mensaje = "Resumen estadístico:\n\n"
       
        
        # Formato para Jurados por Salón y por Mesa
        mensaje += "\nTotal de Jurados por Salón:\n"
        #Recorremos cada salón y su total de jurados para añadirlo al mensaje
        for salon, total in jurados_salon.items():mensaje += f"   - {salon}: {total} jurados\n"

        mensaje += "\nNúmero de Jurados por Mesa:\n"
        # Ordenar las mesas para una mejor presentación,sorted()' organiza los elementos en una nueva lista
        # 'key=lambda item ' le dice a 'sorted' cómo ordenar, así, ordena primero por salón, luego por mesa
        organizacion_mesas = sorted(jurados_mesa.items(), key=lambda item: (int(item[0].split(',')[0].split(' ')[1]), int(item[0].split(',')[1].split(' ')[2])))
        # Añadimos cada mesa y su total de jurados al mensaje
        for mesainfo, total_jurados in organizacion_mesas:
            mensaje += f"   - {mesainfo}: {total_jurados} jurado(s)\n"

        mensaje += "\nTotal de Votantes por Salón:\n"
        # Recorremos cada salón y su total de votante
        for salon, total in votantes_salon.items():
            mensaje += f"   - {salon}: {total} votantes\n"
        
        # Formato para Porcentaje de Mesas Completas
        mensaje += f"\nPorcentaje de Mesas Completas:\n"
        #.2 es para que solo esten dos dígitos después del punto decimal, y la 'f' como float (decimal)
        mensaje += f"   - {porcentaje_completas:.2f}% ({mesas_completas}/{total_mesas} mesas)\n"

        mensaje += "\nAsistencia de Votantes por Salón:\n" 
        # Recorremos cada salón y su total de votantes asistidos.
        for salon, total in asistencia_salon.items():
            mensaje += f"   - {salon}: {total} asistido(s)\n" 
        
        #Se verifica si hay datos que mostrar
        if resumen_votos:
            mensaje += "\nResumen de Votaciones:\n"
            # Recorremos cada pregunta y sus respuestas, en el diccionario
            for pregunta, respuestas in resumen_votos.items():
                # Aquí 'join()' pega los elementos de la lista
                #.items()  es una secuencia de pares 
                respuestas_str = ", ".join([f"{x}={y}" for x, y in respuestas.items()])
                mensaje += f"   - {pregunta}: {respuestas_str}\n"
        else:
            mensaje += "\nResumen de Votaciones: No hay datos disponibles\n"

        messagebox.showinfo("Resumen Estadístico", mensaje)

    except Exception as e:
        error = f"Error al generar el resumen estadístico:\n{str(e)}"
        messagebox.showerror("Error", error)

#Defino el botón de BUscar la cédula del jurado
def Buscar_Jurados():
    #donde la cedula_buscar es igual a la cédula que entro el Jurado
    cedula_buscar= EntryCedulajurado.get()

    if not cedula_buscar:
      messagebox.showerror("Error","Debe ingresar un número de cédula")

      return
    
    #Hago uso del try para que me detecte el error inmediato
    try:
    #Aqui convierto como número entero la cédula
        cedula_buscar=int(cedula_buscar)
    except ValueError:
        messagebox.showerror("Erro", "La cédula debe ser un número")
        return
 

    #La defino como False antes de empezar el ciclo, ya que no he encontrado nada aún
    encontrado=False
    #Se pone que salon = 1 ya que se debe empezar por un número mayor a 0 en todos los datos
    num_salon = 1
    #realizo un ciclo for para validar uno por uno y verificar la cédula del jurado
    #mesajurados es la lista que contiene la información, pero como contiene todos los datos, debe realizar el ciclo, hasta llegar a jurados

    
    #Se pone que salon = 1 ya que se debe empezar por un número mayor a 0 en todos los datos
    num_salon = 1
    for salon in mesajurados:
        num_mesa = 1
        for mesa in salon:
            for jurado in mesa:
                #Si el dato que esta en Jurado[1] es decir la posición dos en la lista, en este caso es la cédula
                if jurado[1]== cedula_buscar:
                    #Aquí se muestran como información todos los datos del jurado
                    messagebox.showinfo("El Jurado existe",  f"Nombre: {jurado[0]}\nCédula: {jurado[1]}\nTeléfono: {jurado[2]}\nDirección: {jurado[3]}\nMesa: {num_mesa}\nSalón: {num_salon}")
                 
                    #podemos colocar un True para mostrar que se encontro y asi un error si este no ha sido encontrado
                    encontrado= True
                     
                    #Rompemos el ciclo 
                    break

                #Se debe romper cada ciclo del for, para que no recorra los datos de nuevo si ya se encontro la cédula.

            if encontrado:
                break


                 # Solo se aumenta el número del mesa si el jurado no ha sido encontrado
                 # Evitando  mostrar una mesa incorrecta si se encontró antes
            num_mesa +=1

        if encontrado:
            break
            
             #Se suma el número de salón si no se ha encontrado al jurado, hasta encontrar el salón con la cédula del jurado. Si se encuentra se hace break
        num_salon +=1
            
    #Si no se encuentra la cédula informamos 
    if not encontrado:
        messagebox.showinfo("No encontrado", "No se encontró ningún Jurado con esa cédula" )


#Aqui lo que hago es probar si el número que se registro es un entero, uso try para que directamente me diga que es un error
def Números_Enteros(*número):
    try:
        #all devuelve True solo si todos los números cumplen la condición, ciclo for  para que verifique las condiciones de los números ingresados
        return all(int(n)>=1 for n in número)     
    #si no cumplen con las condiciones termina en False
    except ValueError:
        return False

def EliminarDatos():
    #esto me elimina los datos que estan en la ventana
    for borrar in frame_principal.winfo_children():
        borrar.destroy()

def CentroVotacion():
    #Elabro entradas a los datos que son estos:
    Salones = EntrySalones.get()
    Mesas = EntryMesas.get()
    Jurados = EntryJurados.get()

 #Aqui corroboro que lo que se ingreso en cada casilla sean enteros, si no lo son muestra un error
    if not Números_Enteros(Salones, Mesas, Jurados):
        messagebox.showerror("Error", "Todos los valores deben ser números enteros positivos.")
        return

 #luego de definir, hacemos uso de esta para eliminar los datos anteriores 
    EliminarDatos()

 #Ingreso valores como enteros
    Salones = int(Salones)
    Mesas = int(Mesas)
    Jurados = int(Jurados)

    # Usamos un bucle que itera el número de veces requerido para los salones
    for n in range(Salones):
        salon_actual = []
        # un bucle para las mesas dentro de cada salón
        for n in range(Mesas):
            # Cada mesa es una lista vacía para los jurados
            salon_actual.append([])  
        mesajurados.append(salon_actual)
 
    #Empiezo con salones donde hago un ciclo while para ir enumerando, uso *100 para que se haga un espaio grande en Salones
    s = 1
    while s <= Salones:
        label_salones = tk.Label(frame_principal,text=f"Salón {s}", font=("Arial", 12, "bold"))
        label_salones.grid(row=s*100, column=0,pady=10)
        
        #Para mesas realizo lo mismo que es un ciclo while y a este le agrego el boton.
        m = 1
        while m <= Mesas:
            # En este boton lo que hará es mostrarme el registro de jurados, lambda es una función que me ayuda a pasar argumentos correctos al botón
            BotonMesa = tk.Button(frame_principal, text=f"Mesa {m}", command=lambda m=m, s=s: mostrar_jurados(m, s))
            BotonMesa.grid(row=s * 100 + m, column=0, padx=10, pady=5)
           

            #con jurados hago el mismo proceso anterior, aqui me mostrara los datos del jurado
            j = 1
            while j <= Jurados:
                jurado_button = tk.Button(frame_principal, text=f"Jurado {j}", width=15, command=lambda j=j, m=m, s=s: jurado_datos(j, m, s))
                jurado_button.grid(row=s * 100 + m, column=j, padx=5, pady=5)
                j += 1
            m += 1
        s += 1


#Defino mostrar jurados para al hacer click en Mesa me muestre todo los datos
def mostrar_jurados(Mesas, Salon):

    #Uso try para que me muestre el error al instante
    try:
        #mesajurados es una lista, por lo tanto al usarla con Salon y Mesas debo restarles 1 para que empiecen en el dato correcto que es 0
        #elaboro la condición if para asegurar que lod datos para acceder a la lista no se salgan del rango, len(mesajurados) es la cantidad de salones registrados.
        #mesajurados[Salon - 1] es la lista de mesas del salón y len(mesajurados[Salon - 1]) indica cuantas mesas hay en el salón
        
        jurados = mesajurados[Salon - 1][Mesas - 1]  if Salon <= len(mesajurados) and Mesas <= len(mesajurados[Salon - 1]) else []


        if not jurados:
            Salidatexto = "No se encuentran jurados registrados en esta mesa.\n"
        else:
             #Si hay jurados, se muestra un mensaje con los datos
            Salidatexto = ""
            #Uso ciclo For para recorrer cada dato de la lista
            for n, jurado in enumerate(jurados):

                #uso los número 0,1,2,3 en la lista para que recorra cada dato que se ingreso en ese mismo orden, empezando por el nombre
                Salidatexto += (f"Jurado {n+1} \n"f"Nombre: {jurado[0]} \nCédula: {jurado[1]} \nTeléfono: {jurado[2]} \nDirección: {jurado[3]}\n\n")

        #pongo esta como una lista vacía
        mesaVotantes=[] 

        #Realizo un ciclo for para ver los datos de la lista "votantes"
        for votante in votantes :
         #la condición if es para ver si coinciden los datos con los que se estan buscando
         if int(votante['salon']) == Salon and int(votante['mesa']) == Mesas:
            #por lo tanto, si coinciden se agregan los datos a la lista mesaVotantes vacía
            mesaVotantes.append(votante)
        
        #Para ralizar el texto que se mostrará
         salida_votantes = ""
         
        #Se verifica si la lista esta vacía para mostrar el texto
        if not mesaVotantes:
            salida_votantes = "No se encuentran Votantes registrados."

        #else ya que significa que si, si hay votantes se realiza lo siguiente
        else:
            #un ciclo for donde i es el número de votante y enumera cada dato que esta en la lista mesaVotantes
            for i, votante in enumerate(mesaVotantes):
                #se suman los datos a la salida, y se va dando el nombre y la cédula que estan en la lista votantes
                salida_votantes += (f"Votante {i+1} \n"f"Nombre: {votante['nombre']} \nCédula: {votante['cedula']} \n\n")
                
        #Aqui muestra el mensaje completo de las casillas
        messagebox.showinfo(
            f"Mesa {Mesas}, Salón {Salon}",f"  Jurados  \n{Salidatexto}\n Votantes   \n{salida_votantes}")

    except IndexError:
        messagebox.showerror("Error", "El Salón o La Mesa, no existen.")


#Aqui es donde defino el botón de Guardar Centro de Votación
def Guardar_Centrode_Votacion():
    
     try:
        #Muestra en la cosa donde estará guardado el archivo directamente
        print("El archivo se guardará en:", os.path.abspath("CentrodeVotacion.csv"))
        #Aquí se crea y se abre el archivo. newline es para que no se usen filas y encoding para los caracteres especiales, 'w' como write
        with open("CentrodeVotacion.csv", "w",newline='', encoding="utf-8") as Archivotaciones:
        
            #Se crea un escritor CSV usando el archivo abierto.
            writer = csv.writer(Archivotaciones)
        
            #Aqui es donde escribe las columnas de los datos
            writer.writerow(["Salón", "Mesa", "Nombre", "Cédula", "Teléfono", "Dirección"])

            #Reazlizo un ciclo for para recorrer la lista de mesajurados que son los salones y las mesas
            for salon in range(len(mesajurados)):
                for mesa in range(len(mesajurados[salon])):
                    #mesajurados contiene una lista de jurados, donde tienen los 4 datos (nombre, cédula, télefono y dirección)
                    for jurado in mesajurados[salon][mesa]:
                        
                        #al Salón se le suma 1 junto con la mesa y a esto el jurado
                        writer.writerow([salon + 1, mesa + 1] + jurado)
                        


        messagebox.showinfo("Guardado", "El Centro de Votación se ha guardado correctamente en CentrodeVotacion.csv")

     #Realiza esto si no se ha podido ejecutar
     except Exception as ex:

        messagebox.showerror("Error", f"No se pudo guardar el centro de votación:\n{ex}")

        
def jurado_datos(numjurado, Mesa, Salon):

 #Aqui creo una nueva ventana en donde se hará el formulario de registro
    windowdatos = tk.Toplevel()
    windowdatos.title(f"Registrar Jurado{numjurado} Mesa {Mesa} y Salón {Salon}")
    windowdatos.geometry("250x200")

 #Nombre
    tk.Label(windowdatos, text="Nombre").grid(row=1, column=1)
    EntryNombre = tk.Entry(windowdatos)
    EntryNombre.grid(row=2, column=1)

 #Cédula
    tk.Label(windowdatos, text="Cédula").grid(row=3, column=1)
    EntryCedula = tk.Entry(windowdatos)
    EntryCedula.grid(row=4, column=1, padx=70)

 #Teléfono
    tk.Label(windowdatos, text="Teléfono").grid(row=5, column=1)
    EntryTel = tk.Entry(windowdatos)
    EntryTel.grid(row=6, column=1)
 
 #Dirección
    tk.Label(windowdatos, text="Dirección").grid(row=7, column=1)
    EntryDire = tk.Entry(windowdatos)
    EntryDire.grid(row=8, column=1)
 
 #En este botón de guardar, uso lambda para la variable guardar datos y todos sus parámetros
    BotonGuardar = tk.Button(windowdatos, text="Guardar",command=lambda: guardar_Datos(EntryNombre, EntryCedula, EntryTel, EntryDire, numjurado, Mesa, Salon))
    BotonGuardar.grid(row=9, column=1, columnspan=2, pady=10)


def guardar_Datos(EntryNombre, EntryCedula, EntryTel, EntryDire, numjurado, Mesa, Salon):

    #Aquí guardo todos los datos que ingresan
    Nombre = EntryNombre.get()
    Direccion = EntryDire.get()
 
 #Uso try para lo mismo, que me informe si hay un error al ingresar datos que no son int
    try:
        Cedula = int(EntryCedula.get())
        Telefono = int(EntryTel.get())
    except ValueError:
        messagebox.showerror("Error", "Cédula y Teléfono deben ser números.")
        return

    if not Nombre or not Cedula or not Telefono or not Direccion:
        messagebox.showerror("Error", "Por favor, complete todos los campos.")
        return
 
 #Debo verificar si la cédula ya existe 
    if Cedula in cedula_jurados:
        messagebox.showerror("Error",f"La cédula {Cedula} ya está registrada")
        #Uso el return para detenr la función y evitar guardar los datos duplicados
        return

 #Aquí agrego un conjunto con .add que permite que se le agreguen los datos al conjunto vacio de cedula_jurados
    cedula_jurados.add(Cedula)

 #Creo una lista de los Datos
    Datos = [Nombre, Cedula, Telefono, Direccion]

 #Creo un ciclo while en donde uso len para contar los datos de la lista "mesajurados"
    while len(mesajurados) < Salon:
        mesajurados.append([])

    while len(mesajurados[Salon - 1]) < Mesa:
        mesajurados[Salon - 1].append([])

    #Aquí es para guardar los datos en la mesa correspondiente

    mesajurados[Salon - 1][Mesa - 1].append(Datos)
    messagebox.showinfo("Guardado", f"Jurado {numjurado} registrado en la Mesa {Mesa} y en el Salón {Salon} ")

# INTERFAZ PRINCIPAL

window = tk.Tk()
window.title("Registro de Votación")
window.geometry("200x300")

#Realizo todos los datos con la filas y las columnas , al finalizar realizo el botón 

tk.Label(window, text="Número de Salones: ").grid(row=0, column=0, padx=10, pady=5)
EntrySalones = tk.Entry(window)
EntrySalones.grid(row=0, column=1, padx=10, pady=5)

tk.Label(window, text="Número de Mesas por Salón: ").grid(row=1, column=0, padx=10, pady=5)
EntryMesas = tk.Entry(window)
EntryMesas.grid(row=1, column=1, padx=10, pady=5)

tk.Label(window, text="Número de Jurados por Mesa: ").grid(row=2, column=0, padx=10, pady=5)
EntryJurados = tk.Entry(window)
EntryJurados.grid(row=2, column=1, padx=10, pady=5)

#------------------------------------------------------------------------------------------------

#BUSCAR JURADO POR CEDULA

tk.Label(window, text="Buscar Jurado por Cédula: ").grid(row=12, column=0, padx=10, pady=5)
EntryCedulajurado = tk.Entry(window)
EntryCedulajurado.grid(row=12, column=1, padx=10, pady=5)

tk.Button(window,text="Buscar", command=Buscar_Jurados).grid(row=12,column=2, pady=5)

#BUSCAR VOTANTE POR CÉDULA

tk.Label(window, text="Buscar Votante por Cédula: ").grid(row=13, column=0, padx=10, pady=5)
EntryVotante = tk.Entry(window)
EntryVotante.grid(row=13, column=1, padx=10, pady=5)

tk.Button(window, text="Buscar", command=Buscar_votante).grid(row=13, column=2, pady=5)


#BOTÓN GUARDAR CENTRO DE VOTACIÓN 

tk.Button(window,text="Guardar Centro de Votación", command=Guardar_Centrode_Votacion).grid(row=4, column=1, pady=10)


#BOTÓN CARGAR CENTRO DE VOTACIÓN

tk.Button(window,text="Cargar Centro de Votación", command="").grid(row=6,column=1, pady=5)

#BOTÓN CARGAR VOTANTES

tk.Button(window, text="Cargar Votantes", command=Cargar_Votantes).grid(row=8, column=1, pady=5)

#BOTÓN PARA LA ASISTENCIA

tk.Button(window, text="Asistencia Votantes", command=votantes_asistencia).grid(row=9, column=1, pady=5)

#BOTÓN PARA CARGAR RESULTADOS CSV

tk.Button(window, text="Cargar resultados csv", command=Cargar_Resultados).grid(row=10, column=1, pady=5)

#BOTÓN PARA EL RESUMEN ESTADÍSTICO

tk.Button(window, text="Resumen Estadístico", command=lambda: resumen_estadistico(mesajurados, votantes, Asistencia_Vo, resultados)).grid(row=11, column=1, pady=5)

#----------------------------------------------------------------------------------------------------

#Botón Centro de votación

tk.Button(window, text="Generar Centro de Votación", command=CentroVotacion).grid(row=3, column=1, pady=10)

#padx es para el espacio  horizontal y pady para el vertical
#Aqui es donde hago el Frame para el diseño de Salones y los otros datos
frame_principal = tk.Frame(window)
frame_principal.grid(row=14, column=0, columnspan=2,padx=10, pady=10)

window.mainloop()
