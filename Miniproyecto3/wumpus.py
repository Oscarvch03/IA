import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
import numpy as np
from random import choice, sample
from logica import ASK

def truncar(x):
    if x < 0:
        return 0
    elif x > 3:
        return 3
    else:
        return x

def adyacentes(casilla):
    x, y = casilla
    adyacentes = [
        (truncar(x - 1), y), (truncar(x + 1), y),
        (x, truncar(y - 1)), (x, truncar(y + 1))
    ]
    adyacentes = [c for c in adyacentes if c != casilla]
    return adyacentes

class Wumpus:

    def __init__(self, wumpus=None, oro=None, pozos=None):
        casillas = [(x, y) for x in range(4) for y in range(4)]
        casillas_sin_inicial = [casilla for casilla in casillas if casilla != (0,0)]
        if wumpus is None:
            self.wumpus = choice(casillas_sin_inicial)
        else:
            self.wumpus = wumpus
        self.wumpus_vivo = True
        self.hedor = adyacentes(self.wumpus)
        if oro is None:
            self.oro = choice(casillas)
        else:
            self.oro = oro
        self.oro_tomado = False
        if pozos is None:
            self.pozos = sample(casillas_sin_inicial, int(len(casillas_sin_inicial)*0.2))
        else:
            self.pozos = pozos
        aux = []
        for c in self.pozos:
            aux += adyacentes(c)
        self.brisa = aux
        self.heroe = (0, 0)
        self.flecha = True
        self.direccion = 'este'
        self.puntaje = 0
        self.juego_activo = True
        self.grito = False # para determinar cuándo el wumpus grita de agonía
        self.bump = False # para determinar cuándo el agente golpea un muro
        self.mensaje = ''

    def pintar_todo(self):
        # Dibuja el tablero correspondiente al estado
        fig, axes = plt.subplots(figsize=(8, 8))

        # Dibujo el tablero
        step = 1./4
        offset = 0.001
        tangulos = []

        # Borde del tablero
        tangulos.append(patches.Rectangle((0,0),0.998,0.998,\
                                          facecolor='cornsilk',\
                                         edgecolor='black',\
                                         linewidth=2))

        # Creo las líneas del tablero
        for j in range(4):
            locacion = j * step
            # Crea linea horizontal en el rectangulo
            tangulos.append(patches.Rectangle(*[(0, locacion), 1, 0.008],\
                    facecolor='black'))
            # Crea linea vertical en el rectangulo
            tangulos.append(patches.Rectangle(*[(locacion, 0), 0.008, 1],\
                    facecolor='black'))

        for t in tangulos:
            axes.add_patch(t)

        # Cargando imagen del heroe
        arr_img_hero = plt.imread("./imagenes/hero_" + self.direccion + ".png", format='png')
        image_hero = OffsetImage(arr_img_hero, zoom=0.3)
        image_hero.image.axes = axes

        # Cargando imagen del Wumpus
        arr_img_wumpus = plt.imread("./imagenes/wumpus.png", format='png')
        image_wumpus = OffsetImage(arr_img_wumpus, zoom=0.45)
        image_wumpus.image.axes = axes

        # Cargando imagen del hedor
        arr_img_stench = plt.imread("./imagenes/stench.png", format='png')
        image_stench = OffsetImage(arr_img_stench, zoom=0.35)
        image_stench.image.axes = axes

        # Cargando imagen del oro
        arr_img_gold = plt.imread("./imagenes/gold.png", format='png')
        image_gold = OffsetImage(arr_img_gold, zoom=0.25)
        image_gold.image.axes = axes

        # Cargando imagen del pozo
        arr_img_pit = plt.imread("./imagenes/pit.png", format='png')
        image_pit = OffsetImage(arr_img_pit, zoom=0.35)
        image_pit.image.axes = axes

        # Cargando imagen de la brisa
        arr_img_breeze = plt.imread("./imagenes/breeze.png", format='png')
        image_breeze = OffsetImage(arr_img_breeze, zoom=0.35)
        image_breeze.image.axes = axes

        offsetX = 0.125
        offsetY = 0.125

        for casilla in self.pozos:
            # Pintando un pozo
            X, Y = casilla
            ab = AnnotationBbox(
                image_pit,
                [(X*step) + offsetX, (Y*step) + offsetY],
                frameon=False)
            axes.add_artist(ab)

        if self.wumpus_vivo:
            for casilla in self.hedor:
                # Pintando el hedor
                X, Y = casilla
                ab = AnnotationBbox(
                    image_stench,
                    [(X*step) + offsetX, (Y*step) + offsetY - 0.075],
                    frameon=False)
                axes.add_artist(ab)

        for casilla in self.brisa:
            # Pintando la brisa
            X, Y = casilla
            ab = AnnotationBbox(
                image_breeze,
                [(X*step) + offsetX, (Y*step) + offsetY + 0.075],
                frameon=False)
            axes.add_artist(ab)

        # Pintando el wumpus
        if self.wumpus_vivo:
            X, Y = self.wumpus
            ab = AnnotationBbox(
                image_wumpus,
                [(X*step) + offsetX, (Y*step) + offsetY],
                frameon=False)
            axes.add_artist(ab)

        # Pintando el heroe
        X, Y = self.heroe
        ab = AnnotationBbox(
            image_hero,
            [(X*step) + offsetX, (Y*step) + offsetY],
            frameon=False)
        axes.add_artist(ab)

        # Pintando el oro
        if not self.oro_tomado:
            X, Y = self.oro
            ab = AnnotationBbox(
                image_gold,
                [(X*step) + offsetX, (Y*step) + offsetY],
                frameon=False)
            axes.add_artist(ab)

        axes.axis('off')
        return axes

    def pintar_casilla(self):
        if self.juego_activo:
            # Dibuja el tablero correspondiente al estado
            fig, axes = plt.subplots(figsize=(8, 8))

            # Dibujo el tablero
            step = 1./4
            offset = 0.001
            tangulos = []

            # Borde del tablero
            tangulos.append(patches.Rectangle((0,0),0.998,0.998,\
                                              facecolor='cornsilk',\
                                             edgecolor='black',\
                                             linewidth=2))

            # Creo las líneas del tablero
            for j in range(4):
                locacion = j * step
                # Crea linea horizontal en el rectangulo
                tangulos.append(patches.Rectangle(*[(0, locacion), 1, 0.008],\
                        facecolor='black'))
                # Crea linea vertical en el rectangulo
                tangulos.append(patches.Rectangle(*[(locacion, 0), 0.008, 1],\
                        facecolor='black'))

            for t in tangulos:
                axes.add_patch(t)

            # Cargando imagen del heroe
            arr_img_hero = plt.imread("./imagenes/hero_" + self.direccion + ".png", format='png')
            image_hero = OffsetImage(arr_img_hero, zoom=0.3)
            image_hero.image.axes = axes

            # Cargando imagen del Wumpus
            arr_img_wumpus = plt.imread("./imagenes/wumpus.png", format='png')
            image_wumpus = OffsetImage(arr_img_wumpus, zoom=0.45)
            image_wumpus.image.axes = axes

            # Cargando imagen del hedor
            arr_img_stench = plt.imread("./imagenes/stench.png", format='png')
            image_stench = OffsetImage(arr_img_stench, zoom=0.35)
            image_stench.image.axes = axes

            # Cargando imagen del oro
            arr_img_gold = plt.imread("./imagenes/gold.png", format='png')
            image_gold = OffsetImage(arr_img_gold, zoom=0.25)
            image_gold.image.axes = axes

            # Cargando imagen del pozo
            arr_img_pit = plt.imread("./imagenes/pit.png", format='png')
            image_pit = OffsetImage(arr_img_pit, zoom=0.35)
            image_pit.image.axes = axes

            # Cargando imagen de la brisa
            arr_img_breeze = plt.imread("./imagenes/breeze.png", format='png')
            image_breeze = OffsetImage(arr_img_breeze, zoom=0.35)
            image_breeze.image.axes = axes

            offsetX = 0.125
            offsetY = 0.125

            casilla = self.heroe

            if casilla in self.pozos:
                # Pintando un pozo
                X, Y = casilla
                ab = AnnotationBbox(
                    image_pit,
                    [(X*step) + offsetX, (Y*step) + offsetY],
                    frameon=False)
                axes.add_artist(ab)

            if casilla in self.hedor:
                # Pintando el hedor
                X, Y = casilla
                ab = AnnotationBbox(
                    image_stench,
                    [(X*step) + offsetX, (Y*step) + offsetY - 0.075],
                    frameon=False)
                axes.add_artist(ab)

            if casilla in self.brisa:
                # Pintando la brisa
                X, Y = casilla
                ab = AnnotationBbox(
                    image_breeze,
                    [(X*step) + offsetX, (Y*step) + offsetY + 0.075],
                    frameon=False)
                axes.add_artist(ab)

            if casilla == self.wumpus:
                # Pintando el wumpus
                X, Y = self.wumpus
                ab = AnnotationBbox(
                    image_wumpus,
                    [(X*step) + offsetX, (Y*step) + offsetY],
                    frameon=False)
                axes.add_artist(ab)

            # Pintando el heroe
            X, Y = casilla
            ab = AnnotationBbox(
                image_hero,
                [(X*step) + offsetX, (Y*step) + offsetY],
                frameon=False)
            axes.add_artist(ab)

            if casilla == self.oro:
                # Pintando el oro
                if not self.oro_tomado:
                    X, Y = self.oro
                    ab = AnnotationBbox(
                        image_gold,
                        [(X*step) + offsetX, (Y*step) + offsetY],
                        frameon=False)
                    axes.add_artist(ab)

            axes.axis('off')
            return axes
        else:
            return None

    def transicion(self, accion):
        if self.juego_activo:
            self.grito = False
            self.bump = False
            self.puntaje -= 1
            if accion == 'agarrar':
                if (self.oro == self.heroe) and (self.oro_tomado == False):
                    self.puntaje += 1000
                    self.oro_tomado = True
            elif accion == 'adelante':
                x, y = self.heroe
                if self.direccion == 'este':
                    self.heroe = (truncar(x + 1), y)
                    self.bump = True if truncar(x + 1) == x else False
                if self.direccion == 'oeste':
                    self.heroe = (truncar(x - 1), y)
                    self.bump = True if truncar(x - 1) == x else False
                if self.direccion == 'norte':
                    self.heroe = (x, truncar(y + 1))
                    self.bump = True if truncar(y + 1) == y else False
                if self.direccion == 'sur':
                    self.heroe = (x, truncar(y - 1))
                    self.bump = True if truncar(y - 1) == y else False
            elif accion == 'salir':
                if self.heroe == (0, 0):
                    self.juego_activo = False
                    print("¡Juego terminado!")
                    print("Puntaje:", self.puntaje)
                    self.mensaje = "Juego terminado!\n Puntaje: " + str(self.puntaje)
                    self.pintar_todo()
            elif accion == 'voltearIzquierda':
                if self.direccion == 'este':
                    self.direccion = 'norte'
                elif self.direccion == 'oeste':
                    self.direccion = 'sur'
                elif self.direccion == 'norte':
                    self.direccion = 'oeste'
                elif self.direccion == 'sur':
                    self.direccion = 'este'
            elif accion == 'voltearDerecha':
                if self.direccion == 'este':
                    self.direccion = 'sur'
                elif self.direccion == 'oeste':
                    self.direccion = 'norte'
                elif self.direccion == 'norte':
                    self.direccion = 'este'
                elif self.direccion == 'sur':
                    self.direccion = 'oeste'
            elif accion == 'disparar':
                if self.flecha:
                    self.flecha = False
                    if self.wumpus_vivo:
                        x_wumpus, y_wumpus = self.wumpus
                        x_heroe, y_heroe = self.heroe
                        if (self.direccion == 'este') and ((x_heroe < x_wumpus) and (y_heroe == y_wumpus)):
                            self.wumpus_vivo = False
                            self.grito = True
                        if (self.direccion == 'oeste') and ((x_heroe > x_wumpus) and (y_heroe == y_wumpus)):
                            self.wumpus_vivo = False
                            self.grito = True
                        if (self.direccion == 'norte') and ((y_heroe < y_wumpus) and (x_heroe == x_wumpus)):
                            self.wumpus_vivo = False
                            self.grito = True
                        if (self.direccion == 'sur') and ((y_heroe > y_wumpus) and (x_heroe == x_wumpus)):
                            self.wumpus_vivo = False
                            self.grito = True
            else:
                print('¡Acción incorrecta!', accion)
            if self.heroe in self.pozos:
                self.puntaje -= 1000
                self.juego_activo = False
                self.mensaje = "¡Juego terminado!\n" + "El héroe a caido en un pozo\n" + "Puntaje: " + str(self.puntaje)
                print("¡Juego terminado!")
                print("El héroe a caido en un pozo")
                print("Puntaje:", self.puntaje)
                self.pintar_todo()
            elif (self.heroe == self.wumpus) and self.wumpus_vivo:
                self.puntaje -= 1000
                self.juego_activo = False
                self.mensaje = "¡Juego terminado!\n" + "El héroe ha sido devorado por el Wumpus\n" + "Puntaje: " + str(self.puntaje)
                print("¡Juego terminado!")
                print("El héroe ha sido devorado por el Wumpus")
                print("Puntaje:", self.puntaje)
                self.pintar_todo()
        else:
            print("El juego ha terminado.")

class Agente:

    def __init__(self, mundo, base_conocimiento = None, descriptor = None):
        self.mundo = mundo
        self.base_conocimiento = base_conocimiento
        self.cods = descriptor

    def percibir(self):
        # Lista de sensores [hedor, brisa, brillo, batacazo, grito]
        hedor = 'hedor' if ((self.mundo.heroe in self.mundo.hedor) and self.mundo.wumpus_vivo) else None
        brisa = 'brisa' if self.mundo.heroe in self.mundo.brisa else None
        brillo = 'brillo' if ((self.mundo.heroe == self.mundo.oro) and not self.mundo.oro_tomado) else None
        batacazo = 'batacazo' if self.mundo.bump else None
        grito = 'grito' if self.mundo.grito else None
        return [hedor, brisa, brillo, batacazo, grito]

def voltear(direccion_inicial, direccion_final):
    acciones = []
    if direccion_inicial == direccion_final:
        return acciones
    else:
        if direccion_final == 'este':
            if direccion_inicial == 'norte':
                acciones.append('voltearDerecha')
            elif direccion_inicial == 'sur':
                acciones.append('voltearIzquierda')
            elif direccion_inicial == 'oeste':
                acciones.append('voltearDerecha')
                acciones.append('voltearDerecha')
        elif direccion_final == 'norte':
            if direccion_inicial == 'este':
                acciones.append('voltearIzquierda')
            elif direccion_inicial == 'sur':
                acciones.append('voltearIzquierda')
                acciones.append('voltearIzquierda')
            elif direccion_inicial == 'oeste':
                acciones.append('voltearDerecha')
        elif direccion_final == 'oeste':
            if direccion_inicial == 'este':
                acciones.append('voltearIzquierda')
                acciones.append('voltearIzquierda')
            elif direccion_inicial == 'sur':
                acciones.append('voltearDerecha')
            elif direccion_inicial == 'norte':
                acciones.append('voltearIzquierda')
        elif direccion_final == 'sur':
            if direccion_inicial == 'este':
                acciones.append('voltearDerecha')
            elif direccion_inicial == 'norte':
                acciones.append('voltearDerecha')
                acciones.append('voltearDerecha')
            elif direccion_inicial == 'oeste':
                acciones.append('voltearIzquierda')
    return acciones

def acciones_camino(camino, direccion):
    acciones = []
    for i in range(len(camino) - 1):
        x1, y1 = camino[i]
        x2, y2 = camino[i + 1]
        diferencia_x = x2 - x1
        diferencia_y = y2 - y1
        if (diferencia_x != 0) and (diferencia_y != 0):
            print("Camino incorrecto!: No debe incluir diagonales.")
            return None
        elif diferencia_x > 0:
            acciones += voltear(direccion, 'este')
            direccion = 'este'
        elif diferencia_x < 0:
            acciones += voltear(direccion, 'oeste')
            direccion = 'oeste'
        elif diferencia_y > 0:
            acciones += voltear(direccion, 'norte')
            direccion = 'norte'
        elif diferencia_y < 0:
            acciones += voltear(direccion, 'sur')
            direccion = 'sur'
        acciones.append('adelante')
    return acciones

class Rejilla:

    # Problema del tránsito por la rejilla
    # desde donde está el héroe hasta una
    # casilla objetivo

    def __init__(self, actual, objetivo, seguras):
        self.estado_inicial = actual
        self.estado_objetivo = objetivo
        self.casillas_seguras = seguras

    def acciones_aplicables(self, estado):
        return [casilla for casilla in adyacentes(estado) if casilla in self.casillas_seguras]

    def transicion(self, estado, accion):
        return accion

    def test_objetivo(self, estado):
        return estado == self.estado_objetivo

    def costo(self, estado, accion):
        x1, y1 = estado
        x2, y2 = self.transicion(estado, accion)
        return abs(x1 - x2) + abs(y1 - y2)

    def codigo(self, estado):
        x, y = estado
        return f"{x}-{y}"
