import pygame
from random import choice, randint
from settings import *
from piece import Tetromino
from pygame_timer import Timer
from score import Score
from preview import Preview, NextPiece
from pygame import font

class Game:

    def __init__(self) -> None:
        self.createScreen()
        self.createInitialText()
        self.createField()
        self.createLines()
        self.initiateScore()
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
        self.main_screen_surface.blit(self.score_text_surface, self.score_text_rect)
        self.main_screen_surface.blit(self.points_text_surface, self.points_text_rect)
        self.main_screen_surface.blit(self.level_text_surface, self.level_text_rect)
        self.main_screen_surface.blit(self.level_number_surface, self.level_number_rect)
        self.main_screen_surface.blit(self.preview_surface, self.preview_rect)
        self.main_screen_surface.blit(self.preview_text_surface, self.preview_text_rect)
        self.main_screen_surface.blit(self.next_piece_surface, self.next_piece_rect)

        if self.game_over:
            self.main_screen_surface.blit(self.transparent_surf, (0,0))
            self.main_screen_surface.blit(self.game_over_text, self.game_over_text_rect)
            self.main_screen_surface.blit(self.ended_menu, self.ended_menu_rect)
            self.main_screen_surface.blit(self.ended_restart, self.ended_restart_rect)
    
    def movePiece(self):
        if not self.piece.pieceFall():
            self.updatefield()
            
    def createScreen(self):
        """Creates PyGame main screen surface and rectangle
        """
        self.main_screen_surface = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
        self.main_screen_rect = self.main_screen_surface.get_rect()
        self.main_screen_surface.fill(MAIN_SCREEN_SURFACE_COLOR)

    def resetScreen(self):
        self.main_screen_surface.fill(MAIN_SCREEN_SURFACE_COLOR)

    def createInitialText(self):
        font_text = font.Font('freesansbold.ttf', 30)
        title = font_text.render("Welcome to Pygame Tetris", True, (255,255,255), None).convert_alpha()
        font_text = font.Font('freesansbold.ttf', 20)
        credits = font_text.render("GitHub: @FRM95", True, (255,255,255), None).convert_alpha()
        font_text = font.Font('freesansbold.ttf', 32)
        start = font_text.render("Press F1 to Start! :)", True, (255,255,255), None).convert_alpha()
        font_text = font.Font('freesansbold.ttf', 24)
        control = font_text.render("Piece movement: WASD keys", True, (255,255,255), None).convert_alpha()
        control2 = font_text.render("Piece rotation: Space key", True, (255,255,255), None).convert_alpha()
        title_rect = title.get_rect()
        title_rect.center = (self.main_screen_rect.centerx, self.main_screen_rect.centery // 1.5)
        credits_rect = credits.get_rect()
        credits_rect.center = (self.main_screen_rect.centerx, self.main_screen_rect.centery // 1.3)
        start_rect = start.get_rect()
        start_rect.center = (self.main_screen_rect.centerx, self.main_screen_rect.centery)
        control_rect = control.get_rect()
        control_rect.center = (self.main_screen_rect.centerx, self.main_screen_rect.centery * 1.2)
        control2_rect = control2.get_rect()
        control2_rect.center = (self.main_screen_rect.centerx, self.main_screen_rect.centery * 1.3)
        self.main_screen_surface.blit(title, title_rect)
        self.main_screen_surface.blit(credits, credits_rect)
        self.main_screen_surface.blit(start, start_rect)
        self.main_screen_surface.blit(control, control_rect)
        self.main_screen_surface.blit(control2, control2_rect)

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
        self.score_object = Score(score_coordinates, WIDHT_SCORE_FIELD, HEIGHT_SCORE_FIELD)
        self.score_object.addBorderLine(BORDER_LINE_COLOR)
        self.score_surface = self.score_object.surface
        self.score_rect = self.score_object.rect

        self.score_text_surface, self.score_text_rect = self.score_object.createText('Score', size = SCORE_FONT_SIZE)
        self.score_text_rect.midtop = (self.score_rect.midtop[0], self.score_rect.midtop[1] + BLOCK_DIMENSION * 0.6)
        self.score_object.displayScore(self.game_score)
        self.points_text_surface = self.score_object.points_surface
        self.points_text_rect = self.score_object.points_rect
        self.points_text_rect.midtop = (self.score_text_rect.midtop[0], self.score_text_rect.midtop[1] + BLOCK_DIMENSION)

        self.level_text_surface, self.level_text_rect = self.score_object.createText('Level', size = SCORE_FONT_SIZE)
        self.level_text_rect.midtop = (self.points_text_rect.midtop[0], self.points_text_rect.midtop[1] + BLOCK_DIMENSION * 1.1)
        self.score_object.displayLevel(self.game_level)
        self.level_number_surface = self.score_object.level_surface
        self.level_number_rect = self.score_object.level_rect
        self.level_number_rect.midtop = (self.level_text_rect.midtop[0], self.level_text_rect.midtop[1] + BLOCK_DIMENSION)

    def createPreviewField(self):
        """Creates Score Field surface
        """
        preview_coordinates = (self.field_rect.right + 30, self.score_rect.bottom + 10)
        preview_object = Preview(preview_coordinates, WIDHT_PREVIEW_FIELD, HEIGHT_PREVIEW_FIELD)
        preview_object.addBorderLine(BORDER_LINE_COLOR)
        self.preview_surface = preview_object.surface
        self.preview_rect = preview_object.rect
        preview_object.createText('Next', size = PREVIEW_FONT_SIZE)
        self.preview_text_surface = preview_object.text_surface
        self.preview_text_rect = preview_object.text_rect
        self.preview_text_rect.midtop = (self.preview_rect.midtop[0], self.preview_rect.midtop[1] + BLOCK_DIMENSION * 0.6)

    def createSpritesGroup(self):
        self.active_pieces = pygame.sprite.Group()
        self.static_pieces = pygame.sprite.Group()

    def updatefield(self):
        for block in self.piece.blocks:
            if block.y <= 0:
                self.game_over = True
                self.endedGame()
                return False
            else:
                self.field_data[block.y][block.x] = 1
                self.static_pieces.add(block)
        self.active_pieces.empty()
        self.checkRow()
        self.createPiece()

    def checkRow(self):
        found_row = False
        combo = 0

        for row_index, row in enumerate(self.field_data[::-1]):
            if all(row):
                found_row = True
                self.lines_cleared += 1
                combo +=1
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

        if combo != 0:
            self.updateGameStatus(combo)

    def setNextPieces(self):
        figure = choice(PIECES_LIST)
        item = (PIECES.get(figure), PIECES_COLORS.get(figure))
        self.nextPiece = NextPiece(item)

    def createPiece(self):
        next_item = self.nextPiece.getItem()
        random_figure = next_item[0]
        random_color = next_item[1]
        x_offset = self.calculateXOffset(random_figure)
        y_offset = self.calculateYOffset(random_figure)
        self.piece = Tetromino(self.active_pieces, 
                            random_color, 
                            random_figure, 
                            x_offset = x_offset,
                            y_offset = y_offset, 
                            field_data = self.field_data)
        
        new_figure = choice(PIECES_LIST)
        new_item = (PIECES.get(new_figure), PIECES_COLORS.get(new_figure))
        self.nextPiece.updateItem(new_item)
        self.next_piece_surface = self.nextPiece.drawNextPiece()
        self.next_piece_rect = self.nextPiece.getRect()
        self.next_piece_rect.midtop = (self.preview_text_rect.midtop[0], self.preview_text_rect.midtop[1] + BLOCK_DIMENSION * 1.5)

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

    def initiateScore(self):
        self.game_score = 0
        self.game_level = 0
        self.lines_cleared = 0
        self.game_over = False

    def endedGame(self):
        font_text = font.Font('freesansbold.ttf', 34)
        self.game_over_text = font_text.render("GAME OVER :(", True, (255,255,255), None).convert_alpha()
        font_text = font.Font('freesansbold.ttf', 28)
        self.ended_menu = font_text.render("Press F1 to go back to menu", True, (255,255,255), None).convert_alpha()
        self.ended_restart = font_text.render("Press F2 to start a new game", True, (255,255,255), None).convert_alpha()
        self.game_over_text_rect = self.game_over_text.get_rect()
        self.ended_menu_rect = self.ended_menu.get_rect()
        self.ended_restart_rect = self.ended_restart.get_rect()
        self.game_over_text_rect.center = (self.main_screen_rect.centerx, self.main_screen_rect.centery // 1.5)
        self.ended_menu_rect.midtop = (self.game_over_text_rect.centerx, self.game_over_text_rect.bottom + self.game_over_text_rect.height * 1.5)
        self.ended_restart_rect.midtop = (self.ended_menu_rect.centerx, self.ended_menu_rect.bottom + 10)
        self.transparent_surf = pygame.Surface((WIDTH_SCREEN, HEIGHT_SCREEN), pygame.SRCALPHA, 32).convert_alpha()
        self.transparent_surf.fill((0,0,0,200))
        
    def updateGameStatus(self, combo:int):
        current_level = self.lines_cleared//10
        points_earned = POINTS.get(combo) * (current_level + 1)
        self.game_score += points_earned

        self.score_object.updateScore(self.game_score)
        self.points_text_surface = self.score_object.points_surface
        self.points_text_rect = self.score_object.points_rect
        self.points_text_rect.midtop = (self.score_text_rect.midtop[0], self.score_text_rect.midtop[1] + BLOCK_DIMENSION)

        if self.game_level != current_level:
            self.game_level = current_level
            self.score_object.updateLevel(self.game_level)
            self.level_number_surface = self.score_object.level_surface
            self.level_number_rect = self.score_object.level_rect
            self.level_number_rect.midtop = (self.level_text_rect.midtop[0], self.level_text_rect.midtop[1] + BLOCK_DIMENSION)
            self.down_speed = self.down_speed * 0.75
            self.down_speed_faster = self.down_speed * 0.1


        
        

        
        
        
