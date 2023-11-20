def minmax(board, depth, isMaximizingPlayer, alpha, beta):
    """
    Minimax algorithm with Alpha-Beta pruning.
    """
    winner = check_winner(board)
    if winner == "X":
        return -10 + depth
    elif winner == "O":
        return 10 - depth
    elif "" not in board:
        return 0

    if isMaximizingPlayer:
        maxEval = float("-inf")
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                eval = minmax(board, depth + 1, False, alpha, beta)
                board[i] = ""
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cut-off
        return maxEval

    else:
        minEval = float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                eval = minmax(board, depth + 1, True, alpha, beta)
                board[i] = ""
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cut-off
        return minEval


def check_winner(board):
    """
    Check for a winner on the board.
    """
    winning_combinations = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]
    for combo in winning_combinations:
        if (
            board[combo[0]] == board[combo[1]] == board[combo[2]]
            and board[combo[0]] != ""
        ):
            return board[combo[0]]
    return None


def print_board(board):
    """
    Print the Tic Tac Toe board.
    """
    for i in range(0, 9, 3):
        print(" | ".join(board[i : i + 3]).replace("", " "))
        if i < 6:
            print("---------")
    print()


def player_move(board):
    """
    Player makes a move by entering a number.
    """
    move = int(input("Enter your move (1-9): ")) - 1
    if 0 <= move < 9 and board[move] == "":
        board[move] = "X"
    else:
        print("Invalid move. Try again.")
        player_move(board)


def computer_move(board):
    """
    Computer makes a move using the Minimax algorithm with Alpha-Beta pruning.
    """
    best_score = float("-inf")
    best_move = None
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minmax(board, 0, False, float("-inf"), float("inf"))
            board[i] = ""
            if score > best_score:
                best_score = score
                best_move = i

    if best_move is not None:
        board[best_move] = "O"


def play_game():
    """
    Main function to play the Tic Tac Toe game.
    """
    board = ["" for _ in range(9)]
    turn = "X"

    while True:
        print_board(board)
        if turn == "X":
            player_move(board)
            turn = "O"
        else:
            computer_move(board)
            turn = "X"

        winner = check_winner(board)
        if winner or "" not in board:
            print_board(board)
            if winner:
                print(f"Player {winner} wins!")
            else:
                print("It's a draw!")
            break


if __name__ == "__main__":
    play_game()
