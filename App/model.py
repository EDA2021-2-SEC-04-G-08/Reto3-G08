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
#from DISClib.Algorithms.Trees import traversal as tv
import datetime
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
    analyzer['cityIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    return analyzer


# Funciones para agregar informacion al catalogo

def addAvistamiento(analyzer, avistamiento):
    """
    """
    lt.addLast(analyzer['ufos'], avistamiento)
    updateDateIndex(analyzer['cityIndex'], avistamiento)
    return analyzer


def updateDateIndex(map, avistamiento):
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
        datentry = newDataEntry(avistamiento)
        om.put(map, ufodate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, avistamiento)
    return map


def addDateIndex(datentry, avistamiento):
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


def newDataEntry(crime):
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


def newCityEntry(offensegrp, avistamiento):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ctentry = {'city': None, 'lstcity': None}
    ctentry['city'] = offensegrp
    ctentry['lstcity'] = lt.newList('SINGLELINKED', compareCity)
    return ctentry


# ==============================
# Funciones de consulta
# ==============================


def ufosSize(analyzer):
    """
    Número de avistamientos
    """
    return lt.size(analyzer['ufos'])


def indexHeight(analyzer):
    """
    Altura del arbol
    """
    return om.height(analyzer['cityIndex'])


def indexSize(analyzer):
    """
    Numero de elementos en el indice
    """
    return om.size(analyzer['cityIndex'])


def minKey(analyzer):
    """
    Llave mas pequena
    """
    return om.minKey(analyzer['cityIndex'])


def maxKey(analyzer):
    """
    Llave mas grande
    """
    return om.maxKey(analyzer['cityIndex'])


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

# ==============================
# Requerimiento 1
# ==============================

def getUfosByCiudad(analyzer, city):
    """
    Para una fecha determinada, retorna el numero de crimenes
    de un tipo especifico.
    """
    ufosCity = om.get(analyzer['cityIndex'], city)
    if ufosCity['key'] is not None:
        ufosmap = me.getValue(ufosCity)['cityIndex']
        numUfos = mp.get(ufosmap, ufosCity)
        if numUfos is not None:
            return mp.size(me.getValue(numUfos)['lstcity'])
    return 0

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
    return lista_ordenada


def getListaOrdenada(lista):
    return sa.sort(lista, ordenar_duracion)

def ordenar_duracion(avi1, avi2):
    return (float(avi1["duration (seconds)"]) < float(avi2["duration (seconds)"]))

def getListaAcotada(lista_ordenada, lim_inf, lim_sup):
    print(lim_inf)
    print(lim_sup)
    tamahnoSublista= lt.isPresent(lista_ordenada,float(lim_sup))-lt.isPresent(lista_ordenada, float(lim_inf))
    a= lt.subList(lista_ordenada, lt.isPresent(lista_ordenada, float(lim_inf)), tamahnoSublista)
    return a




# Construccion de modelos

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
