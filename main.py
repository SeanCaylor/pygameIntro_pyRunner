import pygame
from sys import exit
from random import randint, choice

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_1 = pygame.image.load('./graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('./graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('./graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('./graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1500), y_pos))
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('./graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('./graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('./graphics/Player/jump.png').convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: self.rect.bottom = 300
    def animation_state(self):
        if self.rect.bottom < 300: self.image = self.player_jump
        else: 
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
    def update(self):
        self.animation_state()
        self.apply_gravity()
        self.player_input()
def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True
def collision_sprites():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False): 
        obstacle_group.empty()
        return False
    else: return True
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
def player_animation():
    global player_surface, player_index
    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surface = player_walk[int(player_index)]
pygame.init()
WIDTH = 800
HEIGHT = 400
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('./font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()
sky_surface = pygame.image.load('./graphics/Sky.png').convert()
ground_surface = pygame.image.load('./graphics/ground.png').convert()
player_stand = pygame.image.load('./graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))
game_name = test_font.render('pyRunner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 80))
game_message = test_font.render('Press Space To Run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center = (400, 330))
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, randint(1500, 2500))
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)
fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: 
                    game_active = True
                    start_time = pygame.time.get_ticks()
    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()
        game_active = collision_sprites()
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        score_message = test_font.render(f'Your Score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (400, 330))
        screen.blit(game_name, game_name_rect)
        if score == 0: screen.blit(game_message, game_message_rect)
        else: screen.blit(score_message, score_message_rect)
    pygame.display.update()
    clock.tick(FPS)