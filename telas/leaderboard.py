import pygame

from config.parametros import LARGURA, ALTURA, ASSETS


class LeaderboardScreen:
	def __init__(self, window):
		self.window = window
		self.clock = pygame.time.Clock()
		self.fonte_titulo = pygame.font.SysFont(None, 120)
		self.fonte_subtitulo = pygame.font.SysFont(None, 60)
		self.fonte_header = pygame.font.SysFont(None, 40)
		self.fonte_item = pygame.font.SysFont(None, 35)
		self.fonte_hint = pygame.font.SysFont(None, 46)
		self.cor_titulo = (255, 220, 0)
		self.fundo = pygame.image.load(ASSETS + 'bgleaderboard.jpg')
		self.fundo = pygame.transform.scale(self.fundo, (LARGURA, ALTURA))

	def desenhar_fundo(self):
		self.window.blit(self.fundo, (0, 0))

	def cor_por_posicao(self, indice):
		cores = [
			(255, 220, 0),
			(210, 210, 220),
			(212, 150, 68),
		]
		if indice < len(cores):
			return cores[indice]
		return (180, 180, 180)

	def desenhar_box(self, x, y, largura, altura, cor_borda, cor_fundo, espessura=2):
		pygame.draw.rect(self.window, cor_fundo, (x, y, largura, altura))
		pygame.draw.rect(self.window, cor_borda, (x, y, largura, altura), espessura)

	def executar(self, ranking, jogador_atual=None, score_atual=None):
		if not pygame.mixer.music.get_busy():
			pygame.mixer.music.load('assets/sons/ost_menu.mp3')
			pygame.mixer.music.play(-1)

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
			titulo_rect = titulo.get_rect(center=(LARGURA // 2, 60))
			self.window.blit(titulo_sombra, (titulo_rect.x + 4, titulo_rect.y + 4))
			self.window.blit(titulo, titulo_rect)

			y_atual = 140
			if jogador_atual is not None and score_atual is not None:
				self.desenhar_box(80, y_atual - 5, LARGURA - 160, 50, (104, 255, 123), (20, 40, 20), 3)
				
				linha_jogador = self.fonte_subtitulo.render(
					f'Sua pontuação: {jogador_atual} - {score_atual} pontos',
					True,
					(104, 255, 123)
				)
				linha_rect = linha_jogador.get_rect(center=(LARGURA // 2, y_atual + 15))
				self.window.blit(linha_jogador, linha_rect)
				y_atual += 80

			subtitulo = self.fonte_subtitulo.render('TOP 10', True, (240, 240, 240))
			subtitulo_rect = subtitulo.get_rect(center=(LARGURA // 2, y_atual))
			self.window.blit(subtitulo, subtitulo_rect)
			y_atual += 60

			header_y = y_atual
			col_pos = 70
			col_nome = 130
			col_score = 480
			col_nivel = 750
			col_tempo = 950

			self.desenhar_box(col_pos - 35, header_y - 5, LARGURA - 120, 32, (200, 200, 200), (40, 40, 40), 2)
			
			header_texts = [
				("#", col_pos),
				("Nome", col_nome),
				("Score", col_score),
				("Nível", col_nivel),
				("Tempo", col_tempo)
			]
			
			for text, x in header_texts:
				header = self.fonte_header.render(text, True, (200, 200, 200))
				self.window.blit(header, (x, header_y))

			y_items = header_y + 40
			item_altura = 32
			
			if ranking:
				top10 = ranking[:10]
				
				for indice, entrada in enumerate(top10):
					nome = entrada.get('nome', 'SEM NOME')
					score = entrada.get('score', 0)
					nivel = entrada.get('nivel', 1)
					tempo = entrada.get('tempo', '0:00')
					
					cor_fundo_linha = (30, 30, 30) if indice % 2 == 0 else (25, 25, 25)
					self.desenhar_box(col_pos - 35, y_items - 4, LARGURA - 120, item_altura, 
									 self.cor_por_posicao(indice), cor_fundo_linha, 1)
					
					cor_texto = self.cor_por_posicao(indice)
					
					pos_text = self.fonte_item.render(f"{indice + 1}", True, cor_texto)
					self.window.blit(pos_text, (col_pos, y_items))
					
					nome_truncado = nome[:18] if len(nome) > 18 else nome
					nome_text = self.fonte_item.render(nome_truncado, True, cor_texto)
					self.window.blit(nome_text, (col_nome, y_items))
					
					score_text = self.fonte_item.render(f"{score}", True, (255, 200, 100))
					self.window.blit(score_text, (col_score, y_items))
					
					nivel_text = self.fonte_item.render(f"Nv. {nivel}", True, (150, 200, 255))
					self.window.blit(nivel_text, (col_nivel, y_items))
					
					tempo_text = self.fonte_item.render(tempo, True, (150, 255, 150))
					self.window.blit(tempo_text, (col_tempo, y_items))
					
					y_items += item_altura + 1
			else:
				vazio = self.fonte_item.render('Nenhum recorde salvo ainda.', True, (200, 200, 200))
				vazio_rect = vazio.get_rect(center=(LARGURA // 2, y_items + 50))
				self.window.blit(vazio, vazio_rect)

			hint_text = self.fonte_hint.render('Pressione ENTER ou ESC para voltar ao menu', True, (150, 150, 150))
			hint_rect = hint_text.get_rect(center=(LARGURA // 2, ALTURA - 50))
			self.window.blit(hint_text, hint_rect)

			pygame.display.update()
			self.clock.tick(60)
