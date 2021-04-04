import pygame
import math
import random
import colorsys

pygame.init()

SIZE = int(input('side length in pixels: '))
PAUSE_ON_STEP = False
BRIGHTNESS_FUNCTION = lambda it: 1-(2**-it)

surf = pygame.display.set_mode((SIZE, SIZE))
step_counter = 0

class step:
    def __init__(self, *data):
        self.data = data

    def __enter__(self):
        global step_counter
        step_counter+=1
        print('STEP', step_counter, ':',  *self.data)
        if PAUSE_ON_STEP:
            pygame.display.flip()
            input('enter to continue> ')
            
    def __exit__(self, *_): pygame.display.flip()

def get_color_for_iter(n):
    '''Get consistently random color to identify iterations of drawing pattern.'''
    random.seed(n)
    hue = random.random()
    value = random.random()
    r,g,b = map(lambda x: int(x*255), colorsys.hsv_to_rgb(hue, 1, value))
    print(n, '->', r, g, b)
    return pygame.Color(r, g, b)

def replace_color(surface, what, with_what):
    '''Replace all pixels in surface that have one color with another color.'''
    replaced_pixels = pygame.transform.threshold(surface, surface, what, set_color=with_what, inverse_set=True)
    print('Replaced color', what, 'with', with_what, 'affected', replaced_pixels, 'pixels')

width_of_center_square = int(SIZE / 3)
screen_rect = surf.get_rect()
center_square_rect = pygame.Rect((0, 0, width_of_center_square, width_of_center_square))
center_square_rect.center = screen_rect.center
with step('Draw square with hole'):
    surf.fill(pygame.Color('white'))
    surf.fill(get_color_for_iter(0), rect=center_square_rect)



width_of_square = SIZE/3
current_iteration = 1

while width_of_square > 1:
    with step('Copy surface to inner squares (current width of innermost hole is', width_of_square,')'):
        surf_to_draw = surf.copy()
        surf_to_draw = pygame.transform.scale(surf, (int(SIZE/3), int(SIZE/3)))

        # find all places to place the inner pattern
        # 
        # XX XX XX
        # XX .. XX
        # XX XX XX
        positions = []
        for x in range(3):
            for y in range(3):
                if x==y==1: continue
                coords = (x * surf_to_draw.get_width(), y * surf_to_draw.get_height())
                positions.append(coords)

        # draw inner pattern in these positions
        for coords in positions:
            surf.blit(surf_to_draw, coords)

        # fill current center with color of current iteration    
        surf.fill(get_color_for_iter(current_iteration), rect=center_square_rect)
        
        width_of_square /= 3
        current_iteration += 1

current_iteration -= 1
brightness = 0
brightness_iteration = 0
while current_iteration >= 0:
    brightness = BRIGHTNESS_FUNCTION(brightness_iteration)
    with step('Recolor pixels on iteration', current_iteration, 'with brightness', brightness):
        color = pygame.Color(*[int(brightness*255) for _ in range(3)])
        replace_color(surf, get_color_for_iter(current_iteration), color)
        current_iteration -= 1
        brightness_iteration += 1

with step('Save to file'):
    pygame.image.save(surf, input('path to file to save: '))
