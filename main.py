from bgtrainer.board import Board
from bgtrainer.games import games
from bgtrainer.shell import bear_off_question, select_game, welcome


def main():
    welcome()

    # Let's play games!
    game_choice = select_game()
    board = Board(bear_off_left=bear_off_question())
    game = games[game_choice](board)
    game.play()

    # An example of saving/loading a board:
    # from backgammon.shell import print_board
    # board.setup()
    # board.save('temp.json')
    # board.load('temp.json')
    # print_board(board)

    # # Here's examples of how to manipulate the board:
    # print('Original board')
    # board.setup()
    # print_board(board)
    #
    # print('Moving 24/13')
    # board.move_checkers(24, 13)
    # print_board(board)
    #
    # print('Moving 12/14, 12/17')
    # board.move_checkers(12, 14)
    # board.move_checkers(12, 17)
    # print_board(board)
    #
    # print('Moving 24/14')
    # board.move_checkers(24, 14)
    # print_board(board)
    #
    # print('Moving bar to 5')
    # board.move_checkers(0, 5)
    # print_board(board)


if __name__ == "__main__":
    main()
