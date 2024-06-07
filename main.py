import pygame
from pygame.locals import *
import sys
from logic import *
from treelogic import *

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Pygame Image Display")

# Load the image
image = pygame.image.load('board.png')

def draw_button(screen, color, x, y, width, height):
    pygame.draw.rect(screen, color, (x, y, width, height))


# player status
current_player = 1

# Define the button properties
button_color = (0, 0, 0)  # black
button_width = 45
button_height = 45
marginW = 29
marginH = 29   # size of the space between buttons
btnW = 257
btnH = 58

game_board = []
for i in range(6):
    game_board.append([0, 0, 0, 0, 0, 0, 0])

# Restart the game
def restart_game():
    board = []
    for i in range(6):
        board.append([0, 0, 0, 0, 0, 0, 0])
    return board, 0


# Load the images and set the size
CHIP_SIZE = 75

EMPTY = pygame.transform.scale(pygame.image.load('empty.png'), (CHIP_SIZE, CHIP_SIZE))
PLAYER1 = pygame.transform.scale(pygame.image.load('red.png'), (CHIP_SIZE, CHIP_SIZE))
PLAYER2 = pygame.transform.scale(pygame.image.load('black.png'), (CHIP_SIZE, CHIP_SIZE))
chipMarginW = 28.7
chipMarginH = 29   # size of the space between buttons
chipW = 242.5
chipH = 42

def draw_board(board):
    for i in range(6):
        for j in range(7):
            # Determine the image of the chip
            if board[i][j] == 0:
                image = EMPTY
            elif board[i][j] == 1:
                image = PLAYER1
            else:
                image = PLAYER2

            # Draw the chip
            screen.blit(image, (chipW + j * (button_width + chipMarginW), chipH + i * (button_height + chipMarginH)))

# colours, font, and coordinates for text
X = 400
Y = 400

    
def draw_text(text, x, y, size):
    font = pygame.font.Font('freesansbold.ttf', size)
    # text object
    text_surface = font.render(text, True, (255,255,255))
    
    # text box object
    textRect = text_surface.get_rect()
    
    # center of text box
    textRect.center = (x // 2, y // 2)

    # Draw the text onto the surface and return it
    screen.blit(text_surface, textRect)
    return text_surface


# Main loop
running = True
waiting_for_player1 = False
waiting_for_player2 = True
menu = True
player_win = 0
player1wins = 0
player2wins = 0
draws = 0
AI = False

# menu button props
start_button_color = (200, 0, 0)  # red
start_button_x = 550
start_button_y = 400
start_button_width = 200
start_button_height = 75

# menu button props
start2_button_color = (0, 0, 200)  # blue
start2_button_x = 245
start2_button_y = 400
start2_button_width = 210
start2_button_height = 75


while running:
    if menu:
        # Fill the screen with a color (optional)
        game_board, player_win = restart_game()
        current_player = 1
        screen.fill((30, 30, 30))
        draw_text('Connect 4 Demo', 1000, 500, 90)
        draw_text('By Christian Duarte', 1000, 700, 40)
        draw_button(screen, start_button_color, start_button_x, start_button_y, start_button_width, start_button_height)
        draw_text('Vs. CPU', 1300, 880, 40)
        draw_button(screen, start2_button_color, start2_button_x, start2_button_y, start2_button_width, start2_button_height)
        draw_text('Vs. Player', 700, 880, 40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_x < mouse_pos[0] < start_button_x + start_button_width and start_button_y < mouse_pos[1] < start_button_y + start_button_height:
                    menu = False
                    waiting_for_player1 = False
                    waiting_for_player2 = True
                    AI = True
                elif start2_button_x < mouse_pos[0] < start2_button_x + start2_button_width and start2_button_y < mouse_pos[1] < start2_button_y + start2_button_height:
                    menu = False
                    AI = False
    else:
        if AI:
            # handle the gameplay
            if waiting_for_player1:
                tree = GameTree(game_board, 1)
                move = tree.get_move()
                if drop_piece(game_board, current_player, move):
                    current_player = 1
                    waiting_for_player1 = False
                    waiting_for_player2 = True
                if check_winner(game_board) != 0:
                    player2wins += 1
                    player_win = 2
                                        
            elif waiting_for_player2:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            if 31 < mouse_pos[0] < 31 + 40 and 29 < mouse_pos[1] < 29 + 40:
                                pygame.quit()
                                sys.exit()
                            elif 30 < mouse_pos[0] < 30 + 115 and 75 < mouse_pos[1] < 75 + 44:
                                waiting_for_player1 = False
                                menu = True
                                
                            for i in range(6):
                                for j in range(7):
                                    button_x = btnW + j * (button_width + marginW)
                                    button_y = btnH + i * (button_height + marginH)
                                    if button_x < mouse_pos[0] < button_x + button_width and button_y < mouse_pos[1] < button_y + button_height:
                                        if drop_piece(game_board, current_player, j):
                                            current_player = 2
                                            waiting_for_player1 = True
                                            waiting_for_player2 = False
                                        if check_winner(game_board) != 0:
                                            player1wins += 1
                                            player_win = 1
                                        
        else:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if 31 < mouse_pos[0] < 31 + 40 and 29 < mouse_pos[1] < 29 + 40:
                            pygame.quit()
                            sys.exit()
                        elif 30 < mouse_pos[0] < 30 + 115 and 75 < mouse_pos[1] < 75 + 44:
                            menu = True
                                
                        for i in range(6):
                            for j in range(7):
                                button_x = btnW + j * (button_width + marginW)
                                button_y = btnH + i * (button_height + marginH)
                                if button_x < mouse_pos[0] < button_x + button_width and button_y < mouse_pos[1] < button_y + button_height:
                                    if drop_piece(game_board, current_player, j):
                                        current_player = 1 if current_player == 2 else 2
                                        waiting_for_player1 = True
                                        waiting_for_player2 = False
                                    if check_winner(game_board) != 0 and current_player == 1:
                                        player1wins += 1
                                        player_win = current_player
                                    elif check_winner(game_board) != 0 and current_player == 2:
                                        player2wins += 1
                                        player_win = current_player
                                    
        # Fill the screen with a color (optional)
        screen.fill((30, 30, 30))

        # Draw the buttons
        for i in range(6):  # Assuming a 6x7 Connect 4 board
            for j in range(7):
                draw_button(screen, button_color, btnW + j * (button_width + marginW), btnH + i * (button_height + marginH), button_width, button_height)

        # Draw the image onto the screen
        screen.blit(image, (160, 25))

        #draw the board
        draw_board(game_board)
        draw_text('P1: ' + str(player1wins), 1800, 100, 50)
        draw_text('P2: ' + str(player2wins), 1800, 200, 50)
        draw_button(screen, start_button_color, 31, 29, 40, 40)
        draw_text('X', 100, 100, 40)
        draw_button(screen, (0, 0, 200), 30, 75, 115, 44)
        draw_text("Player " + str(current_player) + "'s turn.", 1000, 1100, 40)
        if player_win == 1 or player_win == 2:
            draw_text('Back', 170, 200, 40)
            waiting_for_player1 = False
            waiting_for_player2 = False
            colour = (255, 0, 0)
            if player_win == 2:
                colour = (0, 0, 0)
            pygame.draw.rect(screen, colour, (175, 190, 650, 120))
            draw_text('Player ' + str(player_win) + ' wins!', 1000, 500, 90)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if 31 < mouse_pos[0] < 31 + 40 and 29 < mouse_pos[1] < 29 + 40:
                        pygame.quit()
                        sys.exit()
                    elif 30 < mouse_pos[0] < 30 + 115 and 75 < mouse_pos[1] < 75 + 44:
                        waiting_for_player1 = False
                        menu = True
        else:
            draw_text('Menu', 170, 200, 40)
        
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()