from typing import Any
import pygame
from settings import *

class Piece(pygame.sprite.Sprite):

    def __init__(self, group, x_offset, y_offset) -> None:
        super().__init__(group)
        self.structure = None
        self.color = None
        self.rect = None
        self.image = None
        self.type = None
        self.x = 0
        self.y = 0
        self.x_offset = x_offset
        self.y_offset = y_offset

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
                    
        self.rect = self.image.get_rect(topleft = (self.x * BLOCK_DIMENSION + self.x_offset, self.y * BLOCK_DIMENSION + self.y_offset))

    def movePiece(self, movement:str):

        match movement:
            case 'DOWN':
                self.y += 1
            case 'UP':
                self.y -= 1
            case 'LEFT':
                self.x -= 1
            case 'RIGHT':
                self.x += 1

        self.rect.x = self.x * BLOCK_DIMENSION + self.x_offset
        self.rect.y = self.y * BLOCK_DIMENSION + self.y_offset

    def update(self):
        self.movePiece('DOWN')
        print('movement')
       
    