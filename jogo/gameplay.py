from enemies.ghost import Ghost
from enemies.skeleton import Skeleton
from enemies.wizard import Wizard
from jogador.player import Player


class Gameplay(Player):
    def __init__(self, posicao):
        super().__init__(posicao)
        self.nivel = 1
        self.score = 0
        self.inimigos_derrotados = 0
        self.limite_inimigos = 2
        self.bonus_velocidade_por_nivel = 0.5
        self.bonus_dano_por_nivel = 1

    def registrar_abate(self):
        self.inimigos_derrotados += 1

        kills_necessarios = self.nivel * 10
        if self.inimigos_derrotados >= kills_necessarios:
            self.inimigos_derrotados = 0
            self.nivel += 1
            self.limite_inimigos += 1

    def aplicar_scaling_inimigo(self, inimigo):
        bonus_nivel = max(self.nivel - 1, 0)
        inimigo.speed += bonus_nivel * self.bonus_velocidade_por_nivel
        inimigo.damage += bonus_nivel * self.bonus_dano_por_nivel

    def capitalizacao(self, inimigo):
        bonus_score = (self.nivel - 1) * 10
        if isinstance(inimigo, Ghost):
            self.dinheiro += 2
            self.score += 10 + bonus_score
        elif isinstance(inimigo, Skeleton):
            self.dinheiro += 3
            self.score += 20 + bonus_score
        elif isinstance(inimigo, Wizard):
            self.dinheiro += 5
            self.score += 30 + bonus_score

        self.registrar_abate()
