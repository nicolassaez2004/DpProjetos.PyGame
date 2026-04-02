import pygame

from config.parametros import ALTURA, LARGURA


class Combat:
    def atualizar_animacoes_vento(self):
        agora = pygame.time.get_ticks()

        if self.soco_vento and agora < self.soco_vento_expira_ms and self.soco_vento_frames:
            duracao_total = max(1, self.duracao_vento_ms)
            tempo_decorrido = max(0, agora - self.soco_vento_inicio_ms)
            progresso = min(0.999, tempo_decorrido / duracao_total)
            frame_indice = min(len(self.soco_vento_frames) - 1, int(progresso * len(self.soco_vento_frames)))

            if frame_indice != self.soco_vento_frame_indice:
                centro = self.soco_vento.center
                self.soco_vento_frame_indice = frame_indice
                self.soco_vento_image = self.soco_vento_frames[frame_indice]
                self.soco_vento_image_rotated = pygame.transform.rotate(self.soco_vento_image, self.soco_vento_angulo)
                self.soco_vento = self.soco_vento_image_rotated.get_rect(center=centro)

        if self.espada_vento and agora < self.espada_vento_expira_ms and self.espada_vento_frames:
            duracao_total = max(1, self.duracao_vento_ms)
            tempo_decorrido = max(0, agora - self.espada_vento_inicio_ms)
            progresso = min(0.999, tempo_decorrido / duracao_total)
            frame_indice = min(len(self.espada_vento_frames) - 1, int(progresso * len(self.espada_vento_frames)))

            if frame_indice != self.espada_vento_frame_indice:
                centro = self.espada_vento.center
                self.espada_vento_frame_indice = frame_indice
                self.espada_vento_image = self.espada_vento_frames[frame_indice]
                self.espada_vento_image_rotated = pygame.transform.rotate(self.espada_vento_image, self.espada_vento_angulo)
                self.espada_vento = self.espada_vento_image_rotated.get_rect(center=centro)
                if self.espada_vento_hitbox:
                    self.espada_vento_hitbox.center = self.espada_vento.center

    def criar_flecha(self, posicao, direcao):
        if direcao.length_squared() == 0:
            direcao = pygame.math.Vector2(1, 0)

        sprite = pygame.sprite.Sprite()
        sprite.direcao = direcao.normalize()
        sprite.velocidade = 18
        sprite.damage = 10

        direcao_base_sprite = pygame.math.Vector2(1, -1)
        angulo = -direcao_base_sprite.angle_to(sprite.direcao)
        sprite.image = pygame.transform.rotate(self.arrow_image, angulo)
        sprite.rect = sprite.image.get_rect(center=posicao)
        sprite.mask = pygame.mask.from_surface(sprite.image)
        return sprite

    def atualizar_flecha(self, flecha):
        deslocamento = flecha.direcao * flecha.velocidade
        flecha.rect.move_ip(deslocamento.x, deslocamento.y)

    def flecha_fora_da_tela(self, flecha):
        return (
            flecha.rect.right < 0 or flecha.rect.left > LARGURA or
            flecha.rect.bottom < 0 or flecha.rect.top > ALTURA
        )

    def atualizar_projeteis(self):
        for flecha in list(self.flechas_disparadas):
            self.atualizar_flecha(flecha)
            if self.flecha_fora_da_tela(flecha):
                flecha.kill()

    def ataque_soco(self, mouse_pos):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_soco_ms < self.cooldown_soco_ms:
            if agora >= self.soco_vento_expira_ms:
                self.sprite_idle()
            return
        self.ultimo_soco_ms = agora
        self.soco_vento_expira_ms = agora + self.duracao_vento_ms
        self.image = self.knight_soco if self.olhando_direita else self.knight_soco_flip
        self.mask = pygame.mask.from_surface(self.image)
        direction = pygame.math.Vector2(mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery)
        if direction.length() > 0:
            direction = direction.normalize()
        else:
            direction = pygame.math.Vector2(1, 0)

        wind_distance = 80
        wind_pos = pygame.math.Vector2(self.rect.center) + direction * wind_distance

        self.soco_vento_inicio_ms = agora
        self.soco_vento_frame_indice = 0
        self.soco_vento_image = self.soco_vento_frames[0]
        self.soco_vento_angulo = -pygame.math.Vector2(1, 0).angle_to(direction)
        self.soco_vento_image_rotated = pygame.transform.rotate(self.soco_vento_image, self.soco_vento_angulo)
        self.soco_vento = self.soco_vento_image_rotated.get_rect(center=wind_pos)
        self.espada_vento = None
        self.espada_vento_hitbox = None

    def ataque_espada(self, mouse_pos):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_espada_ms < self.cooldown_espada_ms:
            if agora >= self.espada_vento_expira_ms:
                self.sprite_idle()
            return
        self.ultimo_espada_ms = agora
        self.espada_vento_expira_ms = agora + self.duracao_vento_ms
        self.image = self.knight_golpe_espada if self.olhando_direita else self.knight_golpe_espada_flip
        self.mask = pygame.mask.from_surface(self.image)
        direction = pygame.math.Vector2(mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery)
        if direction.length() > 0:
            direction = direction.normalize()
        else:
            direction = pygame.math.Vector2(1, 0)

        wind_distance = 80
        wind_pos = pygame.math.Vector2(self.rect.center) + direction * wind_distance

        self.espada_vento_inicio_ms = agora
        self.espada_vento_frame_indice = 0
        self.espada_vento_image = self.espada_vento_frames[0]
        self.espada_vento_angulo = -pygame.math.Vector2(1, 0).angle_to(direction)
        self.espada_vento_image_rotated = pygame.transform.rotate(self.espada_vento_image, self.espada_vento_angulo)
        self.espada_vento = self.espada_vento_image_rotated.get_rect(center=wind_pos)
        self.espada_vento_hitbox = pygame.Rect(0, 0, 160, 160)
        self.espada_vento_hitbox.center = self.espada_vento.center
        self.soco_vento = None

    def sprite_idle(self):
        self.atualizar_estado_combate()
        if self.estado_combate == 'soco':
            self.image = self.knight_parado if self.olhando_direita else self.knight_parado_flip
        elif self.estado_combate == 'espada':
            self.image = self.knight_espada if self.olhando_direita else self.knight_espada_flip
        elif self.estado_combate == 'arco_soco':
            self.image = self.knight_arco_soco if self.olhando_direita else self.knight_arco_soco_flip
        elif self.estado_combate == 'arco_espada':
            self.image = self.knight_arco_espada if self.olhando_direita else self.knight_arco_espada_flip
        self.mask = pygame.mask.from_surface(self.image)
        self.soco_vento = None
        self.espada_vento = None
        self.espada_vento_hitbox = None

    def atacar(self):
        self.atualizar_animacoes_vento()
        mouse_pos = pygame.mouse.get_pos()
        botoes_mouse = pygame.mouse.get_pressed()
        self.olhando_direita = (mouse_pos[0] >= self.rect.centerx)
        self.atualizar_estado_combate()

        if botoes_mouse[2] and self.estado_combate in ('arco_soco', 'arco_espada'):
            self.ataque_arco(mouse_pos)
        elif botoes_mouse[0]:
            if self.tem_espada and self.ataque_base == 'espada':
                self.ataque_espada(mouse_pos)
            else:
                self.ataque_soco(mouse_pos)
        else:
            agora = pygame.time.get_ticks()
            soco_ativo = agora < self.soco_vento_expira_ms
            espada_ativa = agora < self.espada_vento_expira_ms
            if not soco_ativo and not espada_ativa:
                self.sprite_idle()

    def ataque_arco(self, mouse_pos):
        self.image = self.knight_arco_espada if self.estado_combate == 'arco_espada' else self.knight_arco_soco
        if not self.olhando_direita:
            self.image = self.knight_arco_espada_flip if self.estado_combate == 'arco_espada' else self.knight_arco_soco_flip

        self.mask = pygame.mask.from_surface(self.image)
        self.soco_vento = None
        self.espada_vento = None
        self.espada_vento_hitbox = None

        if self.flechas <= 0:
            return

        agora = pygame.time.get_ticks()
        if agora - self.ultimo_disparo_flecha_ms < self.cooldown_flecha_ms:
            return

        direcao = pygame.math.Vector2(mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery)
        if direcao.length_squared() == 0:
            direcao = pygame.math.Vector2(1, 0)

        origem = pygame.math.Vector2(self.rect.center) + direcao.normalize() * 48
        flecha = self.criar_flecha(origem, direcao)
        self.flechas_disparadas.add(flecha)
        self.flechas -= 1
        self.ultimo_disparo_flecha_ms = agora