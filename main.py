import pygame
import random

LARGURA = 1280
ALTURA = 720
PRETO = (0, 0, 0)
FPS = 60

class Player(pygame.sprite.Sprite):
    def __init__(self, posicao):
        super(Player, self).__init__()
        size = (80,80)
        aux = pygame.image.load('assets/sprites/knight.png')
        self.image = pygame.transform.scale(aux, size)
        self.rect = pygame.Rect(posicao, size)
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
        size = (80,80)
        aux = pygame.image.load('assets/sprites/skeleton.png')
        self.image = pygame.transform.scale(aux, size)
        self.rect = pygame.Rect(posicao, size)
        self.velocidade = pygame.math.Vector2(0, 0)

    def update(self):
        self.velocidade.x = -1
        self.velocidade.y = -1
        self.rect.move_ip(*self.velocidade)

class Object(pygame.sprite.Sprite):
    def __init__(self):
        pass

class Game:
    def __init__(self):
        
        self.rodando = True
        
        pygame.init()
        self.bg = pygame.image.load('assets/sprites/background.jpg')
        self.bg = pygame.transform.scale(self.bg, (1280, 720))
        self.window = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption('Claustrophobia the Game! 🤤')
        self.relogio = pygame.time.Clock()
        player1 = Player((LARGURA/2 - 40, ALTURA/2 - 40))
        inimigo1 = Enemy((LARGURA - 200, ALTURA - 200))
        self.todo_mundo = pygame.sprite.Group([player1, inimigo1])
        
    def desenhar(self):
        self.window.fill(PRETO)
        self.window.blit(self.bg, (0, 0))
        self.todo_mundo.update()
        self.todo_mundo.draw(self.window)
        pygame.display.update()
        
    def executar(self):
        while self.rodando:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.rodando = False

            self.desenhar()
            self.relogio.tick(FPS)

        pygame.quit()
        
if __name__ == '__main__':
    jogo = Game()
    jogo.executar()