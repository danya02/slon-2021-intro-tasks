import pygame

image = input('path to image: ')
outp = input('path to output: ')

img = pygame.image.load(image)

outp = open(outp, 'w')

pixels_img_space = []
for y in range(img.get_height()):
    for x in range(img.get_width()):
        if img.get_at( (x, y) ) != pygame.Color('black'):  # XXX: here is where you can edit the condition for pixel inclusion.
            pixels_img_space.append( (x, y) )

bbox = img.get_rect()
bbox.center = (0, 0)

pixels_turtle_space = []
for x,y in pixels_img_space:
    x += bbox.top
    y += bbox.left
    x = x * -1
    pixels_turtle_space.append( (x, y) )

lx, ly = 0, 0

pixels_turtle_space = pixels_turtle_space[1:]

paint = len(pixels_turtle_space)
fuel = 0

iter = 0
while pixels_turtle_space:
    print(len(pixels_turtle_space), ' '*8, end='\r')
    if iter % 100 == 0:
        dist = lambda loc: abs(loc[0]-lx) + abs(loc[1]-ly)
        pixels_turtle_space.sort(key=dist)
    tx, ty = pixels_turtle_space[0]
    pixels_turtle_space = pixels_turtle_space[1:]
    disp_x = tx-lx
    disp_y = ty-ly
    if disp_x:
        if abs(disp_x)>1: print(abs(disp_x), 'times', file=outp)
        print('right' if disp_x>0 else 'left', file=outp)
        if abs(disp_x)>1: print('end', file=outp)
    if disp_y:
        if abs(disp_y)>1: print(abs(disp_y), 'times', file=outp)
        print('up' if disp_y>0 else 'down', file=outp)
        if abs(disp_y)>1: print('end', file=outp)
    fuel += abs(disp_x) + abs(disp_y)
    print('paint', file=outp)
    lx, ly = tx, ty
    iter += 1

outp.close()

battery = fuel + paint

print('To run script completely, at least this amount of resources is needed:')
print('Battery:', battery)
print('Fuel:', fuel)
print('Paint:', paint)
