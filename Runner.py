import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('Graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('Graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump  = pygame.image.load('Graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0
        
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.2)
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
            
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom > 300:
            self.rect.bottom = 300
        
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
        
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == 'fly':
            fly_frame_1 = pygame.image.load('Graphics/Fly/Fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('Graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 210
                
        elif type == 'snail':
            snail_frame_1 = pygame.image.load('Graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('Graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
        
    def animation_state(self):
        if self.rect.bottom == 210:
            self.animation_index += 0.2
        elif self.rect.bottom == 300:
            self.animation_index += 0.09

        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
        
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
        
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int((pygame.time.get_ticks() - start_time)/1000)
    score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('Font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.4)
bg_music.play(loops = -1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('Graphics/Sky.png').convert()
ground_surface = pygame.image.load('Graphics/ground.png').convert()

obstacle_rect_list = []

# Intro Screen
player_stand = pygame.image.load('Graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

title = test_font.render('Pixel Runner', False, (111,196,169))
title_rect = title.get_rect(center = (400, 75))

instructions = test_font.render('Press space to run!', False, (111,196,169))
instructions_rect = instructions.get_rect(center = (400, 325))

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if game_active:
            
            #Obstacle Timer
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
                
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
            
                


        
    if game_active:
        # Actual game loop
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        
        score = display_score()

        # Player
        player.draw(screen)
        player.update()
        
        # Obstacle Movement
        obstacle_group.draw(screen)
        obstacle_group.update()
        
        # Collision
        game_active = collision_sprite()


    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        player.midbottom = (80,300)
        player_gravity = 0
        
        score_message = test_font.render(f'Congratulations! You got a score of {score} !', False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400, 325))
        screen.blit(title, title_rect)
        
        if score == 0: screen.blit(instructions, instructions_rect)
        else: screen.blit(score_message, score_message_rect)
    
    pygame.display.update()
    clock.tick(60)
    