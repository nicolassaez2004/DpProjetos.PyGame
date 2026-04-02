import pygame

from config.parametros import LARGURA, ALTURA
from dados.leaderboard_repo import LeaderboardRepository
from jogo.game import Game
from telas.leaderboard import LeaderboardScreen
from telas.menu import MenuScreen


class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption('Trapped Knight')

        self.menu_screen = MenuScreen(self.window)
        self.leaderboard_screen = LeaderboardScreen(self.window)
        self.leaderboard_repo = LeaderboardRepository()

    def executar(self):
        estado = 'MENU'
        ultimo_jogador = None
        ultimo_score = None

        while True:
            if estado == 'MENU':
                acao, nome = self.menu_screen.executar()
                if acao == 'SAIR':
                    break
                if acao == 'LEADERBOARD':
                    estado = 'LEADERBOARD'
                    ultimo_jogador = None
                    ultimo_score = None
                elif acao == 'JOGAR':
                    jogo = Game(player_name=nome)
                    resultado = jogo.executar()

                    self.window = pygame.display.set_mode((LARGURA, ALTURA))
                    pygame.display.set_caption('Trapped Knight')
                    self.menu_screen.window = self.window
                    self.leaderboard_screen.window = self.window

                    if resultado.get('status') == 'SAIR':
                        break

                    ultimo_jogador = resultado.get('nome')
                    ultimo_score = resultado.get('score', 0)
                    self.leaderboard_repo.adicionar_pontuacao(ultimo_jogador, ultimo_score)
                    estado = 'LEADERBOARD'

            elif estado == 'LEADERBOARD':
                ranking = self.leaderboard_repo.carregar()
                acao = self.leaderboard_screen.executar(ranking, ultimo_jogador, ultimo_score)
                if acao == 'SAIR':
                    break
                estado = 'MENU'

        pygame.quit()


if __name__ == '__main__':
    App().executar()