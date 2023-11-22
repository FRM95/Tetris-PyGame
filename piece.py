from typing import Any
import pygame
from settings import *

class Piece(pygame.sprite.Sprite):

    def __init__(self, group, field_rect, initial_x:int = 0, initial_y:int = 0, time_lapse:float = DEFAULT_TIME_LAPSE) -> None:
        super().__init__(group)
        self.structure = None
        self.color = None
        self.type = None
        self.field_rect = field_rect
        self.x = initial_x
        self.y = initial_y
        self.time_lapse = time_lapse

    def createPiece(self):
        self.createImage()
        self.createRect()
        self.time_movement = 0
        self.limit_x = (self.field_rect.left, self.field_rect.right)
        self.limit_y = (self.field_rect.top, self.field_rect.bottom)
        self.final = False

    def createImage(self):
        width = len(self.structure[0]) * BLOCK_DIMENSION
        height = len(self.structure) * BLOCK_DIMENSION
        self.image = pygame.surface.Surface((width, height)).convert_alpha()
        self.image.fill((0,255,0))
        self.image.set_colorkey((0,255,0))

    def createRect(self):
        self.x_offset = self.field_rect.left
        self.y_offset = self.field_rect.top
        for i_row, row in enumerate(self.structure):
            for i_col, col in enumerate(row):
                if col == 1:
                    pygame.draw.rect(self.image, self.color, 
                        (BLOCK_DIMENSION * i_col, BLOCK_DIMENSION * i_row, BLOCK_DIMENSION, BLOCK_DIMENSION))          
        self.rect = self.image.get_rect(topleft = (self.x * BLOCK_DIMENSION + self.x_offset, self.y * BLOCK_DIMENSION + self.y_offset))
        self.mask = pygame.mask.from_surface(self.image)

    def movePiece(self, movement:str):
        movement_allowed = self.movementAllowed(movement)
        if movement_allowed:
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
            print(self.x, self.y)
            print('MOVEMENT DONE ' + movement)
        return movement_allowed
            
    def movementAllowed(self, movement:str):
            allowed_movement = True
            match movement:
                case 'DOWN':
                    if self.rect.bottom >= self.limit_y[1]:
                        allowed_movement = False
                case 'UP':
                    pass
                case 'LEFT':
                    if self.rect.left <= self.limit_x[0] or self.rect.bottom >= self.limit_y[1]:
                        allowed_movement = False
                case 'RIGHT':
                    if self.rect.right >= self.limit_x[1] or self.rect.bottom >= self.limit_y[1]:
                        allowed_movement = False
            return allowed_movement
    
    def checkCollision(self):
        pass

    def pieceFall(self):
        self.time_movement += self.time_lapse
        if self.time_movement >= 1:
            if not self.movePiece('DOWN'):
                self.final = True
            self.time_movement = 0
            
    def update(self):
        if not self.final:
            self.pieceFall()
        
       
    