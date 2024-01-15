from settings import *
import pygame

class CustomSurface:

    def __init__(self, coordinates:tuple, width:int, height:int) -> None:
        self.coordinates = coordinates
        self.createSurface(width, height)

    def createSurface(self, width:int, height:int):
        self.surface = pygame.surface.Surface((width, height)).convert_alpha()
        self.rect = self.surface.get_rect(topleft = self.coordinates)
        
    def addBorderLine(self, color:tuple):
        pygame.draw.rect(self.surface, color, self.surface.get_rect(), width=1)
