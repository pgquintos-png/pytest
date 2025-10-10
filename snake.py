import pygame
import sys
import random

# Initialize pygame
pygame.init()
def draw_main_menu():
    screen.fill(BLACK)
    title_text = font.render('Snake Mini Game', True, GREEN)
    start_text = button_font.render('Start Game', True, BLACK)

    # Draw Title
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 100))

    # Draw Start Button
    button_width, button_height = 200, 50
    button_x = WIDTH // 2 - button_width // 2
    button_y = HEIGHT // 2
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, GRAY, button_rect)
    pygame.draw.rect(screen, BLUE, button_rect, 3)
    screen.blit(start_text, (button_x + button_width//2 - start_text.get_width()//2, button_y + button_height//2 - start_text.get_height()//2))

    pygame.display.flip()
    return button_rect

def main_menu_loop():
    while True:
        start_button_rect = draw_main_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return  # Exit menu to start game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return  # Allow keyboard start

        pygame.time.wait(20)

# Set up display
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
INITIAL_SNAKE_LENGTH = 10  # Increased by 2 (original: 3)
MAIN_MENU = True
GRID_HEIGHT = HEIGHT // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Mini Game')

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 155, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)  # No longer used for extra food

def random_position(exclude=None):
    while True:
        pos = [random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)]
        if not exclude or pos not in exclude:
            return pos

def draw_cell(pos, color):
    rect = pygame.Rect(pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)

clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 24)
button_font = pygame.font.SysFont('Arial', 22)

def draw_restart_button():
    button_width, button_height = 140, 40
    button_x = WIDTH // 2 - button_width // 2
    button_y = HEIGHT // 2 + 40
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, GRAY, button_rect)
    pygame.draw.rect(screen, BLUE, button_rect, 2)
    text = button_font.render('Restart', True, BLACK)
    screen.blit(text, (button_x + button_width//2 - text.get_width()//2, button_y + button_height//2 - text.get_height()//2))
    return button_rect

def game_over_screen(score, high_score):
    screen.fill(BLACK)
    text = font.render('Game Over!', True, RED)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2 - 60))
    score_text = font.render('Score: {}'.format(score), True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - score_text.get_height()//2 - 20))
    hs_text = font.render('High Score: {}'.format(high_score), True, YELLOW)
    screen.blit(hs_text, (WIDTH//2 - hs_text.get_width()//2, HEIGHT//2 - hs_text.get_height()//2 + 20))
    button_rect = draw_restart_button()
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_r:
                    waiting = False
        clock.tick(20)

def spawn_extra_foods(snake, food, stage):
    # Helper to spawn all extra foods at once, not one at a time
    extra_foods = []
    exclude = list(snake)
    if food is not None:
        exclude.append(food)
    for _ in range(stage):
        ef = random_position(exclude=exclude + extra_foods)
        while ef in snake or ef in extra_foods or (food is not None and ef == food):
            ef = random_position(exclude=exclude + extra_foods)
        extra_foods.append(ef)
    return extra_foods

def reset_game():
    snake = [[GRID_WIDTH // 2, GRID_HEIGHT // 2]]
    direction = [0, -1]
    food = random_position(exclude=snake)
    score = 0
    stage = 1
    food_eaten_this_stage = 0
    # Do not spawn extra foods at the start; only after food is eaten
    extra_foods = []
    extra_food_ready = False
    return snake, direction, food, score, stage, food_eaten_this_stage, extra_foods, extra_food_ready

def draw_pause_screen():
    pause_text = font.render('Paused', True, WHITE)
    screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2 - pause_text.get_height()//2))
    pygame.display.flip()

# Main game loop
snake, direction, food, score, stage, food_eaten_this_stage, extra_foods, extra_food_ready = reset_game()
running = True
paused = False

# Add high score tracking
high_score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Pause/unpause with space bar
            if event.key == pygame.K_SPACE:
                paused = not paused
            # Move using arrow keys or WASD (only if not paused)
            if not paused:
                # Arrow keys
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != [0, 1]:
                    direction = [0, -1]
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != [0, -1]:
                    direction = [0, 1]
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != [1, 0]:
                    direction = [-1, 0]
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != [-1, 0]:
                    direction = [1, 0]

    if paused:
        # Draw pause screen over current game state
        screen.fill(BLACK)
        for segment in snake:
            draw_cell(segment, GREEN)
        if food is not None:
            draw_cell(food, RED)
        for ef in extra_foods:
            draw_cell(ef, RED)  # Extra food is now red
        score_text = font.render('Score: {}'.format(score), True, WHITE)
        screen.blit(score_text, (5, 5))
        hs_text = font.render('High Score: {}'.format(high_score), True, YELLOW)
        screen.blit(hs_text, (5, 35))
        stage_text = font.render('Stage: {}'.format(stage), True, BLUE)
        screen.blit(stage_text, (5, 65))
        draw_pause_screen()
        clock.tick(15)
        continue

    # If no food, spawn main food
    if food is None:
        while True:
            nf = random_position(exclude=snake + extra_foods)
            if nf not in snake and nf not in extra_foods:
                food = nf
                break

    # Only spawn extra foods if main food is not present (i.e., after food is eaten)
    if not extra_foods and food is None:
        extra_foods = spawn_extra_foods(snake, food, stage)

    # Move snake
    new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]

    # Check collisions
    if (new_head in snake or
        new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
        new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
        if score > high_score:
            high_score = score
        # Show the game over screen with the score that was just reached
        snake, direction, food, score, stage, food_eaten_this_stage, extra_foods, extra_food_ready = reset_game()
        game_over_screen(score, high_score)
        paused = False
        continue

    snake.insert(0, new_head)

    # Check if food eaten
    ate_food = False
    if food is not None and new_head == food:
        score += 1
        food_eaten_this_stage += 1
        ate_food = True
        food = None  # Remove main food from the board
        # Level up every 10 food
        if food_eaten_this_stage >= 10:
            stage += 1
            food_eaten_this_stage = 0
            # All extra foods for the new stage will be spawned at once in the next loop

    # Check if extra food eaten
    extra_food_eaten = False
    for ef in extra_foods:
        if new_head == ef:
            score += 2  # Extra food gives more points
            extra_foods.remove(ef)
            extra_food_eaten = True
            break
    if not ate_food and not extra_food_eaten:
        snake.pop()

    # Draw everything
    screen.fill(BLACK)
    for segment in snake:
        draw_cell(segment, GREEN)
    if food is not None:
        draw_cell(food, RED)
    for ef in extra_foods:
        draw_cell(ef, RED)  # Extra food is now red

    # Draw score, high score, and stage
    score_text = font.render('Score: {}'.format(score), True, WHITE)
    screen.blit(score_text, (5, 5))
    hs_text = font.render('High Score: {}'.format(high_score), True, YELLOW)
    screen.blit(hs_text, (5, 35))
    stage_text = font.render('Stage: {}'.format(stage), True, BLUE)
    screen.blit(stage_text, (5, 65))
    # (Removed extra food display here)

    pygame.display.flip()
    clock.tick(15)
