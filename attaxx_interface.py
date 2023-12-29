import torch
from torch.optim import Adam
import random
import numpy as np
from attaxx.attaxx import Attaxx

from alphazero import ResNet
from alphazero import AlphaZero
from alphazero import MCTS

import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
torch.manual_seed(0)
random.seed(0)
np.random.seed(0)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

SAVE_NAME = None


SAVE_NAME = input("Alias of the model: ")
MODEL = input("Model name: ")
OPT = input("Optimizer name: ")

TEST = input("Test:\nTrue will play against the model, False will train the model (True/False):\n")
args = {
'game': 'Attaxx',
'num_iterations': 8,              # number of highest level iterations
'num_selfPlay_iterations': 400,   # number of self-play games to play within each iteration
'num_mcts_searches': 60,          # number of mcts simulations when selecting a move within self-play
'num_epochs': 4,                  # number of epochs for training on self-play data for each iteration
'batch_size': 40,                 # batch size for training
'temperature': 1.25,              # temperature for the softmax selection of moves
'C': 2,                           # the value of the constant policy
'augment': False,                 # whether to augment the training data with flipped states
'dirichlet_alpha': 0.3,           # the value of the dirichlet noise
'dirichlet_epsilon': 0.125,       # the value of the dirichlet noise
'alias': ('Attaxx' + SAVE_NAME)
}

game = Attaxx((4,4))
model = ResNet(game, 9, 3, device)
optimizer = Adam(model.parameters(), lr=0.001, weight_decay=0.0001)


model.load_state_dict(torch.load(f'AlphaZero/Models/{GAME+SAVE_NAME}/{MODEL}.pt', map_location=device))
optimizer.load_state_dict(torch.load(f'AlphaZero/Models/{GAME+SAVE_NAME}/{OPT}.pt', map_location=device))

if not TEST:
os.makedirs(f'AlphaZero/Models/{GAME+SAVE_NAME}', exist_ok=True)
alphaZero = AlphaZero(model, optimizer, game, args)
alphaZero.learn()
else
game = Attaxx((4,4))

mcts = MCTS(model, game, args)
state = game.get_initial_state()
game.print_board(state)

player = 1

while True:
    if player == 1:
        move=[0,0,0,0]
        # input do player
        move[0], move[1], move[2], move[3]= tuple(int(x.strip()) for x in input("\nInput your move: ").split(' '))
        action =  move[3] + move[2]*4 + move[1]*4**2 + move[0]*4**3
        state = game.get_next_state(state, action, player)
    else:
        neut = game.change_perspective(state, player)

        action = mcts.search(neut, player)

        action = np.argmax(action)

        state = game.get_next_state(state, action, player)

    winner, win = game.get_value_and_terminated(state, action)
    if win:
        game.print_board(state)
        print(f"player {winner} wins")
        exit()

    player = - player
    game.print_board(state)