import pygame

from config.parametros import ASSETS


class Object(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        size = (80,80)
        auxbau = pygame.image.load(ASSETS + 'bau.png')
        self.bau = pygame.transform.scale(auxbau, size)
        auxkitmedico = pygame.image.load(ASSETS + 'kitmedico.png')
        self.kitmedico = pygame.transform.scale(auxkitmedico, size)
        auxarco = pygame.image.load(ASSETS + 'arco.png')
        self.arco = pygame.transform.scale(auxarco, size)
        auxespada = pygame.image.load(ASSETS + 'espada.png')
        self.espada = pygame.transform.scale(auxespada, size)

        self.plataforma = pygame.Rect(360, 120, 560, 480)
        self.colisao_bau = pygame.Rect(400, 160, 80, 80)
        self.colisao_kitmedico = pygame.Rect(800, 160, 80, 80)
        self.colisao_arco = pygame.Rect(400, 480, 80, 80)
        self.colisao_espada = pygame.Rect(800, 480, 80, 80)