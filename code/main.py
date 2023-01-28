print('hello')
import pygame, sys, time
from settings import *
from sprites import Background, Fire, Player, Wrench
import random
import time


class Game:
	def __init__(self):
		
		# setup
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		pygame.display.set_caption('Running Man')
		self.clock = pygame.time.Clock()
		self.playBall = False

		# sprite groups
		self.all_sprites = pygame.sprite.Group()
		self.player_sprites = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()

		# scale factor for assets
		self.scaleFactor = WINDOW_WIDTH / pygame.image.load('C:/Users/lessl/Desktop/Semester 5/Projects/runningMan/graphics/environment/bgVertical2x.png').get_width()
		self.playerScaleFactor = WINDOW_WIDTH/160

		# sprite setup
		Background(self.all_sprites,self.scaleFactor)
		Fire([self.all_sprites,self.collision_sprites],self.scaleFactor)
		self.player = Player([self.player_sprites],self.playerScaleFactor)

		# spawning obsticle timer
		self.obstacleTimer = pygame.USEREVENT + 1
		pygame.time.set_timer(self.obstacleTimer,1400)
		self.score =-1

		# menu
		self.menu_surf = pygame.image.load('C:/Users/lessl/Desktop/Semester 5/Projects/runningMan/graphics/ui/menu2clr.png')
		self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2.7))
		
	# display the score
	def score_display(self,score):
		SCORE_FONT = pygame.font.Font('freesansbold.ttf', 32)
		if score == -1:
			display = SCORE_FONT.render(f"Score: 0", True, (255,255,255))
		else:
			display = SCORE_FONT.render(f"Score: {score}", True, (255,255,255))
		self.display_surface.blit(display, (WINDOW_WIDTH/2 - 55,WINDOW_HEIGHT/20 ))

	# sprite collision detection and deletion
	def collision(self):
		if pygame.sprite.spritecollide(self.player,self.collision_sprites,False,pygame.sprite.collide_mask) or self.player.rect.bottom>=WINDOW_HEIGHT:
			# for sprite in self.collision_sprites.sprites():
			# 	if sprite.sprite_type == 'obstacle':
			# 		sprite.kill()
			self.playBall = False
			self.player.kill()
			self.score = -1
	
	# display game board 
	def run(self):

		last_time = time.time()
		while True:

			# delta time
			dt = time.time() - last_time
			last_time = time.time()

			# event loop
			for event in pygame.event.get():
				
				# event: exit keys
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					pygame.quit()
					sys.exit()

				# event: user input keys
				if event.type == pygame.KEYDOWN:
					if self.playBall:
						if event.key == pygame.K_a:
							self.player.jumpLeft()
						if event.key == pygame.K_d:
							self.player.jumpRight()
					else:
						if event.key == pygame.K_a or event.key == pygame.K_d:
							self.player = Player([self.all_sprites],self.playerScaleFactor)
							self.playBall = True

				# event: spawn obsticle
				if event.type == self.obstacleTimer and self.playBall:
					Wrench([self.all_sprites,self.collision_sprites],self.scaleFactor)
					self.score +=1
					
			
			# draw assets - sprites + score
			self.display_surface.fill('black')
			self.all_sprites.update(dt)
			self.all_sprites.draw(self.display_surface)
			self.score_display(self.score)

			# activae colision 
			if self.playBall:
				self.collision()
			else:
				self.display_surface.blit(self.menu_surf,self.menu_rect)
			
			# update
			pygame.display.update()
			
if __name__ == '__main__':
	game = Game()
	game.run()



# debug with colors
		# self.assetsColor = pygame.Color('white')
		# self.assetsColor = pygame.Color('black')
		# pygame.draw.rect(self.display_surface,self.assetsColor,pygame.Rect(0,WINDOW_HEIGHT/2 -50, 10,100))