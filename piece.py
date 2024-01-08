import pygame
from settings import *
import numpy as np

class Block(pygame.sprite.Sprite):

    def __init__(self, group, color, initial_position, field_data) -> None:
        super().__init__(group)
        self.image = pygame.Surface((BLOCK_DIMENSION, BLOCK_DIMENSION))
        self.image.fill(color)
        self.x = initial_position[0]
        self.y = initial_position[1]
        self.field_data = field_data
        self.rect = self.image.get_rect(topleft = (self.x * BLOCK_DIMENSION, self.y * BLOCK_DIMENSION))

    def allowedBottom(self):
        if (self.y >= ROWS - 1) or (self.y < ROWS - 1 and self.field_data[self.y+1][self.x] == 1):
            return False
        else: 
            return True

    def allowedLeft(self):
        if (self.x <= 0) or (self.x > 0 and self.field_data[self.y][self.x-1] == 1):
            return False
        else: 
            return True
        
    def allowedRight(self):
        if (self.x >= COLUMNS - 1) or (self.x < COLUMNS - 1 and self.field_data[self.y][self.x+1] == 1):
            return False
        else: 
            return True
        
    def allowedRotate(self, block):
        if (block[0] < 0 or block[0] > COLUMNS - 1) or (block[1] < 0 or block[1] > ROWS - 1) or self.field_data[block[1]][block[0]] == 1:
            return False
        else:
            return True

    def update(self):
        self.rect.x = self.x * BLOCK_DIMENSION
        self.rect.y = self.y * BLOCK_DIMENSION

class Tetromino:

    def __init__(self, group, color, structure, x_offset = 0, y_offset = 0, time_lapse = 0, field_data = None) -> None:
        self.structure = structure
        self.color = color
        self.group = group
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.block_positions, self.figure_positions = self.initialPositions()
        self.blocks = [Block(self.group, self.color, pos, field_data) for pos in self.block_positions]
        self.time_lapse = time_lapse
        self.time_movement = 0
        
    def initialPositions(self):
        block_list = []
        full_block_list = []
        for i_row, row in enumerate(self.structure):
            row_list = []
            for i_col, col in enumerate(row):
                if col == 1:
                    block_list.append((i_col + self.x_offset, i_row + self.y_offset))
                row_list.append((i_col + self.x_offset, i_row + self.y_offset))
            full_block_list.append(row_list)
        return block_list, full_block_list
    
    def movePiece(self, movement:str):

        match movement:

            case 'DOWN':

                for block in self.blocks:
                    if not block.allowedBottom():
                        return False
                
                for block in self.blocks:
                    block.y+=1
                    block.update()
                
                for row_i, row in enumerate(self.figure_positions):
                    for col_i, col in enumerate(row):
                        new_val = (col[0], col[1]+1)
                        self.figure_positions[row_i][col_i] = new_val

            case 'LEFT':
                
                for block in self.blocks:
                    if not block.allowedLeft():
                        return False

                for block in self.blocks:
                    block.x-=1
                    block.update()
                
                for row_i, row in enumerate(self.figure_positions):
                    for col_i, col in enumerate(row):
                        new_val = (col[0]-1, col[1])
                        self.figure_positions[row_i][col_i] = new_val
                        
            case 'RIGHT':

                for block in self.blocks:
                    if not block.allowedRight():
                        return False

                for block in self.blocks:
                    block.x+=1
                    block.update()

                for row_i, row in enumerate(self.figure_positions):
                    for col_i, col in enumerate(row):
                        new_val = (col[0]+1, col[1])
                        self.figure_positions[row_i][col_i] = new_val
            
            case 'ROTATE':
                rotated_structure = self.rotateTetronimo(self.structure)
                aux_blocks = self.recreateBlocksList(rotated_structure, self.figure_positions)
                for auxliar_block in aux_blocks:
                    if not self.blocks[0].allowedRotate(auxliar_block):
                        return False

                for block_index, block in enumerate(self.blocks):
                    block.x = aux_blocks[block_index][0]
                    block.y = aux_blocks[block_index][1]
                    block.update()
                self.structure = rotated_structure

        return True
    
    def rotateTetronimo(self, structure:list):
        aux_structure = np.rot90(structure, k = -1)
        return aux_structure.tolist()
        
    def recreateBlocksList(self, structure:list, figure:list):
        new_blocks = []
        for i_row, row in enumerate(structure):
            for i_col, col in enumerate(row):
                if col==1:
                    new_blocks.append(figure[i_row][i_col])
        return new_blocks
        
    # def pieceFall(self):
    #     self.time_movement += self.time_lapse
    #     if self.time_movement >= 1:
    #         piece_falling = self.movePiece('DOWN')
    #         self.time_movement = 0
    #         return piece_falling
    #     else:
    #         return True
        
    def pieceFall(self):
        piece_falling = self.movePiece('DOWN')
        return piece_falling
      
            



                
        
        
        