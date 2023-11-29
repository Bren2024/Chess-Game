import chess

# def print_board(board):
#     print(board)

def main():
    board = chess.Board()

    while not board.is_game_over():
        print(board)
        
        # Get the move from the user
        move_uci = input("Enter your move (in UCI format, e.g., 'e2e4'): ")
        
        # Try to make the move
        try:
            move = chess.Move.from_uci(move_uci)
            if move in board.legal_moves:
                board.push(move)
            else:
                print("Illegal move. Try again.")
        except ValueError:
            print("Invalid move format. Try again.")
    
    print("Game over. Result: {}".format(board.result()))

if __name__ == "__main__":
    main()
