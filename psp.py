import random
import sys
import pygame
from pygame.locals import *

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 499

FPS = 32
BIRD_FLAP_VELOCITY = -8
BIRD_ACCELERATION_Y = 1
BIRD_MAX_VELOCITY_Y = 10

SEA_LEVEL_IMAGE_PATH = 'images/bg2.png'
NUMBER_IMAGES_PATH = ['images/0.png', 'images/1.png', 'images/2.png',
                      'images/3.png', 'images/4.png', 'images/5.png',
                      'images/6.png', 'images/7.png', 'images/8.png', 'images/9.png']
PIPE_IMAGE_PATH = 'images/pipe.png'  

FLAP_SOUND_PATH = 'sounds/wing.mp3'
HIT_SOUND_PATH = 'sounds/hit.mp3'
POINT_SOUND_PATH = 'sounds/point.mp3'
DIE_SOUND_PATH = 'sounds/die.mp3'
BACKGROUND_MUSIC_PATH = 'sounds/background_music.mp3'

BACKGROUND_THEMES = ['images/bg1.png', 'images/bg2.png', 'images/bg3.png']

PLAYER_IMAGES_PATHS = [
    'images/ebee1.png',
    'images/ebee2.png',
    'images/ebee3.png'
]

pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Flabee')

sea_level_image = pygame.image.load(SEA_LEVEL_IMAGE_PATH).convert_alpha()
pipe_images = [pygame.image.load(PIPE_IMAGE_PATH).convert_alpha()]  

number_images = [pygame.image.load(path).convert_alpha() for path in NUMBER_IMAGES_PATH]

flap_sound = pygame.mixer.Sound(FLAP_SOUND_PATH)
hit_sound = pygame.mixer.Sound(HIT_SOUND_PATH)
point_sound = pygame.mixer.Sound(POINT_SOUND_PATH)
die_sound = pygame.mixer.Sound(DIE_SOUND_PATH)

pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)
pygame.mixer.music.set_volume(0.2)

player_images = [pygame.image.load(path).convert_alpha() for path in PLAYER_IMAGES_PATHS]

clock = pygame.time.Clock()


def flappy_game(difficulty):
    your_score = 0
    bird_velocity = 0
    bird_rect = player_images[difficulty].get_rect(center=(100, WINDOW_HEIGHT // 2))
    pipes = []
    is_flapped = False

    pygame.mixer.music.play(-1)  

    background_image = pygame.image.load(BACKGROUND_THEMES[difficulty]).convert_alpha()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and
                                      event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if bird_rect.centery > 0:
                    bird_velocity = BIRD_FLAP_VELOCITY
                    is_flapped = True
                    flap_sound.play()

        bird_velocity = min(bird_velocity + BIRD_ACCELERATION_Y, BIRD_MAX_VELOCITY_Y)
        bird_rect.centery += bird_velocity

        if bird_rect.top <= 0 or bird_rect.bottom >= WINDOW_HEIGHT:
            hit_sound.play()
            pygame.mixer.music.stop() 
            pygame.time.delay(500)  
            return your_score

        for pipe in pipes:
            pipe['x'] += difficulty + 1  

        if pipes and pipes[-1]['x'] < WINDOW_WIDTH // 2:
            pipes.extend(create_pipe())

        pipes = [pipe for pipe in pipes if pipe['x'] + pipe_images[0].get_width() > 0]

        for pipe in pipes:
            if bird_rect.colliderect(pipe['rect']):
                hit_sound.play()
                pygame.mixer.music.stop()  
                pygame.time.delay(500)  
                return your_score

        for pipe in pipes:
            if pipe['x'] < bird_rect.centerx < pipe['x'] + difficulty + 1:
                your_score += 1
                point_sound.play()

        window.blit(background_image, (0, 0))

        for pipe in pipes:
            window.blit(pipe_images[0], pipe['rect'].topleft)

        window.blit(sea_level_image, (ground, WINDOW_HEIGHT - sea_level_image.get_height()))
        window.blit(player_images[difficulty], bird_rect.topleft)

        display_score(your_score)

        pygame.display.update()
        clock.tick(FPS)


def create_pipe():
    pipe_height = pipe_images[0].get_height()
    pipe_x = WINDOW_WIDTH
    pipe_y = random.randint(pipe_height, WINDOW_HEIGHT - sea_level_image.get_height() - pipe_height)
    pipe_rect = pipe_images[0].get_rect(topleft=(pipe_x, pipe_y))
    return [{'rect': pipe_rect, 'x': pipe_x, 'y': pipe_y}]


def display_score(score):
    numbers = [int(digit) for digit in str(score)]
    total_width = sum(number_images[number].get_width() for number in numbers)
    x_offset = (WINDOW_WIDTH - total_width) / 2

    for number in numbers:
        window.blit(number_images[number], (x_offset, WINDOW_WIDTH * 0.02))
        x_offset += number_images[number].get_width()


def game_over_screen(final_score):
    game_over_font = pygame.font.Font('freesansbold.ttf', 50)
    game_over_text = game_over_font.render('Game Over', True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))

    score_font = pygame.font.Font('freesansbold.ttf', 36)
    score_text = score_font.render(f'Your Score: {final_score}', True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))

    window.blit(game_over_text, game_over_rect)
    window.blit(score_text, score_rect)

    pygame.display.update()
    pygame.time.delay(2000) 
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    difficulty = 0  
    while True:
        your_score = flappy_game(difficulty)
        game_over_screen(your_score)
        difficulty = (difficulty + 1) % len(BACKGROUND_THEMES) 

