import pygame
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, posicao):
        super().__init__()

        self.health = 10
        self.damage = 10
        self.speed = 2

        self.pos_inicial = pygame.math.Vector2(posicao)
        self.rect = pygame.Rect(posicao, (80, 80))
        self.velocidade = pygame.math.Vector2(0, 0)

    def random_spawn(self):
        self.spawn_pos = ()
        lado = random.randint(1, 4)
        if lado == 1: #cima
            self.spawn_pos = (random.randint(80, 1200), -80)
        if lado == 2: #baixo
            self.spawn_pos = (random.randint(80, 1200), 660)
        if lado == 3: #esquerda
            self.spawn_pos = (-80, random.randint(80, 660))
        if lado == 4: #direita
            self.spawn_pos = (1200, random.randint(80, 660))

        self.pos_atual = self.spawn_pos
        return self.spawn_pos

    def disparo(self):
        pass
