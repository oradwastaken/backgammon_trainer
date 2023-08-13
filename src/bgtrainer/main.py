from bgtrainer.board import Board
from bgtrainer.database import cleanup
from bgtrainer.games import games
from bgtrainer.shell import bear_off_question, select_game, welcome


def main():
    welcome()

    # Let's play games!
    game_choice = select_game()
    board = Board(bear_off_left=bear_off_question())
    game = games[game_choice](board)
    game.play()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cleanup()
