import pygame

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

        self.skeleton = Skeleton((0, 0))
        spawn_pos = self.skeleton.random_spawn()
        self.skeleton.rect.topleft = spawn_pos
        self.skeleton.player = self.player
        self.skeleton.objeto = self.objeto

        self.wizard = Wizard((0, 0))
        self.wizard.player = self.player
        self.wizard.objeto = self.objeto
        spawn_wizard_pos = self.wizard.spawn_wizard()
        self.wizard.rect.topleft = spawn_wizard_pos

        self.ghost = Ghost((0, 0))
        self.ghost.player = self.player
        self.ghost.objeto = self.objeto
        spawn_ghost_pos = self.ghost.random_spawn()
        self.ghost.rect.topleft = spawn_ghost_pos

        self.todo_mundo = pygame.sprite.Group([self.player, self.skeleton, self.wizard, self.ghost])
        
        self.pode_comprar_espada = False
        self.pode_interagir_bau = False
        self.pode_interagir_kit = False
        self.pode_interagir_arco = False

    def desenhar(self):
        self.window.fill(PRETO)
        self.window.blit(self.bg, (0, 0))
        self.window.blit(self.objeto.bau, (400, 160))
        self.window.blit(self.objeto.kitmedico, (800, 160))
        self.window.blit(self.objeto.arco, (400, 480))   
        self.window.blit(self.objeto.espada, (800, 480))        

        if self.skeleton.alive() and self.skeleton.health > 0:
            self.skeleton.movimentacao()
        if self.wizard.alive() and self.wizard.health > 0:
            self.wizard.movimentacao()
        if self.ghost.alive() and self.ghost.health > 0:
            self.ghost.movimentacao()

        self.todo_mundo.update()

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
        if self.player.soco_vento:
            self.window.blit(self.player.soco_vento_image_rotated, self.player.soco_vento)
        if self.player.espada_vento:
            self.window.blit(self.player.espada_vento_image_rotated, self.player.espada_vento)
        pygame.display.update()