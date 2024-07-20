import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')

# Board
board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Functions
def draw_lines():
    # Horizontal lines
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, BLACK, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
    # Vertical lines
    for i in range(1, BOARD_COLS):
        pygame.draw.line(screen, BLACK, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, RED, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, RED, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

def print_board():
    for row in board:
        print(" | ".join(row))
        print("---------")

def is_winner(player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            return True
    if all(board[i][i] == player for i in range(BOARD_ROWS)) or all(board[i][BOARD_COLS - 1 - i] == player for i in range(BOARD_ROWS)):
        return True
    return False

def is_board_full():
    return all(cell != ' ' for row in board for cell in row)

def get_empty_cells():
    return [(i, j) for i in range(BOARD_ROWS) for j in range(BOARD_COLS) if board[i][j] == ' ']

def evaluate():
    if is_winner('X'):
        return -1
    elif is_winner('O'):
        return 1
    elif is_board_full():
        return 0
    else:
        return None

def minimax(depth, maximizing_player):
    score = evaluate()
    if score is not None:
        return score

    if maximizing_player:
        max_eval = float('-inf')
        for i, j in get_empty_cells():
            board[i][j] = 'O'
            eval = minimax(depth + 1, False)
            board[i][j] = ' '
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i, j in get_empty_cells():
            board[i][j] = 'X'
            eval = minimax(depth + 1, True)
            board[i][j] = ' '
            min_eval = min(min_eval, eval)
        return min_eval

def find_best_move():
    best_val = float('-inf')
    best_move = None
    for i, j in get_empty_cells():
        board[i][j] = 'O'
        move_val = minimax(0, False)
        board[i][j] = ' '
        if move_val > best_val:
            best_move = (i, j)
            best_val = move_val
    return best_move

def draw_winner(winner):
    font = pygame.font.Font(None, 54)
    text = font.render(winner + " wins!", True, BLACK)
    rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, rect)
    pygame.display.update()
    pygame.time.delay(2000)

def play_game():
    player_turn = True  # True for 'X', False for 'O'
    game_over = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX, mouseY = event.pos
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                if player_turn and board[clicked_row][clicked_col] == ' ':
                    board[clicked_row][clicked_col] = 'X'
                    if is_winner('X'):
                        draw_winner('X')
                        game_over = True
                    player_turn = not player_turn

        if not player_turn and not game_over:
            best_move = find_best_move()
            board[best_move[0]][best_move[1]] = 'O'
            if is_winner('O'):
                draw_winner('O')
                game_over = True
            player_turn = not player_turn

        screen.fill(WHITE)
        draw_lines()
        draw_figures()
        pygame.display.update()

if __name__ == "__main__":
    play_game()
