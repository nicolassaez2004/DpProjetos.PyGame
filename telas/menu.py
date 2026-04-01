import pygame

from config.parametros import LARGURA, ALTURA, FPS


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
		self.bg_top = (20, 18, 60)
		self.bg_bottom = (60, 20, 90)
		self.cor_titulo = (255, 220, 0)
		self.cor_texto = (220, 220, 220)
		self.cor_selecionado = (255, 220, 0)

		self.popup_nome_aberto = False
		self.nome_digitado = ''
		self.nome_maximo = 15

	def _desenhar_fundo(self):
		for y in range(ALTURA):
			t = y / ALTURA
			r = int(self.bg_top[0] * (1 - t) + self.bg_bottom[0] * t)
			g = int(self.bg_top[1] * (1 - t) + self.bg_bottom[1] * t)
			b = int(self.bg_top[2] * (1 - t) + self.bg_bottom[2] * t)
			pygame.draw.line(self.window, (r, g, b), (0, y), (LARGURA, y))

	def _retangulos_opcoes(self):
		retangulos = []
		y_inicial = ALTURA // 2 + 10
		espacamento = 84
		for indice, opcao in enumerate(self.opcoes):
			cor = self.cor_selecionado if indice == self.indice_selecionado else self.cor_texto
			texto = self.fonte_opcao.render(opcao, True, cor)
			rect = texto.get_rect(center=(LARGURA // 2, y_inicial + indice * espacamento))
			retangulos.append((texto, rect))
		return retangulos

	def _desenhar_menu(self):
		self._desenhar_fundo()

		titulo_sombra = self.fonte_titulo.render('PITAGORAS OPS', True, (0, 0, 0))
		titulo = self.fonte_titulo.render('PITAGORAS OPS', True, self.cor_titulo)
		subtitulo = self.fonte_subtitulo.render('Sobreviva às ondas de inimigos!', True, (195, 195, 220))

		titulo_rect = titulo.get_rect(center=(LARGURA // 2, 190))
		self.window.blit(titulo_sombra, (titulo_rect.x + 4, titulo_rect.y + 4))
		self.window.blit(titulo, titulo_rect)
		self.window.blit(subtitulo, subtitulo.get_rect(center=(LARGURA // 2, 270)))

		for texto, rect in self._retangulos_opcoes():
			if texto.get_at((0, 0))[:3] == self.cor_selecionado:
				destaque = pygame.Rect(rect.x - 24, rect.y - 12, rect.width + 48, rect.height + 20)
				pygame.draw.rect(self.window, (72, 38, 110), destaque, border_radius=14)
				pygame.draw.rect(self.window, self.cor_selecionado, destaque, 3, border_radius=14)
			self.window.blit(texto, rect)

		hint = self.fonte_hint.render('Use ↑↓ ou W/S para navegar | ENTER ou CLIQUE para selecionar', True, (160, 160, 190))
		self.window.blit(hint, hint.get_rect(center=(LARGURA // 2, ALTURA - 52)))

	def _desenhar_popup_nome(self):
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
		texto_nome_rect = texto_nome.get_rect(midleft=(caixa.x + 22, caixa.centery))
		self.window.blit(texto_nome, texto_nome_rect)

		limite = self.fonte_popup_hint.render(f'Máximo {self.nome_maximo} caracteres', True, (180, 180, 205))
		self.window.blit(limite, limite.get_rect(center=(LARGURA // 2, 456)))

		if self.nome_digitado.strip():
			instrucoes = 'ENTER para começar | ESC para voltar'
		else:
			instrucoes = 'Digite seu nome para começar | ESC para voltar'
		hint = self.fonte_popup_hint.render(instrucoes, True, (180, 180, 205))
		self.window.blit(hint, hint.get_rect(center=(LARGURA // 2, 660)))

	def _iniciar_popup_nome(self):
		self.popup_nome_aberto = True
		self.nome_digitado = ''

	def _aplicar_opcao(self):
		opcao = self.opcoes[self.indice_selecionado]
		if opcao == 'JOGAR':
			self._iniciar_popup_nome()
			return None
		if opcao == 'LEADERBOARD':
			return ('LEADERBOARD', None)
		return ('SAIR', None)

	def _tratar_evento_menu(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key in (pygame.K_UP, pygame.K_w):
				self.indice_selecionado = (self.indice_selecionado - 1) % len(self.opcoes)
			elif event.key in (pygame.K_DOWN, pygame.K_s):
				self.indice_selecionado = (self.indice_selecionado + 1) % len(self.opcoes)
			elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
				return self._aplicar_opcao()

		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			for indice, (_, rect) in enumerate(self._retangulos_opcoes()):
				if rect.collidepoint(event.pos):
					self.indice_selecionado = indice
					return self._aplicar_opcao()
		return None

	def _tratar_evento_popup_nome(self, event):
		if event.type != pygame.KEYDOWN:
			return None

		if event.key == pygame.K_ESCAPE:
			self.popup_nome_aberto = False
			return None

		if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
			nome = self.nome_digitado.strip()
			if nome:
				return ('JOGAR', nome)
			return None

		if event.key == pygame.K_BACKSPACE:
			self.nome_digitado = self.nome_digitado[:-1]
			return None

		if len(self.nome_digitado) < self.nome_maximo:
			caractere = event.unicode
			if caractere.isprintable() and not caractere.isspace():
				self.nome_digitado += caractere
		return None

	def executar(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return ('SAIR', None)

				if self.popup_nome_aberto:
					resultado = self._tratar_evento_popup_nome(event)
					if resultado:
						return resultado
				else:
					resultado = self._tratar_evento_menu(event)
					if resultado:
						return resultado

			self._desenhar_menu()
			if self.popup_nome_aberto:
				self._desenhar_popup_nome()
			pygame.display.update()
			self.clock.tick(FPS)
