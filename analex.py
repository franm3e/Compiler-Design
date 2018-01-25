#!/usr/bin/env python
# coding=utf-8

import componentes
import errores
import flujo
import string
import sys

from sys import argv
from sets import ImmutableSet

class Analex:
    #############################################################################
    ##  Conjunto de palabras reservadas para comprobar si un identificador es PR
    #############################################################################
    PR = ImmutableSet(
        ["PROGRAMA", "VAR", "VECTOR", "DE", "ENTERO", "REAL", "BOOLEANO", "PROC", "FUNCION", "INICIO", "FIN", "SI",
         "ENTONCES", "SINO", "MIENTRAS", "HACER", "LEE", "ESCRIBE", "Y", "O", "NO", "CIERTO", "FALSO"])

    listaNumeros = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    ############################################################################
    #
    #  Funcion: __init__
    #  Tarea:  Constructor de la clase
    #  Prametros:  flujo:  flujo de caracteres de entrada
    #  Devuelve: --
    #
    ############################################################################
    def __init__(self, flujo):
        # Debe completarse con  los campos de la clase que se consideren necesarios
        self.flujo = flujo
        self.nlinea = 0  # contador de lineas para identificar errores

    ############################################################################
    #
    #  Funcion: Analiza
    #  Tarea:  Identifica los diferentes componentes lexicos
    #  Prametros:  --
    #  Devuelve: Devuelve un componente lexico
    #
    ############################################################################
    def Analiza(self):

        ch = self.flujo.siguiente()

        ## ESPACIO BLANCO ##
        if ch == " ":
            # quitar todos los caracteres blancos

            # buscar el siguiente componente lexico que sera devuelto

            ### IMPORTANTE ###
            # Hacer un bucle que mientras tengamos caracteres en blanco, pase al siguiente
            # Una vez nos encontremos con un caracter "no en blanco" llamar otra vez a ANALIZA

            return self.Analiza()

        ## OPERADORES ARITMETICOS ##
        elif ch == "+":
            return componentes.OpAdd(ch, self.nlinea)

        elif ch == "-":
            return componentes.OpAdd(ch, self.nlinea)

        elif ch == "*":
            return componentes.OpMult(ch, self.nlinea)

        elif ch == "/":
            return componentes.OpMult(ch, self.nlinea)


        ## OPERADOR RELACIONALES ##

        elif ch == "<":
            ch = self.flujo.siguiente()
            if ch == "=":
                return componentes.OpRel("<=", self.nlinea)
            elif ch == ">":
                return componentes.OpRel("<>", self.nlinea)
            else:
                self.flujo.devuelve(ch)
                return componentes.OpRel("<", self.nlinea)

        elif ch == ">":
            ch = self.flujo.siguiente()
            if ch == "=":
                return componentes.OpRel(">=", self.nlinea)
            else:
                self.flujo.devuelve(ch)
                return componentes.OpRel(">", self.nlinea)

        elif ch == "=":
            return componentes.OpRel(ch, self.nlinea)


        ## COMENTARIOS ##
        elif ch == "{":
            # Saltar todos los caracteres del comentario y encontrar el siguiente componente lexico
            while ch != "}":
                ch = self.flujo.siguiente()
            ch = self.flujo.siguiente()

        elif ch == "}":
            return errores.ErrorLexico("Comentario no abierto")  # tenemos un comentario no abierto

        ## ASIGNACION ##
        elif ch == ":":
            # Comprobar con el siguiente caracter si es una definicion de la declaracion o el operador de asignacion
            ch = self.flujo.siguiente()
            if ch == "=":
                return componentes.OpAsigna(self.nlinea)
            else:
                self.flujo.devuelve(ch)
                return componentes.DosPtos(self.nlinea)


        ## OPERADORES Y CATEGORIAS LEXICAS QUE FALTAN ##
        # Completar los operadores y categorias lexicas que faltan
        elif ch == "(":
            return componentes.ParentAp(self.nlinea)

        elif ch == ")":
            return componentes.ParentCi(self.nlinea)

        elif ch == "[":
            return componentes.CorAp(self.nlinea)

        elif ch == "]":
            return componentes.CorCi(self.nlinea)

        elif ch == ";":
            return componentes.PtoComa(self.nlinea)

        elif ch == ",":
            return componentes.Coma(self.nlinea)


        ## CARACTERES ##
        elif ch.lower() in list(string.ascii_lowercase):
            ident = []
            while (ch.lower() in list(string.ascii_lowercase)) or (ch in self.listaNumeros):
                ident.append(ch)
                ch = self.flujo.siguiente();
            self.flujo.devuelve(ch)

            ## PALABRAS CLAVE ##
            for x in self.PR:
                if x == ''.join(ident):
                    return componentes.PR(x, self.nlinea)
            return componentes.Identif(''.join(ident),self.nlinea)


        ## NUMEROS ##
        elif any(ch == x for x in self.listaNumeros):
            hayPunto = False
            numero = []
            numero.append(ch)
            ch = self.flujo.siguiente()
            lista = []
            while (ch in self.listaNumeros or ch == "."):
                if ch in self.listaNumeros:
                    numero.append(ch)
                    ch = self.flujo.siguiente()
                else:
                    if not hayPunto:
                        numero.append(ch)
                        hayPunto = True
                        ch = self.flujo.siguiente()
                    else:
                        self.flujo.devuelve(ch)
                        return componentes.Numero(''.join(numero),self.nlinea)
            self.flujo.devuelve(ch)
            if hayPunto:
                return componentes.Numero(''.join(numero),"real", self.nlinea)
            else:
                return componentes.Numero(''.join(numero),"entero", self.nlinea)



        # Leer todos los elementos que forman el numero
        # devolver el ultimo caracter que ya no pertenece al numero a la entrada
        # Devolver un objeto de la categoria correspondiente


        ## TABULACION ##
        elif ch == "\t":
            # devolver el siguiente componente encontrado
            return self.Analiza()

        ## SALTO DE LINEA ##
        elif ch == "\n":
            # incrementa el numero de linea ya que acabamos de saltar a otra
            self.nlinea += 1
            # devolver el siguiente componente encontrado
            return self.Analiza()

        elif ch == ".":
            return componentes.Punto(self.nlinea)

        elif True:
            return errores.ErrorLexico("Caracter no permitido.")

############################################################################
#
#  Funcion: __main__
#  Tarea:  Programa principal de prueba del analizador lexico
#  Prametros:  --
#  Devuelve: --
#
############################################################################
if __name__ == "__main__":
    script, filename = argv
    txt = open(filename)
    print("Este es tu fichero %r" % filename)
    i = 0
    fl = flujo.Flujo(txt)
    analex = Analex(fl)
    try:
        c = analex.Analiza()
        while c:
            print(c)
            c = analex.Analiza()
        i = i + 1
    except errores.Error as err:
        sys.stderr.write("%s\n" % err)
        analex.muestraError(sys.stderr)