"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________

ufosFile = 'UFOS/UFOS-utf8-small.csv'
cont = None
# ___________________________________________________
#  Menu principal
# ___________________________________________________

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información en el catálogo")
    print("3- Consultar los avistamientos de una ciudad")
    print("4- Consultar los avistamientos por duración")
    print("5- Consultar los avistamientos por hora/minutos del dia")
    print("6- Consultar los avistamientos en un rango de fechas")
    print("7- Consultar los avistamientos de una zona geográfica")
"""     print("0- Salir")
    print("*******************************************")

""" """
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    
    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()
   
    elif int(inputs[0]) == 2:
        print("\nCargando información de los avistamientos ....")
        controller.loadData(cont, ufosFile)
        print('Avistamientos cargados: ' + str(controller.ufosSize(cont)))

    elif int(inputs[0]) == 3:
        city = input("Ingrese la ciudad de búsqueda de avistamientos: ")
        numUfos = controller.getUfosByCiudad(cont, city)
        print("\nTotal de avistamientos en: " + city + " son:  " +
              str(numUfos))

    elif int(inputs[0]) == 4:
        duracion, total_ufos= controller.getTotalUfos(cont)
        print("El total de avistamientos registrados con duración máxima " + str(duracion) +\
            " fue " + str(total_ufos))
        lim_inf = input("Ingrese el limite inferior: ")
        lim_sup = input("Ingrese el limite superior: ")
        avistamientos_rango = controller.getAvistamientosRango(cont, lim_inf, lim_sup)
        print("-----------------------Primeros 3 avistamientos encontrados: ")
        for x in range(3):
            elemento= lt.getElement(avistamientos_rango, x)
            print("\nDia y hora: " + elemento["datetime"])
            print("\nCiudad: " + elemento["city"])
            print("\nPaís: " + elemento["country"])
            print("\nDuración (segundos): " + elemento["duration (seconds)"])
            print("\nForma del objeto: " + elemento["shape"])
            print("-----------------------")
            #print(lt.getElement(avistamientos_rango,x))
        longitud= lt.size(avistamientos_rango)
        print("-----------------------Últimos 3 avistamientos encontrados: ")
        for x in range(longitud-2,longitud+1):
            elemento= lt.getElement(avistamientos_rango, x)
            print("\nDia y hora: " + elemento["datetime"])
            print("\nCiudad: " + elemento["city"])
            print("\nPaís: " + elemento["country"])
            print("\nDuración (segundos): " + elemento["duration (seconds)"])
            print("\nForma del objeto: " + elemento["shape"])
            print("-----------------------")
            #print(lt.getElement(avistamientos_rango,x))

    elif int(inputs[0]) == 5:
        print("Ingrese el rango de horas: ")
        hora1 = int(input("Hora inicial: "))
        minuto1 = int(input("Minuto inicial: "))
        hora2 = int(input("Hora final: "))
        minuto2 = int(input("Minuto final: "))
        result = controller.Req3(cont,hora1,minuto1,hora2,minuto2)

        print("El avistamiento más tardío que se tiene registrado es:")
        print('')
        print(result[0]," : ",result[1])
        print('')
        print("En el rango de horas ingresado por el usuario hay un total de ",result[2]," avistamientos. ")
        print('')
        print('Primeros tres avistamientos: ')   

        for avistamiento in lt.iterator(result[3]):
            print('')
            print("Fecha: ",avistamiento["datetime"])
            print("Ciudad: ",avistamiento["city"])
            print("País: ",avistamiento["country"])
            print("Forma: ",avistamiento["shape"])
            print("Duración (segundos): ",avistamiento["duration (seconds)"],"\n")
            print('')
        print('Últimos tres avistamientos:')     
        print('')
        for avistamiento in lt.iterator(result[4]):
            print('')
            print("Fecha: ",avistamiento["datetime"])
            print("Ciudad: ",avistamiento["city"])
            print("País: ",avistamiento["country"])
            print("Forma: ",avistamiento["shape"])
            print("Duración (segundos): ",avistamiento["duration (seconds)"],"\n")
            print('')


    elif int(inputs[0]) == 6:
        print("Ingrese: ")
        dia1 = int(input("Día inicial del rango: "))
        mes1 = int(input("Mes inicial del rango: "))
        anio1 = int(input("Año inicial del rango: "))
        dia2 = int(input("Día final del rango: "))
        mes2 = int(input("Mes final del rango: "))
        anio2 = int(input("Año final del rango: "))
        result = controller.Req4(cont,dia1,mes1,anio1,dia2,mes2,anio2)

        print("El avistamiento más antiguo que se tiene registrado es: ")
        print(result[0]," : ",result[1])
        print('')
        print("En el rango de fechas ingresado por el usuario hay un total de ",result[2]," avistamientos. ")
        print('')
        print('Primeros tres avistamientos: ')     
        for avistamiento in lt.iterator(result[3]):
            print('')
            print("Fecha: ",avistamiento["datetime"])
            print("Ciudad: ",avistamiento["city"])
            print("País: ",avistamiento["country"])
            print("Forma: ",avistamiento["shape"])
            print("Duración (segundos): ",avistamiento["duration (seconds)"])
            print('')
        print('Últimos tres avistamientos: ')     
        for avistamiento in lt.iterator(result[4]):
            print('')
            print("Fecha: ",avistamiento["datetime"])
            print("Ciudad: ",avistamiento["city"])
            print("País: ",avistamiento["country"])
            print("Forma: ",avistamiento["shape"])
            print("Duración (segundos): ",avistamiento["duration (seconds)"])
            print('')

    elif int(inputs[0]) == 7:
        print("Ingrese: ")
        longInicial = round(float(input("Longitud mínima del rango: ")), 2)
        longFinal = round(float(input("Longitud máxima del rango: ")), 2)
        latInicial = round(float(input("Latitud mínima del rango: ")), 2)
        latFinal = round(float(input("Latitud máxima del rango: ")), 2)
        result = controller.Req5(cont,longInicial,latInicial,longFinal,latFinal)

        print("El total de avistamientos dentro del área definida es: ",result[0])
        print('')
        print('Primeros cinco avistamientos: ')
        print('')
        for avistamiento in range(1,6):
            print('')
            print("Fecha: ",lt.getElement(result[1], avistamiento)["datetime"])
            print("Ciudad: ",lt.getElement(result[1], avistamiento)["city"])
            print("País: ",lt.getElement(result[1], avistamiento)["country"])
            print("Forma: ",lt.getElement(result[1], avistamiento)["shape"])
            print("Duración (segundos): ",lt.getElement(result[1], avistamiento)["duration (seconds)"])
            print("Longitud: ",lt.getElement(result[1], avistamiento)["longitude"])
            print("Latitud: ",lt.getElement(result[1], avistamiento)["latitude"])
            print('')
        print('Últimos cinco avistamientos: ')     
        for avistamiento in range(0,5):
            print('')
            print("Fecha: ",lt.getElement(result[1], result[0] - avistamiento)["datetime"])
            print("Ciudad: ",lt.getElement(result[1], result[0] - avistamiento)["city"])
            print("País: ",lt.getElement(result[1], result[0] - avistamiento)["country"])
            print("Forma: ",lt.getElement(result[1], result[0] - avistamiento)["shape"])
            print("Duración (segundos): ",lt.getElement(result[1], result[0] - avistamiento)["duration (seconds)"])
            print("Longitud: ",lt.getElement(result[1], result[0] - avistamiento)["longitude"])
            print("Latitud: ",lt.getElement(result[1], result[0] - avistamiento)["latitude"])
            print('')
    else:
        sys.exit(0)
    
sys.exit(0)

