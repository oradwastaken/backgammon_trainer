from backgammon.board import Board
from backgammon.games import point_number_game
from backgammon.shell import print_board


def main():
    # Play the point_number quiz game!
    point_number_game()


    # Here's examples of how to manipulate the board:
    board = Board(bear_off_left=True)

    print('Original board')
    board.setup()
    print_board(board)

    print('Moving 24/13')
    board.move_checkers(24, 13)
    print_board(board)

    print('Moving 12/14, 12/17')
    board.move_checkers(12, 14)
    board.move_checkers(12, 17)
    print_board(board)

    print('Moving 24/14')
    board.move_checkers(24, 14)
    print_board(board)

    print('Moving bar to 5')
    board.move_checkers(0, 5)
    print_board(board)


if __name__ == '__main__':
    main()
