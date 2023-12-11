import pygame
import chess
import math

class ChessBoard(chess.Board):
    # Constants
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    BOARD_SIZE = 8
    SQUARE_SIZE = SCREEN_WIDTH // BOARD_SIZE

    # Colors
    LIGHT_COLOR = (240, 217, 181)
    DARK_COLOR = (181, 136, 99)

    def __init__(self):
        chess.Board.__init__(self)
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

                piece = self.piece_at(chess.square(col, self.BOARD_SIZE - 1 - row))
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
            
    def get_moves(self, start_square, end_square):
        return [move for move in self.legal_moves if move.from_square == start_square and move.to_square == end_square]
        
    def print_result(self):
        print("Game over. Result: {}".format(self.result()))

class Chess:
    PIECE_VALUES = [0, 1, 3, 3, 5, 9, 20]

    def __init__(self):
        self.board = ChessBoard()
        self.dragging_piece = None
    
    def play_two_player(self):
        # Initialize Pygame
        pygame.init()
        
        screen = pygame.display.set_mode((ChessBoard.SCREEN_WIDTH, ChessBoard.SCREEN_HEIGHT))
        pygame.display.set_caption("Chess Game")

        clock = pygame.time.Clock()

        running = True
        while running and not self.board.is_game_over():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    start_square = self.board.get_square_from_mouse(pygame.mouse.get_pos())
                    piece = self.board.piece_at(start_square)
                    if piece:
                        self.dragging_piece = {"piece" : self.board.get_piece_symbol(piece.color, piece.symbol()), "square" : start_square}
                elif event.type == pygame.MOUSEBUTTONUP:
                    end_square = self.board.get_square_from_mouse(pygame.mouse.get_pos())
                    moves = self.board.get_moves(start_square, end_square)
                    if moves:
                        move = moves[0]
                        self.board.push(move)
                    self.dragging_piece = None

            screen.fill((255, 255, 255))
            self.board.draw(screen, self.dragging_piece)
            pygame.display.flip()
            clock.tick(60)

        self.board.print_result()

    def think(self):
        # Replace this with your AI logic to generate a move for the AI player
        moves = list(self.board.legal_moves)
        if (len(moves) == 1):
            return moves[0]

        bestMove = moves[0]

        depth = 3

        bestEval = -math.inf
        for move in moves:
            self.board.push(move)
            eval = -self.Minimax(depth, -bestEval)
            self.board.pop()
            if (eval > bestEval):
                bestEval = eval
                bestMove = move

        decidedMove = bestMove
        return decidedMove
    
    def Minimax(self, depth, bestPrev):
        if self.board.is_checkmate():
            return -math.inf
        if self.board.can_claim_draw() or self.board.is_insufficient_material() or self.board.is_stalemate():
            return 0
        if depth == 0:
            return self.evaluate()
        
        bestEval = -math.inf
        moves = self.board.legal_moves
        for move in moves:
            self.board.push(move)
            eval = -self.Minimax(depth-1, -bestEval)
            self.board.pop()

            if eval >= bestPrev:
                return eval
            
            bestEval = max(bestEval, eval)
        return bestEval
    
    def evaluate(self):
        allPieces = self.board.piece_map()
        whiteScore = 0
        blackScore = 0
        for pieceList in allPieces.values():
            if pieceList.color:
                whiteScore += self.PIECE_VALUES[pieceList.piece_type]
            else:
                blackScore += self.PIECE_VALUES[pieceList.piece_type]

        return (whiteScore - blackScore) * (1 if self.board.turn == chess.WHITE else -1)

    def play_one_player(self):
        # Initialize Pygame
        pygame.init()
        
        screen = pygame.display.set_mode((ChessBoard.SCREEN_WIDTH, ChessBoard.SCREEN_HEIGHT))
        pygame.display.set_caption("Chess Game")

        clock = pygame.time.Clock()

        running = True
        while running and not self.board.is_game_over():
            if self.board.turn == chess.WHITE:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        start_square = self.board.get_square_from_mouse(pygame.mouse.get_pos())
                        piece = self.board.piece_at(start_square)
                        if piece:
                            self.dragging_piece = {"piece" : self.board.get_piece_symbol(piece.color, piece.symbol()), "square" : start_square}
                    elif event.type == pygame.MOUSEBUTTONUP:
                        end_square = self.board.get_square_from_mouse(pygame.mouse.get_pos())
                        moves = self.board.get_moves(start_square, end_square)
                        if moves:
                            move = moves[0]
                            self.board.push(move)
                        self.dragging_piece = None
            else:
                # AI move
                ai_move = self.think()
                if ai_move:
                    self.board.push(ai_move)
            
            screen.fill((255, 255, 255))
            self.board.draw(screen, self.dragging_piece)
            pygame.display.flip()
            clock.tick(60)

        self.board.print_result()


if __name__ == "__main__":
    chessGame = Chess()
    chessGame.play_one_player()
    pygame.quit()