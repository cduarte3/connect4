import math
import copy
import random

def copy_board(board):    
    current_board = []
    height = len(board)
    for i in range(height):
        current_board.append(board[i].copy())
    return current_board

def check_tie(board):
    # Check if the board is full and return True if it is
    for row in board:
        if 0 in row:
            return False
    return True

def check_winner(board):
    # Check horizontal locations for win
    for row in range(6):
        for col in range(4):
            if board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3] != 0:
                return board[row][col]

    # Check vertical locations for win
    for col in range(7):
        for row in range(3):
            if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] != 0:
                return board[row][col]

    # Check positively sloped diagonals
    for row in range(3):
        for col in range(4):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] != 0:
                return board[row][col]

    # Check negatively sloped diagonals
    for row in range(3, 6):
        for col in range(4):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] != 0:
                return board[row][col]

    return 0  # No winner

def valid_move(game_board, col):
    if col > 6 or col < 0:
        return False
    return game_board[0][col] == 0

def drop_piece(game_board, player, col):
    for i in reversed(range(6)):
        if game_board[i][col] == 0:
            game_board[i][col] = player
            return True
    return False

class GameTree:
    class Node:
        # initializes the node and its children
        def __init__(self, board, depth, player, tree_height=4):
            self.board = copy_board(board)
            self.depth = depth
            self.player = player
            self.tree_height = tree_height
            self.children = []
            if self.depth < self.tree_height:
                self.generateChildren()

        # recursive minimax method to find min or max of a move
        def minimax(self, alpha=-math.inf, beta=math.inf, depth=0):
            winner = check_winner(self.board)
            if depth == 0 or self.depth == self.tree_height or not self.children or winner:
                if winner == self.player:
                    return 1000
                elif winner:
                    return -1000
                else:
                    # Calculate score based on number of pieces in a row
                    score = 0
                    for row in range(6):
                        for col in range(4):
                            if self.board[row][col:col+4].count(self.player) == 3:
                                score += 100  # Reward for 3 pieces in a row
                            elif self.board[row][col:col+4].count(3-self.player) == 3:
                                score -= 100  # Penalty for opponent having 3 pieces in a row
                    return score
            if self.player == 2:  # AI tries to maximize its score
                value = -math.inf
                for child in self.children:
                    value = max(value, child[1].minimax(alpha, beta))
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break  # Beta cut-off
                return value
            elif self.player == 1:  # Human tries to minimize its score
                value = math.inf
                for child in self.children:
                    value = min(value, child[1].minimax(alpha, beta))
                    beta = min(beta, value)
                    if beta <= alpha:
                        break  # Alpha cut-off
                return value
        
        # generates the children of the Root and/or Node(s)
        def generateChildren(self):
            for col in range(7):  # Assuming a 7-column Connect 4 board
                if not valid_move(self.board, col):
                    continue  # Skip this column if it's full

                new_board = copy_board(self.board)
                for row in reversed(range(6)):  # Assuming a 6-row Connect 4 board
                    if new_board[row][col] == 0:
                        new_board[row][col] = self.player
                        break

                next_player = 1 if self.player == 2 else 2  # Alternate between 1 and 2
                child = GameTree.Node(new_board, self.depth + 1, next_player, self.tree_height)
                self.children.append((col, child))  # Only store the column index

    # initializes the GameTree
    def __init__(self, board, player, tree_height=6):
        self.player = player
        self.board = copy_board(board)
        self.tree_height = tree_height
        self.depth = 0
        self.root = None

    # gets a move from the tree
    def get_move(self):
        self.root = self.Node(self.board, self.depth, self.player, self.tree_height)
        best_move = None
        for depth in range(1, self.tree_height + 1):
            move = self.best_move(self.player, depth)
            if move is not None:
                best_move = move
                break
        drop_piece(self.board, self.player, best_move)
        return best_move
    
    def best_move(self, player, depth):
        # On the first move, play random
        # player 1 always plays first
        if sum(sum(row) for row in self.board) == 1:
            valid_moves = [i for i in range(7) if valid_move(self.board, i)]
            if valid_moves is not None:
                return random.choice(valid_moves)
        
        # Check for a winning move
        for i in range(7):
            temp_board = copy.deepcopy(self.board)
            if valid_move(temp_board, i):
                drop_piece(temp_board, player, i)
                if check_winner(temp_board) == player:
                    return i
                    
        # Check for a winning move for the opponent
        opponent = 1 if player == 2 else 2
        for i in range(7):
            temp_board = copy.deepcopy(self.board)
            if valid_move(temp_board, i):
                drop_piece(temp_board, opponent, i)
                if check_winner(temp_board) == opponent:
                    return i

        
        # No winning move, do another move
        best_score = -math.inf
        best_move = None
        for child in self.root.children:
            score = child[1].minimax(-math.inf, math.inf, depth)  # Pass alpha and beta
            if score > best_score:
                best_score = score
                best_move = child[0]

        # Random valid move if all else fails
        if best_move is None:
            valid_moves = [i for i in range(7) if valid_move(self.board, i)]
            if valid_moves:
                best_move = random.choice(valid_moves)

        return best_move

'''
game_board = []
for i in range(5):
    game_board.append([0, 0, 0, 0, 0, 0, 0])
game_board.append([0, 0, 0, 0, 0, 0, 0])
tree = GameTree(game_board, 2)

def print_board(board):
    for row in board:
        print(row)  
    print("\n")

print_board(game_board)

for i in range(5):
    drop_piece(game_board, 2, tree.get_move())
    print_board(game_board)
    drop_piece(game_board, 1, random.randint(0, 6))
'''