import pygame 
from settings import *
from random import choice, randint

class vertMove(pygame.sprite.Sprite):
	# animates vertical
	def update(self,dt):
		self.pos.y += 300*dt
		if self.rect.centery >= WINDOW_HEIGHT:
			self.pos.y = -WINDOW_HEIGHT
		self.rect.y = round(self.pos.y)
		


		
class Background(vertMove):
	def __init__(self, group,scaleFactor):
		super().__init__(group)
		background = pygame.image.load('C:/Users/lessl/Desktop/Semester 5/Projects/runningMan/graphics/environment/bgVertical2x.png').convert()

		# Calcualate desired dimensions
		bgWidth = background.get_width() * scaleFactor
		bgHeight = WINDOW_HEIGHT *2

		self.image = pygame.transform.scale(background,(bgWidth,bgHeight))

		self.rect = self.image.get_rect(midleft =(0,0))
		self.pos = pygame.math.Vector2(self.rect.topleft)
	def animate(self,dt):
		return


class Wrench(pygame.sprite.Sprite):
	def __init__(self,groups,scale_factor):
		super().__init__(groups)
		self.sprite_type = 'obstacle'
		orientation = choice(('left','right'))

		# images - import and transform
		wrench = pygame.image.load(f'C:/Users/lessl/Desktop/Semester 5/Projects/runningMan/graphics/obstacles/{choice((0,1,2,3))}.png').convert_alpha()
		wrenchResized = pygame.transform.scale(wrench,pygame.math.Vector2(wrench.get_size()) * scale_factor)
		wrenchResizedFlipped = pygame.transform.flip(wrenchResized,True,False)

		# place image
		if orientation == 'left':
			self.image = wrenchResized
			self.rect = self.image.get_rect(midleft =(-75*(1/scale_factor),0))
		else:
			self.image = wrenchResizedFlipped
			self.rect = self.image.get_rect(midright =(WINDOW_WIDTH+ 75*(1/scale_factor),0))

		# pos for animation
		self.pos = pygame.math.Vector2(self.rect.topleft)

		# mask
		self.mask = pygame.mask.from_surface(self.image)

	# animates sprite
	def update(self,dt):
		self.pos.y += 400 * dt
		self.rect.y = round(self.pos.y)
		if self.rect.top >=WINDOW_HEIGHT:
			self.kill()
		

class Fire(vertMove):
	def __init__(self,group,scaleFactor):
		super().__init__(group)
		self.sprite_type = 'fire'
		self.scaleFactor = scaleFactor

		#image
		self.importFrames(scaleFactor) #create array of images
		self.frameIndex = 0 # var fram index
		

		# creating window
		surface = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT*2))
		surface.set_colorkey((0,0,0))# removes black

		# placing transparent surface in window
		self.image = surface

		# position placing imageage and position
		self.rect = self.image.get_rect(topleft = (0,0))
		self.pos = pygame.math.Vector2(self.rect.topleft)


	# import images, resize and append to array
	def importFrames(self,scaleFactor):
		self.frames = []
		for i in range(16):
			fire = pygame.image.load(f'C:/Users/lessl/Desktop/Semester 5/Projects/runningMan/graphics/environment/fire/{i}.png').convert_alpha()
			scaledFire = pygame.transform.scale(fire,(fire.get_width()*scaleFactor, WINDOW_HEIGHT))
			self.imgWidth = fire.get_width()*scaleFactor
			self.frames.append(scaledFire)

	# asnimate frames
	def animate(self,dt):
		# counter for frames
		self.frameIndex += 10 * dt
		if self.frameIndex >= len(self.frames):
			self.frameIndex = 0

		# assign current frame to variable
		x = self.frames[int(self.frameIndex)]
		# flips frames 
		xflip = pygame.transform.flip(x,True,False)

		# display flames on image
		self.image.blit(x,(WINDOW_WIDTH-self.imgWidth,0))
		self.image.blit(xflip,(0,0))
		self.image.blit(x,(WINDOW_WIDTH-self.imgWidth,WINDOW_HEIGHT))
		self.image.blit(xflip,(0,WINDOW_HEIGHT))

		# mask
		self.mask = pygame.mask.from_surface(self.image)


class Player(pygame.sprite.Sprite):
	def __init__(self, group, scaleFactor):
		super().__init__(group)

		# image

		# x = pygame.image.load('C:/Users/lessl/Desktop/Semester 5/Projects/runningMan/graphics/player/up0.png').convert_alpha()
		# self.image = pygame.transform.scale(x,pygame.math.Vector2(x.get_size())* scaleFactor)

		self.importFrames(scaleFactor)
		self.frameIndex = 0
		self.image = self.frames[self.frameIndex]
		
		# position
		self.rect = self.image.get_rect(midbottom = (WINDOW_WIDTH/2,WINDOW_HEIGHT*.8))
		self.pos = pygame.math.Vector2(self.rect.topleft)

		self.gravity = 600
		self.direction = 0

		
		if (choice((True,False))==True):
			self.lattitude = 10
		else:
			self.lattitude = -10

		self.left = 0
		
		# mask
		self.mask = pygame.mask.from_surface(self.image)


	def importFrames(self,scaleFactor):
		self.frames = []
		for i in range(4):
			player = pygame.image.load(f'C:/Users/lessl/Desktop/Semester 5/Projects/runningMan/graphics/player/up{i}.png').convert_alpha()
			scaledPlayer = pygame.transform.scale(player,pygame.math.Vector2(player.get_size())*scaleFactor)
			self.frames.append(scaledPlayer)

	def animate(self,dt):
		self.frameIndex += 10 * dt
		if self.frameIndex >= len(self.frames):
			self.frameIndex = 0
		self.image = self.frames[int(self.frameIndex)]

	def apply_gravity(self,dt):
		self.direction += self.gravity * dt
		self.pos.y += self.direction * dt
		self.rect.y = round(self.pos.y)

		self.left += self.lattitude * dt
		self.pos.x += self.left * dt
		self.rect.x = round(self.pos.x)

	def jump(self):
		self.direction = -400

	def jumpLeft(self):
		self.left = -300
		self.direction = -150
	
	def jumpRight(self):
		self.left = 300
		self.direction = -150

	def update(self,dt):
		self.apply_gravity(dt)
		self.animate(dt)