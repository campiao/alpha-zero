import numpy as np
import math
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
import os
from tqdm import trange

class ResNet(nn.Module):
    def __init__(self, game, num_resBlocks, num_hidden, device):
        super().__init__()
        self.device = device

        self.startBlock = nn.Sequential(
            nn.Conv2d(3, num_hidden, kernel_size=3, padding=1),
            nn.BatchNorm2d(num_hidden),
            nn.ReLU()
        )
        self.backBone = nn.ModuleList(
            [ResBlock(num_hidden) for i in range(num_resBlocks)]
        )
        self.policyHead = nn.Sequential(
            nn.Conv2d(num_hidden, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(32 * game.row_count * game.column_count, game.action_size)
        )
        self.valueHead = nn.Sequential(
            nn.Conv2d(num_hidden, 3, kernel_size=3, padding=1),
            nn.BatchNorm2d(3),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(3 * game.row_count * game.column_count, 1),
            nn.Tanh()
        )
        
        self.to(device)
        
    def forward(self, x):
        x = self.startBlock(x)
        for resBlock in self.backBone:
            x = resBlock(x)
        policy = self.policyHead(x)
        value = self.valueHead(x)
        return policy, value
        
class ResBlock(nn.Module):
    def __init__(self, num_hidden):
        super().__init__()
        self.conv1 = nn.Conv2d(num_hidden, num_hidden, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(num_hidden)
        self.conv2 = nn.Conv2d(num_hidden, num_hidden, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(num_hidden)
        
    def forward(self, x):
        residual = x
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.bn2(self.conv2(x))
        x += residual
        x = F.relu(x)
        return x

class Node:
    def __init__(self, game, args, state, parent=None, action_taken=None, prior=0, visit_count=0):
        self.game = game
        self.args = args
        self.state = state
        self.parent = parent
        self.action_taken = action_taken
        self.prior = prior
        self.children = []
        
        self.visit_count = visit_count
        self.value_sum = 0
        
    def is_expanded(self):
        return len(self.children) > 0
    
    def select(self):
        best_child = None
        best_ucb = -np.inf
        
        for child in self.children:
            ucb = self.get_ucb(child)
            if ucb > best_ucb:
                best_child = child
                best_ucb = ucb
                
        return best_child
    
    def get_ucb(self, child):
        if child.visit_count == 0:
            q_value = 0
        else:
            q_value = 1 - ((child.value_sum / child.visit_count) + 1) / 2
        return q_value + self.args['C'] * (math.sqrt(self.visit_count) / (child.visit_count + 1)) * child.prior
    
    def expand(self, policy):
        for action, prob in enumerate(policy):
            if prob > 0:
                child_state = self.state.copy()
                child_state = self.game.get_next_state(child_state, action, 1)
                child_state = self.game.change_perspective(child_state, player=-1)

                child = Node(self.game, self.args, child_state, self, action, prob)
                self.children.append(child)
            
    def backpropagate(self, value):
        self.value_sum += value
        self.visit_count += 1
        
        if self.parent is not None:
            value = self.game.get_opponent_value(value)
            self.parent.backpropagate(value)  

class MCTS:
    def __init__(self, model, game, args):
        self.model = model
        self.game = game
        self.args = args
        
    @torch.no_grad()
    def search(self, state, player):
        root = Node(self.game, self.args, state, visit_count=1)
        
        policy, _ = self.model(
            torch.tensor(self.game.get_encoded_state(state), device=self.model.device).unsqueeze(0)
        )
        policy = torch.softmax(policy, axis=1).squeeze(0).cpu().numpy()
        policy = (1 - self.args['dirichlet_epsilon']) * policy + self.args['dirichlet_epsilon'] \
            * np.random.dirichlet([self.args['dirichlet_alpha']] * self.game.action_size)
        
        valid_moves = self.game.get_valid_moves(state, player)
        policy *= valid_moves
        policy /= np.sum(policy)
        root.expand(policy)
        
        for search in range(self.args['num_mcts_searches']):
            node = root
            # print("A")
            while node.is_expanded():
                node = node.select()
                
            value, is_terminal = self.game.get_value_and_terminated(node.state,player)
            value = self.game.get_opponent_value(value)
            
            if not is_terminal:
                policy, value = self.model(torch.tensor(self.game.get_encoded_state(node.state), device=self.model.device).unsqueeze(0)
                )
                policy = torch.softmax(policy, axis=1).squeeze(0).cpu().numpy()
                valid_moves = self.game.get_valid_moves(node.state, player)
                policy *= valid_moves
                policy /= np.sum(policy)
                
                value = value.item()
                
                node.expand(policy)
            # print("B")
            node.backpropagate(value)    
            
        action_probs = np.zeros(self.game.action_size)
        for child in root.children:
            action_probs[child.action_taken] = child.visit_count
        action_probs /= np.sum(action_probs)
        return action_probs

class AlphaZero:
    def __init__(self, model, optimizer, game, args):
        self.model = model
        self.optimizer = optimizer
        self.game = game
        self.args = args
        self.mcts = MCTS(model, game, args)

    def check_simmetries(self, state):
        rot90_state = np.rot90(state, k=1)
        rot90 = (state == rot90_state).all()

        rot180_state = np.rot90(state, k=2)
        rot180 = (state == rot180_state).all()

        rot270_state = np.rot90(state, k=3)
        rot270 = (state == rot270_state).all()

        flip_hori_state = np.fliplr(state)
        flip_hori = (state == flip_hori_state).all()

        flip_vert_state = np.flipud(state)
        flip_vert = (state == flip_vert_state).all()

        rot90_flip_hor_state = np.rot90(np.fliplr(state), k=1)
        rot90_flip_hor = (state == rot90_flip_hor_state).all()

        rot90_flip_vert_state = np.rot90(np.flipud(state), k=1)
        rot90_flip_vert = (state == rot90_flip_vert_state).all()

        return ((rot90, rot90_state), (rot180, rot180_state), (rot270, rot270_state), 
                (flip_hori, flip_hori_state), (flip_vert, flip_vert_state), 
                (rot90_flip_hor, rot90_flip_hor_state), (rot90_flip_vert, rot90_flip_vert_state))


    def augment_state(self, state):
        
        rot90, rot180, rot270, flip_hori, flip_vert, rot90_flip_hor, rot90_flip_vert = self.check_simmetries(state)

        augmented_states = []
        
        # Original state
        augmented_states.append(state)
        
        # Rotate 90 degrees clockwise
        if not rot90[0]:
            augmented_states.append(rot90[1])
        
        # Rotate 180 degrees clockwise
        if not rot180[0]:
            augmented_states.append(rot180[1])
        
        # Rotate 270 degrees clockwise
        if not rot270[0]:
            augmented_states.append(rot270[1])
        
        # Flip horizontally
        if not flip_hori[0]:
            augmented_states.append(flip_hori[1])
        
        # Flip vertically
        if not flip_vert[0]:
            augmented_states.append(flip_vert[1])
        
        # Rotate 90 degrees clockwise and flip horizontally
        if not rot90_flip_hor[0]:
            augmented_states.append(rot90_flip_hor[1])
        
        # Rotate 90 degrees clockwise and flip vertically
        if not rot90_flip_vert[0]:
            augmented_states.append(rot90_flip_vert[1])
        
        return augmented_states
        
    def selfPlay(self):
        memory = []
        player = 1
        state = self.game.get_initial_state()
        while True:

            neutral_state = self.game.change_perspective(state, player)
            action_probs = self.mcts.search(neutral_state, 1)
            
            memory.append((neutral_state, action_probs, player))
            
            temperature_action_probs = action_probs ** (1 / self.args['temperature'])
            temperature_action_probs /= np.sum(temperature_action_probs)
            action = np.random.choice(self.game.action_size, p=temperature_action_probs)
            if self.game.name == 'Attaxx':
                state = self.game.get_next_state(state, action, player)
            else:
                state = self.game.get_next_state_mcts(state, action, player)
            
            value, is_terminal = self.game.get_value_and_terminated(state,player)
            
            if is_terminal:
                returnMemory = []
                for hist_neutral_state, hist_action_probs, hist_player in memory:
                    hist_outcome = value if hist_player == player else self.game.get_opponent_value(value)
                    if self.args['augment']:
                        augmented_states = self.augment_state(hist_neutral_state)
                    else:
                        augmented_states = []
                        augmented_states.append(hist_neutral_state)

                    for augmented_state in augmented_states:
                        returnMemory.append((self.game.get_encoded_state(augmented_state), hist_action_probs, hist_outcome))

                return returnMemory

            player = self.game.get_opponent(player)
                
    def train(self, memory):
        random.shuffle(memory)
        for batchIdx in range(0, len(memory), self.args['batch_size']):
            sample = memory[batchIdx:batchIdx+self.args['batch_size']]
            state, policy_targets, value_targets = zip(*sample)
            
            state, policy_targets, value_targets = np.array(state), np.array(policy_targets), np.array(value_targets).reshape(-1, 1)
            
            state = torch.tensor(state, dtype=torch.float32, device=self.model.device)
            policy_targets = torch.tensor(policy_targets, dtype=torch.float32, device=self.model.device)
            value_targets = torch.tensor(value_targets, dtype=torch.float32, device=self.model.device)
            
            out_policy, out_value = self.model(state)
            
            policy_loss = F.cross_entropy(out_policy, policy_targets)
            value_loss = F.mse_loss(out_value, value_targets)
            loss = policy_loss + value_loss
            
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
    
    def learn(self):
        for iteration in range(self.args['num_iterations']):
            memory = []
            
            print(f"Iteration {iteration + 1}")
            for selfPlay_iteration in trange(self.args['num_selfPlay_iterations']):
                memory += self.selfPlay()

                
            self.model.train()
            for epoch in trange(self.args['num_epochs']):
                self.train(memory)
            print("\n")
            
            torch.save(self.model.state_dict(), f"AlphaZero/Models/{self.args['alias']}/model.pt")
            torch.save(self.optimizer.state_dict(), f"AlphaZero/Models/{self.args['alias']}/optimizer.pt")