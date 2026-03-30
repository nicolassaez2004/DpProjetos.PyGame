import pygame

from enemies.ghost import Ghost
from enemies.skeleton import Skeleton
from enemies.wizard import Wizard
from jogo.objetos import Object
from jogo.gameplay import Gameplay
from config import parametros
from config.parametros import ALTURA, LARGURA, PRETO, ASSETS, FPS
from jogo.spawn import Spawn


class Game:
    def __init__(self):
        self.rodando = True
        pygame.init()
        self.spawn = Spawn()

        self.bg = pygame.image.load(ASSETS + 'background.jpg')
        self.bg = pygame.transform.scale(self.bg, (1280, 720))
        self.window = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption('Claustrophobia Knight')

        self.relogio = pygame.time.Clock()

        self.font_score = pygame.font.SysFont(None, 64)
        self.font_money = pygame.font.SysFont(None, 56)
        self.font_hud = pygame.font.SysFont(None, 52)
        self.font_hud_valor = pygame.font.SysFont(None, 40)

        self.mouse_pos = pygame.Rect((0, 0), (0, 0))
        self.player = Gameplay((LARGURA/2 - 40, ALTURA/2 - 40))

        self.objeto = Object()

        self.todo_mundo = pygame.sprite.Group([self.player])
        self.tipos_inimigos = [Skeleton, Wizard, Ghost]
        self.spawn_cooldown_ms = 900
        self.ultimo_spawn_ms = pygame.time.get_ticks()

        self.spawn.player = self.player
        self.spawn.objeto = self.objeto
        self.spawn.tipos_inimigos = self.tipos_inimigos
        self.spawn.spawn_cooldown_ms = self.spawn_cooldown_ms
        self.spawn.ultimo_spawn_ms = self.ultimo_spawn_ms

        for _ in range(self.player.limite_inimigos):
            self.spawn.spawn_inimigo()
        
        self.pode_comprar_espada = False
        self.pode_interagir_bau = False
        self.pode_interagir_kit = False
        self.pode_interagir_arco = False

    def desenhar_barra(self, pos, tamanho, valor_atual, valor_maximo, cor_preenchimento, cor_fundo):
        barra_rect = pygame.Rect(pos, tamanho)
        pygame.draw.rect(self.window, cor_fundo, barra_rect)
        pygame.draw.rect(self.window, (255, 255, 255), barra_rect, 2)

        if valor_maximo <= 0:
            return

        proporcao = max(0, min(valor_atual / valor_maximo, 1))
        largura_preenchida = int((tamanho[0] - 4) * proporcao)
        if largura_preenchida > 0:
            preenchimento_rect = pygame.Rect(pos[0] + 2, pos[1] + 2, largura_preenchida, tamanho[1] - 4)
            pygame.draw.rect(self.window, cor_preenchimento, preenchimento_rect)


    def desenhar(self):
        self.window.fill(PRETO)
        self.window.blit(self.bg, (0, 0))
        self.window.blit(self.objeto.bau, (400, 160))
        self.window.blit(self.objeto.kitmedico, (800, 160))
        self.window.blit(self.objeto.arco, (400, 480))   
        self.window.blit(self.objeto.espada, (800, 480))        

        for inimigo in self.spawn.inimigos:
            if inimigo.alive() and inimigo.health > 0:
                inimigo.movimentacao()

        score_text = self.font_score.render(f'SCORE: {self.player.score}', True, (255, 255, 255))
        money_text = self.font_money.render(f'${self.player.dinheiro}', True, (255, 215, 0))

        score_rect = score_text.get_rect(center=(LARGURA // 2, 40))
        money_rect = money_text.get_rect(center=(LARGURA // 2, 90))

        self.window.blit(score_text, score_rect)
        self.window.blit(money_text, money_rect)

        vida_label = self.font_hud.render('VIDA', True, (255, 255, 255))
        self.window.blit(vida_label, (24, 70))
        self.desenhar_barra((105, 77), (200, 34), self.player.vida, self.player.max_vida, (0, 255, 0), (40, 40, 40))
        vida_text = self.font_hud_valor.render(f'{self.player.vida}/{self.player.max_vida}', True, (255, 255, 255))
        self.window.blit(vida_text, (315, 79))

        flecha_label = self.font_hud.render('FLECHA', True, (255, 255, 255))
        self.window.blit(flecha_label, (905, 70))
        self.desenhar_barra((1025, 77), (200, 34), self.player.flechas, self.player.max_flechas, (255, 60, 60), (40, 40, 40))
        flecha_text = self.font_hud_valor.render(f'{self.player.flechas}/{self.player.max_flechas}', True, (255, 255, 255))
        self.window.blit(flecha_text, (1230, 79))

        nivel_text_outline = self.font_hud.render(f'Nivel: {self.player.nivel}', True, (10, 35, 90))
        nivel_text = self.font_hud.render(f'Nivel: {self.player.nivel}', True, (95, 210, 255))
        nivel_rect = nivel_text.get_rect(center=(self.objeto.plataforma.centerx, self.objeto.plataforma.bottom + 48))
        self.window.blit(nivel_text_outline, (nivel_rect.x + 2, nivel_rect.y + 2))
        self.window.blit(nivel_text, nivel_rect)

        if self.pode_comprar_espada:
            buy_text = self.font_money.render("aperte E para comprar espada (1$)", True, (255, 255, 255))
            buy_rect = buy_text.get_rect(center=(LARGURA // 2, ALTURA // 2))
            self.window.blit(buy_text, buy_rect)
        elif self.pode_interagir_bau:
            if self.player.tem_arco:
                if self.player.flechas >= self.player.max_flechas:
                    flechas_text = self.font_money.render("Você já tem o máximo de flechas possíveis", True, (255, 255, 255))
                else:
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
            if self.player.estado_combate in ('arco_soco', 'arco_espada'):
                arco_text = self.font_money.render("você já comprou um arco", True, (255, 255, 255))
            else:
                arco_text = self.font_money.render("aperte E para comprar arco (1$)", True, (255, 255, 255))
            arco_rect = arco_text.get_rect(center=(LARGURA // 2, ALTURA // 2))
            self.window.blit(arco_text, arco_rect)

        mouse_pos = pygame.mouse.get_pos()
        tamanho_mouse = 10
        self.mouse_pos = pygame.Rect(mouse_pos[0], mouse_pos[1], tamanho_mouse, tamanho_mouse)
        pygame.draw.rect(self.window, parametros.MOUSE_COLOR, self.mouse_pos)
        
        self.todo_mundo.draw(self.window)
        self.spawn.inimigos.draw(self.window)
        self.player.flechas_disparadas.draw(self.window)
        for inimigo in self.spawn.inimigos:
            if isinstance(inimigo, Skeleton):
                inimigo.flechas_disparadas.draw(self.window)
            elif isinstance(inimigo, Wizard):
                inimigo.fireballs_disparadas.draw(self.window)
        if self.player.soco_vento:
            self.window.blit(self.player.soco_vento_image_rotated, self.player.soco_vento)
        if self.player.espada_vento:
            self.window.blit(self.player.espada_vento_image_rotated, self.player.espada_vento)
        pygame.display.update()

    def colisoes(self): #testador de colisões
        parametros.MOUSE_COLOR = (255, 255, 255)
        if any(self.mouse_pos.colliderect(inimigo.rect) for inimigo in self.spawn.inimigos):
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

        for inimigo in list(self.spawn.inimigos):
            if not isinstance(inimigo, Ghost):
                continue

            if not self.player.rect.colliderect(inimigo.rect):
                continue

            mascara_inimigo = pygame.mask.from_surface(inimigo.image)
            offset = (inimigo.rect.x - self.player.rect.x, inimigo.rect.y - self.player.rect.y)
            if self.player.mask.overlap(mascara_inimigo, offset):
                inimigo.kill()
                self.player.vida = max(0, self.player.vida - 1)

        if self.player.soco_vento:
            for inimigo in list(self.spawn.inimigos):
                if self.player.soco_vento.colliderect(inimigo.rect) and inimigo.health > 0:
                    inimigo.health -= 5
                    if inimigo.health <= 0:
                        inimigo.kill()
                        self.player.capitalizacao(inimigo)

        if self.player.espada_vento_hitbox:
            for inimigo in list(self.spawn.inimigos):
                if self.player.espada_vento_hitbox.colliderect(inimigo.rect) and inimigo.health > 0:
                    inimigo.health -= 5
                    if inimigo.health <= 0:
                        inimigo.kill()
                        self.player.capitalizacao(inimigo)

        for flecha in list(self.player.flechas_disparadas):
            for inimigo in list(self.spawn.inimigos):
                if isinstance(inimigo, Ghost):
                    continue

                if inimigo.health <= 0 or not flecha.rect.colliderect(inimigo.rect):
                    continue

                mascara_inimigo = pygame.mask.from_surface(inimigo.image)
                offset = (inimigo.rect.x - flecha.rect.x, inimigo.rect.y - flecha.rect.y)
                if flecha.mask.overlap(mascara_inimigo, offset):
                    inimigo.health -= flecha.damage
                    flecha.kill()
                    if inimigo.health <= 0:
                        inimigo.kill()
                        self.player.capitalizacao(inimigo)
                    break

        for inimigo in self.spawn.inimigos:
            if not isinstance(inimigo, Skeleton):
                continue

            for flecha in list(inimigo.flechas_disparadas):
                if not flecha.rect.colliderect(self.player.rect):
                    continue

                offset = (self.player.rect.x - flecha.rect.x, self.player.rect.y - flecha.rect.y)
                if flecha.mask.overlap(self.player.mask, offset):
                    flecha.kill()
                    self.player.vida = max(0, self.player.vida - 1)

        for inimigo in self.spawn.inimigos:
            if not isinstance(inimigo, Wizard):
                continue

            for fireball in list(inimigo.fireballs_disparadas):
                if not fireball.rect.colliderect(self.player.rect):
                    continue

                offset = (self.player.rect.x - fireball.rect.x, self.player.rect.y - fireball.rect.y)
                if fireball.mask.overlap(self.player.mask, offset):
                    fireball.kill()
                    self.player.vida = max(0, self.player.vida - 1)

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
                    elif event.key == pygame.K_e and self.pode_interagir_arco and self.player.dinheiro >= 1 and self.player.estado_combate not in ('arco_soco', 'arco_espada'):
                        self.player.dinheiro -= 1
                        self.player.equipar_arco()
                        self.pode_interagir_arco = False
                    elif event.key == pygame.K_e and self.pode_interagir_bau and self.player.dinheiro >= 1 and self.player.flechas < self.player.max_flechas:
                        self.player.dinheiro -= 1
                        self.player.flechas = min(self.player.flechas + 5, self.player.max_flechas)
                        self.pode_interagir_bau = False
                    elif event.key == pygame.K_e and self.pode_interagir_kit and self.player.vida < 10 and self.player.dinheiro >= 1:
                        self.player.dinheiro -= 1
                        self.player.vida = min(self.player.vida + 1, self.player.max_vida)
                        self.pode_interagir_kit = False

            self.player.movimentacao()
            self.player.atacar()
            self.player.atualizar_projeteis()
            self.desenhar()
            self.colisoes()
            self.spawn.atualizar_spawn_inimigos()
            self.relogio.tick(FPS)

        pygame.quit()