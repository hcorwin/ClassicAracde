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
        self.rect.x += 2

    def move_left(self):
        self.rect.x -= 2

    def update(self, time_counter):

        if time_counter < 200:
            self.move_right()
        if time_counter > 200:
            self.move_left()


class Overlay(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([800, 40])
        self.image.fill((127, 127, 127))
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font('freesansbold.ttf', 18)
        self.render('Score: 0        Lives: 3')

    def render(self, text):
        self.text = self.font.render(text, True, (255, 255, 255))
        self.image.blit(self.text, self.rect)

    def draw(self, screen):
        screen.blit(self.text, (0, 0))

    def update(self, score, lives):
        self.render('Score: ' + str(score) + '        Lives: ' + str(lives))


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
            hit_object = pygame.sprite.spritecollideany(self, ships)
            if hit_object:
                hit_object.kill()
                game.score += 10
        if self.direction == 1:
            self.rect.y += 5
            #if self.rect.y >= 600:
                #game.e_bullets.remove(self)
            hit_object = pygame.sprite.spritecollideany(self, ships)
            if hit_object:
                game.live -= 1
                if game.live == 0:
                    hit_object.kill()


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
        self.live = 3

        #Enemy related
        self.eX = [0, 60, 120, 180, 240, 300, 360, 30, 100, 170, 240, 310, 60, 160, 260]
        self.eY = [100, 100, 100, 100, 100, 100, 100, 150, 150, 150, 150, 150, 200, 200, 200]

        self.clock = pygame.time.Clock()


def main():
    # create event for enemy shooting
    g = Game()
    shoot_event = pygame.USEREVENT + 1
    pygame.time.set_timer(shoot_event, 1000)
    # Game Loop
    ships = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    #bullets.add(Bullet(100, 100, 0))
    e_bullets = pygame.sprite.Group()
    #e_bullets.add(Bullet(100, 100, 1))
    players = pygame.sprite.Group()
    p = Player(350, 480)
    players.add(p)
    pressed_left = False
    pressed_right = False
    overlay = Overlay()
    #create enemies
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
                num_ships = 0
                for e in ships:
                    if isinstance(e, Enemy):
                        num_ships += 1
                if num_ships != 0:
                    pick_enemy = random.randint(0, num_ships - 1)
                    bullet = Bullet(ships.sprites()[pick_enemy].rect.x, ships.sprites()[pick_enemy].rect.y, 1)
                    e_bullets.add(bullet)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pressed_left = True
                if event.key == pygame.K_RIGHT:
                    pressed_right = True
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(p.rect.x, p.rect.y, 0)
                    bullets.add(bullet)
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
        overlay.update(g.score, g.live)
        bullets.update(g, ships)
        e_bullets.update(g, players)

        ships.update(time_counter)

        players.draw(g.scr)
        ships.draw(g.scr)
        bullets.draw(g.scr)
        e_bullets.draw(g.scr)
        overlay.draw(g.scr)

        pygame.display.update()
        g.clock.tick(60)

        if time_counter >= 400:
            time_counter = 0


if __name__ == '__main__':
    main()
