import pygame

from config import parametros
from config.parametros import FPS


class Colisoes:
    def colisoes(self): #testador de colisões
        parametros.MOUSE_COLOR = (255, 255, 255)
        if self.mouse_pos.colliderect(self.skeleton.rect):
            parametros.MOUSE_COLOR = (0, 255, 0)
        elif self.mouse_pos.colliderect(self.objeto.plataforma):
            parametros.MOUSE_COLOR = (125, 0, 0)
            
        if self.mouse_pos.colliderect(self.objeto.colisao_bau):
            parametros.MOUSE_COLOR = (0, 0, 255)
        if self.mouse_pos.colliderect(self.objeto.colisao_kitmedico):
            parametros.MOUSE_COLOR = (0, 0, 255)
        if self.mouse_pos.colliderect(self.objeto.colisao_arco):
            parametros.MOUSE_COLOR = (0, 0, 255)
        if self.mouse_pos.colliderect(self.objeto.colisao_espada):
            parametros.MOUSE_COLOR = (0, 0, 255)

        if self.player.rect.colliderect(self.objeto.colisao_espada):
            self.pode_comprar_espada = True
        else:
            self.pode_comprar_espada = False

        if self.player.rect.colliderect(self.objeto.colisao_bau):
            self.pode_interagir_bau = True
        else:
            self.pode_interagir_bau = False

        if self.player.rect.colliderect(self.objeto.colisao_kitmedico):
            self.pode_interagir_kit = True
        else:
            self.pode_interagir_kit = False

        if self.player.rect.colliderect(self.objeto.colisao_arco):
            self.pode_interagir_arco = True
        else:
            self.pode_interagir_arco = False

        if self.player.soco_vento:
            if self.player.soco_vento.colliderect(self.skeleton.rect) and self.skeleton.health > 0:
                self.skeleton.health -= 5
                if self.skeleton.health <= 0:
                    self.skeleton.kill()
                    self.player.capitalizacao(self.skeleton)
            if self.player.soco_vento.colliderect(self.wizard.rect) and self.wizard.health > 0:
                self.wizard.health -= 5
                if self.wizard.health <= 0:
                    self.wizard.kill()
                    self.player.capitalizacao(self.wizard)
            if self.player.soco_vento.colliderect(self.ghost.rect) and self.ghost.health > 0:
                self.ghost.health -= 5
                if self.ghost.health <= 0:
                    self.ghost.kill()
                    self.player.capitalizacao(self.ghost)

        if self.player.espada_vento_hitbox:
            if self.player.espada_vento_hitbox.colliderect(self.skeleton.rect) and self.skeleton.health > 0:
                self.skeleton.health -= 5
                if self.skeleton.health <= 0:
                    self.skeleton.kill()
                    self.player.capitalizacao(self.skeleton)
            if self.player.espada_vento_hitbox.colliderect(self.wizard.rect) and self.wizard.health > 0:
                self.wizard.health -= 5
                if self.wizard.health <= 0:
                    self.wizard.kill()
                    self.player.capitalizacao(self.wizard)
            if self.player.espada_vento_hitbox.colliderect(self.ghost.rect) and self.ghost.health > 0:
                self.ghost.health -= 5
                if self.ghost.health <= 0:
                    self.ghost.kill()
                    self.player.capitalizacao(self.ghost)

    def executar(self):
        while self.rodando:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.rodando = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e and self.pode_comprar_espada and self.player.dinheiro >= 1:
                        self.player.dinheiro -= 1
                        self.player.equipar_espada()
                        self.pode_comprar_espada = False
                    elif event.key == pygame.K_e and self.pode_interagir_arco and self.player.dinheiro >= 1:
                        self.player.dinheiro -= 1
                        self.player.equipar_arco()
                        self.pode_interagir_arco = False
                    elif event.key == pygame.K_e and self.pode_interagir_bau and self.player.dinheiro >= 1:
                        self.player.dinheiro -= 1
                        self.player.flechas = min(self.player.flechas + 5, 30)
                        self.pode_interagir_bau = False
                    elif event.key == pygame.K_e and self.pode_interagir_kit and self.player.vida < 10 and self.player.dinheiro >= 1:
                        self.player.dinheiro -= 1
                        self.player.vida = min(self.player.vida + 1, 10)
                        self.pode_interagir_kit = False

            self.player.movimentacao()
            self.player.atacar()
            self.desenhar()
            self.colisoes()
            self.relogio.tick(FPS)

        pygame.quit()
