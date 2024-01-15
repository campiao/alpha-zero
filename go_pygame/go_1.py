import numpy as np
import copy

class Go():
    EMPTY = 0
    BLACK = 1
    WHITE = -1
    BLACKMARKER = 4
    WHITEMARKER = 5
    LIBERTY = 8

    def __init__(self, small_board):
        self.small_board = small_board
        self.row_count = 7 if small_board else 9
        self.column_count = 7 if small_board else 9
        self.board_size = 7 if small_board else 9
        self.komi = 5.5
        self.action_size = self.row_count * self.column_count + 1
        self.liberties = []
        self.name="Go"
        self.block = []
        self.seki_count = 0
        self.seki_liberties = []
        self.state_history = [self.get_initial_state()]
        self.currrent_player = self.BLACK
        self.passed_player_1 = False
        self.passed_player_2 = False

    def clone(self):
        copia = Go(small_board=self.small_board)
        copia.liberties = copy.deepcopy(self.liberties)
        copia.block = copy.deepcopy(self.block)
        copia.seki_count = copy.deepcopy(self.seki_count)
        copia.seki_liberties = copy.deepcopy(self.seki_liberties)
        copia.state_history = copy.deepcopy(self.state_history)
        copia.currrent_player = copy.deepcopy(self.currrent_player)
        copia.passed_player_1 = copy.deepcopy(self.passed_player_1)
        copia.passed_player_2 = copy.deepcopy(self.passed_player_2)

        return copia

    def get_initial_state(self):
        board = np.zeros((self.row_count, self.column_count))
        self.state_history = [np.copy(board)]

        self.passed_player_1 = False
        self.passed_player_2 = False
        return board

    def count(self, x, y, state: list, player: int, liberties: list, block: list):


        # initialize piece
        piece = state[y][x]
        # if there's a stone at square of the given player
        if piece == player:
            # save stone coords
            block.append((y, x))
            # mark the stone
            if player == self.BLACK:
                state[y][x] = self.BLACKMARKER
            else:
                state[y][x] = self.WHITEMARKER

            # look for neighbours recursively
            if y - 1 >= 0:
                liberties, block = self.count(x, y - 1, state, player, liberties, block)  # walk north
            if x + 1 < self.column_count:
                liberties, block = self.count(x + 1, y, state, player, liberties, block)  # walk east
            if y + 1 < self.row_count:
                liberties, block = self.count(x, y + 1, state, player, liberties, block)  # walk south
            if x - 1 >= 0:
                liberties, block = self.count(x - 1, y, state, player, liberties, block)  # walk west

        # if square is empty
        elif piece == self.EMPTY:
            # mark liberty
            state[y][x] = self.LIBERTY
            # save liberties
            liberties.append((y, x))

        # print("Liberties: " + str(len(self.liberties)) + " in: " + str(x) + "," + str(y))
        # print("Block: " + str(len(self.block)) + " in: " + str(x) + "," + str(y))
        return liberties, block

    # remove captured stones
    def clear_block(self, block: list, state: list) -> list:


        # clears the elements in the block of elements which is captured
        for i in range(len(block)):
            y, x = block[i]
            state[y][x] = self.EMPTY

        return state

    # restore board after counting stones and liberties

    def get_current_state(self):
        return self.state_history[-1]
    def restore_board(self, state: list) -> list:

        for y in range(len(state)):
            for x in range(len(state)):
                # restore piece
                val = state[y][x]
                if val == self.BLACKMARKER:
                    state[y][x] = self.BLACK
                elif val == self.WHITEMARKER:
                    state[y][x] = self.WHITE
                elif val == self.LIBERTY:
                    state[y][x] = self.EMPTY

        # print("After Restore Board")
        # print(state)
        return state

    def print_board(self, state) -> None:

        print("   ", end="")
        for j in range(self.column_count):
            print(f"{j:2}", end=" ")
        print("\n  +", end="")
        for _ in range(self.column_count):
            print("---", end="")
        print()

        for i in range(self.row_count):
            print(f"{i:2}|", end=" ")
            for j in range(self.column_count):
                print(f"{str(int(state[i][j])):2}", end=" ")
            print()

    def captures(self, state: list, player: int, a: int, b: int):

        check = False
        neighbours = []
        if (a > 0): neighbours.append((a - 1, b))
        if (a < self.column_count - 1): neighbours.append((a + 1, b))
        if (b > 0): neighbours.append((a, b - 1))
        if (b < self.row_count - 1): neighbours.append((a, b + 1))

        # loop over the board squares
        for pos in neighbours:
            # print(pos)
            x = pos[0]
            y = pos[1]
            # init piece
            piece = state[x][y]

            # if stone belongs to given colour
            if piece == player:
                # print("opponent piece")
                # count liberties
                liberties = []
                block = []
                liberties, block = self.count(y, x, state, player, liberties, block)
                # print("Liberties in count: " + str(len(liberties)))
                # if no liberties remove the stones
                if len(liberties) == 0:
                    # clear block

                    state = self.clear_block(block, state)

                    # if the move is a "ko" move but causes the capture of stones, then it is not allowed, unless it is the second move, in which case it is dealt afterwards
                    if self.seki_count == 0:
                        # print("Seki Found")
                        # returns False, which means that the move has caused a capture (the logic worked out that way in the initial development and i'm not sure what it would affect if it is changed)
                        check = True
                        self.seki_count = 1
                        continue
                # restore the board
                state = self.restore_board(state)
        # print("Seki Count: " + str(self.seki_count))
        return check, state


 
    
    def set_stone(self, a, b, state, player):
        state[a][b] = player
        return state

    def get_next_state_mcts(self, state, action, player):

        if action == self.row_count * self.column_count:
            if self.passed_player_1:
                self.passed_player_2 = True
            else:
                self.passed_player_1 = True
            state_copy = np.copy(state)
            self.state_history.append(np.copy(state_copy))
            return state # pass move

        a = action // self.row_count
        b = action % self.column_count

        state_copy = np.copy(state)
        state[a][b] = player
        state = self.captures(state, -player, a, b)[1]
        self.passed_player_1 = False
        self.passed_player_2 = False

        self.state_history.append(np.copy(state_copy))

        return state
    
    def get_next_state(self, state, action, player):

        if action == self.row_count * self.column_count:
            if self.passed_player_1:
                self.passed_player_2 = True
            else:
                self.passed_player_1 = True
            
            state_copy = np.copy(state)
            self.state_history.append(np.copy(state_copy))
            return state # pass move

        a = action // self.row_count
        b = action % self.column_count

        state_copy = np.copy(state)
        state[a][b] = player
        state = self.captures(state, -player, a, b)[1]
        self.passed_player_1 = False
        self.passed_player_2 = False

        self.state_history.append(np.copy(state_copy))

        return state

    # Dentro da classe Go

    def is_valid_move(self, state: list, action: tuple, player: int) -> bool:
        a, b = action[0], action[1]  # Mantenha as coordenadas originais
        state_copy = np.copy(state).astype(np.int8)

        neib = 4
        for i in range(a-1,a+2):
            if i == a:
                continue
            if i < 0 or i >= self.row_count:
                neib-=1
                continue
            if state[i][b]==-player:
                neib-=1

        for j in range(b-1,b+2):
            if j == b:
                continue
            if j < 0 or j >= self.column_count:
                neib-=1
                continue
            if state[a][j]==-player:
                neib-=1
        
        if neib <= 0:
            return False


        if len(self.state_history) > 1:
            if np.array_equal(state, self.state_history[-2]):
                #print("Ko violation")
                return False

        # Restante do código permanece inalterado
        if a < 0 or a >= self.row_count or b < 0 or b >= self.column_count:
            #print("Invalid move: Out of bounds")
            return False

        if state[a][b] != self.EMPTY:
            #print("Space Occupied")
            return False

        state_copy = self.set_stone(a, b, state_copy, player)

        if self.captures(state_copy, player, a, b)[0] == True:
            return True
        else:
            libs, block = self.count(b, a, state_copy, player, [], [])
            if len(libs) == 0:
                #print("Invalid move: Suicide")
                return False
            else:
                return True

    def get_valid_moves(self, state, player):

        newstate = np.zeros((self.row_count, self.column_count))
        for a in range(0, self.column_count):
            for b in range(0, self.row_count):
                if self.is_valid_move(state, (a, b), player):
                    newstate[a][b] = 1

        newstate = newstate.reshape(-1)
        newstate = np.concatenate([newstate, [1]])
        return (newstate).astype(np.uint8)

    def get_value_and_terminated(self, state, player):
        
        '''
        # Description:
        Returns the value of the state and if the game is over.
        '''

        winner, game_over, _, _ = self.check_win_and_over(state, action = None)
        return winner, game_over

            
    def check_win_and_over(self, state, action):
        black = 0
        white = 0
        empty = 0
        endgame = False
        
        black, white = self.count_influenced_territory_enhanced(state)
        

        diff = black - white - self.komi

        player1moves = self.get_valid_moves(state, 1)
        player1moves = np.delete(player1moves, -1)
        player2moves = self.get_valid_moves(state, -1)
        player2moves = np.delete(player2moves, -1)

        if max(player1moves) == 0 or max(player2moves)==0:
            endgame=True

        if self.passed_player_1 and self.passed_player_2:
            endgame=True

        if endgame:
            if diff>0:
                winner = 1
            elif diff<0:
                winner = -1
            else:
                winner = 2
        else:
            winner = 0
                            
        return winner, endgame, black, white + self.komi

              

    def scoring(self, state):
        '''
        # Description:
        Checks the score of the game.
        '''
        black = 0
        white = 0
        empty = 0
        endgame = False
        # print("Scoring")

        black, white = self.count_influenced_territory_enhanced(state)
                            
        return black - (white + self.komi), endgame


    def count_influenced_territory_enhanced(self, board):
        black_territory = 0
        white_territory = 0
        visited = set()

        black_pieces = self.count_stones(board, 1)
        white_pieces = self.count_stones(board, -1)

        # Function to calculate influence score
        def influence_score(x, y):
            score = 0
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(board) and 0 <= ny < len(board[0]):
                    score += board[nx][ny]
            return score

        # Function to explore territory
        def explore_territory(x, y):
            nonlocal black_territory, white_territory
            if (x, y) in visited or not (0 <= x < len(board) and 0 <= y < len(board[0])):
                return
            visited.add((x, y))

            if board[x][y] == 0:
                score = influence_score(x, y)
                if score > 0:
                    black_territory += 1
                elif score < 0:
                    white_territory += 1

        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0 and (i, j) not in visited:
                    explore_territory(i, j)

        return black_territory+black_pieces, white_territory+white_pieces
    
    def count_stones(self, state, player):
        """Conta o número de pedras no tabuleiro para um jogador específico."""
        count = 0
        for row in state:
            for stone in row:
                if stone == player:
                    count += 1

        return  count


    def get_opponent(self, player):
        return -player

    def get_opponent_value(self, value):
        return -value

    def get_encoded_state(self, state):
        layer_1 = np.where(np.array(state) == -1, 1, 0).astype(np.float32)
        layer_2 = np.where(np.array(state) == 0, 1, 0).astype(np.float32)
        layer_3 = np.where(np.array(state) == 1, 1, 0).astype(np.float32)

        result = np.stack([layer_1, layer_2, layer_3]).astype(np.float32)

        return result

    def change_perspective(self, state, player):
        return state * player


    def int_to_move_go(self, action):
        a = action // self.row_count
        b = action % self.column_count

        return a,b
