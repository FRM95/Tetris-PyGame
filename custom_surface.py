from settings import *
import pygame

class CustomSurface:

    def __init__(self, coordinates:tuple, width:int, height:int) -> None:
        self.coordinates = coordinates
        self.createSurface(width, height)

    def createSurface(self, width:int, height:int):
        self.surface = pygame.surface.Surface((width, height)).convert_alpha()
        self.rect = self.surface.get_rect(topleft = self.coordinates)

    def createLine(self):
        self.line_surface = self.surface.copy().convert_alpha()
        self.line_surface.fill(LINE_SURFACE_COLOR)
        self.line_surface.set_colorkey(LINE_SURFACE_COLOR)
        pygame.draw.rect(self.line_surface, BORDER_LINE_COLOR, self.surface.get_rect(), width=1)