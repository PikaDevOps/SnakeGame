import pygame
import random
import time

# Initialize pygame
pygame.init()

# Game window size
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 15  # Snake and food block size

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 100, 0)
RED = (213, 50, 80)
BLUE = (50, 153, 213)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
LIGHT_BROWN = (160, 82, 45)
YELLOW = (255, 223, 0)

# Create game window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Set game icon
icon = pygame.image.load("game_controller_icon.png")  # Replace with your icon file
pygame.display.set_icon(icon)

# Snake default position and movement
snake_pos = [100, 50]
snake_body = [[100, 50], [85, 50], [70, 50]]
direction = 'RIGHT'
change_to = direction

# Food position
food_pos = [random.randrange(1, (WIDTH//BLOCK_SIZE)) * BLOCK_SIZE, 
            random.randrange(1, (HEIGHT//BLOCK_SIZE)) * BLOCK_SIZE]
food_spawn = True

# Game variables
score = 0
speed = 12  # Snake speed
clock = pygame.time.Clock()
pause = False

# High score
high_score = 0
try:
    with open("highscores.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    high_score = 0

# Font for score
font = pygame.font.SysFont("bahnschrift", 20)

def show_score():
    score_text = font.render(f"Score: {score}  High Score: {high_score}", True, WHITE)
    win.blit(score_text, [10, 10])

# Show instructions
start_time = None
def show_instructions():
    global start_time
    if start_time is None:
        start_time = time.time()

    if time.time() - start_time < 10:  # Display for 10 seconds
        instructions = font.render("Arrow keys to move, P - Pause", True, WHITE)
        pygame.draw.rect(win, BROWN, pygame.Rect(WIDTH - 300, 5, 290, 30), border_radius=5)  # Brown border
        pygame.draw.rect(win, LIGHT_BROWN, pygame.Rect(WIDTH - 295, 10, 280, 20), border_radius=5)  # Lighter inside
        win.blit(instructions, [WIDTH - 290, 10])

# Display game over screen
def game_over():
    global high_score
    win.fill(BLACK)
    game_over_text = font.render("Game Over! Press R to Restart or Q to Quit.", True, RED)
    final_score = font.render(f"Your Score: {score}", True, YELLOW)
    win.blit(game_over_text, [WIDTH // 2 - 200, HEIGHT // 2 - 30])
    win.blit(final_score, [WIDTH // 2 - 80, HEIGHT // 2 + 10])
    pygame.display.update()

    # Update high score
    if score > high_score:
        high_score = score
        with open("highscores.txt", "w") as file:
            file.write(str(high_score))

    # Wait for user action
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Main game loop
def game_loop():
    global direction, change_to, food_spawn, score, snake_pos, snake_body, food_pos, start_time, pause
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'
                elif event.key == pygame.K_p:
                    pause = not pause

        if pause:
            continue

        # Change direction
        direction = change_to
        if direction == 'UP':
            snake_pos[1] -= BLOCK_SIZE
        elif direction == 'DOWN':
            snake_pos[1] += BLOCK_SIZE
        elif direction == 'LEFT':
            snake_pos[0] -= BLOCK_SIZE
        elif direction == 'RIGHT':
            snake_pos[0] += BLOCK_SIZE

        # Allow snake to move through walls
        if snake_pos[0] < 0:
            snake_pos[0] = WIDTH - BLOCK_SIZE
        elif snake_pos[0] >= WIDTH:
            snake_pos[0] = 0
        if snake_pos[1] < 0:
            snake_pos[1] = HEIGHT - BLOCK_SIZE
        elif snake_pos[1] >= HEIGHT:
            snake_pos[1] = 0

        # Snake growing
        snake_body.insert(0, list(snake_pos))
        if abs(snake_pos[0] - food_pos[0]) < BLOCK_SIZE and abs(snake_pos[1] - food_pos[1]) < BLOCK_SIZE:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()
        
        if not food_spawn:
            food_pos = [random.randrange(1, (WIDTH//BLOCK_SIZE)) * BLOCK_SIZE, 
                        random.randrange(1, (HEIGHT//BLOCK_SIZE)) * BLOCK_SIZE]
        food_spawn = True

        # Check for collision with itself
        for block in snake_body[1:]:
            if snake_pos == block:
                game_over()
                running = False

        # Draw elements
        win.fill(BLUE)
        for i, block in enumerate(snake_body):
            color = DARK_GREEN if i == 0 else GREEN  # Make head darker
            pygame.draw.rect(win, color, pygame.Rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE), border_radius=5)
        pygame.draw.rect(win, RED, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE), border_radius=5)

        # Display score and instructions
        show_score()
        show_instructions()
        
        pygame.display.update()
        clock.tick(speed)

    pygame.quit()
    quit()

def main():
    global score, snake_pos, snake_body, direction, change_to, food_pos, food_spawn, start_time
    score = 0
    snake_pos = [100, 50]
    snake_body = [[100, 50], [85, 50], [70, 50]]
    direction = 'RIGHT'
    change_to = direction
    food_pos = [random.randrange(1, (WIDTH//BLOCK_SIZE)) * BLOCK_SIZE, 
                random.randrange(1, (HEIGHT//BLOCK_SIZE)) * BLOCK_SIZE]
    food_spawn = True
    start_time = None
    game_loop()

# Run the game
if __name__ == "__main__":
    main()
