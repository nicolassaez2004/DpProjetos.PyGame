import random
import pygame
from enemies.wizard import Wizard
from enemies.ghost import Ghost

class Spawn:
    def __init__(self):
        self.inimigos = pygame.sprite.Group()
        self.tipos_inimigos = []
        self.player = None
        self.objeto = None
        self.spawn_cooldown_ms = 900
        self.ultimo_spawn_ms = 0
    
    def spawn_inimigo(self):
            tem_ghost = any(isinstance(i, Ghost) for i in self.inimigos)
            if self.player.nivel == 1 and not tem_ghost:
                tipo_inimigo = Ghost
            else:
                tipo_inimigo = random.choice(self.tipos_inimigos)
            inimigo = tipo_inimigo((0, 0))
            inimigo.player = self.player
            inimigo.objeto = self.objeto

            if isinstance(inimigo, Wizard):
                pos_spawn = inimigo.spawn_wizard()
            else:
                pos_spawn = inimigo.random_spawn()

            inimigo.rect.topleft = pos_spawn
            self.player.aplicar_scaling_inimigo(inimigo)
            self.inimigos.add(inimigo)

    def atualizar_spawn_inimigos(self):
        agora = pygame.time.get_ticks()
        if len(self.inimigos) < self.player.limite_inimigos and (agora - self.ultimo_spawn_ms) >= self.spawn_cooldown_ms:
            self.spawn_inimigo()
            self.ultimo_spawn_ms = agora