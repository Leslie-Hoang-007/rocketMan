import pygame

class background(pygame.sprite.Sprite):#background
    def update(self,dt):
        self.pos.x -= 300 * dt
        if self.rect.centerx <=0:
            self.pox.x = 0
        self.rect.x = round(self.pos.x)