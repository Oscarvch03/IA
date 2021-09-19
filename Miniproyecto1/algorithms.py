# Algoritmos de Busqueda para Espacio de Estados

import numpy as np
import copy as cp

class Nodo:
    # Clase para crear los nodos
    def __init__(self, estado, madre, accion, costo_camino, codigo):
        self.estado = estado
        self.madre = madre
        self.accion = accion
        self.costo_camino = costo_camino
        self.codigo = codigo
        
def nodo_hijo(problema, madre, accion):
    # Función para crear un nuevo nodo
    # Input: problema, que es un objeto de clase ocho_reinas
    #        madre, que es un nodo,
    #        accion, que es una acción que da lugar al estado del nuevo nodo
    # Output: nodo
    estado = problema.transicion(madre.estado, accion)
    costo_camino = madre.costo_camino + problema.costo(madre.estado, accion)
    codigo = problema.codigo(estado)
    return Nodo(estado, madre, accion, costo_camino, codigo)

#######################################################################################

# Algoritmo 1
def depth_first_search(prob):
    nodo = Nodo(prob.estado_inicial, None, None, 0, prob.codigo(prob.estado_inicial))
    if(prob.test_objetivo(nodo.estado)):
        return nodo
    frontera = [nodo] # LIFO
    explorados = [] # FIFO
    while(len(frontera) > 0):
        nodo = frontera.pop()
        explorados.append(nodo.codigo)
        acciones = prob.acciones_aplicables(nodo.estado)
        for accion in acciones:
            hijo = nodo_hijo(prob, nodo, accion)
            if(prob.test_objetivo(hijo.estado)):
                return hijo
            if(hijo.codigo not in explorados):
                frontera.append(hijo)
    return "Falla"

#######################################################################################

# Algoritmo 2
def breadth_first_search(prob):
    nodo = Nodo(prob.estado_inicial, None, None, 0, prob.codigo(prob.estado_inicial))
    if(prob.test_objetivo(nodo.estado)):
        return nodo
    frontera = [nodo] # FIFO
    explorados = [] # FIFO
    while(len(frontera) > 0):
        nodo = frontera.pop(0)
        explorados.append(nodo.codigo)
        acciones = prob.acciones_aplicables(nodo.estado)
        for accion in acciones:
            hijo = nodo_hijo(prob, nodo, accion)
            if(prob.test_objetivo(hijo.estado)):
                return hijo
            if(hijo.codigo not in explorados):
                frontera.append(hijo)
    return "Falla"

#######################################################################################

# Recibe un problema y un nodo, y te devuelve una lista con todos los nodos hijos del nodo entrada (de clase Nodo)
def EXPAND(prob, nodo):
    s = nodo.estado #inicializamos el estado
    nodos = [] #lista vacía donde irán los nodos hijos
    acciones_costo = [[accion, prob.costo(s, accion)] for accion in prob.acciones_aplicables(s)] #lista con acciones y sus costos
    acciones_costo.sort(key=lambda x:x[1]) # se ordenan acciones de menor costo a mayor costo
    for accion, j in acciones_costo: #recorremos las posibles acciones del estado
        hijo = nodo_hijo(prob, nodo, accion) #creamos el nodo hijo
        nodos.append(hijo) #agregamos a la lista
    return nodos

# Función busqueda en profundidad
# Recibe clase problema y Nodo, funciones:  acciones_aplicables, transicion y test_objetivo
# OBS: Modificar el estado inicial en el código antes de ser pasado por está función
# Algoritmo 3
def backtracking_search(problema, nodo):
    if problema.test_objetivo(nodo.estado):
        return nodo
    for hijo in EXPAND(problema, nodo):
        resultado = backtracking_search(problema, hijo)
        if type(resultado) is not str:
            return resultado        
    return "Falla"

#######################################################################################

class ListaPrioritaria():
    
    def __init__(self):
        self.diccionario = {}
        
    def __str__(self):
        cadena = '['
        inicial = True
        for costo in self.diccionario:
            elementos = self.diccionario[costo]
            for elemento in elementos:
                if inicial:
                    cadena += '(' + str(elemento) + ',' + str(costo) + ')'
                    inicial = False
                else:
                    cadena += ', (' + str(elemento) + ',' + str(costo) + ')'

        return cadena + ']'
    
    def push(self, elemento, costo):
        try:
            self.diccionario[costo].append(elemento)
        except:
            self.diccionario[costo] = [elemento]
            
    def pop(self):
        min_costo = np.min(np.array(list(self.diccionario.keys())))
        candidatos = self.diccionario[min_costo]
        elemento = candidatos.pop()
        if len(candidatos) == 0:
            del self.diccionario[min_costo]
        return elemento
    
    def is_empty(self):
        return len(self.diccionario) == 0

def expand(prob, nodo):
    s = nodo.estado
    nodos = [] # LIFO ¿?
    acciones = prob.acciones_aplicables(s)
    for accion in acciones:
        hijo = nodo_hijo(prob, nodo, accion)
        nodos.append(hijo)
    return nodos

# Algoritmo 4
def best_first_search(prob):
    s = prob.estado_inicial
    cod = prob.codigo(s)
    nodo = Nodo(s, None, None, 0, prob.codigo(s))
    frontera = ListaPrioritaria()
    frontera.push(nodo, 0)
    explorados = {cod: 0}
    while(not frontera.is_empty()):
        nodo = frontera.pop()
        if(prob.test_objetivo(nodo.estado)):
            return nodo
        for hijo in expand(prob, nodo):
            s = hijo.estado
            cod = prob.codigo(s)
            c = hijo.costo_camino
            if((cod not in explorados.keys()) or (c < explorados[cod])):
                frontera.push(hijo, c)
                explorados[cod] = c
    return "Falla"