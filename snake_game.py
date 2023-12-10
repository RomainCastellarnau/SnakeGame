import pygame
import random
import sys
import time
import os
import pygame.mixer


# Asset paths
global font_path, title_font_path, defeat_font_path, score_font_path, defeat_background_path
global game_background_path, pause_background_path, menu_sound_path, game_sound_path, death_sound_path
main_path = os.path.dirname(os.path.abspath(__file__))
title_font_path = main_path + "/Fonts/SnakeJacket.ttf"
defeat_font_path = main_path + "/Fonts/Wasted.ttf"
score_font_path = main_path + "/Fonts/MW.ttf"
defeat_background_path = main_path + "/Background/LostMenu/Wasted.jpeg"
game_background_path = main_path + "/Background//Game/GameBackground.jpeg"
pause_background_path = main_path + "/Background/PauseMenu/pausemenu.jpg"


pygame.init()


snake_block = 20
# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
dark_green = (0, 155, 0)
dark_blue = (0, 0, 139)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
bright_blue = (0, 0, 255)
bright_yellow = (255, 255, 0)
purple = (127, 0, 255)
pink = (255, 51, 255)


scroll = 0

global mute_status
mute_status = False


title_custom_font = pygame.font.Font(title_font_path, 60)
defeat_custom_font = pygame.font.Font(defeat_font_path, 80)
score_custom_font = pygame.font.Font(score_font_path, 25)
font_style = pygame.font.SysFont("bahnschrift", 25)
button_custom_font = pygame.font.Font(title_font_path, 15)

# Set up display
dis_width = 1200
dis_height = 800
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Snake Game")

# Food Assets
game_assets_path = main_path + "/Assets"
food_assets_path = game_assets_path + "/Food/"
food_asset = pygame.image.load(food_assets_path + "apple.png").convert_alpha()
food_asset = pygame.transform.scale(food_asset, (snake_block, snake_block))
special_food_asset = pygame.image.load(food_assets_path + "orange.png").convert_alpha()
special_food_asset = pygame.transform.scale(
    special_food_asset, (snake_block, snake_block)
)
speed_food_asset = pygame.image.load(food_assets_path + "lemon.png").convert_alpha()
speed_food_asset = pygame.transform.scale(speed_food_asset, (snake_block, snake_block))

# Rock Assets
rock_assets_path = game_assets_path + "/Rock/"

middle_rock_assets = [
    pygame.transform.scale(
        pygame.image.load(rock_assets_path + f"MiddleRock{i}.png").convert_alpha(),
        (snake_block, snake_block),
    )
    for i in range(1, 5)
]

edge_rock_assets = [
    pygame.transform.scale(
        pygame.image.load(rock_assets_path + f"EdgeRock{i}.png").convert_alpha(),
        (snake_block, snake_block),
    )
    for i in range(1, 5)
]

# Load the menu background
background_assets_path = main_path + "/Background"
bg_images = []
for i in range(1, 6):
    bg_image = pygame.image.load(
        background_assets_path + "/MainMenu/" f"plx-{i}.png"
    ).convert_alpha()
    bg_image = pygame.transform.scale(bg_image, (dis_width, dis_height))
    bg_images.append(bg_image)
bg_width = bg_images[0].get_width()

global defeat_background, game_background
defeat_background = pygame.image.load(defeat_background_path).convert()
defeat_background = pygame.transform.scale(defeat_background, (dis_width, dis_height))
game_background = pygame.image.load(game_background_path).convert()
game_background = pygame.transform.scale(game_background, (dis_width, dis_height))

# Main Menu Icon
icon_path = main_path + "/Assets/Sound/"
mute_icon = pygame.image.load(icon_path + "Mute_Icon.png").convert_alpha()
mute_icon = pygame.transform.scale(mute_icon, (50, 50))
mute_icon.set_colorkey((255, 255, 255))
sound_icon = pygame.image.load(icon_path + "Sound_Icon.png").convert_alpha()
sound_icon = pygame.transform.scale(sound_icon, (50, 50))
sound_icon.set_colorkey((255, 255, 255))
menu_sound = pygame.mixer.Sound(main_path + "/Sound/Menu_OST.mp3")
game_sound = pygame.mixer.Sound(main_path + "/Sound/Game_OST.mp3")
death_sound = pygame.mixer.Sound(main_path + "/Sound/Death_OST.mp3")

clock = pygame.time.Clock()


def your_score(score):
    value = score_custom_font.render("Your Score: " + str(score), True, white)
    dis.blit(value, [0, 0])


_circle_cache = {}


def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points


def render_outlined_text(text, font, gfcolor, ocolor, opx):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()
    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))
    surf = osurf.copy()
    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))
    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))
    surf.blit(textsurface, (opx, opx))
    return surf


def draw_main_title(msg):
    mesg = title_custom_font.render(msg, True, bright_yellow)
    text_rect = mesg.get_rect(midtop=(dis_width // 2, dis_height // 2 - 300))

    dis.blit(mesg, text_rect)


def defeat_message():
    global length_of_snake

    mesg = render_outlined_text("Wasted", defeat_custom_font, bright_red, black, 3)
    score_message = render_outlined_text(
        "Your Score: " + str(length_of_snake - 1),
        defeat_custom_font,
        bright_yellow,
        black,
        3,
    )
    current_time = pygame.time.get_ticks()
    message_duration = 1500
    message_interval = 2000

    # Wait 1 sec before displaying the message
    if current_time > 1000:
        dis.blit(mesg, [dis_width // 2 - mesg.get_width() // 2, dis_height // 2])
        dis.blit(
            score_message,
            [dis_width // 2 - score_message.get_width() // 2, dis_height // 2 - 150],
        )
    # Wait 1 sec before displaying replay message
    if current_time > 2000:
        if current_time % message_interval < message_duration:
            mesg2 = render_outlined_text(
                "Press Q-Quit or C-Play Again",
                defeat_custom_font,
                bright_yellow,
                black,
                3,
            )
            dis.blit(
                mesg2, [dis_width // 2 - mesg2.get_width() // 2, dis_height // 2 + 100]
            )


def blend_colors(color1, color2, ratio):
    return (
        int(color1[0] * ratio + color2[0] * (1 - ratio)),
        int(color1[1] * ratio + color2[1] * (1 - ratio)),
        int(color1[2] * ratio + color2[2] * (1 - ratio)),
    )


def draw_snake_block(x, y, snake_block, gradient_ratio):
    head_color = pink
    tail_color = purple
    color = blend_colors(tail_color, head_color, gradient_ratio)

    pygame.draw.rect(dis, color, [x, y, snake_block, snake_block])


def our_snake(snake_block, snake_list):
    snake_length = len(snake_list)
    if snake_length > 1:
        for i, (x, y) in enumerate(snake_list):
            gradient_ratio = i / (snake_length - 1)
            draw_snake_block(x, y, snake_block, gradient_ratio)
    elif snake_length == 1:
        x, y = snake_list[0]
        draw_snake_block(x, y, snake_block, 1.0)


def draw_button(button_text, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    button_rect = None

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(dis, active_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(dis, inactive_color, (x, y, w, h))

    text_surf = button_custom_font.render(button_text, True, black)
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    dis.blit(text_surf, text_rect)

    button_rect = pygame.Rect(x, y, w, h)
    return button_rect


def draw_quit_button():
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if dis_width - 100 + 50 > mouse[0] > dis_width - 100 and 0 + 50 > mouse[1] > 0:
        pygame.draw.rect(dis, bright_red, (dis_width - 100, 0, 100, 50))
        if click[0] == 1:
            pygame.quit()
            quit()
    else:
        pygame.draw.rect(dis, red, (dis_width - 100, 0, 100, 50))

    text_surf = button_custom_font.render("QUIT", True, black)
    text_rect = text_surf.get_rect()
    text_rect.center = ((dis_width - 50), (25))
    dis.blit(text_surf, text_rect)


def generate_layout(dis_width, dis_height, difficulty, snake_block):
    block_size = snake_block
    min_blocks = difficulty
    layout = []

    # Initial position of the snake
    initial_snake_x = dis_width / 2
    initial_snake_y = dis_height / 2

    min_distance = 4 * block_size
    min_separation = 2 * block_size

    # Initialize the grid of occupied cells
    grid_rows = dis_height // snake_block
    grid_cols = dis_width // snake_block
    occupied_cells = [[False] * grid_cols for _ in range(grid_rows)]

    for _ in range(min_blocks):
        block_width = random.randint(2, 7) * block_size
        block_height = random.randint(2, 7) * block_size

        max_attempts = 400  # Maximum attempts to find a suitable position

        for _ in range(max_attempts):
            block_x = random.randint(0, dis_width - block_width)
            block_y = random.randint(0, dis_height - block_height)

            if (
                block_x // snake_block < 0
                or (block_x + block_width) // snake_block >= grid_cols
                or block_y // snake_block < 0
                or (block_y + block_height) // snake_block >= grid_rows
            ):
                continue
            # Check if the block is far enough from the initial snake position
            if (
                initial_snake_x < block_x + block_width + min_distance
                and initial_snake_x + snake_block > block_x - min_distance
                and initial_snake_y < block_y + block_height + min_distance
                and initial_snake_y + snake_block > block_y - min_distance
            ):
                continue

            # Check if the block is far enough from other layout blocks
            overlap = any(
                occupied_cells[row + r][col + c]
                for row in range(
                    block_y // snake_block, (block_y + block_height) // snake_block
                )
                for col in range(
                    block_x // snake_block, (block_x + block_width) // snake_block
                )
                for r in range(-1, 2)
                for c in range(-1, 2)
            )

            if not overlap:
                # Mark the occupied positions in the grid
                for row in range(
                    block_y // snake_block, (block_y + block_height) // snake_block
                ):
                    for col in range(
                        block_x // snake_block, (block_x + block_width) // snake_block
                    ):
                        occupied_cells[row][col] = True

                layout.append((block_x, block_y, block_width, block_height))
                break

    return layout


def store_layout_appearance(layouts):
    stored_layout_appearance = []
    for layout_block in layouts:
        block_x, block_y, block_width, block_height = layout_block

        # Choose a random edge rock asset and middle rock asset
        edge_rock_asset = random.choice(edge_rock_assets)
        middle_rock_asset = random.choice(middle_rock_assets)

        stored_layout_appearance.append(
            (
                edge_rock_asset,
                middle_rock_asset,
                block_x,
                block_y,
                block_width,
                block_height,
            )
        )

    return stored_layout_appearance


def draw_layout_block(layout_block, block_size):
    (
        edge_rock_asset,
        middle_rock_asset,
        block_x,
        block_y,
        block_width,
        block_height,
    ) = layout_block

    for x in range(block_x, block_x + block_width, block_size):
        dis.blit(edge_rock_asset, (x, block_y))
        dis.blit(edge_rock_asset, (x, block_y + block_height - block_size))

    for y in range(block_y, block_y + block_height, block_size):
        dis.blit(edge_rock_asset, (block_x, y))
        dis.blit(edge_rock_asset, (block_x + block_width - block_size, y))

    for x in range(
        block_x + block_size, block_x + block_width - block_size, block_size
    ):
        for y in range(
            block_y + block_size, block_y + block_height - block_size, block_size
        ):
            dis.blit(middle_rock_asset, (x, y))


def draw_layout(layout_appearance):
    for layout_block in layout_appearance:
        draw_layout_block(layout_block, snake_block)


special_food_appeared = False
special_foodx = 0
special_foody = 0

speed_food_appeared = False
speed_foodx = 0
speed_foody = 0


def generate_food_position_with_layout_constraints(
    layout,
    snake_List,
    snake_block,
    special_food_appeared,
    special_food_pos,
    speed_food_appeared,
    speed_food_pos,
    min_distance=snake_block,
):
    layout_rects = [pygame.Rect(x, y, width, height) for x, y, width, height in layout]
    invalid_positions = set(
        (x, y)
        for rect in layout_rects
        for x in range(rect.left, rect.right, snake_block)
        for y in range(rect.top, rect.bottom, snake_block)
    )

    invalid_positions.update((int(x), int(y)) for x, y in map(tuple, snake_List))

    if special_food_appeared:
        invalid_positions.add((int(special_food_pos[0]), int(special_food_pos[1])))

    if speed_food_appeared:
        invalid_positions.add((int(speed_food_pos[0]), int(speed_food_pos[1])))

    valid_positions = [
        (x, y)
        for x in range(0, dis_width, snake_block)
        for y in range(0, dis_height, snake_block)
        if all(
            abs(x - ix) >= min_distance and abs(y - iy) >= min_distance
            for ix, iy in invalid_positions
        )
    ]

    if valid_positions:
        return random.choice(valid_positions)
    else:
        # Handle the case when there are no valid positions
        raise ValueError("Unable to find a suitable food position")


def draw_food(food_type, food_x, food_y):
    if food_type == "normal":
        dis.blit(food_asset, (food_x, food_y), (0, 0, snake_block, snake_block))
    elif food_type == "special":
        dis.blit(special_food_asset, (food_x, food_y), (0, 0, snake_block, snake_block))
    elif food_type == "speed":
        dis.blit(speed_food_asset, (food_x, food_y), (0, 0, snake_block, snake_block))


def set_easy():
    global difficulty
    global snake_speed
    difficulty = 2
    snake_speed = 10
    gameLoop()


def set_medium():
    global difficulty
    global snake_speed
    difficulty = 4
    snake_speed = 15
    gameLoop()


def set_hard():
    global difficulty
    global snake_speed
    difficulty = 6
    snake_speed = 25
    gameLoop()


def draw_menu_background():
    global scroll
    for x in range(5):
        speed = 0.5
        for i in bg_images:
            dis.blit(i, ((x * bg_width) - scroll * speed, 0))
            speed += 0.2


def play_menu_sound():
    menu_sound.play()
    menu_sound.play(-1)


def play_game_sound():
    game_sound.play()
    game_sound.play(-1)


def play_death_sound():
    death_sound.play()
    death_sound.set_volume(0.5)


def toggle_mute():
    pass


def main_menu():
    pygame.mixer.init()
    global scroll, mute_status
    scroll = 0
    menu_active = True
    play_menu_sound()

    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_menu_background()
        # print the title SNAKE in Custom font
        draw_main_title("SNAKE - GAME")
        draw_quit_button()
        # Draw buttons
        center_x = dis_width // 2
        center_y = dis_height // 2
        # Adjust the x-coordinates for the "Easy", "Medium", and "Hard" buttons
        draw_button(
            "EASY", center_x - 275, center_y, 150, 50, green, bright_green, set_easy
        )
        draw_button(
            "MEDIUM", center_x - 75, center_y, 150, 50, blue, bright_blue, set_medium
        )
        draw_button(
            "HARD", center_x + 125, center_y, 150, 50, red, bright_red, set_hard
        )

        # Mute/Unmute button

        mute_button_rect = pygame.Rect(
            10, 10, mute_icon.get_width(), mute_icon.get_height()
        )

        # Check if a difficulty button is clicked
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        difficulty_buttons = [
            {
                "rect": pygame.Rect(center_x - 275, center_y, 150, 50),
                "action": set_easy,
            },
            {
                "rect": pygame.Rect(center_x - 75, center_y, 150, 50),
                "action": set_medium,
            },
            {
                "rect": pygame.Rect(center_x + 125, center_y, 150, 50),
                "action": set_hard,
            },
        ]

        for button in difficulty_buttons:
            if button["rect"].collidepoint(mouse) and click[0] == 1:
                button["action"]()
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                menu_active = False

        # Check if the mute button is clicked
        if mute_button_rect.collidepoint(mouse) and click[0] == 1:
            # Toggle mute status
            mute_status = not mute_status
            # Toggle sounds based on mute status
            pygame.mixer.music.set_volume(0.0 if mute_status else 1.0)
            menu_sound.set_volume(0.0 if mute_status else 1.0)
            game_sound.set_volume(0.0 if mute_status else 1.0)
            death_sound.set_volume(0.0 if mute_status else 1.0)

        # Draw mute button image
        if mute_status:
            dis.blit(mute_icon, (10, 10))
        else:
            dis.blit(sound_icon, (10, 10))

        # Scroll the background continuously
        scroll += 2
        if scroll >= 3000:
            scroll = 0

        pygame.display.update()


def gameLoop():
    global special_food_appeared, special_foodx, special_foody
    global speed_food_appeared, speed_foodx, speed_foody
    global snake_speed
    global length_of_snake
    global difficulty
    global mute_status

    original_snake_speed = snake_speed
    start_time = time.time()
    speed_boost_duration = 5

    death_sound_played = False
    pygame.mixer.stop()
    if not mute_status:
        play_game_sound()

    game_over = False
    game_close = False
    my_fps = clock.get_fps()
    clock.tick(my_fps)

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    length_of_snake = 1

    # Generate the layout
    layouts = generate_layout(dis_width, dis_height, difficulty, snake_block)
    stored_layout_appearance = store_layout_appearance(layouts)

    foodx, foody = generate_food_position_with_layout_constraints(
        layouts,
        snake_List,
        snake_block,
        special_food_appeared,
        (special_foodx, special_foody),
        speed_food_appeared,
        (speed_foodx, speed_foody),
    )

    special_food_appeared = False
    special_foodx, special_foody = 0, 0
    speed_food_appeared = False
    speed_foodx, speed_foody = 0, 0

    while not game_over:
        while game_close == True:
            dis.blit(defeat_background, [0, 0])
            if not death_sound_played and not mute_status:
                pygame.mixer.stop()  # Stop any playing sounds
                play_death_sound()
                death_sound_played = True

            defeat_message()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        if not mute_status:
                            pygame.mixer.stop()
                            main_menu()
                        else:
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
                    if not mute_status:
                        pygame.mixer.stop()
                        main_menu()
                    else:
                        main_menu()

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

        dis.blit(game_background, [0, 0])
        your_score(length_of_snake - 1)
        draw_layout(stored_layout_appearance)

        # Normal food
        draw_food("normal", foodx, foody)

        # Check the probability of special food appearing
        if not special_food_appeared and random.random() < 0.005:
            (
                special_foodx,
                special_foody,
            ) = generate_food_position_with_layout_constraints(
                layouts,
                snake_List,
                snake_block,
                special_food_appeared,
                (special_foodx, special_foody),
                speed_food_appeared,
                (speed_foodx, speed_foody),
            )
            special_food_appeared = True

        # Check the probability of speed food appearing
        if not speed_food_appeared and random.random() < 0.002:
            speed_foodx, speed_foody = generate_food_position_with_layout_constraints(
                layouts,
                snake_List,
                snake_block,
                special_food_appeared,
                (special_foodx, special_foody),
                speed_food_appeared,
                (speed_foodx, speed_foody),
            )
            speed_food_appeared = True

        # Draw the special food if it has appeared
        if special_food_appeared:
            draw_food("special", special_foodx, special_foody)

        # Draw the speed food if it has appeared
        if speed_food_appeared:
            draw_food("speed", speed_foodx, speed_foody)

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

        # Game over if snake hits a layout block
        for layout_block in layouts:
            layout_x, layout_y, layout_width, layout_height = layout_block

            # Check if the snake's head collides with any part of the layout block
            if (
                x1 + snake_block > layout_x
                and x1 < layout_x + layout_width
                and y1 + snake_block > layout_y
                and y1 < layout_y + layout_height
            ):
                game_close = True

        # Draw the snake
        our_snake(snake_block, snake_List)
        your_score(length_of_snake - 1)
        # Update the display
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food_position_with_layout_constraints(
                layouts,
                snake_List,
                snake_block,
                special_food_appeared,
                (special_foodx, special_foody),
                speed_food_appeared,
                (speed_foodx, speed_foody),
            )

            length_of_snake += 1

        if x1 == special_foodx and y1 == special_foody:
            special_food_appeared = False
            length_of_snake += 2

        if x1 == speed_foodx and y1 == speed_foody:
            speed_food_appeared = False
            start_time = time.time()
            snake_speed += 10
            length_of_snake += 1

        if time.time() - start_time > speed_boost_duration:
            snake_speed = original_snake_speed

        clock.tick(snake_speed)

    pygame.quit()
    quit()


main_menu()
