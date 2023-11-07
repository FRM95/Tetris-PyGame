import pygame
from settings import *

class Piece(pygame.sprite.Sprite):

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.structure = None
        self.color = None
        self.rect = None
        self.image = None
        self.type = None

    def createPiece(self):
        self.createImage()
        self.createRect()

    def createImage(self):
        width = len(self.structure[0]) * BLOCK_DIMENSION
        height = len(self.structure) * BLOCK_DIMENSION
        self.image = pygame.surface.Surface((width, height)).convert_alpha()
        self.image.fill((0,255,0))
        self.image.set_colorkey((0,255,0))

    def createRect(self):
        for i_row, row in enumerate(self.structure):
            for i_col, col in enumerate(row):
                if col == 1:
                    pygame.draw.rect(self.image, self.color, 
                        (BLOCK_DIMENSION * i_col, BLOCK_DIMENSION * i_row, BLOCK_DIMENSION, BLOCK_DIMENSION))
        self.rect = self.image.get_rect(topleft = (0,0))

       
    