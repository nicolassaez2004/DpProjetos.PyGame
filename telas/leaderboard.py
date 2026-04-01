import pygame

from config.parametros import LARGURA, ALTURA, FPS


class LeaderboardScreen:
	def __init__(self, window):
		self.window = window
		self.clock = pygame.time.Clock()
		self.fonte_titulo = pygame.font.SysFont(None, 120)
		self.fonte_destaque = pygame.font.SysFont(None, 68)
		self.fonte_item = pygame.font.SysFont(None, 58)
		self.fonte_hint = pygame.font.SysFont(None, 52)
		self.cor_titulo = (255, 220, 0)
		self.bg_top = (16, 20, 72)
		self.bg_bottom = (10, 10, 42)

	def _desenhar_fundo(self):
		for y in range(ALTURA):
			t = y / ALTURA
			r = int(self.bg_top[0] * (1 - t) + self.bg_bottom[0] * t)
			g = int(self.bg_top[1] * (1 - t) + self.bg_bottom[1] * t)
			b = int(self.bg_top[2] * (1 - t) + self.bg_bottom[2] * t)
			pygame.draw.line(self.window, (r, g, b), (0, y), (LARGURA, y))

	def _cor_por_posicao(self, indice):
		if indice == 0:
			return (255, 220, 0)
		if indice == 1:
			return (210, 210, 220)
		if indice == 2:
			return (212, 150, 68)
		return (205, 205, 205)

	def executar(self, ranking, jogador_atual=None, score_atual=None):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return 'SAIR'
				if event.type == pygame.KEYDOWN:
					if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_KP_ENTER):
						return 'MENU'

			self._desenhar_fundo()

			titulo_sombra = self.fonte_titulo.render('PLACAR', True, (0, 0, 0))
			titulo = self.fonte_titulo.render('PLACAR', True, self.cor_titulo)
			titulo_rect = titulo.get_rect(center=(LARGURA // 2, 120))
			self.window.blit(titulo_sombra, (titulo_rect.x + 4, titulo_rect.y + 4))
			self.window.blit(titulo, titulo_rect)

			if jogador_atual is not None and score_atual is not None:
				linha_jogador = self.fonte_destaque.render(
					f'Sua pontuação: {jogador_atual} - {score_atual} pontos',
					True,
					(104, 255, 123)
				)
				self.window.blit(linha_jogador, linha_jogador.get_rect(center=(LARGURA // 2, 200)))

			subtitulo = self.fonte_destaque.render('TOP 10', True, (240, 240, 240))
			self.window.blit(subtitulo, subtitulo.get_rect(center=(LARGURA // 2, 258)))

			y_inicial = 320
			espacamento = 46
			if ranking:
				for indice, entrada in enumerate(ranking[:10]):
					nome = entrada.get('nome', 'SEM NOME')
					score = entrada.get('score', 0)
					texto = f'{indice + 1}. {nome} - {score} pontos'
					item = self.fonte_item.render(texto, True, self._cor_por_posicao(indice))
					self.window.blit(item, item.get_rect(center=(LARGURA // 2, y_inicial + indice * espacamento)))
			else:
				vazio = self.fonte_item.render('Nenhum recorde salvo ainda.', True, (200, 200, 200))
				self.window.blit(vazio, vazio.get_rect(center=(LARGURA // 2, 360)))

			hint = self.fonte_hint.render('Pressione ENTER ou ESC para voltar ao menu', True, (165, 165, 190))
			self.window.blit(hint, hint.get_rect(center=(LARGURA // 2, ALTURA - 42)))

			pygame.display.update()
			self.clock.tick(FPS)
