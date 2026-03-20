import pygame
import random
import time

LARGURA = 1280
ALTURA = 720
PRETO = (0, 0, 0)
MOUSE_COLOR = (255, 255, 255)
FPS = 60

class Player(pygame.sprite.Sprite):
    def __init__(self, posicao):
        super(Player, self).__init__()
        size = (80,80)
        aux = pygame.image.load('assets/sprites/knight.png')
        self.image = pygame.transform.scale(aux, size)
        self.rect = pygame.Rect(posicao, size)
        self.mask = pygame.mask.from_surface(self.image)
        self.velocidade = pygame.math.Vector2(0, 0)
        
    def update(self):
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
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self, posicao):
        super().__init__()

        self.health = 10
        self.damage = 10
        self.speed = 2

        self.pos_inicial = pygame.math.Vector2(posicao)
        self.rect = pygame.Rect(posicao, (80, 80))
        self.velocidade = pygame.math.Vector2(0, 0)

class Skeleton(Enemy):
    def __init__(self, posicao):
        super().__init__(posicao)

        aux = pygame.image.load('assets/sprites/skeleton.png')
        self.image = pygame.transform.scale(aux, (80, 80))

        self.estado = "indo_player"
        self.timer = 0  
        self.direcao = pygame.math.Vector2(0, 0)
        self.distancia_percorrida = 0

        self.estado = 0
        self.direcaorandom = 0

    def update(self):
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
            if rect_x.left < 80:
                rect_x.left = 80
            if rect_x.right > 1200:
                rect_x.right = 1200
            if not rect_x.colliderect(self.objeto.plataforma):
                new_rect.x = rect_x.x

        if self.velocidade.y != 0:
            rect_y = new_rect.move(0, self.velocidade.y)
            if rect_y.top < 80:
                rect_y.top = 80
            if rect_y.bottom > 640:
                rect_y.bottom = 640
            if not rect_y.colliderect(self.objeto.plataforma):
                new_rect.y = rect_y.y

        self.rect = new_rect

class Wizard(Enemy):
    def __init__(self, posicao):
        super().__init__(posicao)

        aux = pygame.image.load('assets/sprites/wizard.png')
        self.image = pygame.transform.scale(aux, (80, 80))

    def update(self):
        pass

class Ghost(Enemy):
    def __init__(self, posicao):
        super().__init__(posicao)

        aux = pygame.image.load('assets/sprites/ghost.png')
        self.image = pygame.transform.scale(aux, (80, 80))

    def update(self):
        pass

class Object(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.plataforma = pygame.Rect(360, 120, 560, 480)
            
class Game:
    def __init__(self):
        self.rodando = True
        pygame.init()

        self.bg = pygame.image.load('assets/sprites/background.jpg')
        self.bg = pygame.transform.scale(self.bg, (1280, 720))
        self.window = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption('Claustrophobia Knight')

        self.relogio = pygame.time.Clock()

        self.mouse_pos = pygame.Rect((0, 0), (0, 0))
        self.player = Player((LARGURA/2 - 40, ALTURA/2 - 40))

        self.randomizacao()
        self.objeto = Object()
        self.skeleton = Skeleton(self.spawn_pos)
        self.skeleton.player = self.player
        self.skeleton.objeto = self.objeto
        self.todo_mundo = pygame.sprite.Group([self.player, self.skeleton])
        
    def randomizacao(self):
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
        
    def desenhar(self):
        self.window.fill(PRETO)
        self.window.blit(self.bg, (0, 0))
        
        self.skeleton.update()
        self.todo_mundo.update()

        mouse_pos = pygame.mouse.get_pos()
        tamanho_mouse = 10
        self.mouse_pos = pygame.Rect(mouse_pos[0], mouse_pos[1], tamanho_mouse, tamanho_mouse)
        pygame.draw.rect(self.window, (MOUSE_COLOR), self.mouse_pos)
        
        self.todo_mundo.draw(self.window)
        pygame.display.update()
        
    def colisoes(self):  
        global MOUSE_COLOR
        if self.mouse_pos.colliderect(self.skeleton.rect):
            MOUSE_COLOR = (0, 255, 0)
        elif self.mouse_pos.colliderect(self.objeto.plataforma):
            MOUSE_COLOR = (125, 0, 0)
        else:
            MOUSE_COLOR = (255, 255, 255)

    def executar(self):
        while self.rodando:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.rodando = False

            self.desenhar()
            self.colisoes()
            self.relogio.tick(FPS)

        pygame.quit()
        
if __name__ == '__main__':
    jogo = Game()
    jogo.executar()