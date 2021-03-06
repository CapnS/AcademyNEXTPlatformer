import pygame
import sys
import os
import getopt

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.y = y
        self.x = x
        #Create a temp image for the platform... will replace with sprite
        self.image = pygame.image.load(os.path.join('sprite_art','Multi_Platformer_Tileset_v2','Grassland','Terrain','platform.png'))

        #creates a pygame rect to move
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x, self.y)

    def move(self, tick):
        #moves the rectanlge to the left and updates the rect variable
        speed = .085
        left = -tick*speed
        self.x += left
        if (self.x+left+self.width < 0):
            return True
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
