from typing import Any
import pygame
from settings import *
import numpy as np

class Piece(pygame.sprite.Sprite):

    def __init__(self, group, field_rect, initial_x:int = 0, initial_y:int = 0, time_lapse:float = DEFAULT_TIME_LAPSE, field_data = None) -> None:
        super().__init__(group)
        self.structure = None
        self.color = None
        self.type = None
        self.id = None
        self.field_rect = field_rect
        self.x = initial_x
        self.y = initial_y
        self.time_lapse = time_lapse
        self.field_data = field_data
        self.time_movement = 0

    def createPiece(self, was_static = False):
        self.createImage()
        self.createRect()
        self.limit_x = (self.field_rect.left, self.field_rect.right)
        self.limit_y = (self.field_rect.top, self.field_rect.bottom)
        if was_static:
            self.final = True
        else:
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
                # if col == 0:
                #         pygame.draw.rect(self.image, self.color, 
                #             (BLOCK_DIMENSION * i_col, BLOCK_DIMENSION * i_row, BLOCK_DIMENSION, BLOCK_DIMENSION), width=1)    
                           
        self.rect = self.image.get_rect(topleft = (self.x * BLOCK_DIMENSION + self.x_offset, self.y * BLOCK_DIMENSION + self.y_offset))
        self.mask = pygame.mask.from_surface(self.image)

    def movePiece(self, movement:str):
        movement_allowed = self.movementAllowed(movement)
        if movement_allowed:
            match movement:
                case 'DOWN':
                    self.y += 1
                case 'LEFT':
                    self.x -= 1
                case 'RIGHT':
                    self.x += 1
                case 'ROTATE':
                    numpy_structure = np.array(self.structure)
                    numpy_structure = np.rot90(numpy_structure, k=-1)
                    self.structure = numpy_structure.tolist()
                    self.createPiece()

            self.rect.x = self.x * BLOCK_DIMENSION + self.x_offset
            self.rect.y = self.y * BLOCK_DIMENSION + self.y_offset

        return movement_allowed
            
    def movementAllowed(self, movement:str):
        allowed_movement = True
        match movement:
            case 'DOWN':

                for row_i, row in enumerate(self.structure):
                    for col_i, col in enumerate(row):

                        line_x = self.x+col_i
                        line_y = self.y+row_i

                        if col == 1 and line_y == ROWS-1:
                            allowed_movement = False 
                            self.final = True

                        elif col == 1 and line_y+1 < ROWS and line_y >= 0:
                            if self.field_data[line_y+1][line_x] != 0:
                                allowed_movement = False 
                                self.final = True
                        
                                
                # if self.rect.bottom >= self.limit_y[1]:
                #     allowed_movement = False
                #     self.final = True

            case 'LEFT':

                for row_i, row in enumerate(self.structure):

                    for col_i, col in enumerate(row):

                        line_x = self.x + col_i
                        line_y = self.y + row_i

                        if col == 1 and line_x == 0:
                            allowed_movement = False 

                        elif col == 1 and line_x - 1 >= 0 and line_y >= 0:
                            if self.field_data[line_y][line_x - 1] != 0:
                                allowed_movement = False
                            

                # if self.rect.left <= self.limit_x[0] or self.rect.bottom >= self.limit_y[1]:
                #     allowed_movement = False

            case 'RIGHT':
 
                for row_i, row in enumerate(self.structure):
                    for col_i, col in enumerate(row[::-1]):

                        line_x = self.x + len(row) - col_i
                        line_y = self.y + row_i

                        if col == 1 and line_x >= COLUMNS:
                            allowed_movement = False

                        elif col == 1 and line_x < COLUMNS and line_y >= 0:
                            if self.field_data[line_y][line_x] != 0:
                                allowed_movement = False
                            
                # if self.rect.right >= self.limit_x[1] or self.rect.bottom >= self.limit_y[1]:
                #     allowed_movement = False


            case 'ROTATE':

                if self.type != 'O':
                    for row_i, row in enumerate(self.structure):
                        for col_i, col in enumerate(row):
                            if col == 0:
                                line_x = self.x + col_i
                                line_y = self.y + row_i

                                if line_x < 0 or line_x >= COLUMNS:
                                    allowed_movement = False 

                                elif line_y < 0 or line_y >= ROWS:
                                    allowed_movement = False 

                                elif self.field_data[line_y][line_x] != 0:
                                    allowed_movement = False
                    
        return allowed_movement

    def pieceFall(self):
        self.time_movement += self.time_lapse
        if self.time_movement >= 1:
            if not self.movePiece('DOWN'):
                self.final = True
            self.time_movement = 0
            
    def update(self):
        if not self.final:
            self.pieceFall()
        
       
    