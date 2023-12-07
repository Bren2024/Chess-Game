import pygame
import chess

class Board:
    # Constants
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    BOARD_SIZE = 8
    SQUARE_SIZE = SCREEN_WIDTH // BOARD_SIZE

    # Colors
    LIGHT_COLOR = (240, 217, 181)
    DARK_COLOR = (181, 136, 99)

    def __init__(self):
        self.board = chess.Board()

        # Load chess pieces images
        self.pieces = {}
        for piece in (["b"+i for i in chess.PIECE_SYMBOLS[1:]] + ["w"+i for i in chess.PIECE_SYMBOLS[1:]]):
            if (piece == None):
                continue
            img = pygame.image.load(f"images/{piece}.png")
            img = pygame.transform.scale(img, (self.SQUARE_SIZE, self.SQUARE_SIZE))
            self.pieces[piece] = img

    def get_piece_symbol(self, color, symbol):
        return f"{'w' if color else 'b'}{symbol.lower()}"

    def draw(self, screen, dragging_piece):
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                color = self.LIGHT_COLOR if (row + col) % 2 == 0 else self.DARK_COLOR
                pygame.draw.rect(screen, color, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

                piece = self.board.piece_at(chess.square(col, self.BOARD_SIZE - 1 - row))
                if piece and (True if dragging_piece is None else dragging_piece['square'] != (7-row)*8+col):
                    symbol = self.get_piece_symbol(piece.color, piece.symbol())
                    screen.blit(self.pieces[symbol], (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE))

        if dragging_piece:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            screen.blit(self.pieces[dragging_piece['piece']], (mouse_x - self.SQUARE_SIZE // 2, mouse_y - self.SQUARE_SIZE // 2))

    def get_square_from_mouse(self, pos):
        col = pos[0] // self.SQUARE_SIZE
        row = self.BOARD_SIZE - 1 - pos[1] // self.SQUARE_SIZE
        return chess.square(col, row)
    
    def is_game_over(self):
        return self.board.is_game_over()
    
    def push_move(self, move):
        self.board.push(move)

    def get_piece_at(self, square):
        return self.board.piece_at(square)
    
    def get_moves(self, start_square, end_square):
        return [move for move in self.board.legal_moves if move.from_square == start_square and move.to_square == end_square]

    def print_result(self):
        print("Game over. Result: {}".format(self.board.result()))

class Chess:
    def __init__(self):
        self.board = Board()
        self.dragging_piece = None
    
    def play_two_player(self):
        # Initialize Pygame
        pygame.init()
        
        screen = pygame.display.set_mode((Board.SCREEN_WIDTH, Board.SCREEN_HEIGHT))
        pygame.display.set_caption("Chess Game")

        clock = pygame.time.Clock()

        running = True
        while running and not self.board.is_game_over():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    start_square = self.board.get_square_from_mouse(pygame.mouse.get_pos())
                    piece = self.board.get_piece_at(start_square)
                    if piece:
                        self.dragging_piece = {"piece" : self.board.get_piece_symbol(piece.color, piece.symbol()), "square" : start_square}
                elif event.type == pygame.MOUSEBUTTONUP:
                    end_square = self.board.get_square_from_mouse(pygame.mouse.get_pos())
                    moves = self.board.get_moves(start_square, end_square)
                    if moves:
                        move = moves[0]
                        self.board.push_move(move)
                    self.dragging_piece = None

            screen.fill((255, 255, 255))
            self.board.draw(screen, self.dragging_piece)
            pygame.display.flip()
            clock.tick(60)

        self.board.print_result()


if __name__ == "__main__":
    chessGame = Chess()
    chessGame.play_two_player()
    pygame.quit()