import pygame
import random
import sys
sys.path.append('..')


#enemy class holds enemies and their logic 
class Enemy(pygame.sprite.Sprite):
    
    #initiator
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./assets/enemyBlue2.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y

    #moves enemy right
    def move_right(self):
        self.rect.x += 2

    #moves enemy left
    def move_left(self):
        self.rect.x -= 2

    #updates enemy according to positoin
    def update(self, time_counter):

        if time_counter < 200:
            self.move_right()
        if time_counter > 200:
            self.move_left()

#overlay class displays game info
class Overlay(pygame.sprite.Sprite):
    
    #contructor
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([800, 40])
        self.image.fill((127, 127, 127))
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font('freesansbold.ttf', 18)
        self.render('Score: 0        Lives: 3')

    #renders text
    def render(self, text):
        self.text = self.font.render(text, True, (255, 255, 255))
        self.image.blit(self.text, self.rect)

    #draws text
    def draw(self, screen):
        screen.blit(self.text, (0, 0))

    #updates text
    def update(self, score, lives):
        self.render('Score: ' + str(score) + '        Lives: ' + str(lives))
       


#bullet class makes bullet, checks for collisions and updates
class Bullet(pygame.sprite.Sprite):

    #contsructor
    def __init__(self, x, y, direction):

        super().__init__()
        self.images = []
        self.images.append(pygame.image.load('./assets/laserRed02.png'))
        self.images.append(pygame.image.load('./assets/laserBlue02.png'))
        self.images.append(pygame.image.load('./assets/laserGreen02.png'))
        self.x = x + 24
        self.y = y + 10
        # direction will be 0 = up, 1 = down
        self.direction = direction

        self.image = self.images[direction]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.y_change = 10
        self.last_hit = pygame.time.get_ticks()

    #update
    def update(self, game, ships):

        if self.direction == 0:
            self.rect.y -= self.y_change
            hit_object = pygame.sprite.spritecollideany(self, ships)
            if hit_object:
                game.enemyDeath.play()
                hit_object.kill()
                game.bullets.remove(self)
                game.score += 10
                if(len(game.ships) == 0): #if no ships left make new ships
                    for i in range(0, 15):
                        game.ships.add(Enemy(game.eX[i], game.eY[i]))
                if(game.score != 0 and game.score % 250 == 0): #every 250 points add extra life
                    game.live += 1        

        if self.direction == 1:
          
            self.rect.y += self.y_change 
            hit_object = pygame.sprite.spritecollideany(self, ships)
            if hit_object:
                now = pygame.time.get_ticks()
                if now - self.last_hit > 400:
                    game.live -= 1
                    self.last_hit = now
                    game.e_bullets.remove(self)
                if game.live <= 0:
                    hit_object.kill()
        if self.direction == 2:
            pass

#player class
class Player(pygame.sprite.Sprite):
    
    #constructor
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('./assets/playerShip1_red.png')
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y

    
    #moves left
    def move_left(self):
        self.rect.x -= 8
    #moves rigt
    def move_right(self):
        self.rect.x += 8


#game class holds ships and sounds
class Game:
    def __init__(self):
        pygame.init()

        # set screen
        self.scr = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Arcade Game")

        self.enemyDeath = pygame.mixer.Sound('./assets/sfx_twoTone.ogg')
        self.enemyDeath.set_volume(0.8)

        
        # Player related
        self.score = 0
        self.live = 3
        self.lastShot = pygame.time.get_ticks()

        #holds bullets
        self.bullets = pygame.sprite.Group()
        self.e_bullets = pygame.sprite.Group()

        # Enemy related
        self.eX = [0, 60, 120, 180, 240, 300, 360, 30, 100, 170, 240, 310, 60, 160, 260]
        self.eY = [100, 100, 100, 100, 100, 100, 100, 150, 150, 150, 150, 150, 200, 200, 200]

        self.game_over_font = pygame.font.Font('freesansbold.ttf', 64)

        self.clock = pygame.time.Clock()
        #create enemies
        self.ships = pygame.sprite.Group()
        
        for i in range(0, 15):
         
            self.ships.add(Enemy(self.eX[i], self.eY[i]))
    
    #displays game over text
    def game_over_text(self):
        self. over_text = self.game_over_font.render("GAME OVER", True, (255, 255, 255))
        self.scr.blit(self.over_text, (200, 250))


#main method
def main():
    # create event for enemy shooting
    g = Game()
    shoot_event = pygame.USEREVENT + 1
    pygame.time.set_timer(shoot_event, 800)
    # Game Loop
    players = pygame.sprite.Group()
    p = Player(350, 480)
    players.add(p)
    pressed_left = False
    pressed_right = False
    overlay = Overlay()
   
    run = True
    time_counter = 0


    #load sounds
    shot_sound = pygame.mixer.Sound('./assets/sfx_laser1.ogg')
    shot_sound_enemy = pygame.mixer.Sound('./assets/sfx_laser2.ogg')
    
    shot_sound.set_volume(0.4)
    shot_sound_enemy.set_volume(0.4)


    #game loop
    while run:
        g.scr.fill((0, 0, 0))
        # check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = Falserand
            if event.type == shoot_event:
                num_ships = 0
                for e in g.ships:
                    if isinstance(e, Enemy):
                        num_ships += 1
                if num_ships != 0:
                    pick_enemy = random.randint(0, num_ships - 1)
                    bullet = Bullet(g.ships.sprites()[pick_enemy].rect.x, g.ships.sprites()[pick_enemy].rect.y, 1)
                    bullet.y_change = random.randint(1, 15)
                    if(bullet.y_change < 5):
                        bullet.image= bullet.images[2]
                    elif(bullet.y_change > 5 and bullet.y_change< 11):
                        bullet.image=bullet.images[1] 
                    else:
                        bullet.image = bullet.images[0]  
                    shot_sound_enemy.play() 

                    g.e_bullets.add(bullet)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pressed_left = True
                if event.key == pygame.K_RIGHT:
                    pressed_right = True
                if event.key == pygame.K_SPACE:
                    if g.live > 0:
                        now = pygame.time.get_ticks()
                        if now - g.lastShot > 400:
                            bullet = Bullet(p.rect.x, p.rect.y, 0)
                            g.bullets.add(bullet)
                            g.lastShot = now
                            shot_sound.play()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    pressed_left = False
                if event.key == pygame.K_RIGHT:
                    pressed_right = False
            

        # move player based on changed values within boundaries of map
        if pressed_left:
            p.move_left()
        if pressed_right:
            p.move_right()
        if p.rect.x <= 0:
            p.rect.x = 0
        elif p.rect.x >= 700:
            p.rect.x = 700

        #update
        time_counter += 1
        g.bullets.update(g, g.ships)
        g.e_bullets.update(g, players)
        g.ships.update(time_counter)
        players.update()
        overlay.update(g.score, g.live)
        #draw
        players.draw(g.scr)
        g.ships.draw(g.scr)
        g.bullets.draw(g.scr)
        g.e_bullets.draw(g.scr)
        overlay.draw(g.scr)
        #check for game over
        if g.live == 0 or not g.ships:
            g.game_over_text()

        pygame.display.update()
        g.clock.tick(60)

        if time_counter >= 400:
            time_counter = 0


if __name__ == '__main__':
    main()
