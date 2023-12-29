from attaxx import Attaxx

def main():
    game = Attaxx([4,4])
    state = game.get_initial_state()
    game.print_board(state)

    player = 1

    while True:
        move = [0,0,0,0]
        move[0], move[1], move[2], move[3]= tuple(int(x.strip()) for x in input("\nInput your move: ").split(' '))
        print("\n")
        # Adiciona a verificação de jogada válid
        action =  move[3] + move[2]*4 + move[1]*4**2 + move[0]*4**3
        if not game.is_valid_move(state,action, player):
            print("Jogada inválida. Escolha outra jogada.")
            continue  # Pula para a próxima iteração do loop

        state = game.get_next_state(state, action, player)

        winner, win = game.get_value_and_terminated(state, action,player)
        if win:
            game.print_board(state)
            print(f"Player {winner} wins")
            exit()

        player = - player
        game.print_board(state)

if __name__ == "__main__":
    main()