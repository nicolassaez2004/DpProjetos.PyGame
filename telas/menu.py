import pygame
import math

from config.parametros import LARGURA, ALTURA, ASSETS


class MenuScreen:
	def __init__(self, window):
		self.window = window
		self.clock = pygame.time.Clock()
		self.fonte_titulo = pygame.font.SysFont(None, 120)
		self.fonte_subtitulo = pygame.font.SysFont(None, 58)
		self.fonte_opcao = pygame.font.SysFont(None, 72)
		self.fonte_hint = pygame.font.SysFont(None, 42)
		self.fonte_popup = pygame.font.SysFont(None, 64)
		self.fonte_input = pygame.font.SysFont(None, 58)
		self.fonte_popup_hint = pygame.font.SysFont(None, 48)

		self.opcoes = ['JOGAR', 'LEADERBOARD', 'SAIR']
		self.indice_selecionado = 0
		self.cor_titulo = (255, 220, 0)
		self.cor_texto = (220, 220, 220)
		self.cor_selecionado = (255, 220, 0)

		self.popup_nome_aberto = False
		self.nome_digitado = ''
		self.nome_maximo = 15

		self.som_click = pygame.mixer.Sound('assets/sons/sound_clickmenu.mp3')
		self.som_select = pygame.mixer.Sound('assets/sons/sound_clickmenuselect.mp3')
		self.som_start = pygame.mixer.Sound('assets/sons/sound_pressstart.mp3')
		self.som_namedigit = pygame.mixer.Sound('assets/sons/sound_namedigit.mp3')
		self.som_namedelete = pygame.mixer.Sound('assets/sons/sound_namedelete.mp3')

		self.fundo_menu = pygame.image.load(ASSETS + 'bgmenu.jpg')
		self.fundo_menu = pygame.transform.scale(self.fundo_menu, (LARGURA, ALTURA))
		self.titulo_surface = self.fonte_titulo.render('TRAPPED KNIGHT', True, self.cor_titulo)
		self.titulo_sombra_surface = self.fonte_titulo.render('TRAPPED KNIGHT', True, (0, 0, 0))
		y_inicial = ALTURA // 2 + 10
		espacamento = 84
		self.opcoes_rects = [
			self.fonte_opcao.render(opcao, True, self.cor_texto).get_rect(center=(LARGURA // 2, y_inicial + indice * espacamento))
			for indice, opcao in enumerate(self.opcoes)
		]

	def desenhar_fundo(self):
		self.window.blit(self.fundo_menu, (0, 0))

	def desenhar_menu(self):
		tempo = pygame.time.get_ticks() / 1000.0
		self.desenhar_fundo()

		titulo_offset = int(4 * math.sin(tempo * 2.8))
		titulo_escala = 1.0 + (0.06 * math.sin(tempo * 3.0))
		largura_titulo = int(self.titulo_surface.get_width() * titulo_escala)
		altura_titulo = int(self.titulo_surface.get_height() * titulo_escala)
		titulo = pygame.transform.smoothscale(self.titulo_surface, (largura_titulo, altura_titulo))
		titulo_sombra = pygame.transform.smoothscale(self.titulo_sombra_surface, (largura_titulo, altura_titulo))
		subtitulo_offset = int(2 * math.sin(tempo * 2.0))
		subtitulo_cor = (
			195,
			195,
			220 + int(15 * (0.5 + 0.5 * math.sin(tempo * 2.8)))
		)
		subtitulo = self.fonte_subtitulo.render('Sobreviva às ondas de inimigos!', True, subtitulo_cor)

		titulo_rect = titulo.get_rect(center=(LARGURA // 2, 190 + titulo_offset))
		self.window.blit(titulo_sombra, (titulo_rect.x + 4, titulo_rect.y + 4))
		self.window.blit(titulo, titulo_rect)
		self.window.blit(subtitulo, subtitulo.get_rect(center=(LARGURA // 2, 270 + subtitulo_offset)))

		mouse_pos = pygame.mouse.get_pos()
		for indice, opcao in enumerate(self.opcoes):
			rect = self.opcoes_rects[indice]
			hover = rect.collidepoint(mouse_pos)
			selecionado = hover or indice == self.indice_selecionado
			cor_texto = self.cor_selecionado if selecionado else self.cor_texto
			texto = self.fonte_opcao.render(opcao, True, cor_texto)
			if selecionado:
				destaque = pygame.Rect(rect.x - 24, rect.y - 12, rect.width + 48, rect.height + 20)
				pygame.draw.rect(self.window, (28, 74, 138), destaque, border_radius=14)
				pygame.draw.rect(self.window, self.cor_selecionado, destaque, 3, border_radius=14)
			self.window.blit(texto, rect)

		hint_alpha = 170 + int(35 * (0.5 + 0.5 * math.sin(tempo * 2.5)))
		hint = self.fonte_hint.render('Use ↑↓ ou W/S para navegar | ENTER ou CLIQUE para selecionar', True, (hint_alpha, hint_alpha, 190))
		self.window.blit(hint, hint.get_rect(center=(LARGURA // 2, ALTURA - 52)))

	def desenhar_popup_nome(self):
		overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
		overlay.fill((0, 0, 0, 155))
		self.window.blit(overlay, (0, 0))

		titulo = self.fonte_popup.render('DIGITE SEU NOME', True, self.cor_titulo)
		self.window.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 200)))

		caixa = pygame.Rect(260, 310, LARGURA - 520, 76)
		pygame.draw.rect(self.window, (52, 30, 84), caixa, border_radius=12)
		pygame.draw.rect(self.window, self.cor_selecionado, caixa, 4, border_radius=12)

		nome = self.nome_digitado if self.nome_digitado else '|'
		texto_nome = self.fonte_input.render(nome, True, (240, 240, 240))
		texto_nome_rect = texto_nome.get_rect(center=caixa.center)
		self.window.blit(texto_nome, texto_nome_rect)

		limite = self.fonte_popup_hint.render(f'Máximo {self.nome_maximo} caracteres', True, (180, 180, 205))
		self.window.blit(limite, limite.get_rect(center=(LARGURA // 2, 456)))

		if self.nome_digitado.strip():
			instrucoes = 'ENTER para começar | ESC para voltar'
		else:
			instrucoes = 'Digite seu nome para começar | ESC para voltar'
		hint = self.fonte_popup_hint.render(instrucoes, True, (180, 180, 205))
		self.window.blit(hint, hint.get_rect(center=(LARGURA // 2, 660)))

	def iniciar_popup_nome(self):
		self.popup_nome_aberto = True
		self.nome_digitado = ''

	def aplicar_opcao(self):
		opcao = self.opcoes[self.indice_selecionado]
		if opcao == 'JOGAR':
			self.som_select.play()
			self.iniciar_popup_nome()
			return None
		if opcao == 'LEADERBOARD':
			self.som_select.play()
			return ('LEADERBOARD', None)
		self.som_select.play()
		return ('SAIR', None)

	def tratar_evento_menu(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key in (pygame.K_UP, pygame.K_w):
				self.indice_selecionado = (self.indice_selecionado - 1) % len(self.opcoes)
				self.som_click.play()
			elif event.key in (pygame.K_DOWN, pygame.K_s):
				self.indice_selecionado = (self.indice_selecionado + 1) % len(self.opcoes)
				self.som_click.play()
			elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
				return self.aplicar_opcao()

		if event.type == pygame.MOUSEMOTION:
			for indice, rect in enumerate(self.opcoes_rects):
				if rect.collidepoint(event.pos):
					if indice != self.indice_selecionado:
						self.indice_selecionado = indice
						self.som_click.play()
					break

		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			for indice, rect in enumerate(self.opcoes_rects):
				if rect.collidepoint(event.pos):
					self.indice_selecionado = indice
					return self.aplicar_opcao()
		return None

	def tratar_evento_popup_nome(self, event):
		if event.type != pygame.KEYDOWN:
			return None

		if event.key == pygame.K_ESCAPE:
			self.popup_nome_aberto = False
			return None

		if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
			nome = self.nome_digitado.strip()
			if nome:
				self.som_start.play()
				self.popup_nome_aberto = False
				return ('JOGAR', nome)
			return None

		if event.key == pygame.K_BACKSPACE:
			if self.nome_digitado:
				self.nome_digitado = self.nome_digitado[:-1]
				self.som_namedelete.play()
			return None

		if len(self.nome_digitado) < self.nome_maximo:
			caractere = event.unicode
			if caractere and caractere.isprintable():
				self.nome_digitado += caractere
				self.som_namedigit.play()
		return None

	def executar(self):
		self.popup_nome_aberto = False
		self.nome_digitado = ''

		if not pygame.mixer.music.get_busy():
			pygame.mixer.music.load('assets/sons/ost_menu.mp3')
			pygame.mixer.music.play(-1)

		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return ('SAIR', None)

				if self.popup_nome_aberto:
					resultado = self.tratar_evento_popup_nome(event)
					if resultado:
						return resultado
				else:
					resultado = self.tratar_evento_menu(event)
					if resultado:
						return resultado

			self.desenhar_menu()
			if self.popup_nome_aberto:
				self.desenhar_popup_nome()
			pygame.display.update()
			self.clock.tick(60)
