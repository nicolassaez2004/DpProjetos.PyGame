import pygame

from jogador.guerreiro import Combat
from config.parametros import ASSETS


class Player(Combat, pygame.sprite.Sprite):
    def __init__(self, posicao):
        super(Player, self).__init__()
        aux_movimento = ['parado', 'andando', 'batendo']
        size = (80, 80)
        self.tem_arco = False
        self.tem_espada = False
        self.ataque_base = 'soco'
        self.estado_combate = 'soco'
        self.estado_movimento = aux_movimento[0]

        aux = pygame.image.load(ASSETS + 'knight.png')
        self.knight_parado = pygame.transform.scale(aux, size)
        self.knight_parado_flip = pygame.transform.flip(self.knight_parado, True, False)
        self.knight_soco = pygame.transform.scale(pygame.image.load(ASSETS + 'knight_soco.png'), size)
        self.knight_soco_flip = pygame.transform.flip(self.knight_soco, True, False)
        self.knight_espada = pygame.transform.scale(pygame.image.load(ASSETS + 'knight_espada.png'), size)
        self.knight_espada_flip = pygame.transform.flip(self.knight_espada, True, False)
        self.knight_arco_soco = pygame.transform.scale(pygame.image.load(ASSETS + 'knight_arco.png'), size)
        self.knight_arco_soco_flip = pygame.transform.flip(self.knight_arco_soco, True, False)
        self.knight_arco_espada = pygame.transform.scale(pygame.image.load(ASSETS + 'knight_arco_espada.png'), size)
        self.knight_arco_espada_flip = pygame.transform.flip(self.knight_arco_espada, True, False)
        self.knight_golpe_espada = pygame.transform.scale(pygame.image.load(ASSETS + 'knight_golpe_espada.png'), size)
        self.knight_golpe_espada_flip = pygame.transform.flip(self.knight_golpe_espada, True, False)
        self.olhando_direita = True
        self.image = self.knight_parado
        self.rect = pygame.Rect(posicao, size)
        self.mask = pygame.mask.from_surface(self.image)
        self.velocidade = pygame.math.Vector2(0, 0)
        self.soco_vento = None
        self.soco_vento_image = pygame.transform.scale(pygame.image.load(ASSETS + 'soco_vento.png'), (80, 80))
        self.soco_vento_image_rotated = self.soco_vento_image
        self.soco_vento_image_rotated = self.soco_vento_image
        
        self.espada_vento = None
        self.espada_vento_hitbox = None
        self.espada_vento_image = pygame.transform.scale(pygame.image.load(ASSETS + 'espada_vento.png'), (160, 160))
        self.espada_vento_image_rotated = self.espada_vento_image

        self.arrow_image = pygame.transform.scale_by(pygame.image.load(ASSETS + 'arrow.png'), 5)
        self.flechas_disparadas = pygame.sprite.Group()
        self.cooldown_flecha_ms = 250
        self.ultimo_disparo_flecha_ms = -self.cooldown_flecha_ms
        self.cooldown_soco_ms = 1000
        self.ultimo_soco_ms = -self.cooldown_soco_ms
        self.soco_vento_expira_ms = 0
        self.cooldown_espada_ms = 1000
        self.ultimo_espada_ms = -self.cooldown_espada_ms
        self.espada_vento_expira_ms = 0
        self.duracao_vento_ms = 300
        
        self.dinheiro = 0
        self.max_vida = 10
        self.vida = 10
        self.max_flechas = 30
        self.flechas = 0
        
    def movimentacao(self):
        self.key = pygame.key.get_pressed()

        self.velocidade.x = 0
        self.velocidade.y = 0

        if self.key[pygame.K_w]:
            self.velocidade.y = -7
        if self.key[pygame.K_s]:
            self.velocidade.y = 7
        if self.key[pygame.K_a]:
            self.velocidade.x = -7
        if self.key[pygame.K_d]:
            self.velocidade.x = 7

        self.rect.move_ip(*self.velocidade)

        if self.rect.x < 380:
            self.rect.x = 380
        if self.rect.x > 820:
            self.rect.x = 820
        if self.rect.y < 160:
            self.rect.y = 160
        if self.rect.y > 480:
            self.rect.y = 480

    def atualizar_estado_combate(self):
        if self.tem_arco and self.tem_espada:
            self.estado_combate = 'arco_espada'
        elif self.tem_arco:
            self.estado_combate = 'arco_soco'
        elif self.tem_espada:
            self.estado_combate = 'espada'
        else:
            self.estado_combate = 'soco'

    def equipar_arco(self):
        if not self.tem_arco:
            self.flechas = 5
        self.tem_arco = True
        self.atualizar_estado_combate()

    def equipar_espada(self):
        self.tem_espada = True
        self.ataque_base = 'espada'
        self.atualizar_estado_combate()