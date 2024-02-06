from custom_surface import CustomSurface
from pygame import font, draw, surface
from settings import * 

class Preview(CustomSurface):

    def __init__(self, coordinates, width, height) -> None:
        super().__init__(coordinates, width, height)

    def createText(self, input:str = "", color:tuple = (255,255,255), background_color = None, size:int = 32):
        font_text = font.Font('freesansbold.ttf', size)
        self.text_surface = font_text.render(input, True, color, background_color).convert_alpha()
        self.text_rect = self.text_surface.get_rect()

class NextPiece():

    def __init__(self, piece_item:tuple) -> None:
        self.piece_structure = piece_item[0]
        self.piece_color = piece_item[1]

    def createImage(self):
        square_size = len(self.piece_structure) * BLOCK_DIMENSION
        coordinates = (square_size, square_size)
        self.image = surface.Surface(coordinates).convert_alpha()
        self.image.fill((0,255,0))
        self.image.set_colorkey((0,255,0))

    def drawNextPiece(self):
        self.createImage()
        for i_row, row in enumerate(self.piece_structure):
            for i_col, col in enumerate(row):
                if col == 1:
                    draw.rect(self.image, self.piece_color, 
                        (BLOCK_DIMENSION * i_col, BLOCK_DIMENSION * i_row, BLOCK_DIMENSION, BLOCK_DIMENSION))
                    draw.rect(self.image, (0,0,0), 
                        (BLOCK_DIMENSION * i_col, BLOCK_DIMENSION * i_row, BLOCK_DIMENSION, BLOCK_DIMENSION), width=1)
        return self.image
    
    def getRect(self):
        return self.image.get_rect()

    def updateItem(self, new_item:tuple):
        self.piece_structure = new_item[0]
        self.piece_color = new_item[1]
    
    def getItem(self):
        return (self.piece_structure, self.piece_color)

