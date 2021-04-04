import pygame
import math
import random
import colorsys

pygame.init()

SIZE = int(input('side length in pixels: '))
BRIGHTNESS_FUNCTION = lambda it: 1-(2**-it)


#surf = pygame.display.set_mode((SIZE, SIZE))

surf = pygame.Surface((SIZE, SIZE))

def draw_sierpinski_iteration(surface, current_iteration=0, color_black=pygame.Color('black'), color_white=pygame.Color('white')):
    if surface.get_width() / 3 < 1: return

    width_of_center_square = int(surface.get_width() / 3)
    screen_rect = surface.get_rect()
    center_square_rect = pygame.Rect((0, 0, width_of_center_square, width_of_center_square))
    center_square_rect.center = screen_rect.center

    surface.fill(color_white)
    surface.fill(color_black, rect=center_square_rect)
    

    # find all places to place the inner pattern
    # 
    # XX XX XX
    # XX .. XX
    # XX XX XX
    positions = []
    for x in range(3):
        for y in range(3):
            if x==y==1: continue
            coords = (x * width_of_center_square, y * width_of_center_square)
            positions.append(coords)

    # draw inner pattern in these positions
    for coords in positions:
        draw_rect = center_square_rect.copy()
        draw_rect.topleft = coords
        inner_surf = surface.subsurface(draw_rect)
        brightness = BRIGHTNESS_FUNCTION(current_iteration+1)
        color = pygame.Color(*map(lambda x: int(x*255), [brightness for _ in range(3)]))
        draw_sierpinski_iteration(inner_surf, current_iteration=current_iteration+1, color_black=color)

draw_sierpinski_iteration(surf)

pygame.image.save(surf, input('path to file to save: '))
