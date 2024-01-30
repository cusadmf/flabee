# *********************************************************
# Program: flabee.py
# Course: PSP0101 PROBLEM SOLVING AND PROGRAM DESIGN
# Class: TL6L
# Year: 2023/24 Trimester 1
# Names: JASMYNE YAP | LIEW ZI RONG | ONG JIAN HAO | MUHANNAD AYMAN ABDELHADY HASSAN
# IDs: 1221108743 | 1221106917 | 1221108313 | 1221102097
# Emails: 1221108743@student.mmu.edu.my | 1221106917@student.mmu.edu.my | 1221108313@student.mmu.edu.my | 1221102097@student.mmu.edu.my
# Phones: 011-63464323 | 012-6162645 | 017-2032059 | 016-7608073
# *********************************************************


import pygame
import math
import sys
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1280
screen_height = 720

mouse_x, mouse_y = pygame.mouse.get_pos()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flabee')

#define text
font = pygame.font.SysFont('Impact', 40)

#define colors
color = (82, 91, 138)

restart_button_img = pygame.image.load('images/restart.png')
menu_button_img = pygame.image.load('images/menubutton.png')
game_over_image = pygame.image.load('images/game_over.png')
menu_bg = pygame.image.load('images/menu.png')

#define game variables
scroll = 0
flying = False
game_over = False
obs_frequency = 1500  # milliseconds
last_obs = pygame.time.get_ticks() - obs_frequency
score = 0
high_score = 0
pass_obs = False
collision_occurred = False
show_game_over = False

#define sounds
flap_sound = pygame.mixer.Sound('sounds/wing.mp3')
hit_sound = pygame.mixer.Sound('sounds/hit.wav')
point_sound = pygame.mixer.Sound('sounds/point.wav')
die_sound = pygame.mixer.Sound('sounds/die.wav')

# Lowering the volume of sound effects
flap_sound.set_volume(0.3)  # Adjust the volume level as needed
hit_sound.set_volume(0.3)
point_sound.set_volume(0.3)
die_sound.set_volume(0.3)

try:
    with open('highscore.txt', 'r') as file: # Open file and r is for reading mode
        content = file.read().strip()  # Read the content and removing the trailing space
        if content: # Check for content
            high_score = int(content) # Convert content into highscore (int)
except (FileNotFoundError, ValueError): # File cannot be found, if content cannot be convert into int
    pass


#score display
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#resetting the game
def reset_game():
    obs_group.empty()
    flabee.rect.x = 150
    flabee.rect.y = int(screen_height / 1.8)
    score = 0
    global collision_occurred
    collision_occurred = False
    return score
    

#ebee sprite animation
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
        # Flying physics
        if flying == True:
            # Gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 770:
                self.rect.y += int(self.vel)

        if game_over == False:
            # Jump
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and not self.space_pressed:
                self.space_pressed = True
                self.vel = -10
                flap_sound.play()
            if not keys[pygame.K_SPACE]:
                self.space_pressed = False

            # Handle Ebee sprite animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # Rotate the Ebee
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

#ebee position
ebee_group = pygame.sprite.Group()
flabee = Ebee(150, int(screen_height / 1.5))
ebee_group.add(flabee)        

#obstacles
class Obs(pygame.sprite.Sprite):
    def __init__(self, x, y,obs_image):
        pygame.sprite.Sprite.__init__(self)
        self.image = obs_image
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.scroll_speed = 6

    #to make the obstacle move
    def update(self):
        self.rect.x -= self.scroll_speed
        if self.rect.right < 0:
            self.kill()

obs_group = pygame.sprite.Group()            

#restart button
class RestartButton():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        # mouse position
        pos = pygame.mouse.get_pos()

        #check if clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        #draw restart button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

restart_button = RestartButton(screen_width // 2 - 110, screen_height // 2.5 - 100, restart_button_img)

#option for player to go back to menu when game over
class BackToMenuButton():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check if clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        # Draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

back_to_menu_button = BackToMenuButton(screen_width // 2 - 110, screen_height // 2 + 80, menu_button_img)

#choosing map1 (DTC) button
class Map1Button():
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("images/DTC.png")
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width() // 2, 375)

    def draw_button(self):
        screen.blit(self.image, self.rect)

#choosing map2 (Lake) button
class Map2Button():
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("images/LAKE.png")
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width() // 2, 500)

    def draw_button(self):
        screen.blit(self.image, self.rect)


#creating buttons
map1_Button = Map1Button(screen)
map2_Button = Map2Button(screen)


#selecting map button 
def check_background_select(mouse_x, mouse_y, map1_Button, map2_Button):
    #check which background the user chooses.
    bg1_selected = map1_Button.rect.collidepoint(mouse_x, mouse_y)
    bg2_selected = map2_Button.rect.collidepoint(mouse_x, mouse_y)

    if bg1_selected:
        bg1 = pygame.image.load('images/bg1.png').convert()
        background_image = bg1
        background_width = background_image.get_width()
        background_selection = False
        obs_image = pygame.image.load("images/palm.png")
        return background_image, background_width,background_selection,obs_image

    elif bg2_selected:
        bg2 = pygame.image.load('images/bg2.png').convert()
        background_image = bg2
        background_width = background_image.get_width()
        background_selection = False
        obs_image = pygame.image.load("images/bush.png")
        return background_image, background_width,background_selection,obs_image


#menu screen
background_image = None
background_width = 0
background_selection = True
while background_selection:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            background_image, background_width, background_selection,obs_image = check_background_select(mouse_x, mouse_y, map1_Button, map2_Button)


    screen.blit(menu_bg, (0, 0))

    #drawing buttons onto the screen
    map1_Button.draw_button()
    map2_Button.draw_button()
    pygame.display.update()


#game loop
run = True
while run:
    mouse_x, mouse_y = pygame.mouse.get_pos()

    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN and flying == False and game_over == False:
            flying = True

    #draw scrolling background
    tiles = math.ceil(screen_width / background_width) + 1
    for i in range(0, tiles):
        screen.blit(background_image, (i * background_width + scroll, 0))

    if score > high_score:
            high_score = score    

    ebee_group.draw(screen)
    ebee_group.update()
    obs_group.draw(screen)

    #scroll background
    scroll -= 4

    #check the score
    if len(obs_group) > 0:
        if ebee_group.sprites()[0].rect.left > obs_group.sprites()[0].rect.left \
                and ebee_group.sprites()[0].rect.right < obs_group.sprites()[0].rect.right \
                and pass_obs == False:
            pass_obs = True
        if pass_obs == True:
            if ebee_group.sprites()[0].rect.left > obs_group.sprites()[0].rect.right:
                score += 1
                point_sound.play()
                pass_obs = False

    #draw the scores
    draw_text(str(score), font, color, int(screen_width // 2), 10)
    draw_text(f"Highscore: {high_score}", font, color, screen_width - 220, 10) 

    #look for collision
    if pygame.sprite.groupcollide(ebee_group, obs_group, False, False) or flabee.rect.right < 0 or flabee.rect.top < 0:
        if not collision_occurred:
            hit_sound.play()
            # die_sound.play()
            pygame.mixer.music.stop()
            collision_occurred = True
            show_game_over = True
        game_over = True

    #check if ebee has hit the ground
    if flabee.rect.bottom > 720:
        if not collision_occurred:
            die_sound.play()
            collision_occurred = True
            show_game_over = True
        game_over = True
        flying = False
        scroll = 0

    if game_over == False:
        #generate new obstacles
        time_now = pygame.time.get_ticks()
        if time_now - last_obs > obs_frequency:
            obs_height = random.choice([-10, 40, 100, 170])
            btm_obs = Obs(screen_width + 40, int(screen_height / 2.35) + obs_height , obs_image)
            obs_group.add(btm_obs)
            last_obs = time_now

        #bg stops scrolling after game over
        scroll -= 4
        if abs(scroll) > background_width:
            scroll = 0

        obs_group.update()

    #check for game over and reset
    if game_over:
        if restart_button.draw():
            game_over = False
            score = reset_game()
            show_game_over = False

        if back_to_menu_button.draw():
            game_over = False
            score = reset_game()
            # Reset other game variables as needed
            background_selection = True

            while background_selection:
                clock.tick(fps)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        background_image, background_width, background_selection, obs_image = check_background_select(mouse_x, mouse_y, map1_Button, map2_Button)
                screen.blit(menu_bg, (0, 0))
                map1_Button.draw_button()
                map2_Button.draw_button()
                pygame.display.update() 

        if show_game_over:
            screen.blit(game_over_image, ((screen_width - game_over_image.get_width()) // 2 + 30, 70))  

        with open('highscore.txt', 'w') as file: # Open file in write mode
            file.write(str(high_score)) # Must be Str due to in write mode. Convert highscore into str and update file             

    pygame.display.update()

pygame.quit()
