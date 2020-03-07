import pygame
import random
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./assets/enemyBlue2.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def move_left(self):
        self.x += -1

    def move_right(self):
        self.x += 1


class Game:
    def __init__(self):
        pygame.init()


        #set screen
        self.scr = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Arcade Game")

        #Player related
        self.playerImg = pygame.image.load('./assets/playerShip1_red.png')
        self.playerImg = pygame.transform.scale(self.playerImg, (64, 64))
        self.playerBullet = pygame.image.load('./assets/laserRed02.png')
        self.pX = 350
        self.pY = 500
        self.pXchange = 0
        self.player_bulletX = 0
        self.player_bulletY = self.pY
        self.player_bullet_ychange = 1
        self.bulletState = "go"
        self.score = 0

        #Enemy related
        self.enemyBullet = pygame.image.load('./assets/laserBlue02.png')
        self.eX = [160, 220, 280, 340, 400, 460, 520, 200, 260, 320, 360, 420, 240, 300, 360]
        self.eY = [100, 100, 100, 100, 100, 100, 100, 150, 150, 150, 150, 150, 200, 200, 200]
        self.eXchange = 0
        self.enemy_bulletX = 0
        self.enemy_bulletY = 0
        self.enemy_bullet_ychange = 0
        self.enemies = []
        for i in range(0, 15):
            e = Enemy(self.eX[i], self.eY[i])
            self.enemies.append(e)



    def player(self, x, y):
        self.scr.blit(self.playerImg, (x, y))

    #def enemy(self, x, y):
     #   self.scr.blit(self.enemyImg, (x, y))

    def playerShoot(self, x, y):
        self.bulletState = "moving"
        self.scr.blit(self.playerBullet, (x + 24, y + 10))

    def collisionDetection(self, ex, ey, bx, by):
        distance = math.sqrt((math.pow(ex - bx, 2)) + (math.pow(ey - by, 2)))
        if distance < 30:
            return True
        return False

def main():
    # Game Loop
    ships = pygame.sprite.Group()
    g = Game()
    for i in range(0, 15):
        ships.add(g.enemies[i])
    g = Game()
    run = True
    while run:
        g.scr.fill((0, 0, 0))
        #check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    g.pXchange = -1
                if event.key == pygame.K_RIGHT:
                    g.pXchange = 1
                if event.key == pygame.K_SPACE:
                    if g.bulletState == "go":
                        g.playerShoot(g.pX, g.player_bulletY)
                        g.player_bulletX = g.pX
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    g.pXchange = 0

        #move player based on changed values within boundaries of map
        g.pX += g.pXchange
        if g.pX <= 0:
            g.pX = 0
        elif g.pX >= 700:
            g.pX = 700
        #move enemy back and forth

        #move player bullet
        if g.player_bulletY <= 0:
            g.player_bulletY = 500
            g.bulletState = "go"

        if g.bulletState == "moving":
            g.playerShoot(g.player_bulletX, g.player_bulletY)
            g.player_bulletY -= g.player_bullet_ychange

        #Collision
        for i in range (0,15):
            collision = g.collisionDetection(g.enemies[i].x, g.enemies[i].y, g.player_bulletX, g.player_bulletY)
            if collision:
                g.player_bulletY = 500
                g.bulletState = "go"
                g.score += 10

        g.player(g.pX, g.pY)
        ships.draw(g.scr)
        pygame.display.update()


if __name__ == '__main__':
    main()
