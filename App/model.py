"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Sorting import mergesort as ms
#from DISClib.Algorithms.Trees import traversal as tv
import datetime
import time
assert cf

def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'ufos': None,
                'dateIndex': None
                }

    analyzer['ufos'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    analyzer['cityIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    analyzer['hourIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareHours)
    analyzer['longitudeIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareLongitude)
    return analyzer


# Funciones para agregar informacion al catalogo

def addAvistamiento(analyzer, avistamiento):
    """
    """
    lt.addLast(analyzer['ufos'], avistamiento)
    updateDateIndex(analyzer['dateIndex'], avistamiento)
    updateDateIndex2(analyzer['cityIndex'], avistamiento)
    updateHourIndex(analyzer['hourIndex'], avistamiento)
    updateLongitudeIndex(analyzer['longitudeIndex'], avistamiento)
    return analyzer

def updateHourIndex(map, avistamiento):
    """
    Se toma la hora del avistamiento y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de avistamientos.
    Si no se encuentra creado un nodo para esa hora en el arbol
    se crea uno
    """
    occurredhour = avistamiento['datetime']
    UFOhour = datetime.datetime.strptime(occurredhour, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, UFOhour.time())
    if entry is None:
        datentry = newDataEntry(UFOhour.time())
        om.put(map, UFOhour.time(), datentry)
    else:
        datentry = me.getValue(entry)
    addHourIndex(datentry, avistamiento)
    return map



def updateLongitudeIndex(map, avistamiento):

    longitude = round(float(avistamiento['longitude']),2)
    entry = om.get(map, longitude)
    if entry is None:
        datentry = newLongitudeEntry(longitude)
        om.put(map, longitude, datentry)
    else:
        datentry = me.getValue(entry)
    addLongitudeIndex(datentry, avistamiento)
    return map


def updateLatitudeIndex(map, avistamiento):
    latitude = round(float(avistamiento['latitude']),2)
    entry = om.get(map, latitude)
    if entry is None:
        datentry = newLatitudeEntry(latitude)
        om.put(map, latitude, datentry)
    else:
        datentry = me.getValue(entry)
    addLatitudeIndex(datentry, avistamiento)
    return map


def updateDateIndex2(map, avistamiento):
    """
    Se toma la fecha del avistamiento y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de avistamientos
    y se actualiza el indice de tipos de avistamientos.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de avistamientos
    """
    occurreddate = avistamiento['datetime']
    ufodate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, ufodate.date())
    if entry is None:
        datentry = newDataEntry2(avistamiento)
        om.put(map, ufodate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex2(datentry, avistamiento)
    return map

def updateDateIndex(map, avistamiento):
    """
    Se toma la fecha del avistamiento y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de avistamientos.
    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea uno
    """
    occurreddate = avistamiento['datetime']
    UFOdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, UFOdate.date())
    if entry is None:
        datentry = newDataEntry(UFOdate.date())
        om.put(map, UFOdate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, avistamiento)
    return map


def addHourIndex(datentry, avistamiento):
    lst = datentry['lstUFOS']
    lt.addLast(lst, avistamiento)
    return datentry


def addLongitudeIndex(datentry, avistamiento):
    """
    Actualiza un indice.  Este indice tiene una lista
    de avistamientos y una tabla de hash cuya llave es la longitud y
    el valor es un mapa con la latitud como llave y valor los avistamientos de
    la longitud que se está consultando (dada por el nodo del arbol)
    """
    updateLatitudeIndex(datentry['latitudeIndex'], avistamiento)
    return datentry


def addLatitudeIndex(datentry, avistamiento):
    lst = datentry['lstUFOS']
    lt.addLast(lst, avistamiento)
    return datentry

def addDateIndex(datentry, avistamiento):
    """
    Actualiza un indice.  Este indice tiene una lista
    de avistamientos y una tabla de hash cuya llave es la fecha y
    el valor es una lista con los avistamientos de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstUFOS']
    lt.addLast(lst, avistamiento)
    return datentry

def addDateIndex2(datentry, avistamiento):
    """
    Actualiza un indice de tipo de avistamientos.  Este indice tiene una lista
    de avistamientos y una tabla de hash cuya llave es el tipo de avistamientos y
    el valor es una lista con los avistamientos de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstufos']
    lt.addLast(lst, avistamiento)
    cityIndex = datentry['cityIndex']
    offentry = mp.get(cityIndex, avistamiento['city'])
    if (offentry is None):
        entry = newCityEntry(avistamiento['city'], avistamiento)
        lt.addLast(entry['lstcity'], avistamiento)
        mp.put(cityIndex, avistamiento['city'], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['lstcity'], avistamiento)
    return datentry


def newDataEntry(avistamiento):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'cityIndex': None, 'lstUFOS': None}
    entry['name'] = avistamiento
    entry['cityIndex'] = mp.newMap(numelements=1000,
                                     maptype='PROBING',
                                     comparefunction=compareCity)
    entry['lstUFOS'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def newLongitudeEntry(longitude):
 
    longitudentry = {'longitude': None, 'latitudeIndex': None}
    longitudentry['longitude'] = longitude
    longitudentry['latitudeIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareLatitude)
    return longitudentry



def newLatitudeEntry(latitude):

    latitudentry = {'latitude': None, 'lstUFOS': None}
    latitudentry['latitude'] = latitude
    latitudentry['lstUFOS'] = lt.newList('SINGLE_LINKED', compareDates)
    return latitudentry


def newCityEntry(offensegrp, avistamiento):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ctentry = {'city': None, 'lstcity': None}
    ctentry['city'] = offensegrp
    ctentry['lstcity'] = lt.newList('SINGLELINKED', compareCity)
    return ctentry

def newDataEntry2(crime):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'cityIndex': None, 'lstufos': None}
    entry['cityIndex'] = mp.newMap(numelements=1000,
                                     maptype='PROBING',
                                     comparefunction=compareCity)
    entry['lstufos'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

# ==============================
# Funciones de consulta
# ==============================

def ufosSize(analyzer):
    """
    Número de avistamientos
    """
    return lt.size(analyzer['ufos'])

# ==============================
# Funciones de Comparacion
# ==============================


def compareIds(id1, id2):
    """
    Compara dos ufos
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1


def compareCity(city1, city2):
    """
    Compara dos ciudades
    """
    city = me.getKey(city2)
    if (city1 == city):
        return 0
    elif (city1 > city):
        return 1
    else:
        return -1

def compareHours(hour1, hour2):
    """
    Compara dos horas
    """
    if (hour1 == hour2):
        return 0
    elif (hour1 > hour2):
        return 1
    else:
        return -1

def compareLongitude(lon1, lon2):
    """
    Compara dos longitudes
    """
    if (lon1 == lon2):
        return 0
    elif (lon1 > lon2):
        return 1
    else:
        return -1



def compareLatitude(lat1, lat2):
    """
    Compara dos latitudes
    """
    if (lat1 == lat2):
        return 0
    elif (lat1 > lat2):
        return 1
    else:
        return -1

def cmpUFOByDate(UFO1, UFO2):
    """
    Se obtiene verdadero si el UFO1 ocurre antes del UFO2
    """
    return UFO1["datetime"]<UFO2["datetime"]


def cmpUFOByDateInverso(UFO1, UFO2):
    """
    Se obtiene verdadero si el UFO1 ocurre después del UFO2
    """
    return UFO1["datetime"]>UFO2["datetime"]


# ==============================
# Requerimiento 1
# ==============================

def getUfosByCiudad(analyzer, city):
    """
    Para una fecha determinada, retorna el numero de crimenes
    de un tipo especifico.
    
    ufosCity = om.get(analyzer['cityIndex'], city)
    if ufosCity['key'] is not None:
        ufosmap = me.getValue(ufosCity)['cityIndex']
        numUfos = mp.get(ufosmap, ufosCity)
        if numUfos is not None:
            return mp.size(me.getValue(numUfos)['lstcity'])
    return 0
    """

# ==============================
# Requerimiento 2
# ==============================

"""
def totalUfos(analyzer):
    ufos= om.valueSet(analyzer['cityIndex'])
    ordenado= tv.preorder(analyzer['cityIndex'])
    #for i in lt.iterator(ufos):
    first_key = list(ufos)[0]
    first_val = list(ufos.values())[0]    
    print(first_key)
    print("--------------------")
    print(first_val)
"""
def totalUfos(analyzer):
    mayor_duracion = get_mayor_duracion(analyzer)
    total_mayor_duracion = get_total_duracion(analyzer, mayor_duracion)
    return mayor_duracion, total_mayor_duracion

def lista_avistamientos_city(valueset):
    lista_avistamientos = lt.newList()
    for reg in lt.iterator(valueset):
        values = mp.valueSet(reg['cityIndex'])
        for val in lt.iterator(values):
            for list_av in lt.iterator(val["lstcity"]):
                lt.addLast(lista_avistamientos, list_av)
    return lista_avistamientos

def get_mayor_duracion(analyzer):
    ufos= om.valueSet(analyzer['cityIndex'])
    lista_avistamientos = lista_avistamientos_city(ufos)
    mayor = 0.0
    for avistamiento in lt.iterator(lista_avistamientos):
        if float(avistamiento["duration (seconds)"]) > mayor:
            mayor = float(avistamiento["duration (seconds)"])
    return mayor


def get_total_duracion(analyzer,duracion):
    ufos= om.valueSet(analyzer['cityIndex'])
    lista_avistamientos = lista_avistamientos_city(ufos)
    contador = 0
    for avistamiento in lt.iterator(lista_avistamientos):
        if float(avistamiento["duration (seconds)"]) == duracion:
            contador += 1
    return contador

def getAvistamientosRango(analyzer, lim_inf, lim_sup):
    ufos= om.valueSet(analyzer['cityIndex'])
    lista_avistamientos = lista_avistamientos_city(ufos)
    lista_ordenada = getListaOrdenada(lista_avistamientos)
    lista_acotada = getListaAcotada(lista_ordenada, lim_inf, lim_sup)
    return lista_acotada


def getListaOrdenada(lista):
    return sa.sort(lista, ordenar_duracion)

def ordenar_duracion(avi1, avi2):
    return (float(avi1["duration (seconds)"]) < float(avi2["duration (seconds)"]))

def getListaAcotada(lista_ordenada, lim_inf, lim_sup):
    #print(lim_inf)
    #print(lim_sup)
    index_inferior= 0
    index_superior= 0
    cont_inferior= 0
    cont_superior= 0
    for duracion in lt.iterator(lista_ordenada):
        if float(duracion["duration (seconds)"])>= float(lim_inf):
            index_inferior= cont_inferior+1
            break
        cont_inferior+=1
    for duracion in lt.iterator(lista_ordenada):
        if float(duracion["duration (seconds)"])> float(lim_sup):
            index_superior= cont_superior+1
            break
        cont_superior+=1
    num_pos= index_superior-index_inferior
    lista_filtrada= lt.subList(lista_ordenada, index_inferior, num_pos)
    return lista_filtrada

#===========================================================================================
#                                           Req 3                                           #
#===========================================================================================
def contarAvistamientosHora(analyzer,horaInicial,minutoInicial,horaFinal,minutoFinal):
 
    timeMasTardeKey = om.maxKey(analyzer["hourIndex"])
    timeMasTarde = om.get(analyzer["hourIndex"],timeMasTardeKey)
    cantTimeMasTarde =lt.size(me.getValue(timeMasTarde)["lstUFOS"])
    
    timeInicial = datetime.time(horaInicial,minutoInicial)
    timeFinal = datetime.time(horaFinal,minutoFinal)
    llaveInicial = om.ceiling(analyzer["hourIndex"], timeInicial)
    llaveFinal = om.floor(analyzer["hourIndex"], timeFinal)
    avistamientos = om.values(analyzer["hourIndex"],llaveInicial,llaveFinal)
    
    cantTotalUFOS = 0
    for UFO in lt.iterator(avistamientos):
        lista = UFO['lstUFOS']
        cantTotalUFOS += lt.size(lista)

    primerosUFOS = lt.newList()
    for UFO in lt.iterator(avistamientos):
        lista = UFO['lstUFOS']
        lista = ms.sort(lista,cmpUFOByDate)
        for a in lt.iterator(lista):
            lt.addLast(primerosUFOS, a)
            if lt.size(primerosUFOS) == 3:
                break
        if lt.size(primerosUFOS) == 3:
            break

    i = lt.size(avistamientos)
    completa = False
    ultimosUFOS = lt.newList()
    while lt.size(ultimosUFOS) < 3 and not completa:
        UFO = lt.getElement(avistamientos,i)['lstUFOS']
        if UFO:
            UFO = ms.sort(UFO, cmpUFOByDateInverso)
            for a in lt.iterator(UFO):
                lt.addFirst(ultimosUFOS, a)
                if lt.size(ultimosUFOS) == 3:
                    break
        else:
            completa = True
        i-=1

    return timeMasTardeKey, cantTimeMasTarde, cantTotalUFOS, primerosUFOS, ultimosUFOS




#===========================================================================================
#                                           Req 4                                           #
#===========================================================================================


def contarAvistamientosDia(catalog,diaInicial,mesInicial,anioInicial,diaFinal,mesFinal,anioFinal):

    dateMasTardeKey = om.minKey(catalog["dateIndex"])
    dateMasTarde = om.get(catalog["dateIndex"],dateMasTardeKey)
    cantDateMasTarde =lt.size(me.getValue(dateMasTarde)["lstUFOS"])
    
    dateInicial = datetime.date(anioInicial,mesInicial,diaInicial)
    dateFinal = datetime.date(anioFinal,mesFinal,diaFinal)
    llaveInicial = om.ceiling(catalog["dateIndex"], dateInicial)
    llaveFinal = om.floor(catalog["dateIndex"], dateFinal)
    avistamientos = om.values(catalog["dateIndex"],llaveInicial,llaveFinal)
    
    cantTotalUFOS = 0
    for UFO in lt.iterator(avistamientos):
        lista = UFO['lstUFOS']
        cantTotalUFOS += lt.size(lista)

    primerosUFOS = lt.newList()
    for UFO in lt.iterator(avistamientos):
        lista = UFO['lstUFOS']
        lista = ms.sort(lista,cmpUFOByDate)
        for a in lt.iterator(lista):
            lt.addLast(primerosUFOS, a)
            if lt.size(primerosUFOS) == 3:
                break
        if lt.size(primerosUFOS) == 3:
            break

    i = lt.size(avistamientos)
    completa = False
    ultimosUFOS = lt.newList()
    while lt.size(ultimosUFOS) < 3 and not completa:
        UFO = lt.getElement(avistamientos,i)['lstUFOS']
        if UFO:
            UFO = ms.sort(UFO, cmpUFOByDateInverso)
            for a in lt.iterator(UFO):
                lt.addFirst(ultimosUFOS, a)
                if lt.size(ultimosUFOS) == 3:
                    break
        else:
            completa = True
        i-=1

    return dateMasTardeKey, cantDateMasTarde, cantTotalUFOS, primerosUFOS, ultimosUFOS



#===========================================================================================
#                                           Req 5                                           #
#===========================================================================================

def contarAvistamientosZona(catalog,longInicial,latInicial,longFinal,latFinal):

    avistamientos = lt.newList(datastructure='ARRAY_LIST')
    if longInicial >= longFinal:
        copia1 = longFinal
        longFinal = longInicial
        longInicial = copia1
    llaveInicialLong = om.ceiling(catalog["longitudeIndex"], longInicial)
    llaveFinalLong = om.floor(catalog["longitudeIndex"], longFinal)
    if llaveInicialLong and llaveFinalLong:
        rangoLong = om.values(catalog["longitudeIndex"],llaveInicialLong,llaveFinalLong)
        if lt.size(rangoLong) > 0:
            if latInicial >= latFinal:
                copia2 = latFinal
                latFinal = latInicial
                latInicial = copia2
            for long in lt.iterator(rangoLong):
                llaveInicialLat = om.ceiling(long["latitudeIndex"], latInicial)
                llaveFinalLat = om.floor(long["latitudeIndex"], latFinal)
                if llaveInicialLat and llaveFinalLat:
                    rangoLat = om.values(long["latitudeIndex"],llaveInicialLat,llaveFinalLat)
                    for lat in lt.iterator(rangoLat):
                        for avistamiento in lt.iterator(lat["lstUFOS"]):
                            lt.addLast(avistamientos,avistamiento)
    tamanio = lt.size(avistamientos)
    return tamanio, avistamientos
# Construccion de modelos

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
