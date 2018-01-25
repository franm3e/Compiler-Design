#!/usr/bin/env python
# coding=utf-8

class TS:

    def __init__(self):
        # Tabla de símbolos
        self.TablaS = {"PROGRAMA", "VAR", "VECTOR", "DE", "ENTERO", "REAL", "BOOLEANO", "PROC", "FUNCION", "INICIO", "FIN", "SI",
                       "ENTONCES", "SINO", "MIENTRAS", "HACER", "LEE", "ESCRIBE", "Y", "O", "NO", "CIERTO", "FALSO"}


    def comprobar(self, identificador):
        for x in self.TablaS:
            if x == identificador:
                return False
        return True


    def insertar(self, identificador):
        self.TablaS.add(identificador)