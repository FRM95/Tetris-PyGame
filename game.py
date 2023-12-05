import pygame
import numpy as np
from random import choice, randint
from piece import Piece
from settings import *

class Game:

    def __init__(self) -> None:
        self.id_counter = 0
        self.createScreen()
        self.createField()
        self.createLines()
        self.createGroups()
        self.generatePiece()

    def display(self):
        self.main_screen_surface.fill((80,0,0))
        self.main_screen_surface.blit(self.field_surface, self.field_rect)
        self.active_pieces.draw(self.main_screen_surface)
        self.static_pieces.draw(self.main_screen_surface)
        self.main_screen_surface.blit(self.line_surface, self.field_rect)
        self.active_pieces.update()
        if self.piece.final:
            self.updateFieldData()
            self.checkCompleteRows()
            self.addNewPiece()
        
    def createScreen(self):
        """Creates PyGame main screen surface and rectangle
        """
        self.main_screen_surface = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
        self.main_screen_rect = self.main_screen_surface.get_rect()
        self.main_screen_surface.fill(MAIN_SCREEN_SURFACE_COLOR)
        
    def createField(self):
        """Creates Game Field surface, rectangle and data
        """
        self.field_surface = pygame.surface.Surface((WIDTH_FIELD, HEIGHT_FIELD)).convert_alpha()
        self.field_rect = self.field_surface.get_rect(center = (self.main_screen_rect.centerx * 0.7, self.main_screen_rect.centery))
        self.field_data = [[0] * COLUMNS for _ in range(ROWS)]

    def createLines(self):
        """Creates a line surface from Field Surface.
        Draw column and row lines on the line surface.
        """
        self.line_surface = self.field_surface.copy().convert_alpha()
        self.line_surface.fill(LINE_SURFACE_COLOR)
        self.line_surface.set_colorkey(LINE_SURFACE_COLOR)
        self.line_surface.set_alpha(LINE_SURFACE_ALPHA)
        pygame.draw.rect(self.line_surface, LINE_COLOR, self.field_surface.get_rect(), width=1)
        for col in range(1, COLUMNS):
            x = col * BLOCK_DIMENSION
            pygame.draw.line(self.line_surface, LINE_COLOR, (x,0), (x, self.field_surface.get_height()))
        for row in range(1, ROWS):
            y = row * BLOCK_DIMENSION
            pygame.draw.line(self.line_surface, LINE_COLOR, (0,y), (self.field_surface.get_width(), y))

    def createGroups(self):
        """Sprite method: Creates active and static Sprites groups.
        """
        self.active_pieces = pygame.sprite.GroupSingle()
        self.static_pieces = pygame.sprite.Group()

    def getRandomPositionX(self, structure):
        """Piece method: Creates a random offset for x axis.
        """
        max_structure = len(max(structure))
        randomposition = randint(0,9)
        if randomposition + max_structure > 10:
            randomposition = 10 - max_structure
        return randomposition
    
    def getRandomrotation(self, structure):
        """Piece method: Creates a random rotated structure.
        """
        rotation = randint(1,4)
        array_structure = np.array(structure)
        array_structure = np.rot90(array_structure, k=-rotation)
        return array_structure.tolist()
    
    def generatePiece(self):
        """Piece method: Generates a random Piece instance.
        """
        random_piece = choice(list(PIECES.keys()))
        # random_piece = 'I'
        random_structure = PIECES.get(random_piece)
        random_structure = self.getRandomrotation(random_structure)
        x_position = self.getRandomPositionX(random_structure)
        self.piece = Piece(group = self.active_pieces, field_rect = self.field_rect, initial_x = x_position, field_data = self.field_data)
        self.piece.type = random_piece
        self.piece.structure = random_structure
        self.piece.color = choice(PIECES_COLORS)
        self.id_counter += 1
        self.piece.id = self.id_counter
        self.piece.createPiece()
    
    def updateFieldData(self):
        """Field method: Insert the Piece structure into the field data. Update Field data.
        """
        aux_x = self.piece.x
        aux_y = self.piece.y
        for row in self.piece.structure:
            for col in row:
                if col == 1:
                    self.field_data[aux_y][aux_x] = self.piece.id
                aux_x += 1
            aux_y += 1
            aux_x=self.piece.x
        self.static_pieces.add(self.piece)

    def checkCompleteRows(self):
        """Field and Piece method: Check for completed rows. Updates sprites in static_pieces and updates field data.
        """
        completed_row = None
        for row_i, row in enumerate(self.field_data[::-1]):
            if all(row):
                colision_point_y = ROWS-1-row_i
                completed_row = row
                for sprite in self.static_pieces:
                    if sprite.id in completed_row:
                        rect_to_remove = colision_point_y - sprite.y
                        sprite.structure.pop(rect_to_remove)
                        if len(sprite.structure) > 0:
                            sprite.createPiece(was_static = True)
                        else: 
                            sprite.kill()
                self.field_data.pop(colision_point_y)
                self.field_data.insert(0, [0] * COLUMNS)
                for sprite in self.static_pieces:
                    if sprite.y <= colision_point_y:
                        sprite.rect.x = sprite.x * BLOCK_DIMENSION + sprite.x_offset
                        sprite.y +=1
                        sprite.rect.y = sprite.y * BLOCK_DIMENSION + sprite.y_offset
                self.checkCompleteRows()
                break

    def addNewPiece(self):
        """Piece method: Replace the current Piece and generates a new one.
        """
        self.active_pieces.empty()
        self.generatePiece()
    
    def keyboardInput(self, movement:str):
        self.piece.movePiece(movement)
        
        

        
        
        
