import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int((pygame.time.get_ticks() - start_time)/1000)
    score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            
            screen.blit(snail_surf, obstacle_rect)
            
        return obstacle_list
    else: return []

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('Font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

sky_surface = pygame.image.load('Graphics/Sky.png').convert()
ground_surface = pygame.image.load('Graphics/ground.png').convert()

# Player Surface
player_surf = pygame.image.load('Graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0

# Obstacles
snail_surf = pygame.image.load('Graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom = (600, 300))

obstacle_rect_list = []

# Intro Screen
player_stand = pygame.image.load('Graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

title = test_font.render('Pixel Runner', False, (111,196,169))
title_rect = title.get_rect(center = (400, 75))

instructions = test_font.render('Press space to run!', False, (111,196,169))
instructions_rect = instructions.get_rect(center = (400, 325))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom == 300:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20

            if event.type == pygame.KEYDOWN and player_rect.bottom == 300:
                if event.key == pygame.K_SPACE:
                    player_gravity = -20
            
            if event.type == obstacle_timer:
                obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900,1100), 300)))
                
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.right = 600
                start_time = pygame.time.get_ticks()
        
    if game_active:
        # Actual game loop
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        # pygame.draw.rect(screen,'#c0e8ec',score_rect)
        # pygame.draw.rect(screen,'#c0e8ec',score_rect,10)
        # screen.blit(score_surf, score_rect)
        score = display_score()

        # snail_rect.x -= 4
        # if snail_rect.right <= 0: snail_rect.left = 800
        # screen.blit(snail_surf, snail_rect)

        # Player
        player_rect.y += player_gravity
        player_gravity += 1
        if player_rect.bottom >= 300:
            player_gravity = 0
            player_rect.bottom = 300
        screen.blit(player_surf, player_rect)
        
        # Obstacle Movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        if snail_rect.colliderect(player_rect):
            game_active = False
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        
        score_message = test_font.render(f'Congratulations! You got a score of {score} !', False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400, 325))
        screen.blit(title, title_rect)
        
        if score == 0: screen.blit(instructions, instructions_rect)
        else: screen.blit(score_message, score_message_rect)
    
    pygame.display.update()
    clock.tick(60)
    