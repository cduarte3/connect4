import math
import copy
import random

class Node:
    def __init__(self, board, parent = None):
        self.board = board
        self.parent = parent
        self.children = []
        self.score = 0
        self.visited = 0


class ConnectFour:
    def __init__(self):
        self.game_board = []
        for i in range(6):
            self.game_board.append([0, 0, 0, 0, 0, 0, 0])
        self.winner = 0

    def print_board(self):
        for row in self.game_board:
            print(row)  
        print("\n")

    def drop_piece(self, player, col):
        for i in reversed(range(6)):
            if self.game_board[i][col] == 0:
                self.game_board[i][col] = player
                return True
        return False


    def valid_move(self, col):
        if col > 6 or col < 0:
            return False
        return self.game_board[0][col] == 0
    
    def check_winner(self):
        # Check horizontal locations for win
        for row in range(6):
            for col in range(4):
                if self.game_board[row][col] == self.game_board[row][col+1] == self.game_board[row][col+2] == self.game_board[row][col+3] != 0:
                    return self.game_board[row][col]

        # Check vertical locations for win
        for col in range(7):
            for row in range(3):
                if self.game_board[row][col] == self.game_board[row+1][col] == self.game_board[row+2][col] == self.game_board[row+3][col] != 0:
                    return self.game_board[row][col]


    # The following 2 for loops were helped created with the help of github copilot
    # they are not all my work, and I will not be claiming it as such

    # --------------------------------------------------------- #
        # Check positively sloped diagonals
        for row in range(3):
            for col in range(4):
                if self.game_board[row][col] == self.game_board[row+1][col+1] == self.game_board[row+2][col+2] == self.game_board[row+3][col+3] != 0:
                    return self.game_board[row][col]

        # Check negatively sloped diagonals
        for row in range(3, 6):
            for col in range(4):
                if self.game_board[row][col] == self.game_board[row-1][col+1] == self.game_board[row-2][col+2] == self.game_board[row-3][col+3] != 0:
                    return self.game_board[row][col]
    # --------------------------------------------------------- #

        return 0  # No winner

class MonteCarloSearch:
    def __init__(self, board):
        self.root = Node(board)
        # self.player = player

    def selection(self, node, player):

        if not node.children:
            return node

        # returns node to be searched if it has not been visited
        for child in node.children:
            if child.visited == 0:
                return child

        best_move_index = self.best_move(player)
        if best_move_index is not None:
            return node.children[best_move_index]
        else:
            return node

    def expansion(self, node, player):
        if not node.children:
            self.generate_possible_moves(node, player)

    def simulation(self, node, height):
        # create temporary copy of game node
        temp_state = copy.deepcopy(node)
        player = 1

        # simulate the game until the end
        for i in range (height):
            valid_moves = [i for i in range(7) if temp_state.board.valid_move(i)]
        
        # If there are no valid moves, the game is over
            if not valid_moves:
                break
        # Choose a random valid move and apply it
            move = random.choice(valid_moves)
            temp_state.board.drop_piece(player, move)

        # Switch the active player
            player = 1 if player == 2 else 2

        # Determine the result of the game
        result = temp_state.board.check_winner()
        if result == player:
            node.score += 1
        elif result != 0:
            node.score -= 1

        return result

    def backpropagation(self, node):
        # Start from the terminal node and move to the root
        while node is not None:
            # Increment the visit count
            node.visited += 1

            # Move to the parent
            node = node.parent

    def best_move(self, player):

        # Check for a winning move
        for i in range(7):
            temp_state = copy.deepcopy(self.root)
            if temp_state.board.valid_move(i):
                temp_state.board.drop_piece(player, i)
                if temp_state.board.check_winner() == player:
                    return i
                
        # Check for a winning move for the opponent
        opponent = 1 if player == 2 else 2
        for i in range(7):
            temp_state = copy.deepcopy(self.root)
            if temp_state.board.valid_move(i):
                temp_state.board.drop_piece(opponent, i)
                if temp_state.board.check_winner() == opponent:
                    return i

        # no winning move, do another move
        best_score = -math.inf
        best_move = None

        for i, child in enumerate(self.root.children):
            if child.score > best_score:
                best_score = child.score
                best_move = i

        if best_move is None:
        # If no best move is found, return a random valid move
            valid_moves = [i for i in range(7) if self.root.board.valid_move(i)]
            if valid_moves:
                return random.choice(valid_moves)

        return best_move

    def mcts(self, player, simulations = 100, height = 10):

        for i in range(simulations):
            # Start from the root
            node = self.root

            # Selection
            node = self.selection(node, player)

            # Expansion
            self.expansion(node, player)

            # Simulation
            node.score += self.simulation(node, height)

            # Backpropagation
            self.backpropagation(node)

        # Return the best move
        move = self.best_move(player)
        self.root.children = []
        return move
    
    def generate_possible_moves(self, node, player):
        # copy the current state without modifying original
        # this allows for multiple moves without placing a piece on the original board
        temp_state = copy.deepcopy(node)
        temp_array = []
        for i in range (7):
            if temp_state.board.valid_move(i):
                temp_state.board.drop_piece(player, i)
                temp_state.parent = node
                temp_state.visited = 0
                temp_array.append(temp_state)
                temp_state = copy.deepcopy(node)
        node.children = temp_array
        node.visited += 1

'''
# Initialize the game and the MCST
game = ConnectFour()
MC = MonteCarloSearch(game)

# Start the game loop
player = 1
while True:
    # Player 1's turn
    if player == 1:
        game.drop_piece(player)
        print("")
        game.print_board()
    # Player 2's turn
    else:
        # Use the MCST to determine the best move
        best_move = MC.mcts(player)
        game.drop_piece(player, best_move)
        print("")
        game.print_board()

    # Check if the game is over
    winner = game.check_winner()
    if winner != 0:
        break

    # Switch the active player
    player = 1 if player == 2 else 2

# Announce the result of the game
if winner == 1:
    print("Player 1 wins!")
elif winner == 2:
    print("Player 2 wins!")
else:
    print("It's a draw!")
'''