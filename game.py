import pygame
from sys import exit 
from random import randint
pygame.init()


def display_score():
    
        current_time =int((pygame.time.get_ticks()/1000) - start_time)
        score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64)).convert_alpha()
        
        score_rect= score_surf.get_rect(center= (400, 50))
        screen.blit(score_surf,score_rect)
        return current_time

def obstacle_movement(obstacle_list):
            if obstacle_list:
                for obstacle_rect in obstacle_list:
                    obstacle_rect.x -= 5

                    if obstacle_rect.bottom == 300:
                        screen.blit(snail_surface, obstacle_rect)
                    else: 
                        screen.blit(fly_surface, obstacle_rect)


                obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]   
                return obstacle_list
            else:
                return[]

def collisions(player, obstacles):
        if obstacles:
            for obstacle_rect in obstacles:
                if player.colliderect(obstacle_rect):
                    return False
        return True

def player_animation():
    global player_surface, player_index
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index+=0.1
        if player_index>= len(player_walk):
            player_index=0
        player_surface = player_walk[int(player_index)]


screen=pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock=pygame.time.Clock()

start_time = 0
sky= pygame.image.load('pthon_game/Sky.png').convert_alpha()
ground=pygame.image.load('pthon_game/ground.png').convert_alpha()
test_font=pygame.font.Font('pthon_game/Pixeltype.ttf', 50)
game_active = True
title = test_font.render(f' Welcome to Alien Cart!', False, (64,64,64)).convert_alpha()
title_rect = title.get_rect(center=(400,55))
header = test_font.render(f'Press space to start the game', False, (64, 64,64)).convert_alpha()
header_rect = header.get_rect(center=(400, 340))
snail_surface=pygame.image.load('pthon_game/snail1.png').convert_alpha()
fly_surface= pygame.image.load('pthon_game/Fly1.png').convert_alpha()
snail_x_pos=600
player_gravity=0
player_stand = pygame.image.load('pthon_game/player_stand.png').convert_alpha()
player_surface=pygame.image.load('pthon_game/player_walk_1.png').convert_alpha()
player_stand_rect = player_surface.get_rect(center= (360, 160))
player_stand_scaled = pygame.transform.rotozoom(player_stand, 0, 2)
player_walk_1=pygame.image.load('pthon_game/player_walk_1.png').convert_alpha()
player_walk_2=pygame.image.load('pthon_game/player_walk_2.png').convert_alpha()
player_walk=[player_walk_1,player_walk_2]
player_index=0
player_jump=pygame.image.load('pthon_game/jump.png').convert_alpha()
player_surface=player_walk[player_index]

player_rect=player_surface.get_rect(midbottom=(80,300))
snail_rect=snail_surface.get_rect(midbottom=(600, 300))

obstacle_rect_list = []

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_frame_1= pygame.image.load('pthon_game/snail1.png').convert_alpha()
snail_frame_2= pygame.image.load('pthon_game/snail2.png').convert_alpha()
snail_frame=[snail_frame_1, snail_frame_2]
snail_index=0
snail_surf=snail_frame[snail_index]
fly_frame_1=pygame.image.load('pthon_game/Fly1.png').convert_alpha()
fly_frame_2=pygame.image.load('pthon_game/Fly2.png').convert_alpha()
fly_frame=[fly_frame_1,fly_frame_2]
fly_frame_index=0
fly_surf=fly_frame[fly_frame_index]



snail_animation_timer= pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer= pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)


while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
        
        

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20 
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300 :
                        player_gravity=-20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                # snail_rect.left = 800
                start_time = int(pygame.time.get_ticks()/1000)

        if game_active:
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(900, 1100), 210)))
        
            if event.type== snail_animation_timer:
                if snail_index ==0:
                    snail_index=1
                else:
                    snail_index=0
                snail_surface= snail_frame[snail_index]

            if event.type == fly_animation_timer:
                if fly_frame_index==0:
                    fly_frame_index=1
                else:
                    fly_frame_index=0
                fly_surface= fly_frame[fly_frame_index]
        
        
    
    
    if game_active:
        screen.blit(sky, (0,0))
        screen.blit(ground, (0,300))   

        score = display_score()

        # Player:
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300 
            player_animation()
        screen.blit(player_surface, player_rect)
        
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collisions
        # if snail_rect.colliderect(player_rect):
        game_active= collisions(player_rect, obstacle_rect_list)


    else:
        screen.fill("#bbf6fb")
        screen.blit(player_stand_scaled, player_stand_rect)
        obstacle_rect_list.clear()
        player_gravity=0
        score_message = test_font.render(f'Your score: {score}', False, (111, 190, 170))
        score_rect=score_message.get_rect(center=(400, 330))
        if score==0:            
            screen.blit(header, header_rect)
            screen.blit(title, title_rect)
        else:
            screen.blit(score_message, score_rect)
            screen.blit(title, title_rect)

    pygame.display.update()
    clock.tick(60)


















