import pygame
from sys import exit
#   every pygame project needs this call before any other pygame code is run
pygame.init()
#   making these variables to illustrate the meanings of the arguments 
# in the next method
WIDTH = 800
HEIGHT = 400
#   this is also something that has to be done early in the code, defining
# the window that the program is to be drawn on, typically designated "screen"
# requires at least a tuple of width and height
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#   change the window label (apparently you can reset the icon in a similar way)
pygame.display.set_caption('Runner')
#   choosing to make the frames per second a variable to illustrate where it is
# in the code below
FPS = 60

#   instantiating a timer that counts in milliseconds from the time the code
# launches. The function using it below can be limited by method to the 
# desired FPS
clock = pygame.time.Clock()
#   pygame.font.Font(font_name, font_size)
test_font = pygame.font.Font('./font/Pixeltype.ttf', 50)
game_active = True
#   Display surface like the screen variable above refers to the end user's 
# device. Once it's set it is basically static. The below surfaces are a
# more abstract concept. Basically there will be one for anything drawn on
# the display surface... more akin to layers in a photo editor
#   The surface's first option is a tuple of it's size, Surface((w, h))
# ** test_surface = pygame.Surface((100, 200))
#   Simple fill command, its argument is a color, many named colors can be used
# ** test_surface.fill('Red')
#   the image.load function makes a surface carry an image, standard file format
# of the image location as the argument
sky_surface = pygame.image.load('./graphics/Sky.png').convert()
ground_surface = pygame.image.load('./graphics/ground.png').convert()
snail_surface = pygame.image.load('./graphics/snail/snail1.png').convert_alpha()
snail_x_pos = 600
snail_y_pos = 300
snail_rect = snail_surface.get_rect(midbottom = (snail_x_pos, snail_y_pos))
player_surface = pygame.image.load('./graphics/Player/player_walk_1.png').convert_alpha()
player_x_pos = 80
player_y_pos = 300
player_gravity = 0
player_rect = player_surface.get_rect(midbottom = (player_x_pos, player_y_pos))
# render(text_to_be_written, anti_aliasing_bool, color)
score_surface = test_font.render('My game', False, (64, 64, 64))
score_rect = score_surface.get_rect(center = (400, 50))

#   this is intentionally an infinite loop, its what the game play loop and 
# screen animation update functions exist in
while True:
    #   this is the loop that checks all of the user inputs
    for event in pygame.event.get():
        #   creating an exit event
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() # needs both, first only exits pygame functions!!
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300: player_gravity = -20
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom == 300: player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: 
                    snail_rect.x = 600
                    game_active = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                snail_rect.x = 600
                game_active = True

    if game_active:
        #   blit means "block image transfer", and basically sets on surface on
        # another surface. Essentially it functionally draws something to a surface
        # be that the screen, or like text within a label.
        #   The blit's arguments are the surface thats to be drawn in and its position
        # in pixels counting out from the top left as a tuple (x or horizontal axis, 
        # y or vertical axis)
        # blit(new_graphic_surface, (x_axis, y_axis))
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        pygame.draw.rect(screen, '#c0e8ec', score_rect)
        pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        screen.blit(score_surface, score_rect)
        screen.blit(snail_surface, snail_rect)
        snail_rect.left -= 4
        if snail_rect.right < 0: snail_rect.left = WIDTH - 4
        # [P]layer
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        screen.blit(player_surface, player_rect)
        # [C]ollisions
        if snail_rect.colliderect(player_rect):
            game_active = False
    else:
        screen.fill('Yellow')

    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_SPACE]:
    #     print('jump')

    # if player_rect.colliderect(snail_rect):
    #     print('hit')
    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint(mouse_pos):
    #     print(pygame.mouse.get_pressed())
    #   draw all elements and update everything
    pygame.display.update()
    clock.tick(FPS)
