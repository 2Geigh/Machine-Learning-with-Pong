import pygame
from pygame.locals import *
import game_classes
from random import random
from random import uniform

pygame.init()
pygame.font.init()

#dimensions and attributes for the game's viewport window
window_width = 1000 #px
window_height = 333 #px
window_title = "Pong"

#boolean status that when toggled to False closes the viewport window
window_run_status = True

#creating the viewport window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(window_title)

WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,255,255)

background_colour = (0,0,0)

player1_colour = WHITE
player2_colour = BLUE
ball_colour = RED

#specifications of each sprite on-screen
paddle_height = 50
paddle_width = 10
paddle_thickness = 1
paddle_bound_x = (0, window_width)
paddle_bound_y = (0, window_height)
ball_diameter = 15
ball_width = ball_diameter
ball_height = ball_diameter
ball_thickness = paddle_thickness
ball_bound_x = (0, window_width - ball_width)
ball_bound_y = (0, window_height - ball_height)

#initial positions for player 1, player 2, and the ball
player1_initial_top = (window_height / 2) - (paddle_height / 2)
player1_initial_left = window_width * 0.05
player1_initial_speed_horizontal = 0
player1_initial_speed_vertical = 0


player2_initial_top = player1_initial_top
player2_initial_left = (window_width - (window_width * 0.05))
player2_initial_speed_horizontal = 0
player2_initial_speed_vertical = 0

ball_initial_top = ((window_height / 2) - (ball_diameter / 2))
ball_initial_left = ((window_width / 2) - (ball_diameter / 2))

def get_ball_initial_speed() -> tuple:
    #setting initial speed and horizontal direction of ball
    if random() > 0.5:
        ball_initial_speed_horizontal = 0.5
    else:
        ball_initial_speed_horizontal = -0.5

    #getting a random vertical velocity so that the ball doesn't have the same tragectory every time
    ball_initial_speed_vertical = 0
    while ball_initial_speed_vertical == 0:
        ball_initial_speed_vertical = uniform(-0.33, 0.33)
    
    return (ball_initial_speed_horizontal, ball_initial_speed_vertical)

get_ball_initial_speed()

player1 = game_classes.Player(player1_initial_left, player1_initial_top, player1_initial_speed_horizontal, player1_initial_speed_vertical, paddle_height, paddle_width, player1_colour, paddle_bound_x, paddle_bound_y)
player2 = game_classes.Player(player2_initial_left, player2_initial_top, player2_initial_speed_horizontal, player2_initial_speed_vertical, paddle_height, paddle_width, player2_colour, paddle_bound_x, paddle_bound_y)
ball = game_classes.ball(ball_initial_left, ball_initial_top, get_ball_initial_speed()[0], get_ball_initial_speed()[1], ball_width, ball_height, ball_bound_x, ball_bound_y, ball_colour)

READY_TIME = 1500 #ms #the amount of time inbetween when the game is reset and when the game starts
PAUSE_TIME = 750 #ms #the amount of time inbetween when a point is scored and when the game resets

#for the score
player1_score_position = (window_width / 3, window_height / 6)
player2_score_position = (window_width / 3 * 2, window_height / 6)
score_font_size = int(window_height / 5)
score_font = pygame.font.SysFont('Consolas', score_font_size, True, False)

#keep viewport window open if game is running
while (window_run_status):

    player1.position = (player1_initial_left,player1_initial_top)
    player1.speed = (0,0)
    player2.position = (player2_initial_left, player2_initial_top)
    player2.speed = player1.speed
    ball.position = (ball_initial_left, ball_initial_top)
    ball.speed = get_ball_initial_speed()

    #boolean status that when toggled False ends and resets a round
    game_run = True

    #initialise game
    player1.update()
    player2.update()
    ball.update()
    window.fill(background_colour)
    player1.draw(window)
    player2.draw(window)
    ball.draw(window)

    player1_score_surface = score_font.render(str(player1.score), False, WHITE)
    player2_score_surface = score_font.render(str(player2.score), False, WHITE)
    window.blit(player1_score_surface, player1_score_position)
    window.blit(player2_score_surface, player2_score_position)

    pygame.display.update()
    
    pygame.time.wait(READY_TIME)

    while game_run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window_run_status = False

        #ball collision with wall
        if ball.position[0] <= ball.bounds_x[0] or ball.position[0] >= ball.bounds_x[1]:
            ball.collide_along_x()
            ball.stop()

            if ball.position[0] <= ball.bounds_x[0]:
                player2.score += 1
            else:
                player1.score += 1
            
            game_run = False #Tells the round to stop and restart when a point is scored

        #controls
        keys = pygame.key.get_pressed()
        #joint controls between player1 and player2
        if keys[pygame.K_w] and keys[pygame.K_UP]:
            player1.move_up()
            player2.move_up()
        elif keys[pygame.K_s] and keys[pygame.K_DOWN]:
            player1.move_down()
            player2.move_down()
        elif keys[pygame.K_w] and keys[pygame.K_DOWN]:
            player1.move_up()
            player2.move_down()
        elif keys[pygame.K_s] and keys[pygame.K_UP]:
            player1.move_down()
            player2.move_up()
        #player1 sole controls
        elif keys[pygame.K_w]:
            player1.move_up()
        elif keys[pygame.K_s]:
            player1.move_down()
        #player2 sole controls
        elif keys[pygame.K_UP]:
            player2.move_up()
        elif keys[pygame.K_DOWN]:
            player2.move_down()
        #quit control
        elif keys[pygame.K_ESCAPE]:
            game_run = False
            window_run_status = False

        if ball.position[1] < 0 or ball.position[1] > window_height:
            ball.collide_along_y()

        #ball collision with paddles
        if ball.hitbox.colliderect(player1.hitbox):
            ball.paddle_collide()
        elif ball.hitbox.colliderect(player2.hitbox):
            ball.paddle_collide()


        #update sprites
        player1.update()
        player2.update()
        ball.update()

        #clear the window
        window.fill(background_colour)

        #draw sprites
        player1.draw(window)
        player2.draw(window)
        ball.draw(window)

        #draw score
        window.blit(player1_score_surface, player1_score_position)
        window.blit(player2_score_surface, player2_score_position)
        
        #update the display
        pygame.display.update()
    
    pygame.time.wait(PAUSE_TIME)

pygame.quit()
quit()
