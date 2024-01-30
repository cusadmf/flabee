
import pygame
import math
import sys
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1280
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flabee')

#define text
font = pygame.font.SysFont('Ariel', 60)

#define colors
color = (82, 91 ,138)

#load images
bg1 = pygame.image.load('images/bg1.png').convert()
bg1_width = bg1.get_width()
button_img = pygame.image.load('images/restart.png').convert_alpha()

#define game variables
scroll = 0
tiles = math.ceil(screen_width/ bg1_width) + 1
flying = False 
game_over = False
obs_frequency = 1500 #milliseconds
last_obs = pygame.time.get_ticks() - obs_frequency
score = 0
pass_obs = False


def draw_text(text, font, text_col, x ,y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_game():
    obs_group.empty()
    flabee.rect.x = 150
    flabee.rect.y = int(screen_height / 1.8)
    score = 0
    return score

#Ebee sprite animation
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
            global scroll 
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

                #handle Ebee sprite animation
                self.counter += 1
                flap_cooldown = 5

                if self.counter > flap_cooldown:
                    self.counter = 0
                    self.index += 1
                    if self.index >= len(self.images):
                            self.index = 0
                self.image = self.images[self.index]

                #rotate the Ebee
                self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
            else:
                self.image = pygame.transform.rotate(self.images[self.index], -90)

#obstacles
class Obs(pygame.sprite.Sprite):
    def __init__(self, x ,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/palm.png")   
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.scroll_speed = 6 


#to make the obstacle move
    def update(self):
        self.rect.x -= self.scroll_speed 
        if self.rect.right < 0:
            self.kill()

# restart button
class RestartButton():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False 

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check if mouse over button (collison)
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y)) 

        return action

ebee_group = pygame.sprite.Group()
obs_group = pygame.sprite.Group()

#ebee position
flabee = Ebee(150, int(screen_height / 1.5))
ebee_group.add(flabee)

#create restart button instance
restart_button = RestartButton(screen_width // 2 -110 , screen_height// 2 -100, button_img)

#game loop 
run = True
while run:

        clock.tick(fps)

        #draw scrolling background
        for i in range (0, tiles):
            screen.blit(bg1, (i * bg1_width + scroll , 0))

        ebee_group.draw(screen)
        ebee_group.update()
        obs_group.draw(screen)
        
        #scroll bg
        scroll -= 4

        #check the score
        if len(obs_group) > 0:    
            if ebee_group.sprites()[0].rect.left > obs_group.sprites()[0].rect.left\
                and ebee_group.sprites()[0].rect.right < obs_group.sprites()[0].rect.right\
                and pass_obs == False:
                pass_obs = True 
            if pass_obs == True:
                if ebee_group.sprites()[0].rect.left > obs_group.sprites()[0].rect.right:
                    score += 1
                    pass_obs = False

        draw_text(str(score), font, color, int(screen_width //2), 20)            

        #look for collision
        if pygame.sprite.groupcollide(ebee_group, obs_group, False, False) or flabee.rect.right < 0 or flabee.rect.top < 0:
            game_over = True


        #check if bird has hit the ground
        if flabee.rect.bottom > 720:
            game_over = True
            flying = False
            scroll = 0

        if game_over == False:
            #generate new obs
            time_now = pygame.time.get_ticks()
            if time_now - last_obs > obs_frequency:
                obs_height = random.choice([-10, 40, 100, 170])
                btm_obs = Obs(screen_width + 40 , int(screen_height / 2.35) + obs_height)
                obs_group.add(btm_obs)
                last_obs = time_now

            #draw and scroll the bg    
            scroll -= 4
            if abs(scroll) > bg1_width:
                scroll = 0

            obs_group.update() 


        #check for game over and reset
        if game_over == True: 
            if restart_button.draw() == True:
               game_over = False
               score = reset_game()


        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN and flying == False and game_over == False:
                flying = True
                         

        pygame.display.update()

pygame.quit()
sys.exit()