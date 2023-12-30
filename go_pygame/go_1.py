import numpy as np


class Go():
    EMPTY = 0
    BLACK = 1
    WHITE = -1
    BLACKMARKER = 4
    WHITEMARKER = 5
    LIBERTY = 8

    def __init__(self, small_board=True):
        self.row_count = 7 if small_board else 9
        self.column_count = 7 if small_board else 9
        self.board_size = 7 if small_board else 9
        self.komi = 6.5
        self.action_size = self.row_count * self.column_count + 1
        self.liberties = []
        self.block = []
        self.seki_count = 0
        self.seki_liberties = []
        self.state_history = [self.get_initial_state()]

    def make_move(self, action, player):
        state = self.get_current_state()
        new_state = self.get_next_state(state, action, player)
        self.state_history.append(new_state)

    def get_initial_state(self):
        board = np.zeros((self.row_count, self.column_count))
        self.state_history = [np.copy(board)]
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

    def get_next_state(self, state, action, player):
        if not isinstance(action, tuple):
            # Se action não for uma tupla, trata como um índice especial
            return state

        if len(action) != 2:
            # Se a tupla não tiver exatamente dois elementos, trata como um índice especial
            return state

        a, b = action  # Desempacota a tupla para obter as coordenadas

        state_copy = np.copy(state)
        state[a][b] = player
        state = self.captures(state, -player, a, b)[1]

        self.state_history.append(np.copy(state_copy))

        return state

    def is_valid_move(self, state: list, action: tuple, player: int) -> bool:


        a = action[0]
        b = action[1]
        statecopy = np.copy(state).astype(np.int8)

        if state[a][b] != self.EMPTY:
            print("Space Occupied")
            return False

        statecopy = self.set_stone(a, b, statecopy, player)

        if self.captures(statecopy, -player, a, b)[0] == True:
            return True
        else:
            # print("no captures")
            libs, block = self.count(b, a, statecopy, player, [], [])
            # print(libs)
            if len(libs) == 0:
                print("Invalid, Suicide")
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

    def get_value_and_terminated(self, state, action):
        if self.check_board_full(state=state):
            if self.check_win(state=state, action=action):
                return 1, True
            return 0, False
        return 0, False

    def check_win(self, state, action):
        if action == self.row_count * self.column_count:
            return False
        player = state[action // self.row_count][action % self.column_count]
        black_pieces = 0
        white_pieces = 0
        for row in state:
            for stone in row:
                if stone == 1:
                    black_pieces += 1
                if stone == 2:
                    white_pieces += 1

        black_points = black_pieces
        white_points = white_pieces + self.komi

        if player == 1:
            if black_points > white_points:
                return True
            return False
        else:
            if white_points > black_points:
                return True
            return False

    def check_board_full(self, state: list) -> bool:

        empty_count = 0
        for row in state:
            for stone in row:
                if stone == 0:
                    empty_count += 1
                if empty_count >= 3:
                    return False

        return True

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


