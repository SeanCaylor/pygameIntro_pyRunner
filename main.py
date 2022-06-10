import pygame
from sys import exit

pygame.init()

WIDTH = 800
HEIGHT = 400
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('./font/Pixeltype.ttf', 50)
game_active = True
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
score_surface = test_font.render('My game', False, (64, 64, 64))
score_rect = score_surface.get_rect(center = (400, 50))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

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

    pygame.display.update()
    clock.tick(FPS)
