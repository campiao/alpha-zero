from go_pygame.go_1 import Go
from attaxx.attaxx import Attaxx
from args_manager import load_args_from_json, save_args_to_json

import os
import torch, random
from torch.optim import Adam
import numpy as np
from alphazero import ResNet
from alphazero import AlphaZero

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
		print("""Select Attaxx board size(input 1 or 2 or 3)\n\t1. 4*4\n\t2. 6*6\n\t3. flexible(5*5)""")
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
	path = f"AlphaZero/Models/{game_name}_{model_name}"
	os.makedirs(path, exist_ok=True)
	with open(f"{path}/args.json", "w") as openfile:
		pass
	args = load_args_from_json(path, game_name, model_name)
	
	model = ResNet(game_mode, 9, 64, device)
	optimizer = Adam(model.parameters(), lr=0.001, weight_decay=0.0001)
	alphaZero = AlphaZero(model, optimizer, game_mode, args)
	alphaZero.learn()