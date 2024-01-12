import socket
import time
import numpy as np
from attaxx.attaxx import Attaxx
from go_pygame.go_1 import Go
from alphazero import MCTS
import torch
from alphazero import ResNet
from args_manager import load_args_from_json

# Game = "A4x4"
# Game = "A5x5"
# Game = "A6x6"
# Game = "G7x7" 
Game = "G9x9"


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#####################################################
# falta por para diferentes tamanhos e fazer para o go
#####################################################

def prepair_model(sizeBoard):

    global game, mcts, model, args, state
    
    if Game[0]=="A": #jogo ataxx
        if sizeBoard ==4:
            game=Attaxx([int(Game[-1]),int(Game[-1])])
            model_name = "Attaxx_try1"
            args=load_args_from_json(f'AlphaZero/Models/{model_name}', Attaxx, model_name)
            model = ResNet(game, 9, 64, device)
            mcts = MCTS(model, game, args)
            model.load_state_dict(torch.load(f'AlphaZero/Models/{model_name}/model.pt', map_location=device))
            #optimizer.load_state_dict(torch.load(f'AlphaZero/Models/Attax_TestModel/optimizer_4.pt', map_location=device))
            state = game.get_initial_state()
            return state,mcts,game 
        
        # if sizeBoard ==5:
        #     game=Attaxx([int(Game[-1]),int(Game[-1])])
        #     model_name = "Attaxx_try1"
        #     args=load_args_from_json(f'AlphaZero/Models/{model_name}', Attaxx, model_name)
        #     model = ResNet(game, 9, 64, device)
        #     mcts = MCTS(model, game, args)
        #     model.load_state_dict(torch.load(f'AlphaZero/Models/{model_name}/model.pt', map_location=device))
        #     #optimizer.load_state_dict(torch.load(f'AlphaZero/Models/Attax_TestModel/optimizer_4.pt', map_location=device))
        #     state = game.get_initial_state()
        #     return state,mcts,game 
    
        # if sizeBoard ==6:
        #     game=Attaxx([int(Game[-1]),int(Game[-1])])
        #     model_name = "Attaxx_try1"
        #     args=load_args_from_json(f'AlphaZero/Models/{model_name}', Attaxx, model_name)
        #     model = ResNet(game, 9, 64, device)
        #     mcts = MCTS(model, game, args)
        #     model.load_state_dict(torch.load(f'AlphaZero/Models/{model_name}/model.pt', map_location=device))
        #     #optimizer.load_state_dict(torch.load(f'AlphaZero/Models/Attax_TestModel/optimizer_4.pt', map_location=device))
        #     state = game.get_initial_state()

        #     return state,mcts,game 
    
    else: 
        # if sizeBoard == 7:
        #     go_game = Go(board_size)
        #     model_name = "Go_go91"
        #     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        #     model = ResNet(game, 9, 64, device)
        #     model.load_state_dict(torch.load(f'AlphaZero/Models/{model_name}/model.pt', map_location=device))
        #     args=load_args_from_json(f'AlphaZero/Models/{model_name}', "Go", model_name)
        #     #optimizer.load_state_dict(torch.load(f'AlphaZero/Models/Attax_TestModel/optimizer_4.pt', map_location=device))
        #     mcts = MCTS(model, game, args)
        #     return state,mcts,game 
        
        if sizeBoard == 9:
            game = Go(False)
            model_name = "Go_go91"
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model = ResNet(game, 9, 64, device)
            model.load_state_dict(torch.load(f'AlphaZero/Models/{model_name}/model.pt', map_location=device))
            args=load_args_from_json(f'AlphaZero/Models/{model_name}', "Go", model_name)
            #optimizer.load_state_dict(torch.load(f'AlphaZero/Models/Attax_TestModel/optimizer_4.pt', map_location=device))
            mcts = MCTS(model, game, args)
            state = game.get_initial_state()
            return state,mcts,game 
    


def generate_move(state,mcts,game, ag):
    

    if Game[0] == "A":
        #neut = game.change_perspective(state, -ag) 
        action = mcts.search(state,  ag)
        action = np.argmax(action)
        move=game.int_to_move(action)
        state = game.get_next_state(state, action, ag)
        return f"MOVE {move[0]} {move[1]} {move[2]} {move[3]}", state
    
    else: 
        #neut = game.change_perspective(state, -ag)
        action = mcts.search(state, ag)
        action = np.argmax(action)
        x,y = game.int_to_move_go(action)
        state = game.get_next_state_mcts(state, action, ag)
        return f"MOVE {x} {y}" , state


def movimento_adversario(respostaServidor, state,ag):

    if Game[0] =="A":
        resposta = respostaServidor.split()
        #print(resposta)

        movimentos = [int(r) for r in resposta[1:]]
        #print(movimentos)
        sizeBoard = int(Game[-1])
        #print("Size board = " , sizeBoard)
        #print(respostaServidor)
        action = movimentos[3] +  movimentos[2] *  sizeBoard +  movimentos[1] *  sizeBoard ** 2 +  movimentos[0] *  sizeBoard ** 3
        state_new = game.get_next_state(state, action, -ag)
        return state_new
    else: 
        resposta = respostaServidor.split()
        movimentos = [int(r) for r in resposta[1:]]
        #print(movimentos)
        sizeBoard = int(Game[-1])
        #print(resposta, " : resposta ")
        action=movimentos[0] + movimentos[1] * sizeBoard
        #print(action, ": action")
        state_new = game.get_next_state(state, action, -ag)
        return state_new

def connect_to_server(host='localhost', port=12345):
    global ag
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    response = client_socket.recv(1024).decode()
    print(f"Server ResponseINIT: {response}")
    Game = response[-4:]
    print("Playing:", Game)
    
    #print("response[2] = ", response[2] )
    if response[2] == "1":
        ag=1
    else:
        ag=-1
    first=True

    state, mcts, game = prepair_model(Game[-1])

    while True:
        # Generate and send a random move
        #print("entrou")
        if ag == 1 or not first:
               # print("entrou aqui ")
                print("state = \n" , state)
               
                move,state = generate_move(state, mcts,game, ag)
                #print(state)
                time.sleep(1)
                client_socket.send(move.encode())
                #print("\nSend:",move)
            
                # Wait for server response
                response = client_socket.recv(1024).decode()
                print(f"Server Response1: {response}")
                if "END" in response: break
                    
                # while response == 'INVALID':
                #     print("Invalid Move")
                #     move = generate_move(state, mcts,game, ag)
                #     time.sleep(1)
                #     client_socket.send(move.encode())
                #     print("Send:",move)
                #     response = client_socket.recv(1024).decode()
                #     print(f"Server Response1: {response}")
                        
        first=False
        response = client_socket.recv(1024).decode()
        print(f"Server Response2: {response}")
        if "END" in response: break
        state = movimento_adversario(response, state, ag)
        # Add some condition to break the loop, if necessary
        # Example: If server sends a certain message, or after a number of moves

    client_socket.close()

if __name__ == "__main__":
    connect_to_server()





