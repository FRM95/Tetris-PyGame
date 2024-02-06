from sys import exit
import pygame
from game import Game

class Main:
	
	def __init__(self):
		pygame.init()
		pygame.display.set_caption('Tetris')
		self.game = Game()
		self.clock = pygame.time.Clock()
		self.started = False

	def run(self):

		while True:
			
			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
				
				if event.type == pygame.KEYDOWN:

					# First start
					if event.key == pygame.K_F1 and not self.game.game_over:
						self.started = True
						self.game.resetScreen()

					# If game over, goes to start menu
					if event.key == pygame.K_F1 and self.game.game_over:
						self.game = Game()
						self.started = False

					# If game over, start a new game
					if event.key == pygame.K_F2 and self.game.game_over:
						self.game = Game()
						self.game.resetScreen()

			if self.started:

				# display 
				self.game.display()

				# input and timers
				if not self.game.game_over:
					self.game.timerUpdate()
					self.game.keyboardInput()

			# updating the game
			pygame.display.update()
			self.clock.tick(60)

if __name__ == '__main__':
	main = Main()
	main.run()