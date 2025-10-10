import pygame
import sys
import random

# Add color options for selection
def show_main_menu():
    colors = [("Green", (0,255,0)), ("Blue", (0,0,255)), ("Red", (255,0,0)), ("Purple", (180,0,180)), ("Yellow", (255,255,0)), ("White", (255,255,255))]
    color_names = [c[0] for c in colors]
    selected_option = 0
    color_index = 0

    options = ["Start Game", "Snake Color", "Quit"]
    while True:
        screen.fill(BLACK)
        title_text = font.render('Snake Mini Game', True, GREEN)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 170))
        button_width, button_height = 270, 56
        spacing = 30
        base_y = HEIGHT // 2 - (len(options) * (button_height + spacing)) // 2 + 30

        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_rects = []

        for i, option in enumerate(options):
            button_x = WIDTH // 2 - button_width // 2
            button_y = base_y + i * (button_height + spacing)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            button_rects.append(button_rect)
            mouse_over = button_rect.collidepoint(mouse_x, mouse_y)
            draw_color = YELLOW if (i == selected_option or mouse_over) else GRAY
            border_thickness = 4 if (i == selected_option or mouse_over) else 2

            pygame.draw.rect(screen, draw_color, button_rect)
            pygame.draw.rect(screen, BLUE, button_rect, border_thickness)
            if option == "Snake Color":
                btn_text = font.render(f"{option}: {color_names[color_index]}", True, BLACK)
                # Show snake preview beside option
                preview_rect = pygame.Rect(button_x + button_width - 56, button_y + button_height//2 - 16, 32, 32)
                pygame.draw.rect(screen, colors[color_index][1], preview_rect)
            else:
                btn_text = font.render(option, True, BLACK)
            screen.blit(btn_text, (button_x + button_width // 2 - btn_text.get_width() // 2,
                                   button_y + button_height // 2 - btn_text.get_height() // 2))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                    if selected_option == 1:  # Snake Color
                        if event.key == pygame.K_RIGHT:
                            color_index = (color_index + 1) % len(colors)
                        else:
                            color_index = (color_index - 1) % len(colors)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if options[selected_option] == 'Start Game':
                        global SELECTED_SNAKE_COLOR
                        SELECTED_SNAKE_COLOR = colors[color_index][1]
                        return
                    elif options[selected_option] == 'Quit':
                        pygame.quit()
                        sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(event.pos):
                        if options[i] == "Start Game":
                            SELECTED_SNAKE_COLOR = colors[color_index][1]
                            return
                        elif options[i] == "Quit":
                            pygame.quit()
                            sys.exit()
                        elif options[i] == "Snake Color":
                            color_index = (color_index + 1) % len(colors)
        pygame.time.wait(20)

# Keep track of selected color globally (default GREEN)
SELECTED_SNAKE_COLOR = (0,255,0)

# (Removed older draw_snake; see improved version below)

# End Generation Here

# Constants
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
FPS = 30

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 155, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 24)

def random_position(exclude=None):
    while True:
        pos = [random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)]
        if not exclude or pos not in exclude:
            return pos

def draw_cell(pos, color):
    rect = pygame.Rect(pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)

def draw_snake(snake, current_direction):
    """Render snake with rounded segments, outline, head eyes, and subtle shadow."""
    border_radius = max(4, CELL_SIZE // 4)
    outline_color = (20, 60, 20)
    body_color = DARK_GREEN
    head_color = SELECTED_SNAKE_COLOR

    for segment_index, grid_pos in enumerate(snake):
        pixel_x = grid_pos[0] * CELL_SIZE
        pixel_y = grid_pos[1] * CELL_SIZE

        # Shadow
        shadow = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 70), shadow.get_rect(), border_radius=border_radius)
        screen.blit(shadow, (pixel_x + 2, pixel_y + 2))

        # Segment body
        segment_color = head_color if segment_index == 0 else body_color
        rect = pygame.Rect(pixel_x, pixel_y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, segment_color, rect, border_radius=border_radius)
        pygame.draw.rect(screen, outline_color, rect, width=2, border_radius=border_radius)

        # Head details: eyes
        if segment_index == 0:
            dx, dy = current_direction
            eye_radius = max(2, CELL_SIZE // 8)
            pupil_radius = max(1, eye_radius - 1)

            # Eye positions relative to head based on direction
            if dx == 1 and dy == 0:  # right
                eye1 = (pixel_x + CELL_SIZE - 6, pixel_y + 6)
                eye2 = (pixel_x + CELL_SIZE - 6, pixel_y + CELL_SIZE - 6)
                pupil_offset = (-1, 0)
            elif dx == -1 and dy == 0:  # left
                eye1 = (pixel_x + 6, pixel_y + 6)
                eye2 = (pixel_x + 6, pixel_y + CELL_SIZE - 6)
                pupil_offset = (1, 0)
            elif dx == 0 and dy == -1:  # up
                eye1 = (pixel_x + 6, pixel_y + 6)
                eye2 = (pixel_x + CELL_SIZE - 6, pixel_y + 6)
                pupil_offset = (0, 1)
            else:  # down
                eye1 = (pixel_x + 6, pixel_y + CELL_SIZE - 6)
                eye2 = (pixel_x + CELL_SIZE - 6, pixel_y + CELL_SIZE - 6)
                pupil_offset = (0, -1)

            pygame.draw.circle(screen, WHITE, eye1, eye_radius)
            pygame.draw.circle(screen, WHITE, eye2, eye_radius)
            pygame.draw.circle(screen, BLACK, (eye1[0] + pupil_offset[0], eye1[1] + pupil_offset[1]), pupil_radius)
            pygame.draw.circle(screen, BLACK, (eye2[0] + pupil_offset[0], eye2[1] + pupil_offset[1]), pupil_radius)

def draw_food(pos):
    """Render food as a small apple with stem and leaf."""
    center_x = pos[0] * CELL_SIZE + CELL_SIZE // 2
    center_y = pos[1] * CELL_SIZE + CELL_SIZE // 2
    apple_radius = max(6, CELL_SIZE // 2 - 2)

    # Apple body
    pygame.draw.circle(screen, (210, 30, 30), (center_x, center_y), apple_radius)
    pygame.draw.circle(screen, (120, 0, 0), (center_x, center_y), apple_radius, width=2)

    # Stem
    stem_height = max(4, CELL_SIZE // 3)
    stem_width = max(2, CELL_SIZE // 8)
    stem_rect = pygame.Rect(center_x - stem_width // 2, center_y - apple_radius - stem_height + 2, stem_width, stem_height)
    pygame.draw.rect(screen, (110, 70, 30), stem_rect, border_radius=2)

    # Leaf
    leaf_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    leaf_color = (30, 160, 50)
    leaf_rect = pygame.Rect(CELL_SIZE // 2, CELL_SIZE // 2 - apple_radius, apple_radius, apple_radius // 2 + 4)
    pygame.draw.ellipse(leaf_surface, leaf_color, leaf_rect)
    screen.blit(leaf_surface, (pos[0] * CELL_SIZE - CELL_SIZE // 2 + 2, pos[1] * CELL_SIZE - CELL_SIZE // 2 + 2))

def draw_grid():
    """Draw subtle grid background."""
    grid_color = (30, 30, 30)
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, grid_color, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, grid_color, (0, y), (WIDTH, y))

def show_game_over(score):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(220)
    overlay.fill(BLACK)
    screen.blit(overlay, (0,0))

    text1 = font.render(f"Game Over!", True, WHITE)
    text2 = font.render(f"Score: {score}", True, WHITE)
    text3 = font.render("Press R to Restart or Q to Quit", True, YELLOW)

    screen.blit(text1, (WIDTH//2 - text1.get_width()//2, HEIGHT//2 - 60))
    screen.blit(text2, (WIDTH//2 - text2.get_width()//2, HEIGHT//2 - 10))
    screen.blit(text3, (WIDTH//2 - text3.get_width()//2, HEIGHT//2 + 30))
    pygame.display.flip()

def main():
    # Make the initial snake height 3
    snake = [[GRID_WIDTH//2, GRID_HEIGHT//2 + i] for i in range(3)]
    direction = (0, -1)  # Up
    food = random_position(exclude=snake)
    score = 0
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

        new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]

        # Check collisions with walls or itself
        if (new_head in snake or
            new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            show_game_over(score)
            while True:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main()
                        return
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

        snake.insert(0, new_head)
        if new_head == food:
            score += 1
            food = random_position(exclude=snake)
        else:
            snake.pop()

        screen.fill(BLACK)
        draw_grid()
        draw_snake(snake, direction)
        draw_food(food)

        # Draw score
        score_txt = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_txt, (10, 10))
        pygame.display.flip()

if __name__ == "__main__":
    show_main_menu()
    main()


