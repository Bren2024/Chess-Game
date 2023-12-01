import pygame
import chess

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BOARD_SIZE = 8
SQUARE_SIZE = SCREEN_WIDTH // BOARD_SIZE

# Colors
LIGHT_COLOR = (240, 217, 181)
DARK_COLOR = (181, 136, 99)

# Load chess pieces images
pieces = {}
for piece in (["b"+i for i in chess.PIECE_SYMBOLS[1:]] + ["w"+i for i in chess.PIECE_SYMBOLS[1:]]):
    if (piece == None):
        continue
    img = pygame.image.load(f"images/{piece}.png")
    img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
    pieces[piece] = img

def get_piece_symbol(color, symbol):
    return f"{'w' if color else 'b'}{symbol.lower()}"

def draw_board(screen, board, dragging_piece=None):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            piece = board.piece_at(chess.square(col, BOARD_SIZE - 1 - row))
            if piece and (True if dragging_piece == None else dragging_piece['square'] != (7-row)*8+col):
                symbol = get_piece_symbol(piece.color, piece.symbol())
                screen.blit(pieces[symbol], (col * SQUARE_SIZE, row * SQUARE_SIZE))

    if dragging_piece:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(pieces[dragging_piece['piece']], (mouse_x - SQUARE_SIZE // 2, mouse_y - SQUARE_SIZE // 2))

def get_square_from_mouse(pos):
    col = pos[0] // SQUARE_SIZE
    row = BOARD_SIZE - 1 - pos[1] // SQUARE_SIZE
    return chess.square(col, row)

def play_game():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Chess Game")

    board = chess.Board()
    clock = pygame.time.Clock()

    start_square = None
    dragging_piece = None

    running = True
    while running and not board.is_game_over():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                start_square = get_square_from_mouse(pygame.mouse.get_pos())
                piece = board.piece_at(start_square)
                if piece:
                    dragging_piece = {"piece" : get_piece_symbol(piece.color, piece.symbol()), "square" : start_square}
            elif event.type == pygame.MOUSEBUTTONUP:
                end_square = get_square_from_mouse(pygame.mouse.get_pos())
                moves = [move for move in board.legal_moves if move.from_square == start_square and move.to_square == end_square]
                if moves:
                    move = moves[0]
                    board.push(move)
                dragging_piece = None

        screen.fill((255, 255, 255))
        draw_board(screen, board, dragging_piece)
        pygame.display.flip()
        clock.tick(60)

    print("Game over. Result: {}".format(board.result()))

if __name__ == "__main__":
    play_game()
    pygame.quit()
