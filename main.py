from sys import exit
from pyautogui import size
import pygame
from game import Game

class Main:
	
	def __init__(self):
		pygame.init()
		pygame.display.set_caption('Tetris')
		self.game = Game()
		self.clock = pygame.time.Clock()

	def run(self):

		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()

			# display 
			self.game.display()

			# updating the game
			pygame.display.update()
			self.clock.tick(60)

if __name__ == '__main__':
	main = Main()
	main.run()