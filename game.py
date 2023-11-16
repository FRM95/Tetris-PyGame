import pygame
import numpy as np
from random import choice, randint
from piece import Piece
from settings import *

class Game:

    def __init__(self) -> None:
        self.createScreen()
        self.createField()
        self.createLines()
        self.createGroups()
        self.createPiece()

    def display(self):
        self.main_screen_surface.fill((80,0,0))
        self.main_screen_surface.blit(self.field_surface, self.field_rect)
        self.active_pieces.draw(self.main_screen_surface)
        self.main_screen_surface.blit(self.line_surface, self.field_rect)
        # self.active_pieces.update()
        
    def createScreen(self):
        """Creates PyGame main screen surface and rectangle
        """
        self.main_screen_surface = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
        self.main_screen_rect = self.main_screen_surface.get_rect()
        self.main_screen_surface.fill(MAIN_SCREEN_SURFACE_COLOR)
        
    def createField(self):
        """Creates Game Field surface and rectangle
        """
        self.field_surface = pygame.surface.Surface((WIDTH_FIELD, HEIGHT_FIELD)).convert_alpha()
        self.field_rect = self.field_surface.get_rect(center = (self.main_screen_rect.centerx * 0.7, self.main_screen_rect.centery))
        # self.field_surface.fill(FIELD_SURFACE_COLOR)

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
        self.active_pieces = pygame.sprite.GroupSingle()
        self.static_pieces = pygame.sprite.Group()
 
    def createPiece(self):
        """Creates a random Piece instance.
        """
        random_piece = choice(list(PIECES.keys()))
        random_structure = PIECES.get(random_piece)
        random_structure = self.getRandomrotation(random_structure)

        x_offset = self.getRandomOffset_x(random_structure)
        y_offset = self.field_rect.top

        self.piece = Piece(self.active_pieces, x_offset, y_offset)
        self.piece.type = random_piece
        self.piece.structure = random_structure
        self.piece.color = choice(PIECES_COLORS)
        self.piece.createPiece()

    def getRandomOffset_x(self, structure):
        """Creates a random offset for x axis.
        """
        max_structure = len(max(structure))
        randomposition = randint(0,9)
        if randomposition + max_structure > 10:
            randomposition = 10 - max_structure
        return self.field_rect.left + randomposition * BLOCK_DIMENSION
    
    def getRandomrotation(self, structure):
        """Creates a random rotaed structure.
        """
        rotation = randint(1,4)
        array_structure = np.array(structure)
        array_structure = np.rot90(array_structure, k=-rotation)
        return array_structure.tolist()
        

        
        
        
