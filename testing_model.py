import torch
from alphazero import *
from attaxx.attaxx import Attaxx
from go_pygame.go_1 import Go
import random
import os


class RandomPlayer():
    def __init__(self, game) -> None:
        self.game = game
    
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
        valid_moves = self.game.get_valid_moves(state, player)
        tmp = [i for i, j in enumerate(valid_moves) if j == 1]
        action = self.get_best_action(state, tmp, player)

        return action

    def get_best_action(self, state, moves, player):
        values = []
        for move in moves:
            values.append((move, self.get_value(state, move, player)))

        best_action_tuple = max(values, key=lambda tup: tup[1])

        return best_action_tuple[0]
    
    def get_value(self, state, move, player):
        if self.game_type == 1:
            return self.attaxx_heuristic(state, move, player)
        else:
            return self.go_heuristic()
        
    def attaxx_heuristic(self, state, move, player):
        new_state = self.game.get_next_state(state, move, player)
        winner, win, count1, count2 = self.game.check_win_and_over(new_state, move)

        if win:
            return 100000*winner*player

        return (count1-count2)*player
        
    def go_heuristic():
        pass

def get_model_action(game, mcts, state, player):
    neut = game.change_perspective(state, player)
    action = mcts.search(neut, player)
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
            if first_player:
                action = enemy.get_next_action(state, player)
                state = game.get_next_state(state, action, player)
            else:
                action = get_model_action(game, mcts, state, player)
                state = game.get_next_state(state, action, player)

            winner, win = game.get_value_and_terminated(state, action)
            if win:
                outcomes.append(winner*model_player)
                break;

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
    new_set = {int(x.replace('model_', '').replace('.pt','')) for x in files if "optimizer_" not in x}
    return files_path+f"/model_{max(new_set)}.pt"

def main():
    print("Testing Script for Analyzing AlphaZero Models Performance against Random ang Greedy opponents")
    print()

    print("Select the game you wish to play")
    print("\t1.  Go")
    print("\t2.  Attaxx")

    selection = int(input())
    if selection == 1:
        game_type = 1
        small_board = select_go_size()
        game = Go(small_board)
    elif selection == 2:
        game_type = 2
        size = select_attaxx_size()
        game = Attaxx([size,size])

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = ResNet(game, 9, 64, device)
    print("\nInsert only the model's name, as in 'Attaxx_ModelName/model_x' or 'Go_ModelName':")
    print("Input example: 'ParamTweak' (without quotes)")
    print("The latest iteration of the model will be the one selected")
    model_name = input()
    if game_type == 1:
        path = f"AlphaZero/Models/Go_{model_name}"
        model_path = get_latest_iteration(path)
        print(f"\nLatest Model: {model_path}")
        model.load_state_dict(torch.load(model_path, map_location=device))
    elif game_type == 2:
        path = f"AlphaZero/Models/Attaxx_{model_name}"
        model_path = get_latest_iteration(path)
        print(f"\nLatest Model: {model_path}")
        model.load_state_dict(torch.load(model_path, map_location=device))

    args = {
            'game': 'Attaxx',
            'num_iterations': 25,              # number of highest level iterations
            'num_selfPlay_iterations': 100,   # number of self-play games to play within each iteration
            'num_mcts_searches': 10,          # number of mcts simulations when selecting a move within self-play
            'num_epochs': 2,                  # number of epochs for training on self-play data for each iteration
            'batch_size': 1000,                 # batch size for training
            'temperature': 1.0,              # temperature for the softmax selection of moves
            'C': 4,                           # the value of the constant policy
            'augment': False,                 # whether to augment the training data with flipped states
            'dirichlet_alpha': 1.0,           # the value of the dirichlet noise
            'dirichlet_epsilon': 0.125,       # the value of the dirichlet noise
            'alias': ('Attaxx_ParamTweak')
        }
    mcts = MCTS(model, game, args)

    random_opp = RandomPlayer(game)
    greedy_opp = GreedyPlayer(game, game_type=1)
    n_games = 100

    print(f"\nPlaying {n_games} games against RandomOpponent...")
    play_random_results = test_model(game, mcts, random_opp, n_games)
    print(f"Playing {n_games} games against GreedyOpponent...")
    play_greedy_results = test_model(game, mcts, greedy_opp, n_games)

    process_outcomes(play_random_results, "Random")
    process_outcomes(play_greedy_results, "Greedy")

main()
    


