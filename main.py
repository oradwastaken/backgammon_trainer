from backgammon.board import Board, print_board


def main():
    board = Board()
    board.setup()

    print_board(board)


if __name__ == '__main__':
    main()
