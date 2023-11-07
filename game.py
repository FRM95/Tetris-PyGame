import pygame
from settings import *

class Game:

    def __init__(self) -> None:
        self.createScreen()
        self.createField()
        self.createLines()

    def display(self):
        self.main_screen_surface.fill((0,0,0))
        self.main_screen_surface.blit(self.field_surface, self.field_rect)
        self.main_screen_surface.blit(self.line_surface, self.field_rect)

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
        self.field_surface.fill(FIELD_SURFACE_COLOR)

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

        

        
        
        
