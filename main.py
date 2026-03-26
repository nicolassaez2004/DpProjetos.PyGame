import pygame
import random

LARGURA = 1280
ALTURA = 720
PRETO = (0, 0, 0)
MOUSE_COLOR = (255, 255, 255)
FPS = 60

class Player(pygame.sprite.Sprite):
    def __init__(self, posicao):
        super(Player, self).__init__()
        aux_combate = ['soco', 'espada', 'arco_soco', 'arco_espada']
        aux_movimento = ['parado', 'andando', 'batendo']
        size = (80,80)
        self.estado_combate = aux_combate[0]
        self.estado_movimento = aux_movimento[0]
        
        aux = pygame.image.load('assets/sprites/knight.png')
        self.knight_parado = pygame.transform.scale(aux, size)
        self.knight_parado_flip = pygame.transform.flip(self.knight_parado, True, False)
        self.knight_soco = pygame.transform.scale(pygame.image.load('assets/sprites/knight_soco.png'), size)
        self.knight_soco_flip = pygame.transform.flip(self.knight_soco, True, False)
        self.olhando_direita = True
        self.image = self.knight_parado
        self.rect = pygame.Rect(posicao, size)
        self.mask = pygame.mask.from_surface(self.image)
        self.velocidade = pygame.math.Vector2(0, 0)
        self.soco_vento = None
        self.soco_vento_image = pygame.transform.scale(pygame.image.load('assets/sprites/soco_vento.png'), (80, 80))
        self.soco_vento_image_rotated = self.soco_vento_image
        self.soco_vento_image_rotated = self.soco_vento_image
        
        self.dinheiro = 0
        self.vida = 10
        self.flechas = 0
        
    def movimentacao(self):
        self.key = pygame.key.get_pressed()

        self.velocidade.x = 0
        self.velocidade.y = 0

        if self.key[pygame.K_w]:
            self.velocidade.y = -10
        if self.key[pygame.K_s]:
            self.velocidade.y = 10
        if self.key[pygame.K_a]:
            self.velocidade.x = -10
        if self.key[pygame.K_d]:
            self.velocidade.x = 10

        self.rect.move_ip(*self.velocidade)
        
        if self.rect.x < 380: self.rect.x = 380
        if self.rect.x > 820: self.rect.x = 820
        if self.rect.y < 160: self.rect.y = 160
        if self.rect.y > 480: self.rect.y = 480

    def soco(self):
        mouse_pos = pygame.mouse.get_pos()
        self.olhando_direita = (mouse_pos[0] >= self.rect.centerx)

        if pygame.mouse.get_pressed()[0] and self.estado_combate == 'soco':
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
        else:
            self.image = self.knight_parado if self.olhando_direita else self.knight_parado_flip
            self.mask = pygame.mask.from_surface(self.image)
            self.soco_vento = None

    def espada(self):
        pass

    def arco(self):
        pass

class Enemy(pygame.sprite.Sprite):
    def __init__(self, posicao):
        super().__init__()

        self.health = 10
        self.damage = 10
        self.speed = 2

        self.pos_inicial = pygame.math.Vector2(posicao)
        self.rect = pygame.Rect(posicao, (80, 80))
        self.velocidade = pygame.math.Vector2(0, 0)

    def random_spawn(self):
        self.spawn_pos = ()
        lado = random.randint(1, 4)
        if lado == 1: #cima
            self.spawn_pos = (random.randint(80, 1200), -80)
        if lado == 2: #baixo
            self.spawn_pos = (random.randint(80, 1200), 660)
        if lado == 3: #esquerda
            self.spawn_pos = (-80, random.randint(80, 660))
        if lado == 4: #direita
            self.spawn_pos = (1200, random.randint(80, 660))

        self.pos_atual = self.spawn_pos
        return self.spawn_pos

    def disparo(self):
        pass

class Skeleton(Enemy):
    def __init__(self, posicao):
        super().__init__(posicao)

        aux = pygame.image.load('assets/sprites/skeleton.png')
        self.skeleton = pygame.transform.scale(aux, (80, 80))
        self.skeleton_inverso = pygame.transform.flip(self.skeleton, True, False)
        self.image = self.skeleton

        self.estado = "indo_player"
        self.timer = 0  
        self.direcao = pygame.math.Vector2(0, 0)
        self.distancia_percorrida = 0

        self.estado = 0
        self.direcaorandom = 0

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

class Wizard(Enemy):
    def __init__(self, posicao):
        super().__init__(posicao)

        aux = pygame.image.load('assets/sprites/wizard.png')
        self.wizard = pygame.transform.scale(aux, (80, 80))
        self.wizard_flip = pygame.transform.flip(self.wizard, True, False)
        self.image = self.wizard

        self.estado = "spawnando"
        self.timer = 0  
        self.direcao = pygame.math.Vector2(0, 0)
        self.distancia_percorrida = 0

        self.direcaorandom = 0

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
            self.timer += 1
            if self.timer >= 120:
                self.estado = "parado"
                self.timer = 0
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

class Ghost(Enemy):
    def __init__(self, posicao):
        super().__init__(posicao)

        aux = pygame.image.load('assets/sprites/ghost.png')
        self.ghost = pygame.transform.scale(aux, (80, 80))
        self.ghost_flip = pygame.transform.flip(self.ghost, True, False)
        self.image = self.ghost

        self.timer = 0
        self.direcao = pygame.math.Vector2(0, 0)
        self.distancia_percorrida = 0

        self.direcaorandom = 0

    def movimentacao(self):
        direcao = pygame.math.Vector2(
            self.player.rect.centerx - self.rect.centerx,
            self.player.rect.centery - self.rect.centery
        )
        distancia = direcao.length()
        if distancia != 0:
            direcao = direcao.normalize()
            
        self.velocidade = direcao * self.speed
        self.rect.move_ip(*self.velocidade)

        self.image = self.ghost if self.player.rect.centerx >= self.rect.centerx else self.ghost_flip

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGURA:
            self.rect.right = LARGURA
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > ALTURA:
            self.rect.bottom = ALTURA

class Object(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        size = (80,80)
        auxbau = pygame.image.load('assets/sprites/bau.png')
        self.bau = pygame.transform.scale(auxbau, size)
        auxkitmedico = pygame.image.load('assets/sprites/kitmedico.png')
        self.kitmedico = pygame.transform.scale(auxkitmedico, size)
        auxarco = pygame.image.load('assets/sprites/arco.png')
        self.arco = pygame.transform.scale(auxarco, size)
        auxespada = pygame.image.load('assets/sprites/espada.png')
        self.espada = pygame.transform.scale(auxespada, size)

        self.plataforma = pygame.Rect(360, 120, 560, 480)
        self.colisao_bau = pygame.Rect(400, 160, 80, 80)
        self.colisao_kitmedico = pygame.Rect(800, 160, 80, 80)
        self.colisao_arco = pygame.Rect(400, 480, 80, 80)
        self.colisao_espada = pygame.Rect(800, 480, 80, 80)

class Gameplay(Player):
    def __init__(self, posicao):
        super().__init__(posicao)
        self.nivel = 1
        self.score = 0

    def capitalizacao(self, inimigo):
        if isinstance(inimigo, Ghost):
            self.dinheiro += 2
            self.score += 20
        elif isinstance(inimigo, Skeleton):
            self.dinheiro += 3
            self.score += 30
        elif isinstance(inimigo, Wizard):
            self.dinheiro += 5
            self.score += 50

class Game:
    def __init__(self):
        self.rodando = True
        pygame.init()

        self.bg = pygame.image.load('assets/sprites/background.jpg')
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

        mouse_pos = pygame.mouse.get_pos()
        tamanho_mouse = 10
        self.mouse_pos = pygame.Rect(mouse_pos[0], mouse_pos[1], tamanho_mouse, tamanho_mouse)
        pygame.draw.rect(self.window, (MOUSE_COLOR), self.mouse_pos)
        
        self.todo_mundo.draw(self.window)
        if self.player.soco_vento:
            self.window.blit(self.player.soco_vento_image_rotated, self.player.soco_vento)
        pygame.display.update()
        
    def colisoes(self): #testador de colisões
        global MOUSE_COLOR
        if self.mouse_pos.colliderect(self.skeleton.rect):
            MOUSE_COLOR = (0, 255, 0)
        elif self.mouse_pos.colliderect(self.objeto.plataforma):
            MOUSE_COLOR = (125, 0, 0)
        else:
            MOUSE_COLOR = (255, 255, 255)
            
        if self.mouse_pos.colliderect(self.objeto.colisao_bau):
            MOUSE_COLOR = (0, 0, 255)
        if self.mouse_pos.colliderect(self.objeto.colisao_kitmedico):
            MOUSE_COLOR = (0, 0, 255)
        if self.mouse_pos.colliderect(self.objeto.colisao_arco):
            MOUSE_COLOR = (0, 0, 255)
        if self.mouse_pos.colliderect(self.objeto.colisao_espada):
            MOUSE_COLOR = (0, 0, 255)

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

    def executar(self):
        while self.rodando:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.rodando = False

            self.player.movimentacao()
            self.player.soco()
            self.desenhar()
            self.colisoes()
            self.relogio.tick(FPS)

        pygame.quit()
        
if __name__ == '__main__':
    jogo = Game()
    jogo.executar()