import pygame
import random

player_speed_x = 0.75
player_speed_y = 0.75

class Player(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int, speed_x:int, speed_y:int, height:int, width:int, colour:tuple, bounds_horizontal: tuple, bounds_vertical:tuple) -> None:
        super().__init__()
        self.position = (x,y)
        self.speed = (speed_x, speed_y)
        self.height = height
        self.width = width
        self.colour = colour
        self.bounds_x = bounds_horizontal
        self.bounds_y = bounds_vertical
        self.hitbox = pygame.Rect(self.position, (self.width, self.height))
        self.score = 0

    def update(self):
        self.position = (self.position[0] + self.speed[0], self.position[1] - self.speed[1])
        self.hitbox = pygame.Rect(self.position, (self.width, self.height))
        self.speed = (0,0)
    
    def draw(self, surface) :
        """Draws the player to the surface"""
        pygame.draw.rect(surface, self.colour, [self.position[0], self.position[1], self.width, self.height])
        #pygame.draw.rect(window, blue, [player2_initial_left, player2_initial_top, paddle_width, paddle_height], paddle_thickness)

    def move_up(self):
        if self.bounds_y[0] < self.position[1]:
            self.speed = (0, player_speed_y)

    def move_down(self):
        if self.position[1] < (self.bounds_y[1] - self.height):
            self.speed = (0, -player_speed_y)

    def move_left(self):
        self.speed = (-player_speed_x, 0)

    def move_right(self):
        self.speed = (player_speed_x, 0)


class ball(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int, speed_x:int, speed_y:int, width:int, height:int, bounds_horizontal:tuple, bounds_vertical:tuple, colour:tuple) -> None:
        super().__init__()
        self.position = (x,y)
        self.width = width
        self.height = height
        self.speed = (speed_x, speed_y)
        self.bounds_x = bounds_horizontal
        self.bounds_y = bounds_vertical
        self.colour = colour
        self.hitbox = pygame.Rect(self.position, (self.width, self.height))

    def update(self):
        self.position = (self.position[0] + self.speed[0], self.position[1] - self.speed[1])
        self.hitbox = pygame.Rect(self.position, (self.width, self.height))
    
    def draw(self, surface) :
        pygame.draw.rect(surface, self.colour, [self.position[0], self.position[1], self.width, self.height], 10)

    def collide_along_x(self):
        self.speed = (-self.speed[0], self.speed[1])
    def collide_along_y(self):
        self.speed = (self.speed[0], -self.speed[1])

    def paddle_collide(self):
        if random.random() > 0.9:
            self.speed = (self.speed[0], random.uniform(-0.5, 0.5))
        else:
            self.speed = (-self.speed[0], self.speed[1])
    
    def stop(self):
        self.speed = (0,0)