import sys
import pygame
import time
import random
from pygame.locals import *

pygame.init()
ANCHO = 600
ALTO = 600
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)


#-------------------------------------------------------------------------------------------
#Funciones

	#Funcion para trasladar un punto 
def Traslacion((x,y), (tx,ty)):
	x=x+tx
	y=y-ty
	return (x,y)

def InicioJuego(Pantalla, reloj):
	Cargando = 0
	time = 1
	font = pygame.font.Font(None, 80)
	while(Cargando < 100):
		Pantalla.fill(NEGRO)
		texto = font.render("Cargando " + str(Cargando) + "%", True, BLANCO)
		Cargando += time
		time += random.randrange(2)
		Pantalla.blit(texto, (ANCHO/2-150 , ALTO/2))
		reloj.tick(10) 
		pygame.display.flip()

	#Funcion para mostrar el fin del juego 
def FinJuego(Pantalla, jugador, reloj):
	Pantalla.fill(NEGRO)
	font = pygame.font.Font(None, 100)
	font2 = pygame.font.Font(None, 50)
	font.set_bold(True)
	if jugador.vida == 0:
		texto = font.render("Game Over.", True, BLANCO)
	else:
		texto = font.render("You Win.", True, BLANCO)
	texto2 = font2.render("Puntaje = " + str(jugador.puntos), True, VERDE)
	Pantalla.blit(texto, (100, ALTO/2))
	Pantalla.blit(texto2, (ANCHO/2, 2*ALTO/3))
	pygame.display.flip()
	reloj.tick(1)

	#Funcion para limpiar los grupos al pasar de nivel
def ClearNivel(ls_Enemigos, ls_Todos, ls_Balas, ls_eBalas, ls_Explosiones, ls_Pildora):
	ls_Enemigos.empty()
	ls_Pildora.empty()
	ls_Todos.empty()
	ls_Balas.empty()
	ls_eBalas.empty()
	ls_Explosiones.empty()

	#Fucion que inicializar  los niveles, me define cuantos enemigos del nivel
def InitNivel(jugador, ls_Enemigos, ls_Todos, Pantalla, reloj, Fondo):
	font = pygame.font.Font(None, 100)
	InicioJuego(Pantalla, reloj)
	if jugador.nivel == 1:
		texto = font.render("Nivel 1", True, BLANCO)
		Cant = random.randrange(5,7)
		for i in range(Cant):
			e = Enemigo1()
			ls_Enemigos.add(e)
			ls_Todos.add(e)
	else:
		texto = font.render("Nivel 2", True, BLANCO)
		Cant1 = random.randrange(5, 8)
		for i in range(Cant1):
			e = Enemigo1()
			ls_Enemigos.add(e)
			ls_Todos.add(e)		
		Cant2 = random.randrange(3, 5)
		for i in range(Cant2):
			e2 = Enemigo2()
			ls_Enemigos.add(e2)
			ls_Todos.add(e2)
		Cant = Cant1 + Cant2	
	Pantalla.blit(Fondo, (0,0))
	Pantalla.blit(texto, (100, ALTO/2))
	pygame.display.flip()		
	reloj.tick(1)
	return Cant

	# Punto Medio para la posicion de la bala del enemigo 2
def PmBalaEnemigo(bala):
	xy = []
	if bala.direccion == 1:
		m = 4
	else:
		m = -4
	y = bala.rect.y
	x = bala.rect.x
	b = y - m* x
	if bala.direccion != 0:
		while y < 8000:
			if bala.direccion == 1:
				d1 = (x + 1, y)
				d2 = (x + 1, y + 1)
				pm = y + 1/2
				if y > pm:
					xy.append(d1)
				else:
					xy.append(d2)
				x += 1
				y = int(round(m*x + b))
			else:
				d1 = (x - 1, y)
				d2 = (x - 1, y + 1)
				pm = y + 1/2
				if y > pm:
					xy.append(d1)
				else:
					xy.append(d2)
				x -= 1
				y = int(round(m*x + b))
	return xy

	#Funcion usando el punto medio de la circunferencia para darle la posicion al enemigo 2
def PmCircunfPosEnemigo(enemigo):
	centro = (enemigo.rect.x, enemigo.rect.y)
	puntos = []
	p1 = []
	p2 = []
	p3 = []
	p4 = []
	p5 = []
	p6 = []
	p7 = []
	p8 = []
	x = 0
	y = 50
	d = 5/4 - y
	xy = Traslacion(centro, (x ,y))
	p1.append(xy)
	xy = Traslacion(centro, (x, -y))
	p2.append(xy)
	xy = Traslacion(centro, (-x, y))
	p3.append(xy)
	xy = Traslacion(centro, (-x, -y))
	p4.append(xy)
	xy = Traslacion(centro, (y, x))
	p5.append(xy)
	xy = Traslacion(centro, (y, -x))
	p6.append(xy)
	xy = Traslacion(centro, (-y, x))
	p7.append(xy)
	xy = Traslacion(centro, (-y, -x))
	p8.append(xy)
	while x < y:	
		x += 1
		if d < 0:
			d = d + 2*x + 1
		else:
			d = d + 2*(x - y) + 1
			y -= 1		
		xy = Traslacion(centro, (x ,y))
		p1.append(xy)
		xy = Traslacion(centro, (x, -y))
		p2.append(xy)
		xy = Traslacion(centro, (-x, y))
		p3.append(xy)
		xy = Traslacion(centro, (-x, -y))
		p4.append(xy)
		xy = Traslacion(centro, (y, x))
		p5.append(xy)
		xy = Traslacion(centro, (y, -x))
		p6.append(xy)
		xy = Traslacion(centro, (-y, x))
		p7.append(xy)
		xy = Traslacion(centro, (-y, -x))
		p8.append(xy)
	p5.reverse()
	p2.reverse()
	p8.reverse()
	p3.reverse()
	puntos = p1 + p5 + p6 + p2 + p4 + p8 + p7 + p3
	return puntos


#----------------------------------------------------------------------------------------------------
#Clases

	#Jugador
class Jugador(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("Jugador/Recto.png")
		self.rect = self.image.get_rect()
		self.rect.x = ANCHO/2
		self.rect.y = ALTO-100
		self.vida = 3
		self.direccion = 0
		self.move = 5
		self.puntos = 0
		self.win = False
		self.nivel = 1
		self.avanzar = ["Jugador/Recto.png", "Jugador/Derecha.png", "Jugador/Izquierda.png"]

	def update(self, der, izq, enemigos):
		if der:
			self.direccion = 1
			self.image = pygame.image.load(self.avanzar[1]).convert_alpha()

		if izq:
			self.direccion = 2
			self.image = pygame.image.load(self.avanzar[2]).convert_alpha()

		if not(der or izq):
			self.direccion = 0
			self.image = pygame.image.load(self.avanzar[0]).convert_alpha()
		
		if enemigos == 0:
			if self.nivel == 2:
				self.win = True
			self.nivel += 1	

	#Bala del Jugador
class BalaJugador(pygame.sprite.Sprite):

	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("Jugador/BalaRecta.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = pos[0]+28
		self.rect.y = pos[1]-50

	def update(self):
		self.rect.y -= 5


	#Pildora para Jugador, recupera una vida 
class Pildora(pygame.sprite.Sprite):
	def __init__(self, Pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("Extra/Pildora.png")
		self.rect = self.image.get_rect()
		self.rect.x = Pos
		self.rect.y = ALTO-100
		self.tiempo = 200

	def update(self):
			self.tiempo -= 1

	#Bala del Enemigo 1
class BalaEnemigo1(pygame.sprite.Sprite):
	def __init__(self, pos,):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("Enemigos/EB1.png")
		self.rect = self.image.get_rect()
		self.rect.x = pos[0]
		self.rect.y = pos[1]

	def update(self):
		self.rect.y += 3
		
	#Bala del Enemigo 2
class BalaEnemigo2(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		self.direccion = random.randrange(0,3)
		self.balas = ["Enemigos/EB2.png", "Enemigos/EB2I.png", "Enemigos/EB2D.png"]
		self.image = pygame.image.load(self.balas[self.direccion]).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = pos[0]
		self.rect.y = pos[1]
		self.posicion = PmBalaEnemigo(self)
		self.contador = 1
	
	def update(self):
		if self.direccion == 0:
			self.rect.y += 3
		else:
			self.rect.x = self.posicion[self.contador][0]
			self.rect.y = self.posicion[self.contador][1]
			self.contador += 1

	#Enemigo 1
class Enemigo1(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("Enemigos/E1.png")
		self.rect = self.image.get_rect()
		self.direccion = random.randrange(0,2)
		self.rect.x = random.randrange(100, ANCHO-50)
		self.rect.y = random.randrange(0, ALTO/3)
		self.recarga = random.randrange(100, 200)
		self.disparar = False
		self.distintivo = 1

	def update(self):
		if self.rect.x <= 0:
			self.direccion = 1
		
		if self.rect.x >= ALTO-100:
			self.direccion = 0

		if self.direccion == 0:
			self.rect.x -= 5
		else:
			self.rect.x += 5

		if self.recarga == 0:
			self.disparar = True
			self.recarga = random.randrange(100)
		else:
			self.recarga -= 1
			self.disparar = False
	
	#Enemigo 2
class Enemigo2(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("Enemigos/E2.png")
		self.rect = self.image.get_rect()
		self.direccion = 0
		self.rect.x = random.randrange(100, ANCHO-150)
		self.rect.y = random.randrange(50, ALTO/3)
		self.recarga = random.randrange(50, 100)
		self.posicion = PmCircunfPosEnemigo(self)
		self.contador = 0
		self.disparar = False
		self.distintivo = 2

	def update(self):
		if self.contador <= len(self.posicion)-1:
			self.rect.x = self.posicion[self.contador][0]
			self.rect.y = self.posicion[self.contador][1]
			self.contador += 3

		else:
			self.contador = 0
		
		if self.recarga == 0:
			self.disparar = True
			self.recarga = random.randrange(100)
		else:
			self.recarga -= 1
			self.disparar = False

	#Explosion
class Explosion(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("Explosion/e1.png")
		self.rect = self.image.get_rect()
		self.rect.x = pos[0]
		self.rect.y = pos[1]
		self.contador = 0
		self.avanzar = ["Explosion/e1.png", "Explosion/e1.png",
						"Explosion/e2.png", "Explosion/e2.png", "Explosion/e2.png",
						"Explosion/e3.png", "Explosion/e3.png", "Explosion/e3.png",
						"Explosion/e4.png", "Explosion/e4.png", "Explosion/e4.png",
						"Explosion/e5.png", "Explosion/e5.png", "Explosion/e5.png"]

	def update(self):
		if self.contador <= 13:
			self.image = pygame.image.load(self.avanzar[self.contador])
			self.contador += 1

class miniExplosion(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("Explosion/me1.png")
		self.rect = self.image.get_rect()
		self.rect.x = pos[0]
		self.rect.y = pos[1]
		self.contador = 0
		self.avanzar = ["Explosion/me1.png", "Explosion/me1.png",
						"Explosion/me2.png", "Explosion/me2.png", "Explosion/me2.png",
						"Explosion/me3.png", "Explosion/me3.png", "Explosion/me3.png",
						"Explosion/me4.png", "Explosion/me4.png", "Explosion/me4.png",
						"Explosion/me5.png", "Explosion/me5.png", "Explosion/me5.png"]

	def update(self):
		if self.contador <= 13:
			self.image = pygame.image.load(self.avanzar[self.contador])
			self.contador += 1
			
#----------------------------------------------------------------------------------------------------
