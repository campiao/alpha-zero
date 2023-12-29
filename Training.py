from go_pygame.go_1 import Go
from attaxx.attaxx import Attaxx

import os
import torch, random
from torch.optim import Adam
import numpy as np
from alphazero import ResNet
from alphazero import AlphaZero
from alphazero import MCTS

os.chdir(os.path.dirname(os.path.abspath(__file__)))
torch.manual_seed(0)
random.seed(0)
np.random.seed(0)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

if __name__ == '__main__':
	print("-----------------------------")
	print("Training Script for AlphaZero")
	print("-----------------------------")
	print("Select the game(input 1 or 2):\n \t1. Go\n\t2. Attaxx")
	game = int(input())
	if game == 1:
		print("Select Go board size (input 1 or 2)1\n\t1. 7*7\n\t2. 9*9")
		small_board = input()
		if small_board == 1:
			small_board = True
		else:
			small_board = False
		game_mode = Go(small_board)
		game_name = "Go"
	else:
		print("Select Attaxx board size(input 1 or 2 or 3)\n\
		\t1. 4*4\n\
		\t2. 6*6\n\
		\t3. flexible(5*5)")
		board_size = int(input())
		if board_size == 1:
			size = (4,4)
		elif board_size == 2:
			size = (6,6)
		else:
			size = (5,5)
		game_mode = Attaxx(size)
		game_name = "Attaxx"

	model_name = input("Alias of the new model: ")
	args = {
            'game': game_name,
            'num_iterations': 10,             # number of highest level iterations
            'num_selfPlay_iterations': 10,   # number of self-play games to play within each iteration
            'num_mcts_searches': 100,         # number of mcts simulations when selecting a move within self-play
            'num_epochs': 25,                  # number of epochs for training on self-play data for each iteration
            'batch_size': 8,                # batch size for training
            'temperature': 1.25,              # temperature for the softmax selection of moves
            'C': 2,                           # the value of the constant policy
            'augment': False,                 # whether to augment the training data with flipped states
            'dirichlet_alpha': 0.3,           # the value of the dirichlet noise
            'dirichlet_epsilon': 0.25,        # the value of the dirichlet noise
            'alias': (game_name + "_" + model_name)
        }
	model = ResNet(game_mode, 9, 3, device)
	optimizer = Adam(model.parameters(), lr=0.001, weight_decay=0.0001)
	os.makedirs(f'AlphaZero/Models/{game_name+"_"+model_name}', exist_ok=True)
	alphaZero = AlphaZero(model, optimizer, game_mode, args)
	alphaZero.learn()