def minmax(board, depth, isMaximizingPlayer):
    """
    Minimax algorithm to calculate the best move for the computer.
    """
    winner = check_winner(board)
    if winner == "X":
        return -10 + depth
    elif winner == "O":
        return 10 - depth
    elif "" not in board:
        return 0

    if isMaximizingPlayer:
        bestScore = float("-inf")
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minmax(board, depth + 1, False)
                board[i] = ""
                bestScore = max(bestScore, score)
        return bestScore
    else:
        bestScore = float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minmax(board, depth + 1, True)
                board[i] = ""
                bestScore = min(bestScore, score)
        return bestScore


def check_winner(board):
    """
    Check if there is a winner in the game.
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
    Print the game board to the console.
    """
    for i in range(0, 9, 3):
        print(board[i : i + 3])
    print()


def player_move(board):
    """
    Allow the player to input their move.
    """
    move = int(input("Enter your move (1-9): ")) - 1
    if board[move] == "":
        board[move] = "X"
    else:
        print("Invalid move. Try again.")
        player_move(board)


def computer_move(board):
    """
    Determine the computer's move using the minimax algorithm.
    """
    best_score = float("-inf")
    best_move = None
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minmax(board, 0, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                best_move = i

    if best_move is not None:
        board[best_move] = "O"


def play_game():
    """
    Main function to play the game.
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
