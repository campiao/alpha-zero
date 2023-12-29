# run.py

from go_1 import Go

def play_go(board_size, player):
    game = Go(small_board=board_size == 1)
    state = game.get_initial_state()
    game.print_board(state)

    while True:
        a, b = tuple(int(x.strip()) for x in input("\nInput your move (row col): ").split())
        print("\n")

        # Adiciona a verificação de jogada válida
        if not game.is_valid_move(state, (a, b), player):
            print("Jogada inválida. Escolha outra jogada.")
            continue  # Pula para a próxima iteração do loop

        action = a * game.row_count + b
        state = game.get_next_state(state, (a, b), player)

        winner, win = game.get_value_and_terminated(state, action)
        if win:
            game.print_board(state)
            print(f"Player {winner} wins")
            exit()

        player = - player
        game.print_board(state)

if __name__ == "__main__":
    small_board = input("De input de 0 (9x9) ou 1 (7x7): ")
    small_board = int(small_board) == 1

    play_go(small_board, 1)  # Chamada da função com parâmetros adequados

