import tkinter as tk
import tkinter.messagebox


class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.board = ["" for _ in range(9)]
        self.buttons = [
            tk.Button(
                self.window,
                text="",
                width=20,
                height=5,
                command=lambda i=i: self.player_move(i),
            )
            for i in range(9)
        ]
        for i, btn in enumerate(self.buttons):
            row = i // 3
            col = i % 3
            btn.grid(row=row, column=col)
        self.turn = "X"
        self.label = tk.Label(self.window, text="Player X's turn")
        self.label.grid(row=3, columnspan=3)
        self.restart_button = tk.Button(
            self.window, text="Restart", command=self.restart
        )
        self.restart_button.grid(row=4, columnspan=3)

    def player_move(self, position):
        if not self.board[position] and self.turn == "X":
            self.board[position] = "X"
            self.buttons[position].config(text="X")
            winner = check_winner(self.board)
            if winner:
                self.game_over(winner)
                return
            self.turn = "O"
            self.label.config(text="Player O's turn")
            self.computer_move()

    def computer_move(self):
        best_score = float("-inf")
        best_move = None
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                score = minmax(self.board, 0, False)
                self.board[i] = ""
                if score > best_score:
                    best_score = score
                    best_move = i

        if best_move is not None:
            self.board[best_move] = "O"
            self.buttons[best_move].config(text="O")
            winner = check_winner(self.board)
            if winner:
                self.game_over(winner)
            else:
                self.turn = "X"
                self.label.config(text="Player X's turn")
        else:
            print("No valid move found for computer.")

    def game_over(self, winner):
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
        if winner == "X":
            self.label.config(text="Player X wins!")
        elif winner == "O":
            self.label.config(text="Player O wins!")
        else:
            self.label.config(text="It's a draw!")

    def restart(self):
        for i in range(9):
            self.board[i] = ""
            self.buttons[i].config(text="", state=tk.NORMAL)
        self.turn = "X"
        self.label.config(text="Player X's turn")

    def start(self):
        self.window.mainloop()


def minmax(board, depth, isMaximizingPlayer):
    winner = check_winner(board)  # Check for a winner
    if winner == "X":
        return -10 + depth  # Score for X winning
    elif winner == "O":
        return 10 - depth  # Score for O winning
    elif "" not in board:
        return 0  # Score for a draw

    if isMaximizingPlayer:
        bestScore = float("-inf")  # Initialize best score for maximizer
        for i in range(9):
            if board[i] == "":
                board[i] = "O"  # Test O move
                score = minmax(board, depth + 1, False)  # Recurse for minimizing player
                board[i] = ""  # Undo move
                bestScore = max(bestScore, score)  # Update best score
        return bestScore
    else:
        bestScore = float("inf")  # Initialize best score for minimizer
        for i in range(9):
            if board[i] == "":
                board[i] = "X"  # Test X move
                score = minmax(board, depth + 1, True)  # Recurse for maximizing player
                board[i] = ""  # Undo move
                bestScore = min(bestScore, score)  # Update best score
        return bestScore


def check_winner(board):
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


game = TicTacToe()
game.start()
