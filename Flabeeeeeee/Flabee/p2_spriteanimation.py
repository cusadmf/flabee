import pygame
import math
import sys


pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1280
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flabee')


#load images
bg = pygame.image.load('images/bg1.png').convert()
bg_width = bg.get_width()


#define game variables
scroll = 0
tiles= math.ceil(screen_width/ bg_width) + 1

#sprite animation
class Ebee(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.index = 0
		self.counter = 0
		for num in range(1, 4):
			img = pygame.image.load(f'images/ebee{num}.png')
			self.images.append(img)
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]

	def update(self):

		#handle the animation
		self.counter += 1
		flap_cooldown = 5

		if self.counter > flap_cooldown:
			self.counter = 0
			self.index += 1
			if self.index >= len(self.images):
				self.index = 0
		self.image = self.images[self.index]


ebee_group = pygame.sprite.Group()

flabee = Ebee(150, int(screen_height / 1.5))

ebee_group.add(flabee)

#game loop 
run = True
while run:

   clock.tick(fps)

	#draw scrolling background
   for i in range (0, tiles):
	   screen.blit(bg, (i * bg_width + scroll , 0))

   ebee_group.draw(screen)
   ebee_group.update()

   #scroll bg
   scroll -= 5

	#draw and scroll the ground
   if abs(scroll) > bg_width:
         scroll = 0  

    #event handler
   for event in pygame.event.get():
	     if event.type == pygame.QUIT:
              run = False

   pygame.display.update()

pygame.quit()
sys.exit()