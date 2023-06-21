from backgammon.board import Board, print_board


def main():
    board = Board()
    board.random()

    print_board(board)
    print(board.get_pipcount())


if __name__ == '__main__':
    main()
