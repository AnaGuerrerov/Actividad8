
#ACTIVIDAD 8, ANA SOFÍA GUERRERO
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import csv
import os

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

    tk.Label(Ventana, text="Cédula").grid(row=0, column=1)
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

tk.Label(window, text="Buscar Jurado por Cédula: ").grid(row=10, column=0, padx=10, pady=5)
EntryCedulajurado = tk.Entry(window)
EntryCedulajurado.grid(row=10, column=1, padx=10, pady=5)

tk.Button(window,text="Buscar", command=Buscar_Jurados).grid(row=10,column=2, pady=5)

#BUSCAR VOTANTE POR CÉDULA

tk.Label(window, text="Buscar Votante por Cédula: ").grid(row=11, column=0, padx=10, pady=5)
EntryVotante = tk.Entry(window)
EntryVotante.grid(row=11, column=1, padx=10, pady=5)

tk.Button(window, text="Buscar", command=Buscar_votante).grid(row=11, column=2, pady=5)


#BOTÓN GUARDAR CENTRO DE VOTACIÓN 

tk.Button(window,text="Guardar Centro de Votación", command=Guardar_Centrode_Votacion).grid(row=4, column=1, pady=10)


#BOTÓN CARGAR CENTRO DE VOTACIÓN

tk.Button(window,text="Cargar Centro de Votación", command="").grid(row=6,column=1, pady=5)

#BOTÓN CARGAR VOTANTES

tk.Button(window, text="Cargar Votantes", command=Cargar_Votantes).grid(row=8, column=1, pady=5)

#BOTÓN PARA LA ASISTENCIA

tk.Button(window, text="Asistencia Votantes", command=votantes_asistencia).grid(row=9, column=1, pady=5)

#----------------------------------------------------------------------------------------------------

#Botón Centro de votación

tk.Button(window, text="Generar Centro de Votación", command=CentroVotacion).grid(row=3, column=1, pady=10)

#padx es para el espacio  horizontal y pady para el vertical
#Aqui es donde hago el Frame para el diseño de Salones y los otros datos
frame_principal = tk.Frame(window)
frame_principal.grid(row=12, column=0, columnspan=2,padx=10, pady=10)

window.mainloop()
