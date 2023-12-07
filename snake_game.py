import pygame
import random
import sys
import time
import os

## Font style
title_font_path = os.path.dirname(os.path.abspath(__file__)) + "/font_style/ka1.ttf"
global title_custom_font


class Food(object):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        pass

    def eat(self):
        pass

    def appear(self):
        pass

    def disappear(self):
        pass


class SpecialFood(Food):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.color = color

    def draw(self):
        pass

    def eat(self):
        pass

    def appear(self):
        pass

    def disappear(self):
        pass


class SpeedFood(Food):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.color = color

    def draw(self):
        pass

    def eat(self):
        pass

    def appear(self):
        pass

    def disappear(self):
        pass


class Menu(object):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        pass

    def play(self):
        pass

    def quit(self):
        pass


pygame.init()

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
dark_green = (0, 155, 0)  # Darker shade for the snake
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
bright_blue = (0, 0, 255)


title_custom_font = pygame.font.Font(title_font_path, 60)


# Set up display
dis_width = 1200
dis_height = 800
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Snake Game")


clock = pygame.time.Clock()
global my_fps
my_fps = 60


special_food_spawn_probability_per_second = (
    0.1  # 10% chance of spawning special food per second
)
speed_food_spawn_probability_per_second = (
    0.2  # 20% chance of spawning speed food per second
)
special_food_lifetime = 15000  # Special food disappears after 15 seconds
speed_food_lifetime = 20000  # Speed food disappears after 20 seconds
speed_boost_duration = 5000  # Speed boost lasts for 5 seconds


snake_block = 10
font_style = pygame.font.SysFont("bahnschrift", 25)


# Function to display the score of the player
def your_score(score):
    value = font_style.render("Your Score: " + str(score), True, white)
    dis.blit(value, [0, 0])


# Function to display the FPS on the top right corner of the screen
def your_fps(fps):
    fps = round(fps, 2)
    value = font_style.render("Your FPS: " + str(fps), True, white)
    dis.blit(value, [0, 25])


# Function to display the game's main title
def draw_main_title(msg):
    mesg = custom_font.render(msg, True, white)
    dis.blit(mesg, [dis_width // 3 - 100, dis_height // 2 - 300])


# Function to display messages
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 3, dis_height / 2 + 300])


# Our snake function
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, dark_green, [x[0], x[1], snake_block, snake_block])


# Function to draw buttons
def draw_button(button_text, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(dis, active_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(dis, inactive_color, (x, y, w, h))

    text_surf = font_style.render(button_text, True, black)
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    dis.blit(text_surf, text_rect)


def draw_quit_button():
    """Function to draw the quit button should be on the top right corner of the screen"""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if dis_width - 100 + 50 > mouse[0] > dis_width - 100 and 0 + 50 > mouse[1] > 0:
        pygame.draw.rect(dis, bright_red, (dis_width - 100, 0, 100, 50))
        if click[0] == 1:
            pygame.quit()
            quit()
    else:
        pygame.draw.rect(dis, red, (dis_width - 100, 0, 100, 50))

    text_surf = font_style.render("Quit", True, black)
    text_rect = text_surf.get_rect()
    text_rect.center = ((dis_width - 50), (25))
    dis.blit(text_surf, text_rect)


def draw_pause_menu():
    """
    Function to draw the pause menu
    """


def gameLoop():  # Creating a function
    global snake_speed
    game_over = False
    game_close = False

    clock.tick(my_fps)

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    special_food_appeared = False
    special_foodx = 0
    special_foody = 0

    speed_food_appeared = False
    speed_foodx = 0
    speed_foody = 0

    speed_boost_duration = 5000

    while not game_over:
        while game_close == True:
            dis.fill(black)
            message("You lost! Press Q-Quit or C-Play Again", red)
            your_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        main_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_KP8:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_ESCAPE:
                    main_menu()
                # elif event.key == pygame.K_p:
                #     # Pause the game

        # Teleportation
        if x1 >= dis_width:
            x1 = 0
        elif x1 < 0:
            x1 = dis_width - snake_block
        if y1 >= dis_height:
            y1 = 0
        elif y1 < 0:
            y1 = dis_height - snake_block

        x1 += x1_change
        y1 += y1_change

        dis.fill(black)

        # Food
        pygame.draw.rect(dis, blue, [foodx, foody, snake_block, snake_block])

        # Special food
        if (
            not special_food_appeared and random.random() < 0.005
        ):  # Adjust the probability as needed
            special_food_appeared = True
            special_foodx = (
                round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            )
            special_foody = (
                round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            )

        # Speed food
        if (
            not speed_food_appeared and random.random() < 0.002
        ):  # Adjust the probability as needed
            speed_food_appeared = True
            speed_foodx = (
                round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            )
            speed_foody = (
                round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            )

        # Draw the speed boost timer

        # Draw the special food if it has appeared
        if special_food_appeared:
            pygame.draw.rect(
                dis, red, [special_foodx, special_foody, snake_block, snake_block]
            )

        # Draw the speed food if it has appeared
        if speed_food_appeared:
            pygame.draw.rect(
                dis, bright_green, [speed_foodx, speed_foody, snake_block, snake_block]
            )

        # Update the snake Lenght
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > length_of_snake:
            del snake_List[0]

        # Game over if snake hits itself
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # Draw the snake
        our_snake(snake_block, snake_List)
        # Update the score
        your_score(length_of_snake - 1)
        your_fps(clock.get_fps())

        # Update the display
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1

        if x1 == special_foodx and y1 == special_foody:
            special_food_appeared = False
            length_of_snake += 2

        clock.tick(snake_speed)

    pygame.quit()
    quit()


# Functions to set difficulty
def set_easy():
    global snake_speed
    snake_speed = 20
    gameLoop()


def set_medium():
    global snake_speed
    snake_speed = 30
    gameLoop()


def set_hard():
    global snake_speed
    snake_speed = 50
    gameLoop()


# Main menu function
def main_menu():
    menu_active = True
    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        dis.fill(black)  # Background

        # print the title SNAKE in Custom font
        draw_main_title("SNAKE - GAME")

        draw_quit_button()

        # Draw buttons
        center_x = dis_width // 2
        center_y = dis_height // 2
        # Adjust the x-coordinates for the "Easy", "Medium", and "Hard" buttons
        draw_button(
            "Easy", center_x - 275, center_y, 150, 50, green, bright_green, set_easy
        )
        draw_button(
            "Medium", center_x - 75, center_y, 150, 50, blue, bright_blue, set_medium
        )
        draw_button(
            "Hard", center_x + 125, center_y, 150, 50, red, bright_red, set_hard
        )

        pygame.display.update()


# Call the main menu function
main_menu()
