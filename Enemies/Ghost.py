import pygame
from Enemies.Enemy import Enemy
from config.parametros import LARGURA, ALTURA, ASSETS


class Ghost(Enemy):
    def __init__(self, posicao):
        super().__init__(posicao)

        aux = pygame.image.load(ASSETS + 'ghost.png')
        self.ghost = pygame.transform.scale(aux, (80, 80))
        self.ghost_flip = pygame.transform.flip(self.ghost, True, False)
        self.image = self.ghost

        self.timer = 0
        self.direcao = pygame.math.Vector2(0, 0)
        self.distancia_percorrida = 0

        self.direcaorandom = 0

    def movimentacao(self):
        direcao = pygame.math.Vector2(
            self.player.rect.centerx - self.rect.centerx,
            self.player.rect.centery - self.rect.centery
        )
        distancia = direcao.length()
        if distancia != 0:
            direcao = direcao.normalize()

        self.velocidade = direcao * self.speed
        self.rect.move_ip(*self.velocidade)

        self.image = self.ghost if self.player.rect.centerx >= self.rect.centerx else self.ghost_flip

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGURA:
            self.rect.right = LARGURA
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > ALTURA:
            self.rect.bottom = ALTURA
