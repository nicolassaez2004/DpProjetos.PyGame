from enemies.ghost import Ghost
from enemies.skeleton import Skeleton
from enemies.wizard import Wizard
from jogador.player import Player


class Gameplay(Player):
    def __init__(self, posicao):
        super().__init__(posicao)
        self.nivel = 1
        self.score = 0

    def capitalizacao(self, inimigo):
        if isinstance(inimigo, Ghost):
            self.dinheiro += 2
            self.score += 20
        elif isinstance(inimigo, Skeleton):
            self.dinheiro += 3
            self.score += 30
        elif isinstance(inimigo, Wizard):
            self.dinheiro += 5
            self.score += 50
