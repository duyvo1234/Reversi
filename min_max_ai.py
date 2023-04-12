from copy import deepcopy
import math
import random

MAX_DEPTH = 3
MINIMUM = -math.inf
MAXIMUM = math.inf
MOVE_DIRS = [(-1, -1), (-1, 0), (-1, +1),
             (0, -1),           (0, +1),
             (+1, -1), (+1, 0), (+1, +1)]

class StateHolder:
    def __init__(self, board, n, num_tiles, player):
        self.n = n
        self.board = board
        self.num_tiles = num_tiles
        self.current_player = player
        self.move = ()

    def make_move(self):
        if self.is_legal_move(self.move):
            self.board[self.move[0]][self.move[1]] = self.current_player + 1
            self.num_tiles[self.current_player] += 1
            self.flip_tiles()

    def flip_tiles(self):
        curr_tile = self.current_player + 1 
        for direction in MOVE_DIRS:
            if self.has_tile_to_flip(self.move, direction):
                i = 1
                while True:
                    row = self.move[0] + direction[0] * i
                    col = self.move[1] + direction[1] * i
                    if self.board[row][col] == curr_tile:
                        break
                    else:
                        self.board[row][col] = curr_tile
                        self.num_tiles[self.current_player] += 1
                        self.num_tiles[(self.current_player + 1) % 2] -= 1
                        i += 1

    def has_tile_to_flip(self, move, direction):
        i = 1
        if self.current_player in (0, 1) and \
           self.is_valid_coord(move[0], move[1]):
            curr_tile = self.current_player + 1
            while True:
                row = move[0] + direction[0] * i
                col = move[1] + direction[1] * i
                if not self.is_valid_coord(row, col) or \
                    self.board[row][col] == 0:
                    return False
                elif self.board[row][col] == curr_tile:
                    break
                else:
                    i += 1
        return i > 1

    def has_legal_move(self):
        for row in range(self.n):
            for col in range(self.n):
                move = (row, col)
                if self.is_legal_move(move):
                    return True
        return False

    def get_legal_moves(self):
        moves = []
        for row in range(self.n):
            for col in range(self.n):
                move = (row, col)
                if self.is_legal_move(move):
                    moves.append(move)
        return moves
    
    def is_valid_coord(self, row, col):
       
        if 0 <= row < self.n and 0 <= col < self.n:
            return True
        return False
    
    def is_legal_move(self, move):
       
        if move != () and self.is_valid_coord(move[0], move[1]) \
           and self.board[move[0]][move[1]] == 0:
            for direction in MOVE_DIRS:
                if self.has_tile_to_flip(move, direction):
                    return True
        return False



def alpha_beta_minimax(board, player):
    best_value = -10000
    moves = board.get_legal_moves()
    best_move = None

    alpha = MINIMUM
    beta = MAXIMUM

    for move in moves:
        tempBoard = deepcopy(board)
        tempBoard.move = move
        tempBoard.make_move()
        score = alpha_beta_search(tempBoard, 0, alpha, beta, False)

        if score > best_value:
            best_value = score
            best_move = move
        alpha = max(alpha, best_value)
        if beta <= alpha:
            break
    if best_move == None:
        best_move = random.choice(moves)
    return best_move

def alpha_beta_search(board, depth, alpha, beta, player):
    moves = board.get_legal_moves()
    if depth == MAX_DEPTH or moves == []:
        return board_value(board)
    
    
    if player:
        best = MINIMUM        
        for m in moves:
            trvBoard = deepcopy(board)
            trvBoard.move = m
            trvBoard.make_move()
            value = alpha_beta_search(trvBoard, depth + 1, alpha, beta, -1)
            best = max(best, value)
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return best
    else:
        best = MAXIMUM
        for m in moves:
            trvBoard = deepcopy(board)
            trvBoard.move = m
            trvBoard.make_move()
            value = alpha_beta_search(trvBoard, depth + 1, alpha, beta, 1)
            best = min(best, value)
            beta = min(beta, value)
            if beta <= alpha:
                break
        return best

def board_value(state):
    player = state.current_player + 1
    enemy = 2 - player

    player_num = 0
    enemy_num = 0
    player_front = 0
    enemy_front = 0

    p = 0
    c = 0
    l = 0
    m = 0
    f = 0
    d = 0

    X1 = [-1, -1, 0, 1, 1, 1, 0, -1]
    Y1 = [0, 1, 1, 1, 0, -1, -1, -1]

    V = [
            [20, -3, 11, 8, 8, 11, -3, 20],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [20, -3, 11, 8, 8, 11, -3, 20]
        ]
    
    # Step 1
    for i in range(state.n):
        for j in range(state.n):
            if state.board[i][j] == player:
                d += V[i][j]
                player_num += 1
            elif state.board[i][j] == enemy:
                d -= V[i][j]
                enemy_num += 1

            if state.board[i][j] != 0:
                for k in range(8):
                    x = i + X1[k]
                    y = j + Y1[k]
                    if x >= 0 and x < 8 and y >= 0 and y < 8 and state.board[x][y] == 0:
                        if state.board[i][j] == player:
                            player_front += 1
                        else:
                            enemy_front += 1
                        break
    
    # Step 2
    if player_num > enemy_num:
        p = (100.0 * player_num) / (player_num + enemy_num)
    elif player_num < enemy_num:
        p = -(100.0 * enemy_num) / (player_num + enemy_num)
    else:
        p = 0

    # Step 3
    if player_front > enemy_front:
        f = -(100.0 * player_front) / (player_front + enemy_front)
    elif player_front < enemy_front:
        f = (100.0 * enemy_front) / (player_front + enemy_front)
    else:
        f = 0

    # Step 4
    player_num = enemy_num = 0
    if state.board[0][0] == player:
        player_num += 1
    elif state.board[0][0] == enemy:
        enemy_num += 1
    if state.board[0][7] == player:
        player_num += 1
    elif state.board[0][7] == enemy:
        enemy_num += 1
    if state.board[7][0] == player:
        player_num += 1
    elif state.board[7][0] == enemy:
        enemy_num += 1
    if state.board[7][7] == player:
        player_num += 1
    elif state.board[7][7] == enemy:
        enemy_num += 1
    c = 25 * (player_num - enemy_num)

    # Step 5
    player_num = enemy_num = 0
    if state.board[0][0] == 0:
        if state.board[0][1] == player:
            player_num += 1
        elif state.board[0][1] == enemy:
            enemy_num += 1
        if state.board[1][1] == player:
            player_num += 1
        elif state.board[1][1] == enemy:
            enemy_num += 1
        if state.board[1][0] == player:
            player_num += 1
        elif state.board[1][0] == enemy:
            enemy_num += 1

    if state.board[0][7] == 0:
        if state.board[0][6] == player:
            player_num += 1
        elif state.board[0][6] == enemy:
            enemy_num += 1
        if state.board[1][6] == player:
            player_num += 1
        elif state.board[1][6] == enemy:
            enemy_num += 1
        if state.board[1][7] == player:
            player_num += 1
        elif state.board[1][7] == enemy:
            enemy_num += 1

    if state.board[7][0] == 0:
        if state.board[7][1] == player:
            player_num += 1
        elif state.board[7][1] == enemy:
            enemy_num += 1
        if state.board[6][1] == player:
            player_num += 1
        elif state.board[6][1] == enemy:
            enemy_num += 1
        if state.board[6][0] == player:
            player_num += 1
        elif state.board[6][0] == enemy:
            enemy_num += 1

    if state.board[7][7] == 0:
        if state.board[6][7] == player:
            player_num += 1
        elif state.board[6][7] == enemy:
            enemy_num += 1
        if state.board[6][6] == player:
            player_num += 1
        elif state.board[6][6] == enemy:
            enemy_num += 1
        if state.board[7][6] == player:
            player_num += 1
        elif state.board[7][6] == enemy:
            enemy_num += 1

    l = -12.5 * (player_num - enemy_num)

    return (10 * p) + (801.724 * c) + (382.026 * l) + \
               (78.922 * m) + (74.396 * f) + (10 * d)