import pygame
import random
from enemies.enemy import Enemy
from config.parametros import LARGURA, ALTURA, ASSETS


class Skeleton(Enemy):
    def __init__(self, posicao):
        super().__init__(posicao)

        aux = pygame.image.load(ASSETS + 'skeleton.png')
        self.skeleton = pygame.transform.scale(aux, (80, 80))
        self.skeleton_inverso = pygame.transform.flip(self.skeleton, True, False)
        self.image = self.skeleton

        self.estado = "indo_player"
        self.timer = 0
        self.direcao = pygame.math.Vector2(0, 0)
        self.distancia_percorrida = 0

        self.estado = 0
        self.direcaorandom = 0

        self.arrow_skeleton_image = pygame.transform.scale_by(pygame.image.load(ASSETS + 'arrow_skeleton.png'), 5)
        self.flechas_disparadas = pygame.sprite.Group()
        self.cooldown_disparo_ms = 3000
        self.ultimo_disparo_ms = pygame.time.get_ticks()
        self.som_skeleton_arrow = pygame.mixer.Sound('assets/sons/sound_skeletonarrow.mp3')

    def criar_flecha(self, direcao):
        if direcao.length_squared() == 0:
            direcao = pygame.math.Vector2(1, 0)

        nivel_atual = getattr(self.player, 'nivel', 1)
        multiplicador_nivel = 1 + (max(nivel_atual, 1) - 1) * 0.35

        flecha = pygame.sprite.Sprite()
        flecha.direcao = direcao.normalize()
        flecha.velocidade = 6 * multiplicador_nivel
        flecha.damage = 1

        direcao_base_sprite = pygame.math.Vector2(1, -1)
        angulo = -direcao_base_sprite.angle_to(flecha.direcao)
        flecha.image = pygame.transform.rotate(self.arrow_skeleton_image, angulo)
        flecha.rect = flecha.image.get_rect(center=self.rect.center)
        flecha.mask = pygame.mask.from_surface(flecha.image)
        return flecha

    def atualizar_flechas(self):
        for flecha in list(self.flechas_disparadas):
            deslocamento = flecha.direcao * flecha.velocidade
            flecha.rect.move_ip(deslocamento.x, deslocamento.y)
            if (
                flecha.rect.right < 0 or flecha.rect.left > LARGURA or
                flecha.rect.bottom < 0 or flecha.rect.top > ALTURA
            ):
                flecha.kill()

    def disparo(self):
        agora = pygame.time.get_ticks()
        nivel_atual = getattr(self.player, 'nivel', 1)
        multiplicador_nivel = 1 + (max(nivel_atual, 1) - 1) * 0.10
        cooldown_atual = int(self.cooldown_disparo_ms / multiplicador_nivel)
        if (agora - self.ultimo_disparo_ms) < cooldown_atual:
            return

        direcao = pygame.math.Vector2(
            self.player.rect.centerx - self.rect.centerx,
            self.player.rect.centery - self.rect.centery
        )

        flecha = self.criar_flecha(direcao)
        self.flechas_disparadas.add(flecha)
        self.ultimo_disparo_ms = agora
        self.som_skeleton_arrow.play()

    def movimentacao(self):
        direcao = pygame.math.Vector2(
            self.player.rect.centerx - self.rect.centerx,
            self.player.rect.centery - self.rect.centery
        )
        distancia = direcao.length()
        if distancia != 0:
            direcao = direcao.normalize()

        if self.distancia_percorrida < 160:
            self.velocidade = direcao * self.speed
            self.distancia_percorrida += self.velocidade.length()
            new_rect = self.rect.copy()
            rect_x = new_rect.move(self.velocidade.x, 0)
            if not rect_x.colliderect(self.objeto.plataforma):
                new_rect.x = rect_x.x
            rect_y = new_rect.move(0, self.velocidade.y)
            if not rect_y.colliderect(self.objeto.plataforma):
                new_rect.y = rect_y.y
            self.image = self.skeleton if self.player.rect.centerx >= self.rect.centerx else self.skeleton_inverso
            self.rect = new_rect
            return

        if distancia < 160:
            self.velocidade = direcao * self.speed
        else:
            self.timer += 1
            if self.timer > 60:
                self.timer = 0
                self.estado = random.randint(1, 2)
                if self.estado == 1:
                    self.velocidade = pygame.math.Vector2(0, 0)
                else:
                    direcao_random = random.randint(1, 4)

                    if direcao_random == 1:
                        self.velocidade = pygame.math.Vector2(0, -self.speed)
                    if direcao_random == 2:
                        self.velocidade = pygame.math.Vector2(0, self.speed)
                    if direcao_random == 3:
                        self.velocidade = pygame.math.Vector2(-self.speed, 0)
                    if direcao_random == 4:
                        self.velocidade = pygame.math.Vector2(self.speed, 0)

        new_rect = self.rect.copy()

        if self.velocidade.x != 0:
            rect_x = new_rect.move(self.velocidade.x, 0)
            if rect_x.left < 0:
                rect_x.left = 0
            if rect_x.right > LARGURA:
                rect_x.right = LARGURA
            if not rect_x.colliderect(self.objeto.plataforma):
                new_rect.x = rect_x.x

        if self.velocidade.y != 0:
            rect_y = new_rect.move(0, self.velocidade.y)
            if rect_y.top < 0:
                rect_y.top = 0
            if rect_y.bottom > ALTURA:
                rect_y.bottom = ALTURA
            if not rect_y.colliderect(self.objeto.plataforma):
                new_rect.y = rect_y.y

        self.image = self.skeleton if self.player.rect.centerx >= self.rect.centerx else self.skeleton_inverso
        self.rect = new_rect
        self.disparo()
        self.atualizar_flechas()
