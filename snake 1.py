import numpy as np
from numpy import random
import pygame
import time
from pygame.locals import *

score = 0

class Snake(object):

    def __init__(self):

        self.length = [(11, 11), (11, 10), (11, 9), (11, 8)]
        self.direction = (0, 1)

        # (0, 1) = up
        # (0,-1) = down,
        # (1,0) = right,
        # (-1,0) = left

    def snake_figure(self, surface):

        # head
        radius = 6
        color_fill = 6
        color = (255, 255, 255, 255)
        position = (20 + 20*self.length[0][0], 20 + 20*self.length[0][1])
        pygame.draw.circle(surface, color, position, radius, color_fill)

        # body - use loop
        i = 1
        while i <= len(self.length)-1:
            radius = 5
            color_fill = 5
            color = (255, 255, 255,255)
            position = (20 + 20*self.length[i][0], 20 + 20*self.length[i][1])
            pygame.draw.circle(surface, color, position, radius, color_fill)
            i += 1

    def get_head(self):
        return self.length[0]

    def move(self, indicator):
        #indicator: if the snake reaches food

        if indicator == False:
            self.length.pop()

        self.length.insert(0,(self.length[0][0] + self.direction[0], self.length[0][1] + self.direction[1]))

    def eat(self, food):

        global score

        snake_x, snake_y = self.length[0]
        food_x, food_y = food.location

        # use food_location in class food
        if snake_x == food_x and snake_y == food_y:
            score += 1
            return True  # goes to indicator in move()

        else:
            return False  # goes to indicator in move()

    def toward(self, new_direction):

        if new_direction[0]*self.direction[0] >= 0 and new_direction[1]*self.direction[1] >= 0:
            self.direction = new_direction


class food(object):

    #np.random
    #np.random.randint

    def __init__(self):
        self.location = (np.random.randint(21), np.random.randint(21))

    def draw_food(self, surface):

        radius = 6
        color_fill = 6
        color = (255, 255, 255,255)
        position = (20 + 20*self.location[0], 20 + 20*self.location[1])
        pygame.draw.circle(surface, color, position, radius, color_fill)

    def random_food(self, surface, indicator, Snake):
        #do not overlap with the snake
        #indicator = indicator in Snake.eat
        if indicator == True:
            self.location = (np.random.randint(21), np.random.randint(21))
            while self.location in Snake.length:
                self.location = (np.random.randint(21), np.random.randint(21))
            #then draw food


board_width = 21
board_height = 21

def init_board(surface):
    color = (0,0,0,0)
    width = 0

    for i in range(board_height - 1):

        pos = i*20, 0, 20, 20
        pygame.draw.rect(surface, color, pos, width)
        pos = i*20, (board_height - 1)*20, 20, 20
        pygame.draw.rect(surface, color, pos, width)

    for i in range(board_height - 1):

        pos = 0, 20 + i*20, 20, 20
        pygame.draw.rect(surface, color, pos, width)
        pos = (board_width - 1)*20, 20 + 1*20, 20, 20
        pygame.draw.rect(surface, color, pos, width)

def game_over(snake):

    x, y = snake.get_head()
    is_fail = False

    old = len(snake.length)
    new = len(set(snake.length))

    if new < old:
        is_fail = True
    elif x == 0 or x == board_width - 1:
        is_fail = True
    elif y == 0 or y == board_height - 1:
        is_fail = True

    return is_fail

def game_init():

    pygame.init()
    surface = pygame.display.set_mode((21*20, 21*20))
    pygame.display.set_caption("SNAKE")
    return surface

def print_text(surface, font, color, text, position ):
    image_text = font.render(text, True, color)
    surface.blit(image_text, position)

def press(keys, snake):
    global score

    if keys[K_w] or keys[K_UP]:
        snake.toward((0,-1))
    elif keys[K_a] or keys[K_LEFT]:
        snake.toward((-1,0))
    elif keys[K_d] or keys[K_RIGHT]:
        snake.toward((1,0))
    elif keys[K_s] or keys[K_DOWN]:
        snake.toward((0, 1))

    elif keys[K_r]:
        score = 0
        main()

    elif keys[K_ESCAPE]:
        exit()

def game(surface): #main function

    snake = Snake()
    Food = food()
    font = pygame.font.SysFont("Ariel", 35 ) #font
    is_fail = False
    while True:
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 pygame.quit()
                 exit()

        surface.fill((0, 0, 100))
        init_board(surface = surface)

        keys = pygame.key.get_pressed()
        press(keys, snake)

        if is_fail:
            font2 = pygame.font.SysFont("Ariel", 35 )  #font
            print_text(surface, font2, (0,0,255), "Game Over", (11,11))

        if not is_fail:
            indicator = snake.eat(Food)
            text = "score = {}".format(score)
            print_text(surface, font, (0, 0, 255), text, (0, 21))
            Food.random_food(surface, indicator, snake)

            Food.draw_food(surface)

            snake.move(indicator)
            is_fail = game_over(snake = snake)
            snake.snake_figure(surface)

        pygame.display.update()
        time.sleep(0.1)

def main():
    surface = game_init()
    game(surface)

if __name__ == "__main__":
    main()
