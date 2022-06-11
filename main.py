import pygame
from sys import exit
from random import randint

# [I]nit
pygame.init()

# [G1]lobal Constants
WIDTH = 800
HEIGHT = 400
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('./font/Pixeltype.ttf', 50)

# [F]unctions
def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def display_score():
    current_time = round((pygame.time.get_ticks() - start_time) / 100)
    score_surface = test_font.render(f'{current_time}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300: screen.blit(snail_surface, obstacle_rect)
            else: screen.blit(fly_surface, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else: return []

# [G2]lobal variables
game_active = False
start_time = 0
score = 0

# [G3]raphic surfaces
# [G3E1]nvironment graphics
sky_surface = pygame.image.load('./graphics/Sky.png').convert()
ground_surface = pygame.image.load('./graphics/ground.png').convert()
# [G3E2]nemy graphics
snail_surface = pygame.image.load('./graphics/snail/snail1.png').convert_alpha()
fly_surface = pygame.image.load('./graphics/Fly/Fly1.png').convert_alpha()
obstacle_rect_list = []
# [G3P]layer graphics
player_surface = pygame.image.load('./graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80, 300))
player_gravity = 0

# [G4]ame over screen
player_stand = pygame.image.load('./graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))
game_name = test_font.render('pyRunner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 80))
game_message = test_font.render('Press Space To Run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center = (400, 330))

# [T]imer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, randint(1500, 2500))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # [C1]ontrols
        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 2): obstacle_rect_list.append(snail_surface.get_rect(midbottom = (randint(900, 1100), 300)))
                else: obstacle_rect_list.append(fly_surface.get_rect(midbottom = (randint(900, 1100), 210)))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300: player_gravity = -20
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom == 300: player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: 
                    game_active = True
                    start_time = pygame.time.get_ticks()

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        # [P]layer
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        screen.blit(player_surface, player_rect)

        # [O]bstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # [C2]ollisions
        game_active = collisions(player_rect, obstacle_rect_list)

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0
        score_message = test_font.render(f'Your Score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (400, 330))
        screen.blit(game_name, game_name_rect)
        if score == 0: screen.blit(game_message, game_message_rect)
        else: screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(FPS)