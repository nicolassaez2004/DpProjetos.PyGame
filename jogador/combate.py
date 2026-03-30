import pygame


class Combat:
    def _ataque_soco(self, mouse_pos):
        self.image = self.knight_soco if self.olhando_direita else self.knight_soco_flip
        self.mask = pygame.mask.from_surface(self.image)
        direction = pygame.math.Vector2(mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery)
        if direction.length() > 0:
            direction = direction.normalize()
        else:
            direction = pygame.math.Vector2(1, 0)

        wind_distance = 80
        wind_pos = pygame.math.Vector2(self.rect.center) + direction * wind_distance

        angulo = -pygame.math.Vector2(1, 0).angle_to(direction)
        self.soco_vento_image_rotated = pygame.transform.rotate(self.soco_vento_image, angulo)
        self.soco_vento = self.soco_vento_image_rotated.get_rect(center=wind_pos)
        self.espada_vento = None
        self.espada_vento_hitbox = None

    def _ataque_espada(self, mouse_pos):
        self.image = self.knight_golpe_espada if self.olhando_direita else self.knight_golpe_espada_flip
        self.mask = pygame.mask.from_surface(self.image)
        direction = pygame.math.Vector2(mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery)
        if direction.length() > 0:
            direction = direction.normalize()
        else:
            direction = pygame.math.Vector2(1, 0)

        wind_distance = 80
        wind_pos = pygame.math.Vector2(self.rect.center) + direction * wind_distance

        angulo = -pygame.math.Vector2(1, 0).angle_to(direction)
        self.espada_vento_image_rotated = pygame.transform.rotate(self.espada_vento_image, angulo)
        self.espada_vento = self.espada_vento_image_rotated.get_rect(center=wind_pos)
        self.espada_vento_hitbox = pygame.Rect(0, 0, 160, 160)
        self.espada_vento_hitbox.center = self.espada_vento.center
        self.soco_vento = None

    def _sprite_idle(self):
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
        mouse_pos = pygame.mouse.get_pos()
        self.olhando_direita = (mouse_pos[0] >= self.rect.centerx)

        if pygame.mouse.get_pressed()[0]:
            if self.tem_espada and self.ataque_base == 'espada':
                self._ataque_espada(mouse_pos)
            else:
                self._ataque_soco(mouse_pos)
        else:
            self._sprite_idle()

    def soco(self):
        self.atacar()

    def espada(self):
        pass

    def arco(self):
        pass