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
    def __init__(self, player_name='Jogador'):
        self.rodando = True
        self.player_name = player_name
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
        self.font_tempo = pygame.font.SysFont(None, 62)
        self.font_overlay_titulo = pygame.font.SysFont(None, 92)
        self.font_overlay_texto = pygame.font.SysFont(None, 58)
        self.font_overlay_hint = pygame.font.SysFont(None, 52)

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
        self.flechas_orfas = pygame.sprite.Group()
        self.fireballs_orfas = pygame.sprite.Group()

        self.tutorial_inicio_ms = pygame.time.get_ticks()
        self.tutorial_duracao_ms = 5000
        self.tutorial_pulado = False
        self.inicio_gameplay_ms = None
        self.ultimo_bonus_score_ms = None
        self.game_over = False
        self.game_over_inicio_ms = None
        self.game_over_duracao_ms = 2000

        self.preco_espada = 30
        self.preco_arco = 15
        self.preco_flechas = 5
        self.preco_vida = 1
        self.incremento_preco_vida = 1

    def _tutorial_ativo(self):
        if self.tutorial_pulado:
            return False
        tempo_passado = pygame.time.get_ticks() - self.tutorial_inicio_ms
        return tempo_passado < self.tutorial_duracao_ms

    def _garantir_inicio_gameplay(self):
        if self.inicio_gameplay_ms is None:
            agora_ms = pygame.time.get_ticks()
            self.inicio_gameplay_ms = agora_ms
            self.ultimo_bonus_score_ms = agora_ms

    def _atualizar_bonus_score_por_tempo(self):
        if self.ultimo_bonus_score_ms is None:
            return

        agora_ms = pygame.time.get_ticks()
        segundos_completos = (agora_ms - self.ultimo_bonus_score_ms) // 1000
        if segundos_completos > 0:
            self.player.score += int(segundos_completos) * 10
            self.ultimo_bonus_score_ms += int(segundos_completos) * 1000

    def _tempo_decorrido_segundos(self):
        if self.inicio_gameplay_ms is None:
            return 0
        agora_ms = pygame.time.get_ticks()
        return max(0, (agora_ms - self.inicio_gameplay_ms) // 1000)

    def _desenhar_tempo(self):
        tempo_total = self._tempo_decorrido_segundos()
        minutos = tempo_total // 60
        segundos = tempo_total % 60
        tempo_text = self.font_tempo.render(f'{minutos}:{segundos:02d}', True, (255, 255, 255))
        self.window.blit(tempo_text, (24, 18))

    def _desenhar_overlay_tutorial(self):
        if not self._tutorial_ativo():
            return

        tempo_passado = pygame.time.get_ticks() - self.tutorial_inicio_ms

        restante_ms = self.tutorial_duracao_ms - tempo_passado
        restante_segundos = max(1, (restante_ms + 999) // 1000)

        painel = pygame.Rect(220, 110, LARGURA - 440, ALTURA - 220)
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 110))
        self.window.blit(overlay, (0, 0))

        pygame.draw.rect(self.window, (14, 50, 95), painel, border_radius=20)
        pygame.draw.rect(self.window, (88, 170, 255), painel, 5, border_radius=20)

        titulo = self.font_overlay_titulo.render('COMO JOGAR', True, (255, 220, 0))
        self.window.blit(titulo, titulo.get_rect(center=(LARGURA // 2, painel.y + 84)))

        linhas = [
            ('WASD', '- Mover o personagem'),
            ('Mouse Esquerdo', '- Ataque corpo a corpo'),
            ('Mouse Direito', '- Ataque à distância'),
            ('ESC / P', '- Pausar o jogo')
        ]

        y_texto = painel.y + 168
        for comando, descricao in linhas:
            comando_text = self.font_overlay_texto.render(comando, True, (95, 205, 255))
            desc_text = self.font_overlay_texto.render(descricao, True, (230, 230, 230))
            self.window.blit(comando_text, (painel.x + 48, y_texto))
            self.window.blit(desc_text, (painel.x + 280, y_texto))
            y_texto += 66

        objetivo = self.font_overlay_texto.render('Objetivo: Sobreviva e derrote os inimigos!', True, (255, 190, 95))
        self.window.blit(objetivo, objetivo.get_rect(center=(LARGURA // 2, painel.bottom - 84)))

        contador = self.font_overlay_hint.render(
            f'Começando em {restante_segundos}s | ENTER ou Clique Esq. para pular',
            True,
            (205, 205, 225)
        )
        self.window.blit(contador, contador.get_rect(center=(LARGURA // 2, painel.bottom - 36)))

    def _desenhar_overlay_game_over(self):
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 165))
        self.window.blit(overlay, (0, 0))

        titulo = self.font_overlay_titulo.render('GAME OVER', True, (255, 50, 50))
        score = self.font_overlay_texto.render(f'Score Final: {self.player.score}', True, (255, 220, 0))

        self.window.blit(titulo, titulo.get_rect(center=(LARGURA // 2, ALTURA // 2 - 60)))
        self.window.blit(score, score.get_rect(center=(LARGURA // 2, ALTURA // 2 + 20)))

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

        score_text = self.font_score.render(f'SCORE: {self.player.score}', True, (255, 255, 255))
        money_text = self.font_money.render(f'${self.player.dinheiro}', True, (255, 215, 0))

        score_rect = score_text.get_rect(center=(LARGURA // 2, 40))
        money_rect = money_text.get_rect(center=(LARGURA // 2, 90))

        self._desenhar_tempo()
        self.window.blit(score_text, score_rect)
        self.window.blit(money_text, money_rect)

        hud_margem_x = 50
        barra_largura = 200
        barra_altura = 34
        barra_y = 77

        vida_barra_pos = (hud_margem_x, barra_y)
        flecha_barra_pos = (LARGURA - hud_margem_x - barra_largura, barra_y)

        self.desenhar_barra(vida_barra_pos, (barra_largura, barra_altura), self.player.vida, self.player.max_vida, (0, 255, 0), (40, 40, 40))
        self.desenhar_barra(flecha_barra_pos, (barra_largura, barra_altura), self.player.flechas, self.player.max_flechas, (255, 60, 60), (40, 40, 40))

        vida_barra_rect = pygame.Rect(vida_barra_pos, (barra_largura, barra_altura))
        flecha_barra_rect = pygame.Rect(flecha_barra_pos, (barra_largura, barra_altura))

        vida_label = self.font_hud.render('VIDAS', True, (255, 255, 255))
        vida_label_rect = vida_label.get_rect(midbottom=(vida_barra_rect.centerx, vida_barra_rect.top - 6))
        self.window.blit(vida_label, vida_label_rect)

        flecha_label = self.font_hud.render('FLECHAS', True, (255, 255, 255))
        flecha_label_rect = flecha_label.get_rect(midbottom=(flecha_barra_rect.centerx, flecha_barra_rect.top - 6))
        self.window.blit(flecha_label, flecha_label_rect)

        vida_text = self.font_hud_valor.render(f'{self.player.vida}/{self.player.max_vida}', True, (255, 255, 255))
        vida_text_rect = vida_text.get_rect(midleft=(vida_barra_rect.right + 10, vida_barra_rect.centery))
        self.window.blit(vida_text, vida_text_rect)

        flecha_text = self.font_hud_valor.render(f'{self.player.flechas}/{self.player.max_flechas}', True, (255, 255, 255))
        flecha_text_rect = flecha_text.get_rect(midright=(flecha_barra_rect.left - 10, flecha_barra_rect.centery))
        self.window.blit(flecha_text, flecha_text_rect)

        nivel_text_outline = self.font_hud.render(f'Nivel: {self.player.nivel}', True, (10, 35, 90))
        nivel_text = self.font_hud.render(f'Nivel: {self.player.nivel}', True, (95, 210, 255))
        nivel_rect = nivel_text.get_rect(center=(self.objeto.plataforma.centerx, self.objeto.plataforma.bottom + 48))
        self.window.blit(nivel_text_outline, (nivel_rect.x + 2, nivel_rect.y + 2))
        self.window.blit(nivel_text, nivel_rect)

        if self.pode_comprar_espada:
            if self.player.estado_combate in ('espada', 'arco_espada'):
                buy_text = self.font_money.render("você já comprou uma espada!", True, (255, 255, 255))
            else:
                buy_text = self.font_money.render(f"aperte E para comprar espada ({self.preco_espada}$)", True, (255, 255, 255))
            buy_rect = buy_text.get_rect(center=(LARGURA // 2, ALTURA // 2))
            self.window.blit(buy_text, buy_rect)
        elif self.pode_interagir_bau:
            if self.player.estado_combate in ('arco_soco', 'arco_espada'):
                if self.player.flechas >= self.player.max_flechas:
                    flechas_text = self.font_money.render("Você já tem o máximo de flechas possíveis", True, (255, 255, 255))
                else:
                    flechas_text = self.font_money.render(f"aperte E para comprar flechas ({self.preco_flechas}$)", True, (255, 255, 255))
                flechas_rect = flechas_text.get_rect(center=(LARGURA // 2, ALTURA // 2))
                self.window.blit(flechas_text, flechas_rect)
            else:
                msg_text = self.font_money.render("você precisa de um arco.", True, (255, 255, 255))
                msg_rect = msg_text.get_rect(center=(LARGURA // 2, ALTURA // 2))
                self.window.blit(msg_text, msg_rect)
        elif self.pode_interagir_kit:
            if self.player.vida < 10:
                kit_text = self.font_money.render(f"aperte E para usar kitmedico ({self.preco_vida}$)", True, (255, 255, 255))
            else:
                kit_text = self.font_money.render("vida cheia!", True, (255, 255, 255))
            kit_rect = kit_text.get_rect(center=(LARGURA // 2, ALTURA // 2))
            self.window.blit(kit_text, kit_rect)
        elif self.pode_interagir_arco:
            if self.player.estado_combate in ('arco_soco', 'arco_espada'):
                arco_text = self.font_money.render("você já comprou um arco", True, (255, 255, 255))
            else:
                arco_text = self.font_money.render(f"aperte E para comprar arco ({self.preco_arco}$)", True, (255, 255, 255))
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
        self.flechas_orfas.draw(self.window)
        self.fireballs_orfas.draw(self.window)
        if self.player.soco_vento:
            self.window.blit(self.player.soco_vento_image_rotated, self.player.soco_vento)
        if self.player.espada_vento:
            self.window.blit(self.player.espada_vento_image_rotated, self.player.espada_vento)

        self._desenhar_overlay_tutorial()
        if self.game_over:
            self._desenhar_overlay_game_over()

        pygame.display.update()

    def _matar_inimigo(self, inimigo, com_capitalizacao=True):
        if isinstance(inimigo, Skeleton):
            for p in list(inimigo.flechas_disparadas):
                inimigo.flechas_disparadas.remove(p)
                self.flechas_orfas.add(p)
        elif isinstance(inimigo, Wizard):
            for p in list(inimigo.fireballs_disparadas):
                inimigo.fireballs_disparadas.remove(p)
                self.fireballs_orfas.add(p)
        inimigo.kill()
        if com_capitalizacao:
            self.player.capitalizacao(inimigo)

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
                self._matar_inimigo(inimigo, com_capitalizacao=False)
                self.player.vida = max(0, self.player.vida - 1)

        agora_ms = pygame.time.get_ticks()
        if self.player.soco_vento:
            for inimigo in list(self.spawn.inimigos):
                pode_ser_atingido = (agora_ms - inimigo.ultimo_hit_ms) >= inimigo.hit_cooldown_ms
                if self.player.soco_vento.colliderect(inimigo.rect) and inimigo.health > 0 and pode_ser_atingido:
                    inimigo.ultimo_hit_ms = agora_ms
                    inimigo.health -= 10
                    if inimigo.health <= 0:
                        self._matar_inimigo(inimigo)

        if self.player.espada_vento_hitbox:
            for inimigo in list(self.spawn.inimigos):
                pode_ser_atingido = (agora_ms - inimigo.ultimo_hit_ms) >= inimigo.hit_cooldown_ms
                if self.player.espada_vento_hitbox.colliderect(inimigo.rect) and inimigo.health > 0 and pode_ser_atingido:
                    inimigo.ultimo_hit_ms = agora_ms
                    inimigo.health -= 20
                    if inimigo.health <= 0:
                        self._matar_inimigo(inimigo)

            for inimigo in self.spawn.inimigos:
                if isinstance(inimigo, Skeleton):
                    for flecha in list(inimigo.flechas_disparadas):
                        if self.player.espada_vento_hitbox.colliderect(flecha.rect):
                            flecha.kill()
                if isinstance(inimigo, Wizard):
                    for fireball in list(inimigo.fireballs_disparadas):
                        if self.player.espada_vento_hitbox.colliderect(fireball.rect):
                            fireball.kill()
            for flecha in list(self.flechas_orfas):
                if self.player.espada_vento_hitbox.colliderect(flecha.rect):
                    flecha.kill()
            for fireball in list(self.fireballs_orfas):
                if self.player.espada_vento_hitbox.colliderect(fireball.rect):
                    fireball.kill()

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
                        self._matar_inimigo(inimigo)
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

        for flecha in list(self.flechas_orfas):
            deslocamento = flecha.direcao * flecha.velocidade
            flecha.rect.move_ip(deslocamento.x, deslocamento.y)
            if (flecha.rect.right < -80 or flecha.rect.left > LARGURA + 80 or
                    flecha.rect.bottom < -80 or flecha.rect.top > ALTURA + 80):
                flecha.kill()
                continue
            if flecha.rect.colliderect(self.player.rect):
                offset = (self.player.rect.x - flecha.rect.x, self.player.rect.y - flecha.rect.y)
                if flecha.mask.overlap(self.player.mask, offset):
                    flecha.kill()
                    self.player.vida = max(0, self.player.vida - 1)

        for fireball in list(self.fireballs_orfas):
            centro_anterior = fireball.rect.center
            fireball.angulo += fireball.rotacao_por_frame
            fireball.image = pygame.transform.rotate(fireball.base_image, fireball.angulo)
            fireball.rect = fireball.image.get_rect(center=centro_anterior)
            fireball.mask = pygame.mask.from_surface(fireball.image)
            deslocamento = fireball.direcao * fireball.velocidade
            fireball.rect.move_ip(deslocamento.x, deslocamento.y)
            if (fireball.rect.right < -80 or fireball.rect.left > LARGURA + 80 or
                    fireball.rect.bottom < -80 or fireball.rect.top > ALTURA + 80):
                fireball.kill()
                continue
            if fireball.rect.colliderect(self.player.rect):
                offset = (self.player.rect.x - fireball.rect.x, self.player.rect.y - fireball.rect.y)
                if fireball.mask.overlap(self.player.mask, offset):
                    fireball.kill()
                    self.player.vida = max(0, self.player.vida - 1)

    def executar(self):
        while self.rodando:
            tutorial_ativo = self._tutorial_ativo()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.rodando = False
                if self.game_over:
                    continue

                if tutorial_ativo:
                    if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        self.tutorial_pulado = True
                        tutorial_ativo = False
                        self._garantir_inicio_gameplay()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.tutorial_pulado = True
                        tutorial_ativo = False
                        self._garantir_inicio_gameplay()
                    continue

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e and self.pode_comprar_espada and self.player.dinheiro >= self.preco_espada:
                        self.player.dinheiro -= self.preco_espada
                        self.player.equipar_espada()
                        self.pode_comprar_espada = False
                    elif event.key == pygame.K_e and self.pode_interagir_arco and self.player.dinheiro >= self.preco_arco and self.player.estado_combate not in ('arco_soco', 'arco_espada'):
                        self.player.dinheiro -= self.preco_arco
                        self.player.equipar_arco()
                        self.pode_interagir_arco = False
                    elif event.key == pygame.K_e and self.pode_interagir_bau and self.player.dinheiro >= self.preco_flechas and self.player.flechas < self.player.max_flechas and self.player.estado_combate in ('arco_soco', 'arco_espada'):
                        self.player.dinheiro -= self.preco_flechas
                        self.player.flechas = min(self.player.flechas + 5, self.player.max_flechas)
                        self.pode_interagir_bau = False
                    elif event.key == pygame.K_e and self.pode_interagir_kit and self.player.vida < 10 and self.player.dinheiro >= self.preco_vida:
                        self.player.dinheiro -= self.preco_vida
                        self.player.vida = min(self.player.vida + 1, self.player.max_vida)
                        self.preco_vida += self.incremento_preco_vida
                        self.pode_interagir_kit = False

            if not self.game_over and not tutorial_ativo:
                self._garantir_inicio_gameplay()
                self._atualizar_bonus_score_por_tempo()

                for inimigo in self.spawn.inimigos:
                    if inimigo.alive() and inimigo.health > 0:
                        inimigo.movimentacao()

                self.player.movimentacao()
                self.player.atacar()
                self.player.atualizar_projeteis()
                self.colisoes()
                self.spawn.atualizar_spawn_inimigos()

                if self.player.vida <= 0:
                    self.player.vida = 0
                    self.game_over = True
                    self.game_over_inicio_ms = pygame.time.get_ticks()

            self.desenhar()

            if self.game_over and self.game_over_inicio_ms is not None:
                tempo_game_over = pygame.time.get_ticks() - self.game_over_inicio_ms
                if tempo_game_over >= self.game_over_duracao_ms:
                    return {
                        'status': 'GAME_OVER',
                        'nome': self.player_name,
                        'score': self.player.score
                    }

            self.relogio.tick(FPS)

        return {
            'status': 'SAIR',
            'nome': self.player_name,
            'score': self.player.score
        }