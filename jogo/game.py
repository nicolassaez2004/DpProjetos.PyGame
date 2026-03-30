import pygame
import random

from enemies.ghost import Ghost
from enemies.skeleton import Skeleton
from enemies.wizard import Wizard
from jogo.colisoes import Colisoes
from jogo.objetos import Object
from jogo.gameplay import Gameplay
from config import parametros
from config.parametros import ALTURA, LARGURA, PRETO, ASSETS


class Game(Colisoes):
    def __init__(self):
        self.rodando = True
        pygame.init()

        self.bg = pygame.image.load(ASSETS + 'background.jpg')
        self.bg = pygame.transform.scale(self.bg, (1280, 720))
        self.window = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption('Claustrophobia Knight')

        self.relogio = pygame.time.Clock()

        self.font_score = pygame.font.SysFont(None, 64)
        self.font_money = pygame.font.SysFont(None, 56)

        self.mouse_pos = pygame.Rect((0, 0), (0, 0))
        self.player = Gameplay((LARGURA/2 - 40, ALTURA/2 - 40))

        self.objeto = Object()

        self.todo_mundo = pygame.sprite.Group([self.player])
        self.inimigos = pygame.sprite.Group()
        self.tipos_inimigos = [Skeleton, Wizard, Ghost]
        self.spawn_cooldown_ms = 900
        self.ultimo_spawn_ms = pygame.time.get_ticks()

        for _ in range(self.player.limite_inimigos):
            self.spawn_inimigo()
        
        self.pode_comprar_espada = False
        self.pode_interagir_bau = False
        self.pode_interagir_kit = False
        self.pode_interagir_arco = False

    def spawn_inimigo(self):
        tipo_inimigo = random.choice(self.tipos_inimigos)
        inimigo = tipo_inimigo((0, 0))
        inimigo.player = self.player
        inimigo.objeto = self.objeto

        if isinstance(inimigo, Wizard):
            pos_spawn = inimigo.spawn_wizard()
        else:
            pos_spawn = inimigo.random_spawn()

        inimigo.rect.topleft = pos_spawn
        self.player.aplicar_scaling_inimigo(inimigo)
        self.inimigos.add(inimigo)

    def atualizar_spawn_inimigos(self):
        agora = pygame.time.get_ticks()
        if len(self.inimigos) < self.player.limite_inimigos and (agora - self.ultimo_spawn_ms) >= self.spawn_cooldown_ms:
            self.spawn_inimigo()
            self.ultimo_spawn_ms = agora

    def desenhar(self):
        self.window.fill(PRETO)
        self.window.blit(self.bg, (0, 0))
        self.window.blit(self.objeto.bau, (400, 160))
        self.window.blit(self.objeto.kitmedico, (800, 160))
        self.window.blit(self.objeto.arco, (400, 480))   
        self.window.blit(self.objeto.espada, (800, 480))        

        for inimigo in self.inimigos:
            if inimigo.alive() and inimigo.health > 0:
                inimigo.movimentacao()

        score_text = self.font_score.render(f'SCORE: {self.player.score}', True, (255, 255, 255))
        money_text = self.font_money.render(f'${self.player.dinheiro}', True, (255, 215, 0))

        score_rect = score_text.get_rect(center=(LARGURA // 2, 40))
        money_rect = money_text.get_rect(center=(LARGURA // 2, 90))

        self.window.blit(score_text, score_rect)
        self.window.blit(money_text, money_rect)

        if self.pode_comprar_espada:
            buy_text = self.font_money.render("aperte E para comprar espada (1$)", True, (255, 255, 255))
            buy_rect = buy_text.get_rect(center=(LARGURA // 2, ALTURA // 2))
            self.window.blit(buy_text, buy_rect)
        elif self.pode_interagir_bau:
            if self.player.tem_arco:
                flechas_text = self.font_money.render("aperte E para comprar flechas (1$)", True, (255, 255, 255))
                flechas_rect = flechas_text.get_rect(center=(LARGURA // 2, ALTURA // 2))
                self.window.blit(flechas_text, flechas_rect)
            else:
                msg_text = self.font_money.render("você precisa de um arco.", True, (255, 255, 255))
                msg_rect = msg_text.get_rect(center=(LARGURA // 2, ALTURA // 2))
                self.window.blit(msg_text, msg_rect)
        elif self.pode_interagir_kit:
            if self.player.vida < 10:
                kit_text = self.font_money.render("aperte E para usar kitmedico (1$)", True, (255, 255, 255))
            else:
                kit_text = self.font_money.render("vida cheia!", True, (255, 255, 255))
            kit_rect = kit_text.get_rect(center=(LARGURA // 2, ALTURA // 2))
            self.window.blit(kit_text, kit_rect)
        elif self.pode_interagir_arco:
            arco_text = self.font_money.render("aperte E para comprar arco (1$)", True, (255, 255, 255))
            arco_rect = arco_text.get_rect(center=(LARGURA // 2, ALTURA // 2))
            self.window.blit(arco_text, arco_rect)

        mouse_pos = pygame.mouse.get_pos()
        tamanho_mouse = 10
        self.mouse_pos = pygame.Rect(mouse_pos[0], mouse_pos[1], tamanho_mouse, tamanho_mouse)
        pygame.draw.rect(self.window, parametros.MOUSE_COLOR, self.mouse_pos)
        
        self.todo_mundo.draw(self.window)
        self.inimigos.draw(self.window)
        if self.player.soco_vento:
            self.window.blit(self.player.soco_vento_image_rotated, self.player.soco_vento)
        if self.player.espada_vento:
            self.window.blit(self.player.espada_vento_image_rotated, self.player.espada_vento)
        pygame.display.update()