import pygame


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, direction):
        
        super().__init__()
        self.images = []
        self.images[0] = pygame.image.load('./assets/laserRed02.png').convert_alpha()
        self.images[1] = pygame.image.load('./assets/laserBlue02.png').convert_alpha()
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
            game.bullet_state = "moving"
            self.y += self.y_change
        if self.direction == 1:
            game.bullet_state = "moving"
            self.y -= self.y_change
        hit_object = pygame.sprite.spritecollideany(self, ships)
        if hit_object:
            hit_object.kill()
            game.score += 10
