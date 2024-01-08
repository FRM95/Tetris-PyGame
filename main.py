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
					if event.key == pygame.K_F1:
						self.started = True

			if self.started:

				# display 
				self.game.display()

				# input 
				self.game.keyboardInput()

			# updating the game
			pygame.display.update()
			self.clock.tick(60)

if __name__ == '__main__':
	main = Main()
	main.run()