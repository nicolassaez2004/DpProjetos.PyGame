import pygame

from config.parametros import LARGURA, ALTURA, ASSETS


class LeaderboardScreen:
	def __init__(self, window):
		self.window = window
		self.clock = pygame.time.Clock()
		self.fonte_titulo = pygame.font.SysFont(None, 120)
		self.fonte_destaque = pygame.font.SysFont(None, 68)
		self.fonte_item = pygame.font.SysFont(None, 44)
		self.fonte_hint = pygame.font.SysFont(None, 46)
		self.cor_titulo = (255, 220, 0)
		self.fundo = pygame.image.load(ASSETS + 'bgleaderboard.jpg')
		self.fundo = pygame.transform.scale(self.fundo, (LARGURA, ALTURA))

	def desenhar_fundo(self):
		self.window.blit(self.fundo, (0, 0))

	def cor_por_posicao(self, indice):
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

			self.desenhar_fundo()

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

			y_inicial = 300
			y_limite = ALTURA - 96
			if ranking:
				top10 = ranking[:10]
				total = len(top10)
				if total > 1:
					espacamento = (y_limite - y_inicial) / (total - 1)
				else:
					espacamento = 0

				for indice, entrada in enumerate(top10):
					nome = entrada.get('nome', 'SEM NOME')
					score = entrada.get('score', 0)
					texto = f'{indice + 1}. {nome} - {score} pontos'
					item = self.fonte_item.render(texto, True, self.cor_por_posicao(indice))
					y_item = int(y_inicial + indice * espacamento)
					self.window.blit(item, item.get_rect(center=(LARGURA // 2, y_item)))
			else:
				vazio = self.fonte_item.render('Nenhum recorde salvo ainda.', True, (200, 200, 200))
				self.window.blit(vazio, vazio.get_rect(center=(LARGURA // 2, 360)))

			hint = self.fonte_hint.render('Pressione ENTER ou ESC para voltar ao menu', True, (165, 165, 190))
			self.window.blit(hint, hint.get_rect(center=(LARGURA // 2, ALTURA - 42)))

			pygame.display.update()
			self.clock.tick(60)
