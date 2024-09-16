import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UTT Champion")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)

# Paddle dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100

# Ball dimensions
BALL_SIZE = 20

# Game variables
paddle_speed = 5
ball_speed = 5
ai_speed = 4

# Fonts
font = pygame.font.Font(None, 74)
menu_font = pygame.font.Font(None, 50)
instructions_font = pygame.font.Font(None, 36)

# Load images with error handling
def load_image(filename):
    try:
        return pygame.image.load(filename)
    except pygame.error as e:
        print(f"Error loading image {filename}: {e}")
        return pygame.Surface((WIDTH, HEIGHT))  # Return a blank surface if image fails to load

# Load images
menu_background = load_image('utt.jpg')  # Replace with your background image
game_background = load_image('tt.jpg')  # Replace with your background image
logos = [load_image(f'logo {i}.png') for i in range(1, 9)]  # Ensure there are at least 8 logo images

# Button positions and sizes
button_width, button_height = 300, 50
single_button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2, button_width, button_height)
two_player_button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 60, button_width, button_height)
how_to_play_button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 120, button_width, button_height)
back_button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 150, button_width, button_height)

def draw_menu():
    """Draw the main menu."""
    screen.blit(menu_background, (0, 0))  # Draw the background image
    title_text = menu_font.render("Ultimate Table Tennis Champion", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))

    mouse_pos = pygame.mouse.get_pos()

    # Draw buttons and change color on hover
    for button_rect, text, color in [
        (single_button_rect, "Single Player", BUTTON_HOVER_COLOR),
        (two_player_button_rect, "Two Player", BUTTON_HOVER_COLOR),
        (how_to_play_button_rect, "How to Play", BUTTON_HOVER_COLOR)
    ]:
        pygame.draw.rect(screen, color if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR, button_rect)
        button_text = menu_font.render(text, True, BLACK)
        screen.blit(button_text, (button_rect.x + (button_width - button_text.get_width()) // 2, 
                                  button_rect.y + (button_height - button_text.get_height()) // 2))

    pygame.display.flip()

def check_menu_click(pos):
    """Check which menu button was clicked."""
    if single_button_rect.collidepoint(pos):
        return 'single'
    elif two_player_button_rect.collidepoint(pos):
        return 'two'
    elif how_to_play_button_rect.collidepoint(pos):
        return 'how_to_play'
    return None

def how_to_play():
    """Display the instructions for the game."""
    running = True
    while running:
        screen.fill(BLACK)  # Background color for instructions
        instructions = [
            "How to Play:",
            "1. For Single Player Game Controls-",
            "- Team A: W (To move Up), S (To move Down)",
            "2. For Two Player Game Controls-",
            "- Team A: W (To move Up), S (To move Down)",
            "- Team B: Arrow Up (To move Up), Arrow Down (To move Down)",
            "3. The game is played up to 11 points.",
            "4. Golden Point: the event that scores are level at 10-all",
            "then the 11th point will be a Golden Point",
            "and shall decide the winner."
        ]

        for i, line in enumerate(instructions):
            text = instructions_font.render(line, True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 100 + i * 40))

        # Create a smaller "Back to Menu" button on the extreme right
        small_button_width, small_button_height = 150, 40  # Smaller dimensions for the button
        back_button_right_rect = pygame.Rect(WIDTH - small_button_width - 30, HEIGHT - small_button_height - 30, small_button_width, small_button_height)  # Adjusted position for the extreme right

        pygame.draw.rect(screen, BUTTON_COLOR, back_button_right_rect)
        back_text = menu_font.render("Back", True, BLACK)
        screen.blit(back_text, (back_button_right_rect.x + (small_button_width - back_text.get_width()) // 2, 
                                back_button_right_rect.y + (small_button_height - back_text.get_height()) // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button_right_rect.collidepoint(mouse_pos):
                    return  # Return to menu

def select_teams():
    selected_teams = [None, None]  # [Team A, Team B]
    num_rows = 2
    num_cols = 4
    logo_size = WIDTH // num_cols  # Assuming the logos fit equally in the width divided by the number of columns

    # Calculate positions for team logos
    team_rects = [
        pygame.Rect(col * logo_size, row * (HEIGHT // num_rows), logo_size, logo_size)
        for row in range(num_rows)
        for col in range(num_cols)
    ]
    
    team_names = [f"Team {i+1}" for i in range(len(logos))]  # Adjusted to match the number of logos

    # Confirm button with smaller size positioned at the bottom right
    confirm_rect = pygame.Rect(WIDTH - 160, HEIGHT - 70, 150, 40)  # Reduced size: 150x40 pixels and positioned at the bottom right

    # Back button rect positioned at the bottom left corner
    back_button_rect = pygame.Rect(10, HEIGHT - 70, 100, 40)  # "Back" button at the extreme bottom left

    # Determine the position for the heading box
    heading_box_y = (HEIGHT // num_rows) + logo_size + 30  # Below the team logos grid with some padding

    while True:
        screen.fill(BLACK)

        # Draw the "Back" button with a solid fill
        pygame.draw.rect(screen, BUTTON_COLOR, back_button_rect)  # Solid fill for the back button
        back_text = menu_font.render("Back", True, BLACK)
        screen.blit(back_text, (back_button_rect.x + (back_button_rect.width - back_text.get_width()) // 2, 
                                back_button_rect.y + (back_button_rect.height - back_text.get_height()) // 2))

        # Draw the team logos and their outlines
        for i, logo in enumerate(logos):
            # Scale the logo to fit within the calculated size
            logo = pygame.transform.scale(logo, (logo_size, logo_size))
            # Highlight selected logos
            outline_color = BUTTON_COLOR if i not in selected_teams else (0, 255, 0)  # Green for selected
            pygame.draw.rect(screen, outline_color, team_rects[i], 4)  # Thicker outline for selected logos
            screen.blit(logo, team_rects[i])

            # Draw team names below the logos
            team_text = menu_font.render(team_names[i], True, WHITE)
            screen.blit(team_text, (team_rects[i].x + (logo_size - team_text.get_width()) // 2, 
                                    team_rects[i].y + logo_size + 10))

        # Determine heading based on which team is being selected
        if selected_teams[0] is None:
            heading_text = "Select Your Team"
        else:
            heading_text = "Select Opponent's Team"

        # Render heading text and box
        heading = menu_font.render(heading_text, True, WHITE)
        heading_box = pygame.Rect(WIDTH // 2 - heading.get_width() // 2 - 10, heading_box_y, heading.get_width() + 20, heading.get_height() + 10)
        pygame.draw.rect(screen, BUTTON_COLOR, heading_box)  # Draw the box around the heading
        screen.blit(heading, (heading_box.x + 10, heading_box.y + 5))  # Center the text in the box

        # Check if both teams are selected
        if None not in selected_teams:
            # Draw the confirmation button at the bottom of the window
            pygame.draw.rect(screen, BUTTON_COLOR, confirm_rect)
            confirm_text = menu_font.render("Confirm", True, BLACK)
            screen.blit(confirm_text, (confirm_rect.x + (confirm_rect.width - confirm_text.get_width()) // 2,
                                       confirm_rect.y + (confirm_rect.height - confirm_text.get_height()) // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check if the "Back" button was clicked
                if back_button_rect.collidepoint(mouse_pos):
                    return [None, None]  # Return [None, None] to indicate returning to the main menu

                for i, team_rect in enumerate(team_rects):
                    if team_rect.collidepoint(mouse_pos):
                        if selected_teams[0] == i:
                            selected_teams[0] = None  # Deselect Team A if clicked again
                        elif selected_teams[1] == i:
                            selected_teams[1] = None  # Deselect Team B if clicked again
                        elif selected_teams[0] is None:
                            selected_teams[0] = i  # Select team for Team A
                        elif selected_teams[1] is None:
                            selected_teams[1] = i  # Select team for Team B
                        break  # Exit the inner loop

                # Check if both teams are selected and confirm button is clicked
                if None not in selected_teams and confirm_rect.collidepoint(mouse_pos):
                    return selected_teams  # Return selected teams

        pygame.time.Clock().tick(30)  # Use Clock to manage frame rate

def main_game(team_logos, single_player=True):
    # Ensure team selection is valid
    if team_logos is None or None in team_logos:
        print("No teams selected. Returning to main menu.")
        return  # Handle the "Back" button or invalid selection

    # Now, we can safely access team logos
    screen.blit(pygame.transform.scale(logos[team_logos[0]], (50, 50)), (10, 10))  # Top-left corner
    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
    ball_speed_x, ball_speed_y = ball_speed * random.choice((1, -1)), ball_speed * random.choice((1, -1))

    left_paddle_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    right_paddle_y = HEIGHT // 2 - PADDLE_HEIGHT // 2

    left_score, right_score = 0, 0
    left_consecutive_points, right_consecutive_points = 0, 0

    win_score = 11

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button_rect.collidepoint(mouse_pos):
                    return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle_y > 0:
            left_paddle_y -= paddle_speed
        if keys[pygame.K_s] and left_paddle_y < HEIGHT - PADDLE_HEIGHT:
            left_paddle_y += paddle_speed
        if single_player:
            if right_paddle_y + PADDLE_HEIGHT // 2 < ball_y:
                right_paddle_y += ai_speed
            elif right_paddle_y + PADDLE_HEIGHT // 2 > ball_y:
                right_paddle_y -= ai_speed
            right_paddle_y = max(0, min(HEIGHT - PADDLE_HEIGHT, right_paddle_y))
        else:
            if keys[pygame.K_UP] and right_paddle_y > 0:
                right_paddle_y -= paddle_speed
            if keys[pygame.K_DOWN] and right_paddle_y < HEIGHT - PADDLE_HEIGHT:
                right_paddle_y += paddle_speed

        ball_x += ball_speed_x
        ball_y += ball_speed_y

        if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
            ball_speed_y *= -1

        if (ball_x <= PADDLE_WIDTH and left_paddle_y < ball_y < left_paddle_y + PADDLE_HEIGHT) or \
           (ball_x >= WIDTH - PADDLE_WIDTH - BALL_SIZE and right_paddle_y < ball_y < right_paddle_y + PADDLE_HEIGHT):
            ball_speed_x *= -1

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

        if left_score >= win_score or right_score >= win_score:
            if left_score >= win_score and right_score >= win_score:
                if left_consecutive_points >= 2:
                    winner = "left"
                elif right_consecutive_points >= 2:
                    winner = "right"
                else:
                    winner = None
            else:
                if left_score >= win_score:
                    winner = "left"
                if right_score >= win_score:
                    winner = "right"

            if winner:
                running = False

        screen.blit(game_background, (0, 0))
        pygame.draw.rect(screen, WHITE, (0, left_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(screen, WHITE, (WIDTH - PADDLE_WIDTH, right_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        left_text = font.render(str(left_score), True, WHITE)
        right_text = font.render(str(right_score), True, WHITE)
        screen.blit(left_text, (WIDTH // 4, 10))
        screen.blit(right_text, (WIDTH * 3 // 4, 10))

        # Draw team logos in the top corners
        screen.blit(pygame.transform.scale(logos[team_logos[0]], (50, 50)), (10, 10))  # Top-left corner
        screen.blit(pygame.transform.scale(logos[team_logos[1]], (50, 50)), (WIDTH - 60, 10))  # Top-right corner

        pygame.display.flip()
        clock.tick(60)

    # Game over screen
    screen.blit(game_background, (0, 0))
    game_over_text = font.render("Game Over!", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))

    if winner == "left":
        winner_logo = pygame.transform.scale(logos[team_logos[0]], (100, 100))
        screen.blit(winner_logo, (WIDTH // 2 - winner_logo.get_width() // 2, HEIGHT // 2 - 30))
    elif winner == "right":
        winner_logo = pygame.transform.scale(logos[team_logos[1]], (100, 100))
        screen.blit(winner_logo, (WIDTH // 2 - winner_logo.get_width() // 2, HEIGHT // 2 - 30))
    else:
        result_text = font.render("Match Drawn!", True, WHITE)
        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2 - 30))

    # Back to Menu button
    small_button_width, small_button_height = 150, 40
    back_button_right_rect = pygame.Rect(WIDTH - small_button_width - 30, HEIGHT - small_button_height - 30, small_button_width, small_button_height)

    pygame.draw.rect(screen, BUTTON_COLOR, back_button_right_rect)
    back_text = menu_font.render("Back", True, BLACK)
    screen.blit(back_text, (back_button_right_rect.x + (small_button_width - back_text.get_width()) // 2, back_button_right_rect.y + (small_button_height - back_text.get_height()) // 2))

    pygame.display.flip()

    pygame.time.wait(2000)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button_right_rect.collidepoint(mouse_pos):
                    return

# Main menu
game_mode = None
while True:
    draw_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            game_mode = check_menu_click(mouse_pos)

    if game_mode:
        if game_mode == 'single':
            team_logos = select_teams()
            main_game(team_logos, single_player=True)
        elif game_mode == 'two':
            team_logos = select_teams()
            main_game(team_logos, single_player=False)
        elif game_mode == 'how_to_play':
            how_to_play()
        game_mode = None  # Reset the game mode to return to the menu