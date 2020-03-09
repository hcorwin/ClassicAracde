import pygame
import random
import math
import sys
sys.path.append('..')



class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./assets/enemyBlue2.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y

    def move_right(self):
        self.rect.x += 1

    def move_left(self):
        self.rect.x -= 1

    def update(self, time_counter):

        if time_counter < 400:
            self.move_right()
        if time_counter > 400:
            self.move_left()





class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, direction):

        super().__init__()
        self.images = [0, 0]
        self.images[0] = pygame.image.load('./assets/laserRed02.png')
        self.images[1] = pygame.image.load('./assets/laserBlue02.png')
        self.x = x + 24
        self.y = y + 10
        #direction will be 0 = up, 1 = down
        self.direction = direction

        self.image = self.images[direction]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.y_change = 10

    def update(self, game, ships):

        if self.direction == 0:
            self.rect.y -= self.y_change
            #if self.rect.y <= 0:
                 #game.bullets.remove(self)
        if self.direction == 1:
            self.rect.y += self.y_change
            #if self.rect.y >= 600:
                #game.bullets.remove(self)
        hit_object = pygame.sprite.spritecollideany(self, ships)
        if hit_object:
            hit_object.kill()
            game.score += 10


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('./assets/playerShip1_red.png')
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y

    def move_left(self):
        self.rect.x -= 8

    def move_right(self):
        self.rect.x += 8


class Game:
    def __init__(self):
        pygame.init()


        #set screen
        self.scr = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Arcade Game")

        #Player related
        self.score = 0

        #Enemy related
        self.eX = [0, 60, 120, 180, 240, 300, 360, 30, 100, 170, 240, 310, 60, 160, 260]
        self.eY = [100, 100, 100, 100, 100, 100, 100, 150, 150, 150, 150, 150, 200, 200, 200]

        self.clock = pygame.time.Clock()




   # def player(self, x, y):
     #   self.scr.blit(self.playerImg, (x, y))


def main():
    # create event for enemy shooting
    shoot_event = pygame.USEREVENT + 1
    pygame.time.set_timer(shoot_event, 500)
    # Game Loop
    ships = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    players = pygame.sprite.Group()
    p = Player(350, 480)
    players.add(p)
    pressed_left = False
    pressed_right = False
    #create enemies
    g = Game()
    for i in range(0, 15):
        e = Enemy(g.eX[i], g.eY[i])
        ships.add(e)
    run = True
    time_counter = 0

    while run:
        g.scr.fill((0, 0, 0))
        #check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == shoot_event:
                pick_enemy = random.randint(0, 15)
                #bullet = Bullet(ships.sprites()[14].rect.x, ships.sprites()[14].rect.y, 1)
                #bullets.add(bullet)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pressed_left = True
                if event.key == pygame.K_RIGHT:
                    pressed_right = True
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(p.rect.x, p.rect.y, 0)
                    bullets.add(bullet)
                    pass
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    pressed_left = False
                if event.key == pygame.K_RIGHT:
                    pressed_right = False

        #move player based on changed values within boundaries of map
        if pressed_left:
            p.move_left()
        if pressed_right:
            p.move_right()
        if p.rect.x <= 0:
            p.rect.x = 0
        elif p.rect.x >= 700:
            p.rect.x = 700

        #draw
        time_counter += 1
        players.update()
        players.draw(g.scr)
        ships.update(time_counter)
        ships.draw(g.scr)
        bullets.update(g, ships)
        bullets.draw(g.scr)
        pygame.display.update()
        g.clock.tick(60)
        if time_counter >= 800:
            time_counter = 0


if __name__ == '__main__':
    main()
