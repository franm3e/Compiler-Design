#!/usr/bin/env python
# coding=utf-8

import componentes
import errores
import flujo
import sys
import analex
import TS

from sys import argv
from sets import ImmutableSet

class Anasin:

    def __init__(self, lexico, TS):
            self.lexico = lexico
            self.TS = TS
            self.avanza()

    def avanza(self):
        self.componente = self.lexico.Analiza()

    def comprueba(self, cat):
        if self.componente.cat == "Identif":
            if not self.TS.comprobar(self.componente.valor):
                raise errores.ErrorSemantico("Error semántico Comprueba() - Dos identificadores con el nombre %s" % self.componente.valor)
            else:
                self.TS.insertar(self.componente.valor)
        if self.componente.cat == "PR":
            if self.componente.valor == cat:
                self.avanza()
        elif self.componente.cat == cat:
            self.avanza()
        else:
            raise errores.ErrorSintactico("Error sintáctico Comprueba() mientras comprobaba %s" % cat)


    ### MÉTODOS ANALIZA ###

    def analizaPrograma(self):
        try:
            if self.componente.valor == "PROGRAMA":
                # <Programa> -> PROGRAMA id ; <decl_var> <decl_subprg> <instrucciones> .
                self.avanza()
                self.comprueba("Identif")
                self.comprueba("PtoComa")
                self.analizaDecl_var()
                self.analizaDecl_subprg()
                self.analizaInstrucciones()
                self.comprueba("Punto")
            else:
                raise errores.ErrorSintactico("Error sintáctico analizaPrograma()")
        except errores.Error as err:
            sys.stderr.write("%s\n" % err)


    def analizaDecl_var(self):
        try:
            if self.componente.valor == "VAR":
                # <decl_var> -> VAR <lista_id> : <tipo> ; <decl_v>
                self.avanza()
                self.analizaLista_id()
                self.comprueba("DosPtos")
                self.analizaTipo()
                self.comprueba("PtoComa")
                self.analizaDecl_v()
            elif self.componente.valor in ["eof", "PROC", "FUNCION"]: # Siguientes <Decl_var>
                # <decl_var> -> lambda
                pass
            else:
                raise errores.ErrorSintactico("Error sintáctico analizaDecl_var()")
        except errores.Error as err:
            sys.stderr.write("%s\n" % err)


    def analizaDecl_v(self):
        try:
            if self.componente.cat in ["Identif"]: # Primeros de <lista_id>
                # <decl_v> -> <list_id> : <tipo> ; <decl_v>
                self.analizaLista_id()
                self.comprueba("DosPtos")
                self.analizaTipo()
                self.comprueba("PtoComa")
                self.analizaDecl_v()
            elif self.componente.valor in ["eof","PROC", "FUNCION"]: # Siguientes <Decl_v>
                # <decl_v> -> lambda
                pass
            else:
                raise errores.ErrorSintactico("Error sintáctico analizaDecl_v()")
        except errores.Error as err:
            sys.stderr.write("%s\n" % err)


    def analizaLista_id(self):
        try:
            if self.componente.cat == "Identif":
                if not self.TS.comprobar(self.componente.valor):
                    raise errores.ErrorSemantico("Error semántico Comprueba() - Dos identificadores con el nombre %s" % self.componente.valor)
                else:
                    self.TS.insertar(self.componente.valor)
                # <lista_id> -> id <resto_listaid>
                self.avanza()
                self.analizaResto_listaid()
            else:
                raise errores.ErrorSintactico("Error sintáctico analizaLista_id()")
        except errores.Error as err:
            sys.stderr.write("%s\n" % err)


    def analizaResto_listaid(self):
        try:
            if self.componente.cat == "Coma":
                # <resto_listaid> -> , <lista_id>
                self.avanza()
                self.analizaLista_id()
            elif self.componente.cat in ["PtoComa", "DosPtos"]: # Siguientes <lista_id>
                # <resto_listaid> -> lambda
                pass
            else:
                raise errores.ErrorSintactico("Error sintáctico analizaResto_listaid()")
        except errores.Error as err:
            sys.stderr.write("%s\n" % err)


    def analizaTipo(self):
        try:
            if self.componente.valor in ["ENTERO", "REAL", "BOOLEANO"]: # Primeros <tipo_std>
                # <Tipo> -> <tipo_std>
                self.analizaTipo_std()
                self.avanza()
                # self.analizaTipo_std()
            elif self.componente.cat == "VECTOR":
                # <Tipo> -> VECTOR [ num ] de <Tipo>
                self.avanza()
                self.comprueba("LlaveAp")
                self.comprueba("Numero")
                self.comprueba("LlaveCi")
                self.comprueba("DE")
                self.analizaTipo()
            else:
                raise errores.ErrorSintactico("Error sintáctico analizaTipo()")
        except errores.Error as err:
            sys.stderr.write("%s\n" % err)


    def analizaTipo_std(self):
        try:
            if self.componente.valor == "ENTERO":
                # <Tipo_std> -> ENTERO
                pass
            elif self.componente.valor == "VECTOR":
                # <Tipo_std> -> VECTOR
                pass
            elif self.componente.valor == "BOOLEANO":
                # <Tipo_std> -> BOOLEANO
                pass
            else:
                raise errores.ErrorSintactico("Error sintáctico analizaTipo_std()")
        except errores.Error as err:
            sys.stderr.write("%s\n" % err)


    def analizaDecl_subprg(self):
        try:
            if self.componente.valor in ["PROC", "FUNCION"]: # Primeros <decl_sub>
                # <Decl_subprg> -> <decl_sub> ; <decl_subprg>
                self.avanza()
                self.analizaDecl_sub()
                self.comprueba("PtoComa")
                self.analizaDecl_subprg()
            elif self.componente.valor in ["INICIO"]: # Siguientes <Decl_subprg>
                # <Decl_subprg> -> lambda
                self.avanza()

            else:
                raise errores.ErrorSintactico("Error sintáctico analizaDecl_subprg()")
        except errores.Error as err:
            sys.stderr.write("%s\n" % err)


    def analizaDecl_sub(self):
        try:
            if self.componente.valor == "PROC":
                # <Decl_sub> -> PROC id ; <instrucciones>
                self.avanza()
                self.comprueba("Identif")
                self.comprueba("PtoComa")
                self.analizaInstrucciones()
            elif self.componente.cat == "FUNCION":
                # <Decl_sub> -> FUNCION id : <tipo_std> ; <instrucciones>
                self.avanza()
                self.comprueba("Identif")
                self.comprueba("DosPtos")
                self.analizaTipo_std()
                self.comprueba("PtoComa")
                self.analizaInstrucciones()
            else:
                raise errores.ErrorSintactico("Error sintáctico analizaDecl_sub()")
        except errores.Error as err:
            sys.stderr.write("%s\n" % err)


    def analizaInstrucciones(self):
        try:
            if self.componente.valor == "INICIO":
                # <Instrucciones> -> INICIO <lista_inst> FIN
                self.avanza()
                self.analizaLista_inst()
                self.comprueba("FIN")
            else:
                raise errores.ErrorSintactico("Error sintáctico analizaInstrucciones()")
        except errores.Error as err:
            sys.stderr.write("%s\n" % err)


    def analizaLista_inst(self):
        try:
            if self.componente.valor in ["INICIO", "SI", "MIENTRAS"] or self.componente.cat in ["Identif"]: # Primeros <instruccion>
                # <Lista_inst> -> <instruccion> ; <lista_inst>
                self.avanza()
                self.analizaInstruccion()
                self.comprueba("PtoComa")
                self.analizaLista_inst()
            elif self.componente.valor in ["FIN"]:  # Siguientes <Lista_inst>
                # <Lista_inst> -> lambda
                pass
            else:
                raise errores.ErrorSintactico("Error sintáctico analizaLista_inst()")
        except errores.Error as err:
            sys.stderr.write("%s\n" % err)


    def analizaInstruccion(self):
        try:
            if self.componente.valor == "INICIO":
                # <Instruccion> -> INICIO <lista_inst> FIN
                self.avanza()
                self.analizaLista_inst()
                self.comprueba("FIN")
            elif self.componente.cat in ["Identif"]: # Primeros de <Inst_simple>
                # <instruccion> -> <inst_simple>
                self.avanza()
                self.analizaInst_simple()
            elif self.componente.valor in ["LEE", "ESCRIBE"]: # Primeros de <Inst_es>
                # <instruccion> -> <inst_es>
                self.avanza()
                self.analizaInst_es()
            elif self.componente.valor == "SI":
                # <Instruccion> -> SI <expresion> ENTONCES <instruccion> SINO <instruccion>
                self.avanza()
                self.analizaExpresion()
                self.comprueba("ENTONCES")
                self.analizaInstruccion()
                self.comprueba("SINO")
                self.analizaInstruccion()
            elif self.componente.valor == "MIENTRAS":
                # <Instruccion> -> MIENTRAS <expresion> HACER <instruccion>
                self.avanza()
                self.analizaExpresion()
                self.comprueba("HACER")
                self.analizaInstruccion()
            else:
                raise errores.ErrorSintactico("Error sintáctico analizaInstruccion()")
        except errores.Error as err:
            sys.stderr.write("%s\n" % err)


    def analizaInst_simple(self):
        try:
            if self.componente.cat == "Identif":
                if not self.TS.comprobar(self.componente.valor):
                    raise errores.ErrorSemantico(
                        "Error semántico Comprueba() - Dos identificadores con el nombre %s" % self.componente.valor)
                else:
                    self.TS.insertar(self.componente.valor)
                # <Inst_simple> -> id <resto_instsimple>
                self.avanza()
                self.analizaResto_instsimple()
                self.comprueba("FIN")
            else:
                raise errores.ErrorSintactico("Error sintáctico analizaInst_simple()")
        except errores.Error as err:
            sys.stderr.write("%s\n" % err)


    def analizaResto_instsimple(self):
        try:
            if self.componente.cat == "OpAsigna":
                # <Resto_instsimple> -> opasigna <expresion>
                self.avanza()
                self.analizaExpresion()
            elif self.componente.cat == "CorAp":
                # <Resto_instsimple> -> [ <expr_simple> ] opasigna <expresion>
                self.avanza()
                self.analizaExpr_simple()
                self.comprueba("CorCi")
                self.comprueba("OpAsigna")
                self.analizaExpresion()
            elif self.componente.valor in ["SINO"] or self.componente.cat in ["PtoComa"]: # Siguientes de <Resto_instsimple>
                # <Resto_instsimple> -> lambda
                pass
            else:
                raise errores.ErrorSintactico("Error sintáctico analizaResto_instsimple()")
        except errores.Error as err:
            sys.stderr.write("%s\n" % err)


    def analizaVariable(self):
        try:
            if self.componente.cat == "Identif":
                # <Variable> -> id <Resto_var>
                self.avanza()
                self.analizaResto_var()
            else:
                raise errores.ErrorSintactico("Error sintáctico analizaVariable()")
        except errores.Error as err:
            sys.stderr.write("%s\n" % err)


    def analizaResto_var(self):
        try:
            if self.componente.cat == "CorAp":
                # <Resto_var> -> [ <expr_simple> ]
                self.avanza()
                self.analizaExpr_simple()
                self.comprueba("CorCi")
            elif self.componente.valor in ["ENTONCES", "SINO", "HACER", "Y", "O",] or self.componente.cat in ["OpMult", "CorAp", "OpAdd", "OpRel", "ParentAp" ]: # Siguientes de <Resto_var>
                # <Resto_var> -> lambda
                pass
            else:
                raise errores.ErrorSintactico("Error sintáctico analizaResto_var()")
        except errores.Error as err:
            sys.stderr.write("%s\n" % err)


    def analizaInst_es(self):
        try:
            if self.componente.valor == "LEE":
                # <Inst_es> -> LEE ( id )
                self.avanza()
                self.comprueba("ParentAp")
                self.comprueba("Identif")
                self.comprueba("ParentCi")
            elif self.componente.valor == "ESCRIBE":
                # <Inst_es> -> ESCRIBE ( <expr_simple> )
                self.comprueba("ParentAp")
                self.analizaExpr_simple()
                self.comprueba("ParentCi")
            else:
                raise errores.ErrorSintactico("Error sintáctico analizaInst_es()")
        except errores.Error as err:
            sys.stderr.write("%s\n" % err)


    def analizaExpresion(self):
        try:
            if self.componente.valor in ["NO", "CIERTO", "FALSO"] or self.componente.cat in ["OpAdd", "Identif", "Numero", "ParentAp"]: #Primeros de <expr_simple>
                # <Expresion> -> <expr_simple> oprel <expr_simple>
                self.avanza()
                self.analizaExpr_simple()
                self.comprueba("OpRel")
                self.analizaExpr_simple()
            elif self.componente.valor in ["NO", "CIERTO", "FALSO"] or self.componente.cat in ["OpAdd", "Identif", "Numero", "ParentAp"]: # Primeros de <expr_simple>
                # <Expresion> -> <expr_simple>
                self.avanza()
                self.analizaExpr_simple()
            else:
                raise errores.ErrorSintactico("Error sintáctico analizaExpresion()")
        except errores.Error as err:
            sys.stderr.write("%s\n" % err)


    def analizaExpr_simple(self):
        try:
            if self.componente.valor in ["NO", "CIERTO", "FALSO"] or self.componente.cat in ["Numero", "Identif", "ParentAp"]: #Primeros de <Termino>
                # <Expr_simple> -> <Termino> <Resto_Exsimple>
                self.avanza()
                self.analizaTermino()
                self.analizaResto_exsimple()
            elif self.componente.valor in ["+", "-"] : # Primeros de <Signo>
                # <Expr_simple> -> <Signo> <Termino> <Resto_Exsimple>
                self.avanza()
                self.analizaSigno()
                self.analizaTermino()
                self.analizaResto_exsimple()
            else:
                raise errores.ErrorSintactico("Error sintáctico analizaExpr_simple()")
        except errores.Error as err:
            sys.stderr.write("%s\n" % err)


    def analizaResto_exsimple(self):
        try:
            if self.componente.cat == "OpAdd":
                # <Resto_exsimple> -> opsuma <Termino> <Resto_Exsimple>
                self.avanza()
                self.analizaTermino()
                self.analizaResto_exsimple()
            elif self.componente.valor in ["O"]:
                # <Resto_exsimple> -> O <Termino> <Resto_Exsimple>
                self.avanza()
                self.analizaTermino()
                self.analizaResto_exsimple()
                self.analizaResto_exsimple()
            elif self.componente.valor in ["HACER", "ENTONCES", "SINO"] or self.componente.cat in ["ParentAp", "CorCi", "OpRel", "PtoComa"]: # Siguientes de <Resto_exsimple>
                # <Resto_exsimple> -> lambda
                pass
            else:
                raise errores.ErrorSintactico("Error sintáctico analizaResto_exsimple()")
        except errores.Error as err:
            sys.stderr.write("%s\n" % err)


    def analizaTermino(self):
        try:
            if self.componente.valor in ["NO", "CIERTO", "FALSO"] or self.componente.cat in ["Numero", "Identif", "ParentAp"]: #Primeros de <Factor>
                # <Termino> -> <Factor> <Resto_term>
                self.avanza()
                self.analizaFactor()
                self.analizaResto_term()
            else:
                raise errores.ErrorSintactico("Error sintáctico analizaTermino()")
        except errores.Error as err:
            sys.stderr.write("%s\n" % err)


    def analizaResto_term(self):
        try:
            if self.componente.cat == "OpMult":
                # <Resto_term> -> opmult <Factor> <Resto_term>
                self.avanza()
                self.analizaFactor()
                self.analizaResto_term()
            elif self.componente.valor == "Y":
                # <Resto_term> -> Y <Factor> <Resto_term>
                self.avanza()
                self.analizaFactor()
                self.analizaResto_term()
            elif self.componente.valor in ["HACER", "ENTONCES", "SINO", "O"] or self.componente.cat in ["OpAdd", "ParentCi", "CorCi", "OpRel"]: # Siguientes de <Resto_term>
                # <Resto_term> -> lambda
                pass
            else:
                raise errores.ErrorSintactico("Error sintáctico analizaResto_term()")
        except errores.Error as err:
            sys.stderr.write("%s\n" % err)


    def analizaFactor(self):
        try:
            if self.componente.cat in ["Identif"]: # Primeros de <Variable>
                # <Factor> -> <variable>
                self.avanza()
                self.analizaVariable()
            elif self.componente.cat == "Numero":
                # <Factor> -> num
                self.avanza()
            elif self.componente.cat == "ParentAp":
                # <Factor> -> ( <Expresion> )
                self.avanza()
                self.analizaExpresion()
                self.comprueba("ParentCi")
            elif self.componente.valor == "NO":
                # <Factor> -> NO <Factor>
                self.avanza()
                self.analizaFactor()
            elif self.componente.valor == "CIERTO":
                # <Factor> -> CIERTO
                self.avanza()
            elif self.componente.valor == "FALSO":
                # <Factor> -> FALSO
                self.avanza()
            else:
                raise errores.ErrorSintactico("Error sintáctico analizaFactor()")
        except errores.Error as err:
            sys.stderr.write("%s\n" % err)

    def analizaSigno(self):
        try:
            if self.componente.cat == "OpAdd":
                # <Signo> -> +
                pass
            elif self.componente.cat == "OpAdd":
                # <Signo> -> -
                pass
            else:
                raise errores.ErrorSintactico("Error sintáctico analizaTermino()")
        except errores.Error as err:
            sys.stderr.write("%s\n" % err)



    def sincroniza(self, sinc):
        sinc |= "eof"  # Nos aseguramos de que este eof
        while self.componente.cat not in sinc:
            self.avanza()

if __name__ == "__main__":
    script, filename = argv
    txt = open(filename)
    print("Este es tu fichero %r" % filename)
    i = 0
    TS = TS.TS()
    fl = flujo.Flujo(txt)
    analexi = analex.Analex(fl)
    anasint = Anasin(analexi, TS)
    try:
        arbolPrograma = anasint.analizaPrograma()
        anasint.comprueba("eof")
    except errores.Error as err:
        sys.stderr.write("%s\n" % err)