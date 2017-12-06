#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

import string
import sys
import os
######################################################################################
##
##  Define varias clases que definen cada uno de los diferentes componentes lexicos
##
##
##
######################################################################################

# Clase generica que define un componente lexico 
class Componente:
  def __init__(self):
    self.cat= str(self.__class__.__name__)

 #este metodo mostrará por pantalla un componente lexico
  def __str__(self):
    s=[]
    for k,v in self.__dict__.items():
      if k!= "cat": s.append("%s: %s" % (k,v))
    if s:
      return "%s (%s)" % (self.cat,", ".join(s))
    else:
      return self.cat
      
#definicion de las clases que representan cada uno de los componentes lexicos
#Algunas tendran camps adicionales para almacenar informacion importante (valor de un numero, etc)

#clases para los simbolos de puntuacion y operadores

class OpAsigna (Componente):
  def __init__(self, v, nl):
    Componente.__init__(self)
    self.valor = "OpAsigna"
    self.linea = nl

class LlaveAp(Componente):
  def __init__(self, v, nl):
    Componente.__init__(self)
    self.valor = "LlaveAp"
    self.linea = nl

class LlaveCi (Componente):
  def __init__(self, v, nl):
    Componente.__init__(self)
    self.valor = "LlaveCi"
    self.linea = nl

class ParentAp(Componente):
  def __init__(self, v, nl):
    Componente.__init__(self)
    self.valor = "ParentAp"
    self.linea = nl

class ParentCi(Componente):
  def __init__(self, v, nl):
    Componente.__init__(self)
    self.valor = "ParentCi"
    self.linea = nl

class CorAp(Componente):
  def __init__(self, v, nl):
    Componente.__init__(self)
    self.valor = "CorAp"
    self.linea = nl

class CorCi(Componente):
  def __init__(self, v, nl):
    Componente.__init__(self)
    self.valor = "CorCi"
    self.linea = nl

class Punto(Componente):
  def __init__(self, v, nl):
    Componente.__init__(self)
    self.valor = "Punto"
    self.linea = nl

class Coma(Componente):
  def __init__(self, v, nl):
    Componente.__init__(self)
    self.valor = "Coma"
    self.linea = nl

class PtoComa(Componente):
  def __init__(self, v, nl):
    Componente.__init__(self)
    self.valor = "PtoComa"
    self.linea = nl

class DosPtos(Componente):
  def __init__(self, v, nl):
    Componente.__init__(self)
    self.valor = "DosPtos"
    self.linea = nl

# Clase que define la categoria OpAdd 
class OpAdd(Componente):
#debe almacenarse de que operador se trata
  def __init__(self, opadd, nl):
    Componente.__init__(self)
    if (opadd == "+"):
      self.valor = "OpSuma"
    else:
      self.valor = "OpResta"
    self.linea = nl

  
# Clase que define la categoria OpMult
#Debe alnmacenarse que operador es
class OpMult(Componente):
  def __init__(self, opmult, nl):
    Componente.__init__(self)
    if (opmult == "*"):
      self.valor = "OpMul"
    else:
      self.valor = "OpDiv"
    self.linea = nl

#clase para representar los numeros.
#Puede dividirse en 2 para representar los enteros y los reales de forma independiente
#Si se opta por una sola categoria debe alamcenarse el tipo de los datos ademas del valor
class Numero (Componente):
  def __init__(self, v,nl):
    Componente.__init__(self)
    self.valor= v
    self.linea=nl



#clase para representar los identificadores.
class Identif (Componente):
  def __init__(self, v,nl):
    Componente.__init__(self)
    self.valor= v
    self.linea=nl

#Clase que reprresenta las palabras reservadas.
#Sera una clase independiente de los identificadores para facilitar el analisis sintactico
class PR(Componente):
  def __init__(self, v,nl):
   Componente.__init__(self)
   self.valor = v
   self.linea=nl

# Clase que define la categoria OpRel
#Debe almacenarse que operador es concretamente
class OpRel (Componente): 
  def __init__(self,oprel,nl):
    Componente.__init__(self)
    if oprel == "<":
      self.valor = "SimMenor"
    elif oprel == "<=":
      self.valor = "SimMenorIgual"
    elif oprel == "<>":
      self.valor = "SimDist"
    elif oprel == ">":
      self.valor = "SimMayor"
    elif oprel == ">=":
      self.valor = "SimMayorIgual"
    elif oprel == "=":
      self.valor = "SimIgual"
    self.linea = nl


