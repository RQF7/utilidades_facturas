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


ANCHO_DE_REPORTE = 80
LLAVES = [{'denominacionPropia': 'fecha',
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


def imprimirItem(contenido, vinieta = '*', ancho = ANCHO_DE_REPORTE):

    contenido = str(contenido)
    anchoReal = ancho - len(vinieta) - 1
    numeroDeLineas = (len(contenido) // anchoReal) + 1
    if len(contenido) % anchoReal == 0:
        numeroDeLineas -= 1

    print(vinieta + ' ', end='')
    for i in range(numeroDeLineas):
        if i != 0:
            print(' ' * (len(vinieta) + 1), end='')
        if i == numeroDeLineas - 1:
            print(contenido[i * anchoReal:], ' ' * (len(vinieta) + 1), sep='')
        else:
            print(contenido[i * anchoReal : (i + 1) * anchoReal])


def imprimirTitulo(titulo):
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


def imprimirDatos(datos):
    for i in datos:
        imprimirItem(datos[i])
    print('')

def procesarXml(nombreDeArchivo, llaves=LLAVES):
    """Regresa un diccionario con la información relevante del archivo dado."""

    imprimirItem('Procesando ' + nombreDeArchivo, vinieta='=>')
    print('')
    resultado = {}
    raiz = ET.parse(nombreDeArchivo).getroot()
    for llave in llaves:
        resultado[llave['denominacionPropia']] = \
            buscarElemento(raiz, llave['caminoXML'])
    imprimirDatos(resultado)
    return resultado


def buscarElemento(raiz, camino):
    if len(camino) == 1:
        return raiz.attrib[camino[0]]
    else:
        return buscarElemento(raiz.find(
            '{http://www.sat.gob.mx/cfd/3}' + camino[0]), camino[1:])



if __name__ == '__main__':

    carpetaDeFacturas = './'
    if len(sys.argv) > 1:
        carpetaDeFacturas = sys.argv[1]

    imprimirTitulo('Procesamiento')
    datos = []
    subtotal = impuestos = total = 0
    for archivo in os.listdir(carpetaDeFacturas):
        if archivo[-3:] == 'xml':
            datos.append(procesarXml(os.path.join(carpetaDeFacturas, archivo)))
            subtotal += float(datos[-1]['subtotal'])
            impuestos += float(datos[-1]['impuestos'])
            total += float(datos[-1]['total'])

    imprimirTitulo('Resultados')
    imprimirDatos(
            {'subtotal': subtotal, 'impuestos': impuestos, 'total': total})
