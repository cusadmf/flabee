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
bg1 = pygame.image.load('images/bg1.png').convert()
bg1_width = bg1.get_width()


#define game variables
scroll = 0
tiles = math.ceil(screen_width/ bg1_width) + 1
flying = False 
game_over = False

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
            self.vel = 0
            self.space_pressed = False

        def update(self):
            global scroll  # Use the global scroll variable

            #flying physics
            if flying == True:
                    #gravity
                    self.vel += 0.5
                    if self.vel > 8:
                            self.vel = 8
                    if self.rect.bottom < 770:
                            self.rect.y += int(self.vel)

            if game_over == False:

                    #jump
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE] and not self.space_pressed:
                        self.space_pressed = True
                        self.vel = -10
                    if not keys[pygame.K_SPACE]:
                        self.space_pressed = False

                    #handle the animation
                    self.counter += 1
                    flap_cooldown = 5

                    if self.counter > flap_cooldown:
                        self.counter = 0
                        self.index += 1
                        if self.index >= len(self.images):
                                self.index = 0
                    self.image = self.images[self.index]

                    #rotate the bird
                    self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
            else:
                    self.image = pygame.transform.rotate(self.images[self.index], -90)

#ebee position
ebee_group = pygame.sprite.Group()

flabee = Ebee(150, int(screen_height / 1.5))

ebee_group.add(flabee)

#game loop 
run = True
while run:

        clock.tick(fps)

        #draw scrolling background
        for i in range (0, tiles):
            screen.blit(bg1, (i * bg1_width + scroll , 0))

        ebee_group.draw(screen)
        ebee_group.update()

        #scroll bg
        scroll -= 5

        #draw and scroll the bg
        if abs(scroll) > bg1_width:
            scroll = 0 

        #check if bird has hit the ground
        if flabee.rect.bottom > 720:
            game_over = True
            flying = False
            scroll = 0

        if game_over == False:
                #draw and scroll the bg
                scroll -= 5
                if abs(scroll) > bg1_width:
                    scroll = 0
                

        #event handler
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN and flying == False and game_over == False:
                    flying = True
                         

        pygame.display.update()

pygame.quit()
sys.exit()