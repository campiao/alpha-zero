import json

def load_args_from_json(path, game_name, model_name):
    args = {}
    with open(f"{path}/args.json", "r") as openfile:
        print("\nLoading training and MCTS args from JSON file...")
        try:
            args = json.load(openfile)
            print("Args succefully loaded from file")
        except json.decoder.JSONDecodeError as e:
            print("JSON file is empty, args will take default values and will be saved as args.json")
            args = {
                'game': 'Attaxx',
                'num_iterations': 100,              # number of highest level iterations
                'num_selfPlay_iterations': 50,   # number of self-play games to play within each iteration
                'num_mcts_searches': 20,          # number of mcts simulations when selecting a move within self-play
                'num_epochs': 15,                  # number of epochs for training on self-play data for each iteration
                'batch_size': 500,                 # batch size for training
                'temperature': 1.0,              # temperature for the softmax selection of moves
                'C': 4,                           # the value of the constant policy
                'augment': False,                 # whether to augment the training data with flipped states
                'dirichlet_alpha': 0.3,           # the value of the dirichlet noise
                'dirichlet_epsilon': 0.125,       # the value of the dirichlet noise
                'alias': f'{game_name}_{model_name}'
            }
            save_args_to_json(args, path)
            
    return args
    
def save_args_to_json(args, path):
    with open(f"{path}/args.json", "w") as outfile:
        print("\nSaving training and MCTS args to JSON...")
        json.dump(args, outfile)
        print("JSON file succefully saved as args.json")