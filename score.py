from custom_surface import CustomSurface
from pygame import font, draw, surface

class Score(CustomSurface):

    def __init__(self, coordinates, width, height) -> None:
        super().__init__(coordinates, width, height)

    def createText(self, input:str = "", color:tuple = (255,255,255), background_color:tuple = (0,0,0), size:int = 32):
        font_text = font.Font('freesansbold.ttf', size)
        text_surface = font_text.render(input, True, color, background_color).convert_alpha()
        text_rect = text_surface.get_rect()
        return text_surface, text_rect

    def displayScore(self, score:int, color:tuple = (255,255,255), background_color:tuple = (0,0,0), size:int = 20):
        font_text = font.Font('freesansbold.ttf', size)
        self.points_surface = font_text.render(str(score), True, color, background_color).convert_alpha()
        self.points_rect = self.points_surface.get_rect()

    def displayLevel(self, level:int, color:tuple = (255,255,255), background_color:tuple = (0,0,0), size:int = 20):
        font_text = font.Font('freesansbold.ttf', size)
        self.level_surface = font_text.render(str(level), True, color, background_color).convert_alpha()
        self.level_rect = self.points_surface.get_rect()

    def updateScore(self, new_score:int):
        self.displayScore(new_score)

    def updateLevel(self, new_level:int):
        self.displayLevel(new_level)