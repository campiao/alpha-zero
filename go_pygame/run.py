from go_1 import Go

def main():
    small_board = input("De input de 0 (9x9) ou 1 (7x7): ")
    small_board = int(small_board) == 1

    game = Go(small_board=small_board)
    state = game.get_initial_state()
    game.print_board(state)

    player = 1

    while True:
        a, b = tuple(int(x.strip()) for x in input("\nInput your move: ").split(' '))
        print("\n")

        # Adiciona a verificação de jogada válida
        if not game.is_valid_move(state, (a, b), player):
            print("Jogada inválida. Escolha outra jogada.")
            continue  # Pula para a próxima iteração do loop

        action = a * game.row_count + b
        state = game.get_next_state(state, action, player)

        winner, win = game.get_value_and_terminated(state, action)
        if win:
            game.print_board(state)
            print(f"Player {winner} wins")
            exit()

        player = - player
        game.print_board(state)

if __name__ == "__main__":
    main()
