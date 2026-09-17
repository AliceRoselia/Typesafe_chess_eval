# -*- coding: utf-8 -*-



from typesafe_sdk import Choice, Noul, Score, TypeSafeClient, RetryPolicy
import chess
import chess.pgn
board = chess.Board()
side = ["black","white"]

display(board)

with TypeSafeClient(retry=RetryPolicy(max_retries=3, backoff_max=0.2, timeout=1.0)) as client:
    while not board.is_game_over():
        
        response = client.system_one(
            state={"Format": "lowercase letter for black pieces, uppercase letters for white pieces, as in fen notation.", "Board fen": f"{board.fen()}","Pretty print": str(board), "Your side":f"{side[board.turn]}", "Your elo": "Above 3000"},
            questions={
                "evaluation": Choice(instructions = "What is your game outcome assuming neither side makes major mistake?",
                                     criteria = {"win":None, "draw":None, "lose":None}),
                "best move": Choice(instructions = "What is your best move for the current position assuming neither side makes major mistake?",
                                    criteria = {i.uci():None for i in board.legal_moves})
            }
        )
        print("Win:", response.choices["evaluation"].probabilities["win"])
        print("Draw:", response.choices["evaluation"].probabilities["draw"])
        print("Lose:", response.choices["evaluation"].probabilities["lose"])
        print("Played with confidence:",response.choices["best move"].confidence)
        board.push_uci(response.choices["best move"].choice)
        display(board)

print("Replay:")
print(chess.pgn.Game.from_board(board))