import random
import pygame
from enemies.wizard import Wizard
from enemies.ghost import Ghost

class Spawn:
    def __init__(self):
        self.inimigos = pygame.sprite.Group()
        self.tipos_inimigos = []
        self.gameplay = None
        self.objeto = None
        self.spawn_cooldown_ms = 900
        self.ultimo_spawn_ms = 0
        self.som_spawn_wizard = pygame.mixer.Sound('assets/sons/sound_spawnwizard.mp3')
    
    def spawn_inimigo(self):
            tem_ghost = any(isinstance(i, Ghost) for i in self.inimigos)
            if self.gameplay.nivel == 1 and not tem_ghost:
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
            self.gameplay.aplicar_scaling_inimigo(inimigo)
            self.inimigos.add(inimigo)
            if isinstance(inimigo, Wizard):
                self.som_spawn_wizard.play()

    def atualizar_spawn_inimigos(self):
        agora = pygame.time.get_ticks()
        if len(self.inimigos) < self.gameplay.limite_inimigos and (agora - self.ultimo_spawn_ms) >= self.spawn_cooldown_ms:
            self.spawn_inimigo()
            self.ultimo_spawn_ms = agora