import pygame

from jogador.guerreiro import Guerreiro
from config.parametros import ASSETS


class Player(Guerreiro, pygame.sprite.Sprite):
    def __init__(self, posicao):
        super(Player, self).__init__()
        aux_movimento = ['parado', 'andando', 'batendo']
        size = (80, 80)
        self.tem_arco = False
        self.tem_espada = False
        self.ataque_base = 'soco'
        self.estado_combate = 'soco'
        self.estado_movimento = aux_movimento[0]

        self.sprites_parado = {}
        self.sprites_andando = {}
        self.sprites_parado_flip = {}
        self.sprites_andando_flip = {}
        
        self.carregar_sprites_animacao()
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
        
        self.frame_animacao_atual = 0
        self.tempo_frame_ms = 150
        self.ultimo_update_frame_ms = pygame.time.get_ticks()
        
        self.soco_vento = None
        soco_vento_sheet = pygame.image.load(ASSETS + 'soco_vento.png').convert_alpha()
        self.soco_vento_frames = []
        for linha in range(2):
            for coluna in range(2):
                area_frame = pygame.Rect(coluna * 16, linha * 16, 16, 16)
                frame = pygame.Surface((16, 16), pygame.SRCALPHA)
                frame.blit(soco_vento_sheet, (0, 0), area_frame)
                self.soco_vento_frames.append(pygame.transform.scale(frame, (80, 80)))
        self.soco_vento_image = self.soco_vento_frames[0]
        self.soco_vento_image_rotated = self.soco_vento_image
        self.soco_vento_frame_indice = 0
        self.soco_vento_inicio_ms = 0
        self.soco_vento_angulo = 0
        
        self.espada_vento = None
        self.espada_vento_hitbox = None
        espada_vento_sheet = pygame.image.load(ASSETS + 'espada_vento.png').convert_alpha()
        self.espada_vento_frames = []
        for linha in range(2):
            for coluna in range(2):
                area_frame = pygame.Rect(coluna * 32, linha * 32, 32, 32)
                frame = pygame.Surface((32, 32), pygame.SRCALPHA)
                frame.blit(espada_vento_sheet, (0, 0), area_frame)
                self.espada_vento_frames.append(pygame.transform.scale(frame, (160, 160)))
        self.espada_vento_image = self.espada_vento_frames[0]
        self.espada_vento_image_rotated = self.espada_vento_image
        self.espada_vento_frame_indice = 0
        self.espada_vento_inicio_ms = 0
        self.espada_vento_angulo = 0

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
        self.dano_flash_inicio_ms = 0
        self.dano_flash_duracao_ms = 300

        self.som_player_arrow = pygame.mixer.Sound('assets/sons/sound_playerarrow.mp3')
        
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
        
        self.atualizar_sprite_movimento()

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

    def carregar_sprites_animacao(self):
        size_animacao = (80, 80)
        
        sprite_files = {
            'soco': ('knight_parado', 'knight_andando'),
            'arco_soco': ('knightarco_parado', 'knightarco_andando'),
            'espada': ('knightespada_parado', 'knightespada_andando'),
            'arco_espada': ('knightarcoespada_parado', 'knightarcoespada_andando')
        }
        
        for estado_combate, (arquivo_parado, arquivo_andando) in sprite_files.items():
            try:
                spritesheet_parado = pygame.image.load(ASSETS + arquivo_parado + '.png').convert_alpha()
                frames_parado = self.extrair_frames_spritesheet(spritesheet_parado, size_animacao)
                self.sprites_parado[estado_combate] = frames_parado
                self.sprites_parado_flip[estado_combate] = [pygame.transform.flip(frame, True, False) for frame in frames_parado]
                print(f"✓ Carregado: {arquivo_parado}.png ({len(frames_parado)} frames)")
            except (pygame.error, FileNotFoundError) as e:
                print(f"✗ Não encontrado: {arquivo_parado}.png - {e}")
            
            try:
                spritesheet_andando = pygame.image.load(ASSETS + arquivo_andando + '.png').convert_alpha()
                frames_andando = self.extrair_frames_spritesheet(spritesheet_andando, size_animacao)
                self.sprites_andando[estado_combate] = frames_andando
                self.sprites_andando_flip[estado_combate] = [pygame.transform.flip(frame, True, False) for frame in frames_andando]
                print(f"✓ Carregado: {arquivo_andando}.png ({len(frames_andando)} frames)")
            except (pygame.error, FileNotFoundError) as e:
                print(f"✗ Não encontrado: {arquivo_andando}.png - {e}")

    def extrair_frames_spritesheet(self, spritesheet, size_final, linhas=2, colunas=2):
        tamanho_frame = 16
        frames = []
        
        for linha in range(linhas):
            for coluna in range(colunas):
                area_frame = pygame.Rect(coluna * tamanho_frame, linha * tamanho_frame, tamanho_frame, tamanho_frame)
                frame = pygame.Surface((tamanho_frame, tamanho_frame), pygame.SRCALPHA)
                frame.blit(spritesheet, (0, 0), area_frame)
                frame_escalado = pygame.transform.scale(frame, size_final)
                frames.append(frame_escalado)
        
        return frames

    def atualizar_sprite_movimento(self):
        agora = pygame.time.get_ticks()
        
        self.atualizar_estado_combate()
        
        if agora >= self.soco_vento_expira_ms:
            self.soco_vento = None
        if agora >= self.espada_vento_expira_ms:
            self.espada_vento = None
            self.espada_vento_hitbox = None
        
        soco_ativo = agora < self.soco_vento_expira_ms
        espada_ativa = agora < self.espada_vento_expira_ms
        
        if soco_ativo or espada_ativa:
            return
        
        esta_andando = self.velocidade.x != 0 or self.velocidade.y != 0
        
        if agora - self.ultimo_update_frame_ms >= self.tempo_frame_ms:
            self.frame_animacao_atual = (self.frame_animacao_atual + 1) % 4
            self.ultimo_update_frame_ms = agora
        
        frames = None
        if esta_andando:
            if self.estado_combate in self.sprites_andando:
                frames = self.sprites_andando[self.estado_combate] if self.olhando_direita else self.sprites_andando_flip[self.estado_combate]
        
        if frames is None:
            if self.estado_combate in self.sprites_parado:
                frames = self.sprites_parado[self.estado_combate] if self.olhando_direita else self.sprites_parado_flip[self.estado_combate]
        
        if frames:
            self.image = frames[self.frame_animacao_atual]
            self.mask = pygame.mask.from_surface(self.image)