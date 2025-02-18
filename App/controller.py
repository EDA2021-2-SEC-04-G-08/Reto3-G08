﻿"""
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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData(analyzer, ufosFile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    ufosFile = cf.data_dir + ufosFile
    input_file = csv.DictReader(open(ufosFile, encoding="utf-8"),
                                delimiter=",")
                                
    for avistamiento in input_file:
        model.addAvistamiento(analyzer, avistamiento)

    return analyzer


# Funciones de ordenamiento

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def fechas(analyzer):
    pass

def ufosSize(analyzer):
    """
    Numero de crimenes leidos
    """
    return model.ufosSize(analyzer)


def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer)


def indexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer)



def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)


def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)


def getUfosByCiudad(analyzer, city):
    """
    Retorna el total de crimenes de un tipo especifico en una
    fecha determinada
    """
    return model.lista_avistamientosC(analyzer, city)

def getTotalUfos(analyzer):
    return model.totalUfos(analyzer)

def getAvistamientosRango(analyzer, lim_inf, lim_sup):
    return model.getAvistamientosRango(analyzer, lim_inf, lim_sup)

def Req3(catalog,horaInicial,minutoInicial,horaFinal,minutoFinal):
    """
    Cuenta los avistamientos en un rango de horas
    """
    result = model.contarAvistamientosHora(catalog,horaInicial,minutoInicial,horaFinal,minutoFinal)
    return result

def Req4(catalog,diaInicial,mesInicial,anioInicial,diaFinal,mesFinal,anioFinal):
    """
    Cuenta los avistamientos en un rango de fechas
    """
    result = model.contarAvistamientosDia(catalog,diaInicial,mesInicial,anioInicial,diaFinal,mesFinal,anioFinal)
    return result

def Req5(catalog,longInicial,latInicial,longFinal,latFinal):
    """
    Cuenta los avistamientos en un rango de longitudes y latitudes
    """
    result = model.contarAvistamientosZona(catalog,longInicial,latInicial,longFinal,latFinal)
    return result