from Library import *

def main():
	#pygame.init()
	pygame.font.init()
	font = pygame.font.Font(None, 100)
	font2 = pygame.font.Font(None, 40)
	font3 = pygame.font.Font(None, 20)
	Pantalla = pygame.display.set_mode([ANCHO, ALTO])
	pygame.display.set_caption("Naves")
	pygame.mixer.music.load("Sonidos/Sonido1.mp3")
	sonidoExplosion = pygame.mixer.Sound("Explosion/eSonido.mp3")
	pygame.mixer.music.play(-1)
	pygame.mixer.music.set_volume(1)
	reloj = pygame.time.Clock()
	ls_Player = pygame.sprite.Group()
	ls_Todos = pygame.sprite.Group()
	ls_Enemigos = pygame.sprite.Group()
	ls_Balas = pygame.sprite.Group()
	ls_eBalas = pygame.sprite.Group()
	ls_Pildora = pygame.sprite.Group()
	ls_Explosiones = pygame.sprite.Group()
	Fondo = pygame.image.load("Extra/fondo.jpg")
	Pantalla.blit(Fondo, (0,0))
	TimePildora = random.randrange(100, 500)
	pygame.mouse.set_visible(False)
	jugador = Jugador()
	CantBalas = 1
	ls_Player.add(jugador)
	Cant = InitNivel(jugador, ls_Enemigos, ls_Todos, Pantalla, reloj, Fondo)
	while jugador.vida > 0 and jugador.win == False:
		derecha = izquierda = False
		for event in pygame.event.get():
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()
				
			if event.type== KEYDOWN and event.key == K_SPACE:
				if CantBalas <= 5:
					CantBalas += 1
					b = BalaJugador(jugador.rect)
					ls_Balas.add(b)
					ls_Todos.add(b)	
			
		if event.type == KEYDOWN and event.key == K_LEFT:
			if jugador.rect.x != 0:
				izquierda = True
				derecha = False
				jugador.rect.x -= jugador.move
		if event.type == KEYDOWN and event.key == K_RIGHT:
			if jugador.rect.x != ANCHO-60:
				derecha = True
				izquierda = False
				jugador.rect.x += jugador.move
		
		if TimePildora == 0:
			if jugador.vida < 3:
				if len(ls_Pildora) == 0:
					Px = jugador.rect.x
					Pos = random.randrange(ANCHO-50)
					while(Px == Pos or abs(Px-Pos) < 80):
						Pos = random.randrange(ANCHO-50)
					Pil = Pildora(Pos)
					ls_Pildora.add(Pil)
					ls_Todos.add(Pil)
			TimePildora = random.randrange(100, 500)
		else:
			TimePildora -= 1

		for i in ls_Pildora:
			if Pil.tiempo == 0:
				ls_Pildora.remove(Pil)
				ls_Todos.remove(Pil)

		if len(ls_Pildora):
			for Pil in ls_Pildora.sprites():
				texto4 = font2.render(str(Pil.tiempo), True, VERDE)
				Pantalla.blit(texto4, (ANCHO-100, ALTO/2))
				pygame.display.flip()

		ls_cogida = pygame.sprite.spritecollide(jugador, ls_Pildora, True)
		for cogida in ls_cogida:
			jugador.vida += 1
			ls_Pildora.remove(cogida)
			ls_Todos.remove(cogida)

		for enemigo in ls_Enemigos:
			if enemigo.disparar:
				if enemigo.distintivo == 1:
					be = BalaEnemigo1(enemigo.rect)
					ls_eBalas.add(be)
					ls_Todos.add(be)
				else:
					be = BalaEnemigo2(enemigo.rect)
					ls_eBalas.add(be)
					ls_Todos.add(be)

		for bj in ls_Balas:
			ls_impactos = pygame.sprite.spritecollide(bj, ls_Enemigos, True)
			ls_impactosEntreBalas = pygame.sprite.spritecollide(bj, ls_eBalas, True)
			for impactos in ls_impactos:
				pos = bj.rect
				ls_Balas.remove(bj)
				ls_Todos.remove(bj)
				sonidoExplosion.play()
				ex = Explosion(pos)
				ls_Explosiones.add(ex)
				jugador.puntos += 40
				Cant -= 1
				CantBalas -= 1
			for impacbalas in ls_impactosEntreBalas:
				pos = bj.rect
				ls_Balas.remove(bj)
				ls_Todos.remove(bj)
				sonidoExplosion.play()
				mex = miniExplosion(pos)
				ls_Explosiones.add(mex)
				jugador.puntos += 20
				CantBalas -= 1
			if bj.rect.y < 0:
				ls_Balas.remove(bj)
				ls_Todos.remove(bj)
				CantBalas -= 1

		
		for eb in ls_eBalas:
			if eb.rect.y > ALTO:
				ls_eBalas.remove(eb)
				ls_Todos.remove(eb)

		ls_eimpactos = pygame.sprite.spritecollide(jugador, ls_eBalas, True)
		for eimpactos in ls_eimpactos:
			jugador.vida -= 1
			if jugador.puntos >= 10:
				jugador.puntos -= 10
			else:
				jugador.puntos == 0
			ls_eBalas.remove(be)
			ls_Todos.remove(be)

		for ex in ls_Explosiones:
			if ex.contador == 13:
				ls_Explosiones.remove(ex)

		texto = font3.render("Puntaje" + str(jugador.puntos), True, AZUL)
		texto2 = font2.render("x" + str(jugador.vida), True, AZUL)
		imgVida = pygame.image.load("Extra/playerLife.png")
		Pantalla.blit(Fondo,(0,0))
		Pantalla.blit(imgVida, (5,0))
		Pantalla.blit(texto2, (40,00))
		Pantalla.blit(texto, (ANCHO-100,0))
		reloj.tick(50)
		ls_Player.update(derecha, izquierda, Cant)
		ls_Todos.update()
		ls_Explosiones.update()
		ls_Explosiones.draw(Pantalla)
		ls_Player.draw(Pantalla)
		ls_Todos.draw(Pantalla)
		pygame.display.flip()
		control  = 0

		if jugador.puntos <= 400:
			if Cant <= 10:
				if control%2 == 0:
					MasEnemigos = random.randrange(2)
					for i in range(MasEnemigos):
						e = Enemigo1()
						ls_Enemigos.add(e)
						ls_Todos.add(e)
						Cant += 1
						control += 1
				else:
					control += random.randrange(5)

		if jugador.nivel == 1 and jugador.puntos <= 2000:
			if Cant <= 10:
				if control%2 == 0:
					MasEnemigos = random.randrange(1)
					for i in range(MasEnemigos):
						e = Enemigo2()
						ls_Enemigos.add(e)
						ls_Todos.add(e)
						Cant += 1
						control += 1
				else:
					control += random.randrange(5)

		if Cant == 0:
			ClearNivel(ls_Enemigos, ls_Todos, ls_Balas, ls_eBalas, ls_Explosiones, ls_Pildora)
			if jugador.nivel <= 2:
				Cant = InitNivel(jugador, ls_Enemigos, ls_Todos, Pantalla, reloj, Fondo)
	FinJuego(Pantalla, jugador, reloj)
	

if __name__=='__main__':
	main()
