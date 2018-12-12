#!/bin/python

"""
Script para generar reportes de facturas.

Copyright (C) 2018 Ricardo Quezada

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys

import xml.etree.ElementTree as ET


LLAVES = [
        {'denominacionPropia': 'fecha',
         'caminoXML': [
                'Fecha']},
        {'denominacionPropia': 'emisor',
         'caminoXML': [
                'Emisor',
                'Nombre']},
        {'denominacionPropia': 'receptor',
         'caminoXML': [
                'Receptor',
                'Nombre']},
        {'denominacionPropia': 'subtotal',
         'caminoXML': [
                'SubTotal']},
        {'denominacionPropia': 'impuestos',
         'caminoXML': [
                'Impuestos',
                'TotalImpuestosTrasladados']},
        {'denominacionPropia': 'total',
         'caminoXML': [
                'Total']}]


def imprimir_item(contenido, vinieta='*', ancho=80):
    """Imprime el contenido dado como ítem de lista.

    Argumentos:
    contenido -- cadena a imprimir.

    Argumentos en llaves:
    vinieta -- cadena a usar como viñeta (por defecto '*').
    ancho   -- ancho máximo de línea (por defecto 80).
    """
    contenido = str(contenido)
    ancho_real = ancho - len(vinieta) - 1
    numero_de_lineas = (len(contenido) // ancho_real) + 1
    if len(contenido) % ancho_real == 0:
        numero_de_lineas -= 1

    print(vinieta + ' ', end='')
    for i in range(numero_de_lineas):
        if i != 0:
            print(' ' * (len(vinieta) + 1), end='')
        if i == numero_de_lineas - 1:
            print(contenido[i * ancho_real:], ' ' * (len(vinieta) + 1), sep='')
        else:
            print(contenido[i * ancho_real:(i + 1) * ancho_real])


def imprimir_titulo(titulo):
    """Imprime en la salida estándar el título dado."""
    mitad = (80 - len(titulo) + 2) // 2
    par = 1
    if (len(titulo) % 2 == 0):
        par = 2
    print('=' * 80)
    print(' ' * mitad, end='')
    print(' ', titulo, ' ' * par, end='', sep='')
    print(' ' * mitad)
    print('=' * 80)
    print('')


def imprimir_datos(datos):
    """Imprime el diccionario dado como una lista."""
    for i in datos:
        imprimir_item(datos[i])
    print('')


def procesar_xml(nombre_de_archivo, llaves=LLAVES):
    """Regresa un diccionario con la información relevante del archivo dado.

    Cada llave tiene dos elementos: la denominación propia (el nombre que
    tendrá el campo en el diccionario resultado) y el camino en el
    XML del SAT (ver buscar_elemento).

    Argumentos:
    nombre_de_archivo -- ruta al xml fuente.

    Argumentos en llaves:
    llaves -- Arreglo de diccionarios con la información a buscar.
    """
    imprimir_item('Procesando ' + nombre_de_archivo, vinieta='=>')
    print('')
    resultado = {}
    raiz = ET.parse(nombre_de_archivo).getroot()
    for llave in llaves:
        resultado[llave['denominacionPropia']] = \
            buscar_elemento(raiz, llave['caminoXML'])
    imprimir_datos(resultado)
    return resultado


def buscar_elemento(raiz, camino):
    """Busca el elemento dado en la raíz xml dada.

    Función recursiva. El caso base es cuando solamente hay un elemento
    el el arreglo camino; en este caso se regresa el atributo con el
    nombre dado en la raíz dada. En caso contrario, busca la etiqueta
    del primer elemento del camino en la raíz dada.
    """
    if len(camino) == 1:
        return raiz.attrib[camino[0]]
    else:
        return buscar_elemento(raiz.find(
            '{http://www.sat.gob.mx/cfd/3}' + camino[0]), camino[1:])


if __name__ == '__main__':

    carpetaDeFacturas = './'
    if len(sys.argv) > 1:
        carpetaDeFacturas = sys.argv[1]

    imprimir_titulo('Procesamiento')
    datos = []
    subtotal = impuestos = total = 0
    for archivo in os.listdir(carpetaDeFacturas):
        if archivo[-3:] == 'xml':
            datos.append(procesar_xml(
                os.path.join(carpetaDeFacturas, archivo)))
            subtotal += float(datos[-1]['subtotal'])
            impuestos += float(datos[-1]['impuestos'])
            total += float(datos[-1]['total'])

    imprimir_titulo('Resultados')
    imprimir_datos(
            {'subtotal': subtotal, 'impuestos': impuestos, 'total': total})
