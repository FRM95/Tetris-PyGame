import pygame
from random import choice, randint
from settings import *
from piece import Tetromino
from pygame_timer import Timer
from score import Score
from preview import Preview

class Game:

    def __init__(self) -> None:
        self.createScreen()
        self.createField()
        self.createLines()
        self.createScoreField()
        self.createPreviewField()
        self.createSpritesGroup()
        self.setNextPieces()
        self.createPiece()
        self.setTimers()
    
    def setTimers(self):
        self.down_speed = UPDATE_START_SPEED
        self.down_speed_faster = self.down_speed * 0.1
        self.down_pressed = False
        self.timers = {
            'MOVE_DOWN': Timer(self.down_speed, True, self.movePiece),
            'HORIZONTAL_MOVE': Timer(MOVE_WAIT_TIME),
            'ROTATION': Timer(ROTATE_WAIT_TIME)
        }
        self.timers.get('MOVE_DOWN').activate()

    def timerUpdate(self):
        for value in self.timers.values():
            value.update()

    def display(self):
        self.field_surface.fill(FIELD_SURFACE_COLOR)
        self.active_pieces.draw(self.field_surface)
        self.static_pieces.draw(self.field_surface)
        self.main_screen_surface.blit(self.field_surface, self.field_rect)
        self.main_screen_surface.blit(self.line_surface, self.field_rect)
        self.main_screen_surface.blit(self.score_surface, self.score_rect)
        self.main_screen_surface.blit(self.score_line, self.score_rect)
        self.main_screen_surface.blit(self.preview_surface, self.preview_rect)
        self.main_screen_surface.blit(self.preview_line, self.preview_rect)
        self.timerUpdate()
    
    def movePiece(self):
        if not self.piece.pieceFall():
            self.updatefield()
            
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
        for col in range(1, COLUMNS):
            x = col * BLOCK_DIMENSION
            pygame.draw.line(self.line_surface, LINE_COLOR, (x,0), (x, self.field_surface.get_height()))
        for row in range(1, ROWS):
            y = row * BLOCK_DIMENSION
            pygame.draw.line(self.line_surface, LINE_COLOR, (0,y), (self.field_surface.get_width(), y))
        pygame.draw.rect(self.line_surface, BORDER_LINE_COLOR, self.field_surface.get_rect(), width=1)

    def createScoreField(self):
        """Creates Score Field surface
        """
        score_coordinates = (self.field_rect.right + 30, self.field_rect.top)
        score_object = Score(score_coordinates, WIDHT_SCORE_FIELD, HEIGHT_SCORE_FIELD)
        score_object.createLine()
        self.score_surface = score_object.surface
        self.score_rect = score_object.rect
        self.score_line = score_object.line_surface

    def createPreviewField(self):
        """Creates Score Field surface
        """
        preview_coordinates = (self.field_rect.right + 30, self.score_rect.bottom + 10)
        preview_object = Preview(preview_coordinates, WIDHT_PREVIEW_FIELD, HEIGHT_PREVIEW_FIELD)
        preview_object.createLine()
        self.preview_surface = preview_object.surface
        self.preview_rect = preview_object.rect
        self.preview_line = preview_object.line_surface

    def createSpritesGroup(self):
        self.active_pieces = pygame.sprite.Group()
        self.static_pieces = pygame.sprite.Group()

    def updatefield(self):
        for block in self.piece.blocks:
            if block.y <= 0:
                self.game_over = True
                print(self.game_over)
                return False
            else:
                self.field_data[block.y][block.x] = 1
                self.static_pieces.add(block)
        self.active_pieces.empty()
        self.checkRow()
        self.createPiece()

    def checkRow(self):
        found_row = False
        for row_index, row in enumerate(self.field_data[::-1]):
            if all(row):
                found_row = True
                row_index = ROWS - 1 - row_index
                self.field_data.pop(row_index)
                self.field_data.insert(0, [0] * COLUMNS)
                for block in self.static_pieces:
                    if block.y == row_index:
                        self.static_pieces.remove(block)
                    elif block.y < row_index:
                        block.y += 1
                        block.update()
                break
        if found_row:
            self.checkRow()

    def setNextPieces(self):
        self.nextPieces = [choice(PIECES_LIST) for _ in range(3)]

    # def drawNextPieces(self):
    #     for nextPiece in self.nextPieces:
    #         for i_row, row in enumerate(nextPiece):
    #             for i_col, col in enumerate(row):
    #                 if col == 1:
    #                     pygame.draw.rect(self.image, self.color, 
    #                         (BLOCK_DIMENSION * i_col, BLOCK_DIMENSION * i_row, BLOCK_DIMENSION, BLOCK_DIMENSION)

    def createPiece(self):
        random_color = choice(PIECES_COLORS)
        # random_figure = PIECES.get(choice(['I', 'O', 'T', 'L', 'J', 'S', 'Z']))
        random_figure = PIECES.get(self.nextPieces.pop(0))
        self.nextPieces.append(choice(PIECES_LIST))
        x_offset = self.calculateXOffset(random_figure)
        y_offset = self.calculateYOffset(random_figure)
        self.piece = Tetromino(self.active_pieces, 
                            random_color, 
                            random_figure, 
                            x_offset = x_offset,
                            y_offset = y_offset, 
                            time_lapse = DEFAULT_TIME_LAPSE, 
                            field_data = self.field_data)
        print(self.nextPieces)

    def calculateYOffset(self, figure:list):
        y_offset = 0
        for index, row in enumerate(figure):
            if not any(row):
                y_offset += 1
                if any(figure[index+1]):
                    break
        return -y_offset-1
    
    def calculateXOffset(self, figure:list):
        max_structure = len(max(figure, key = lambda x: sum(x)))
        x_offset = randint(0,9)
        if x_offset + max_structure > 10:
            x_offset = 10 - max_structure
        return x_offset


    def keyboardInput(self):
        keys = pygame.key.get_pressed()

        # Checking horizontal movement
        if not self.timers['HORIZONTAL_MOVE'].active:

            if keys[pygame.K_a]:
                self.piece.movePiece('LEFT')
                self.timers['HORIZONTAL_MOVE'].activate()

            if keys[pygame.K_d]:
                self.piece.movePiece('RIGHT')
                self.timers['HORIZONTAL_MOVE'].activate()

        # Checking rotation movement
        if not self.timers['ROTATION'].active:

            if keys[pygame.K_SPACE]:
                self.piece.movePiece('ROTATE')
                self.timers['ROTATION'].activate()

        # Fast DOWN MOVEMENT
        if not self.down_pressed and keys[pygame.K_s]:
            self.down_pressed = True
            self.timers['MOVE_DOWN'].duration = self.down_speed_faster

        # Normal DOWN MOVEMENT
        if self.down_pressed and not keys[pygame.K_s]:
            self.down_pressed = False
            self.timers['MOVE_DOWN'].duration = self.down_speed
        
        

        
        
        
