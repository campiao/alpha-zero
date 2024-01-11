import torch
from alphazero import *
from attaxx.attaxx import Attaxx
from go_pygame.go_1 import Go
import random
import os
from args_manager import load_args_from_json, save_args_to_json


class RandomPlayer():
    def __init__(self, game, game_type) -> None:
        self.game = game
        self.game_type = game_type
    
    def get_next_action(self, state, player):
        valid_moves = self.game.get_valid_moves(state, player)
        tmp = [i for i, j in enumerate(valid_moves) if j == 1]
        action = random.choice(tmp)
        
        return action
    

class GreedyPlayer():
    def __init__(self, game, game_type) -> None:
        self.game_type = game_type
        self.game = game
    
    def get_next_action(self, state, player):
        state1=np.copy(state)
        valid_moves = self.game.get_valid_moves(state1, player)
        tmp = [i for i, j in enumerate(valid_moves) if j == 1]
        action = self.get_best_action(state1, tmp, player)

        return action

    def get_best_action(self, state, moves, player):
        values = []
        for move in moves:
            values.append((move, self.get_value(state, move, player)))

        best_action_tuple = max(values, key=lambda tup: tup[1])

        return best_action_tuple[0]
    
    def get_value(self, state, move, player):
        if self.game_type == 2:
            return self.attaxx_heuristic(state, move, player)
        else:
            return self.go_heuristic(state, move, player)
        
    def attaxx_heuristic(self, state, move, player):
        new_state = self.game.get_next_state(state, move, player)
        winner, win, count1, count2 = self.game.check_win_and_over(new_state, move)

        if win:
            return 100000*winner*player

        return (count1-count2)*player
        
    def go_heuristic(self,state, move, player):
        copy_game = self.game.clone()
        #new_state = copy_game.get_next_state_mcts(state, move, player)

        if move == self.game.action_size-1:
            return 10000
        return 0


def get_model_action(game, mcts, state, player):
    neut = game.change_perspective(state, player)
    action = mcts.search(neut, 1)
    action = np.argmax(action)

    return action

def test_model(game, mcts, enemy, n_games):
    outcomes = []
    first_player_decider = 2
    for _ in range(n_games):
        state = game.get_initial_state()
        player = 1
        first_player = (first_player_decider % 2 == 0)
        model_player = 1 if not first_player else -1
        while True:
            if not player == model_player:
                action = enemy.get_next_action(state, player)
                state = game.get_next_state(state, action, player)
                print(f"Enemy action: {action}")
            else:
                action = get_model_action(game, mcts, state, player)
                state = game.get_next_state(state, action, player)
                print(f"Model action: {action}")
            
            if enemy.game_type == 1:
                print(f"p1: {game.passed_player_1}, p2: {game.passed_player_2}")

            winner, win = game.get_value_and_terminated(state, action)
            if win:
                print(f"Winner: {winner}, model: {model_player}")
                outcomes.append(winner*model_player)
                break;
            #game.print_board(state)
            player = - player
        
        first_player_decider += 1

    return outcomes
    
def process_outcomes(outcomes, opp):
    wins = outcomes.count(1)
    loses = outcomes.count(-1)
    draws = len(outcomes) - wins - loses
    total = wins + loses + draws
    print("-------------")
    print("---Results---")
    print(f"Opponent type: {opp}")
    print(f"""Number of draws: {draws}
Number of AlphaZero Wins: {wins}
Number of AlphaZero Losses: {loses}""")
    print(f"AlphaZero Win Percentage: {100*wins/total}%")

def select_go_size():
    print("Select the size of the Go board:")
    print("\t1.  7*7")
    print("\t2.  9*9")

    selection = int(input())
    if selection == 1:
        small_board = True
    elif selection == 2:
        small_board = False

    return small_board

def select_attaxx_size():
    print("Select the size of the Attaxx board:")
    print("\t1.  4*4")
    print("\t2.  6*6")
    print("\t3.  5*5 flexible board")

    selection = int(input())
    if selection == 1:
        return 4
    elif selection == 2:
        return 6
    elif selection == 3:
        return 5
    
def get_latest_iteration(files_path):
    files = os.listdir(files_path)
    new_set = {int(x.replace('model_', '').replace('.pt','')) for x in files if "model_" in x}
    return files_path+f"/model.pt"

def main():
    print("Testing Script for Analyzing AlphaZero Models Performance against Random ang Greedy opponents")
    print()

    print("Select the game you wish to play")
    print("\t1.  Go")
    print("\t2.  Attaxx")

    selection = int(input())
    if selection == 1:
        game_type = 1
        game_name = "Go"
        small_board = select_go_size()
        game = Go(small_board)
    elif selection == 2:
        game_type = 2
        game_name = "Attaxx"
        size = select_attaxx_size()
        game = Attaxx([size,size])

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = ResNet(game, 9, 64, device)

    print("\nInsert only the model's name, as in 'Attaxx_ModelName/model_x' or 'Go_ModelName':")
    print("Input example: 'ParamTweak' (without quotes)")
    print("The latest iteration of the model will be the one selected")

    model_name = input()
    path = f"AlphaZero/Models/{game_name}_{model_name}"
    model_path = get_latest_iteration(path)
    print(f"\nLatest Model: {model_path}")
    model.load_state_dict(torch.load(model_path, map_location=device))

    args = load_args_from_json(path, game_name, model_name)

    mcts = MCTS(model, game, args)

    random_opp = RandomPlayer(game, game_type)
    greedy_opp = GreedyPlayer(game, game_type=game_type)
    n_games = 5

    print(f"\nPlaying {n_games} games against RandomOpponent...")
    play_random_results = test_model(game, mcts, random_opp, n_games)
    print(f"Playing {n_games} games against GreedyOpponent...")
    play_greedy_results = test_model(game, mcts, greedy_opp, n_games)

    process_outcomes(play_random_results, "Random")
    process_outcomes(play_greedy_results, "Greedy")


main()
    


