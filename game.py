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
        self.generatePiece()

    def display(self):
        self.main_screen_surface.fill((80,0,0))
        self.main_screen_surface.blit(self.field_surface, self.field_rect)
        self.active_pieces.draw(self.main_screen_surface)
        self.static_pieces.draw(self.main_screen_surface)
        self.main_screen_surface.blit(self.line_surface, self.field_rect)
        self.active_pieces.update()
        if self.piece.final:
            self.replacePiece()
        
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
        """Piece method: Creates a random rotaed structure.
        """
        rotation = randint(1,4)
        array_structure = np.array(structure)
        array_structure = np.rot90(array_structure, k=-rotation)
        return array_structure.tolist()
    
    def generatePiece(self):
        """Piece method: Generates a random Piece instance.
        """
        random_piece = choice(list(PIECES.keys()))
        random_structure = PIECES.get(random_piece)
        random_structure = self.getRandomrotation(random_structure)
        x_position = self.getRandomPositionX(random_structure)
        self.piece = Piece(group = self.active_pieces, field_rect = self.field_rect, initial_x = x_position)
        self.piece.type = random_piece
        self.piece.structure = random_structure
        self.piece.color = choice(PIECES_COLORS)
        self.piece.createPiece()
    
    def updatedField(self):
        """Field method: Insert the Piece structure into the field data.
        """
        self.field_data[self.piece.y][self.piece.x] = 1
        print(self.field_data)

    def replacePiece(self):
        """Piece method: Replace the current Piece and generates a new one.
        """

        self.static_pieces.add(self.piece)
        self.active_pieces.empty()
        self.generatePiece()
    
    def keyboardInput(self, movement:str):
        self.piece.movePiece(movement)
        
        

        
        
        
