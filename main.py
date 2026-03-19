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
        super(Enemy, self).__init__()
        size = (80, 80)
        aux = pygame.image.load('assets/sprites/skeleton.png')
        self.image = pygame.transform.scale(aux, size)
        self.rect = pygame.Rect(posicao, size)
        self.velocidade = pygame.math.Vector2(0, 0)

    def update(self):
        self.rect.move_ip(*self.velocidade)

class Object(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.rect_brick_cima = pygame.Rect(400, 120, 480, 40)
        self.rect_brick_baixo = pygame.Rect(400, 560, 480, 40)
        self.rect_brick_esquerda = pygame.Rect(360, 160, 40, 400)
        self.rect_brick_direita = pygame.Rect(880, 160, 40, 400)
            
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
        self.inimigo1 = Enemy((self.spawn_pos))
        self.todo_mundo = pygame.sprite.Group([self.player, self.inimigo1])

        self.objeto = Object()
        
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
        
    def desenhar(self):
        self.window.fill(PRETO)
        self.window.blit(self.bg, (0, 0))

        self.todo_mundo.update()
        self.inimigo1.velocidade = ((self.player.rect.x-self.inimigo1.rect.x)//200,
                              (self.player.rect.y-self.inimigo1.rect.y)//200)
        
        mouse_pos = pygame.mouse.get_pos()
        tamanho_mouse = 10
        self.mouse_pos = pygame.Rect(mouse_pos[0], mouse_pos[1], tamanho_mouse, tamanho_mouse)
        #pygame.draw.rect(self.window, (MOUSE_COLOR), self.mouse_pos)
        
        self.todo_mundo.draw(self.window)
        pygame.display.update()
        
    def colisoes(self):
        pass
    
        # global MOUSE_COLOR
        # if self.mouse_pos.colliderect(self.player):
        #     MOUSE_COLOR = (125, 0, 0)
        # else:
        #     MOUSE_COLOR = (255, 255, 255)

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