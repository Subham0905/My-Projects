import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Table Tennis Game - First to 11 Points with Draw Condition")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100

# Ball dimensions
BALL_SIZE = 20

# Game variables
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_speed_x, ball_speed_y = 5 * random.choice((1, -1)), 5 * random.choice((1, -1))
paddle_speed = 5

left_paddle_y, right_paddle_y = HEIGHT // 2 - PADDLE_HEIGHT // 2, HEIGHT // 2 - PADDLE_HEIGHT // 2

# Scoring
left_score, right_score = 0, 0
left_consecutive_points, right_consecutive_points = 0, 0
font = pygame.font.Font(None, 74)

# Winning score
win_score = 11

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle_y > 0:
        left_paddle_y -= paddle_speed
    if keys[pygame.K_s] and left_paddle_y < HEIGHT - PADDLE_HEIGHT:
        left_paddle_y += paddle_speed
    if keys[pygame.K_UP] and right_paddle_y > 0:
        right_paddle_y -= paddle_speed
    if keys[pygame.K_DOWN] and right_paddle_y < HEIGHT - PADDLE_HEIGHT:
        right_paddle_y += paddle_speed

    # Ball movement
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Ball collision with walls
    if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
        ball_speed_y *= -1

    # Ball collision with paddles
    if (ball_x <= PADDLE_WIDTH and left_paddle_y < ball_y < left_paddle_y + PADDLE_HEIGHT) or \
       (ball_x >= WIDTH - PADDLE_WIDTH - BALL_SIZE and right_paddle_y < ball_y < right_paddle_y + PADDLE_HEIGHT):
        ball_speed_x *= -1

    # Score update
    if ball_x <= 0:
        right_score += 1
        left_consecutive_points = 0
        right_consecutive_points += 1
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_speed_x *= random.choice((1, -1))
        ball_speed_y *= random.choice((1, -1))

    if ball_x >= WIDTH - BALL_SIZE:
        left_score += 1
        right_consecutive_points = 0
        left_consecutive_points += 1
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_speed_x *= random.choice((1, -1))
        ball_speed_y *= random.choice((1, -1))

    # Check for winning condition
    if left_score >= win_score or right_score >= win_score:
        if left_score >= win_score and right_score >= win_score:
            if left_consecutive_points >= 2:
                winner = "Team A"
            elif right_consecutive_points >= 2:
                winner = "Team B"
            else:
                winner = None
        else:
            if left_score >= win_score:
                winner = "Team A"
            if right_score >= win_score:
                winner = "Team B"

        if winner:
            running = False

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (0, left_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (WIDTH - PADDLE_WIDTH, right_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Display scores
    left_text = font.render(str(left_score), True, WHITE)
    right_text = font.render(str(right_score), True, WHITE)
    screen.blit(left_text, (WIDTH // 4, 10))
    screen.blit(right_text, (WIDTH * 3 // 4, 10))

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Display final scores on screen
screen.fill(BLACK)
game_over_text = font.render("Game Over!", True, WHITE)
if winner:
    result_text = font.render(f"{winner} Wins!", True, WHITE)
else:
    result_text = font.render("Match Drawn!", True, WHITE)

screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2 + 10))

pygame.display.flip()

# Wait for a few seconds before quitting
pygame.time.wait(3000)
pygame.quit()