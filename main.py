from backgammon.board import Board

def main():
    board = Board()
    board.setup()
    board.display()
    print(board.get_pipcount())

if __name__ == '__main__':
    main()

