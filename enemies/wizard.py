import pygame
import random
from enemies.enemy import Enemy
from config.parametros import LARGURA, ALTURA, ASSETS


class Wizard(Enemy):
    def __init__(self, posicao):
        super().__init__(posicao)
        self.health = 10

        aux = pygame.image.load(ASSETS + 'wizard.png')
        self.wizard = pygame.transform.scale(aux, (80, 80))
        self.wizard_flip = pygame.transform.flip(self.wizard, True, False)

        wizard_spawn_sheet = pygame.image.load(ASSETS + 'wizard_spawnando.png').convert_alpha()
        self.wizard_spawn_frames = []
        for linha in range(2):
            for coluna in range(2):
                area_frame = pygame.Rect(coluna * 16, linha * 16, 16, 16)
                frame = pygame.Surface((16, 16), pygame.SRCALPHA)
                frame.blit(wizard_spawn_sheet, (0, 0), area_frame)
                self.wizard_spawn_frames.append(pygame.transform.scale(frame, (80, 80)))
        self.image = self.wizard_spawn_frames[0]
        self.spawn_duracao_ms = 1000
        self.spawn_inicio_ms = pygame.time.get_ticks()

        self.estado = "spawnando"
        self.timer = 0  
        self.direcao = pygame.math.Vector2(0, 0)
        self.distancia_percorrida = 0

        self.direcaorandom = 0
        self.fireball_image = pygame.transform.scale(pygame.image.load(ASSETS + 'fireball_wizard.png'), (80, 80))
        self.fireballs_disparadas = pygame.sprite.Group()
        self.cooldown_disparo_ms = 3600
        self.ultimo_disparo_ms = pygame.time.get_ticks()

    def criar_fireball(self, direcao):
        if direcao.length_squared() == 0:
            direcao = pygame.math.Vector2(1, 0)

        nivel_atual = getattr(self.player, 'nivel', 1)
        multiplicador_nivel = 1 + (max(nivel_atual, 1) - 1) * 0.10

        fireball = pygame.sprite.Sprite()
        fireball.direcao = direcao.normalize()
        fireball.velocidade = 2 * multiplicador_nivel
        fireball.damage = 1
        fireball.angulo = 0
        fireball.rotacao_por_frame = -3
        fireball.base_image = self.fireball_image

        fireball.image = fireball.base_image
        fireball.rect = fireball.image.get_rect(center=self.rect.center)
        fireball.mask = pygame.mask.from_surface(fireball.image)
        return fireball

    def atualizar_fireballs(self):
        for fireball in list(self.fireballs_disparadas):
            centro_anterior = fireball.rect.center
            fireball.angulo += fireball.rotacao_por_frame
            fireball.image = pygame.transform.rotate(fireball.base_image, fireball.angulo)
            fireball.rect = fireball.image.get_rect(center=centro_anterior)
            fireball.mask = pygame.mask.from_surface(fireball.image)

            deslocamento = fireball.direcao * fireball.velocidade
            fireball.rect.move_ip(deslocamento.x, deslocamento.y)
            if (
                fireball.rect.right < 0 or fireball.rect.left > LARGURA or
                fireball.rect.bottom < 0 or fireball.rect.top > ALTURA
            ):
                fireball.kill()

    def disparo(self):
        agora = pygame.time.get_ticks()
        if (agora - self.ultimo_disparo_ms) < self.cooldown_disparo_ms:
            return

        if len(self.fireballs_disparadas) >= 1:
            return

        direcao = pygame.math.Vector2(
            self.player.rect.centerx - self.rect.centerx,
            self.player.rect.centery - self.rect.centery
        )

        fireball = self.criar_fireball(direcao)
        self.fireballs_disparadas.add(fireball)
        self.ultimo_disparo_ms = agora

    def spawn_wizard(self):
        while True:
            x = random.randint(80, 1200 - 80)
            y = random.randint(80, 640 - 80)
            rect = pygame.Rect(x, y, 80, 80)
            if not rect.colliderect(self.objeto.plataforma):
                return (x, y)

    def movimentacao(self):
        if self.estado == "spawnando":
            self.velocidade = pygame.math.Vector2(0, 0)
            agora = pygame.time.get_ticks()
            tempo_spawn = agora - self.spawn_inicio_ms

            progresso = min(0.999, max(0, tempo_spawn) / self.spawn_duracao_ms)
            frame_indice = min(len(self.wizard_spawn_frames) - 1, int(progresso * len(self.wizard_spawn_frames)))
            self.image = self.wizard_spawn_frames[frame_indice]

            if tempo_spawn >= self.spawn_duracao_ms:
                self.estado = "parado"
                self.timer = 0
                self.image = self.wizard if self.player.rect.centerx >= self.rect.centerx else self.wizard_flip
            self.atualizar_fireballs()
            return
        
        if self.estado == "parado":
            self.velocidade = pygame.math.Vector2(0, 0)
            self.timer += 1
            if self.timer > 60:
                self.timer = 0
                self.estado = random.choice(["movendo", "parado"])
        
        if self.estado == "movendo":
            if self.timer == 0:
                direcoes = [
                    pygame.math.Vector2(1, 1),
                    pygame.math.Vector2(1, -1),
                    pygame.math.Vector2(-1, 1),
                    pygame.math.Vector2(-1, -1)
                ]
                self.direcao = random.choice(direcoes).normalize()
                self.velocidade = self.direcao * self.speed
            self.timer += 1
            if self.timer > 120:  
                self.timer = 0
                self.estado = "parado"
        
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

        self.image = self.wizard if self.player.rect.centerx >= self.rect.centerx else self.wizard_flip
        self.rect = new_rect
        self.disparo()
        self.atualizar_fireballs()
