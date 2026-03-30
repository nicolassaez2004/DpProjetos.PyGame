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
        self.kills_para_subir_nivel = 5
        self.limite_inimigos = 2
        self.bonus_vida_por_nivel = 2
        self.bonus_dano_por_nivel = 1

    def registrar_abate(self):
        self.inimigos_derrotados += 1

        while self.inimigos_derrotados >= self.kills_para_subir_nivel:
            self.inimigos_derrotados -= self.kills_para_subir_nivel
            self.nivel += 1
            self.limite_inimigos += 1

    def aplicar_scaling_inimigo(self, inimigo):
        bonus_nivel = max(self.nivel - 1, 0)
        inimigo.health += bonus_nivel * self.bonus_vida_por_nivel
        inimigo.damage += bonus_nivel * self.bonus_dano_por_nivel

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

        self.registrar_abate()
