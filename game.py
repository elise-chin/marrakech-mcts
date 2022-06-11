import numpy as np
from itertools import cycle, count
import random 

###########################
# --- GLOBAL VARIABLES ---
###########################

# Colors of the rugs
RED = 1 #player 1
BLUE = 2 #player 2
PINK = 3 #player 1
GREEN = 4 #player 2

colors = [RED, BLUE, PINK, GREEN]
color_cycle = cycle(colors)
#next(color_cycle) gives the next color to play

# Counters for each color to increment when instanciating new Rug, starts at 1
red_counter = count(1)
blue_counter = count(1)
pink_counter = count(1)
green_counter = count(1)

# Orientations of the pawn
NORTH = (0, 1)
SOUTH = (0, -1)
EAST = (1, 0)
WEST = (-1, 0)

orientations_int2str = {NORTH: "north", SOUTH: "south", EAST: "east", WEST: "west"}
colors_int2str = {RED: "red", BLUE: "blue", PINK: "pink", GREEN: "green"}

# U turns (demi tour) of the pawn
u_turn = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
}

####################
# --- FUNCTIONS ---
####################

def adjacent_coord(coord):
    """Returns all squares' coordinates (x', y') adjacent to square of coordinate `coord` (x, y)

    Args:
        coord (tuple of int): coordinate (x,y) of the square of interest

    Returns:
        list of tuples: list of adjacent positions
    """
    x, y = coord
    left = (x-1, y)
    right = (x+1, y)
    up = (x, y+1)
    down = (x, y-1)
    L = [left, right, up, down]

    if x == 0:
        L.remove(left)
    if y == 0:
        L.remove(down)
    if x == 6:
        L.remove(right)
    if y == 6:
        L.remove(up)

    return L

##################
# --- CLASSES ---
##################

class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x},{self.y})'

    def get_coord(self):
        return self.x, self.y

    def is_out_of_board(self, board_limit):
        """Check if the position of coordinates (x,y) is outside the board.
        
        Args:
            board_limit (int): board limit in terms of indices 
                               (e.g. if board is of size 7, then board_limit = 6)
        """

        if self.x < 0 or self.x > board_limit or self.y < 0 or self.y > board_limit:
            return True
        return False


class Rug(object):

    def __init__(self, color, sq1_pos, sq2_pos):
        self.color = color
        self.sq1_pos = sq1_pos 
        self.sq2_pos = sq2_pos
        self.id = self.increment_id()

    def __str__(self):
        return f"Rug {colors_int2str[self.color]} of id {self.id} at position ({self.sq1_pos}, {self.sq2_pos})."

    def increment_id(self):
        if self.color == RED:
            return next(red_counter)
        if self.color == BLUE:
            return next(blue_counter)
        if self.color == PINK:
            return next(pink_counter)
        if self.color == GREEN:
            return next(green_counter)

class Pawn(object):
    def __init__(self):
        # The pawn start at the center of the board
        self.position = Position(3, 3)
        self.orientation = NORTH
    
    def set_position(self, x, y):
        self.position.x = x
        self.position.y = y

    def set_orientation(self, orientation):
        self.orientation = orientation

    def legal_orientations(self):
        # The pawn cannot make a u turn
        orientations = [NORTH, SOUTH, EAST, WEST]
        orientations.remove(u_turn[self.orientation])
        return orientations

    def move(self, dice):
        # Move the pawn according to the dice's result

        #   Case 1: pawn does not go out from the board
        self.position.x = self.position.x + self.orientation[0] * dice 
        self.position.y = self.position.y + self.orientation[1] * dice 

        #   Case 2: pawn goes out from the board (implementation brute-force)
        if self.position.is_out_of_board(board_limit=6): 
            # Count the number of steps left after moving out of the board
            # Place the pawn at the limit of the board
            if self.orientation == NORTH:
                steps_left = self.position.y - 6
                self.position.y = 6
            elif self.orientation == EAST:
                steps_left = self.position.x - 6
                self.position.x = 6
            elif self.orientation == SOUTH:
                steps_left = -self.position.y
                self.position.y = 0
            elif self.orientation == WEST:
                steps_left = -self.position.x
                self.position.x = 0

            # Place the pawn after it has moved out from the board 
            # It counts as a step
            self.move_in_board() # Modifies position and orientation
            steps_left = steps_left - 1
            
            # Move the pawn according to the number of steps left
            self.position.x = self.position.x + self.orientation[0] * steps_left 
            self.position.y = self.position.y + self.orientation[1] * steps_left

    def move_in_board(self):
        # Bottom left corner (0,0)
        #to read again by mathilde
        if (self.position.x, self.position.y) == (0,0) and self.orientation == SOUTH:
            self.orientation = EAST
        elif (self.position.x, self.position.y) == (0,0) and self.orientation == WEST:
            self.orientation = NORTH
        # Top right corner (6,6)
        elif (self.position.x, self.position.y) == (6,6) and self.orientation == EAST:
            self.orientation = SOUTH
        elif (self.position.x, self.position.y) == (6,6) and self.orientation == NORTH:
            self.orientation = WEST
        # Bottom side (y = 0)
        elif self.orientation == SOUTH:
            self.position.x = self.position.x + 1 if self.position.x % 2 == 1 else self.position.x - 1
            self.orientation = NORTH
        # Right side (x = 6)
        elif self.orientation == EAST:
            self.position.y = self.position.y + 1 if self.position.y % 2 == 0 else self.position.y - 1
            self.orientation = WEST
        # Top side (y = 6)
        elif self.orientation == NORTH:
            self.position.x = self.position.x + 1 if self.position.x % 2 == 0 else self.position.x - 1
            self.orientation = SOUTH
        # Left side (x = 0)
        elif self.orientation == WEST:
            self.position.y = self.position.y + 1 if self.position.y % 2 == 1 else self.position.y - 1
            self.orientation = EAST
  
class Player(object):
    def __init__(self, id, colors):
        self.id = id
        self.colors = colors
        #self.rugs : liste de tapis, si deux joueurs, deux couleurs
        #or rugs1_left = 15 and rugs2_left = 15 ? 
        #Or explicit list of rugs, idk
        #We need to manage the alternation of colors
        
        self.coins = 30
    
    def pay(self, amount, opponent_player):
        #I think that we should just focus on the 2 players game
        #Is the player doesn't have enough money
        if self.coins - amount < 0:
            opponent_player.coins += self.coins
            self.coins = 0
        #If the player can pay
        else:
            self.coins -= amount
            opponent_player.coins += amount
  
class Move(object):
    def __init__(self, pawn, new_orientation, rug, dice):
        self.pawn = pawn
        self.new_orientation = new_orientation
        self.rug = rug
        self.dice = dice
        
    def __str__(self):
        de = f'The dice indicates {self.dice}.\n'
        if self.pawn.orientation == self.new_orientation:
            assam = f'The pawn stays in his orientation ({orientations_int2str[self.pawn.orientation]}).\n'
        else:
            assam = f'The pawn is reoriented from {orientations_int2str[self.pawn.orientation]} to {orientations_int2str[self.new_orientation]}.\n'
        tapis = f"A rug of color {colors_int2str[self.rug.color]} (id={self.rug.id}) is placed at ({self.rug.sq1_pos}, {self.rug.sq2_pos})."
        result = de + assam + tapis
        return result
        
    def is_pawn_new_orientation_valid(self):
        # It is valid if no u-turn
        return self.new_orientation in self.pawn.legal_orientations()
    
    def is_rug_adjacent_to_pawn(self):
        # Check if adjacent to pawn and also not on the pawn's position

        # List of all valid coordinates around the pawn
        x, y = self.pawn.position.x, self.pawn.position.y
        init_valid_coord = adjacent_coord((x, y))
        valid_coord = init_valid_coord.copy()
        for coord in init_valid_coord:
            valid_coord.extend(adjacent_coord(coord))
        set_valid_coord = set(valid_coord)
        set_valid_coord.remove((x, y))

        # Check if the rug's both squares are in the set
        if self.rug.sq1_pos.get_coord() and self.rug.sq2_pos.get_coord() in set_valid_coord:
            return True
        return False

    def is_rug_covering_another_rug(self, board):
        # Rug's new placement is valid if it doesn't cover another rug
        # We need to check if the both squares are covered by the same rug (same color and same id)
        sq1_color_and_id = board.board[self.rug.sq1_pos.x, self.rug.sq1_pos.y]
        sq2_color_and_id = board.board[self.rug.sq2_pos.x, self.rug.sq2_pos.y]
        print(sq1_color_and_id, sq2_color_and_id)
        if (sq1_color_and_id == sq2_color_and_id).all():
            return True
        return False

    def valid(self, board):
        if not self.is_pawn_new_orientation_valid():
            return False
        elif not self.is_rug_adjacent_to_pawn():
            return False
        elif self.is_rug_covering_another_rug(board):
            return False
        return True

class Board(object):
    def __init__(self, size=7):
        self.size = size
        self.board = np.zeros((size, size, 2))
        self.pawn = Pawn() # Initialize at (3,3)
        self.players = [Player(0, [RED, PINK]), Player(1, [BLUE, GREEN])]
        self.current_player = self.players[0]
        self.current_color = RED # Start with first color of first player
        
        
    def __str__(self):
        #print(self.board)
        pass

    def throw_dice(self):
        dice = [1, 2, 2, 3, 3, 4]
        return random.choice(dice)
        
    def legal_moves(self, dice):
        """
        A reverifier et remodifier eventuellemnt !
        j'ai juste fait pour voir l'idee globae mais c'est surement tres ameliorable
        """
        moves = []
        # faire la liste de tous les moves possibles
        for orientation in [NORTH, SOUTH, EAST, WEST]:
            #pour chaque case autour de Assam
            for sq1_coord in adjacent_coord((self.pawn.position.x, self.pawn.position.y)):
                #pour chaque case autour de ces cases:
                for sq2_coord in adjacent_coord(sq2_coord):
                    rug = Rug(self.current_color, sq1_coord, sq2_coord)
                    m = Move(self.pawn, orientation, rug, dice) 
                    # pour chacun, verifier s'il est légal
                    if m.valid(self):
                        moves.append(m)
        #s'il est légal on l'ajoute à la liste renvoyée
        return moves

    def score(self):
        #Sum of the coins
        #+ number of squares of the boards of the player's colors
        #We can think the score as points(player1) - points(player2)
        #Such that if it's positive player 1 wins, if negative player 2 wins   
        pass

    def terminal(self):
        #If there are no more rugs
        pass

    def play(self, move):
        # 1. Orientate the pawn
        self.pawn.set_orientation(move.new_orientation)

        # 2. Place a rug
        self.board[self.rug.sq1_pos.x, self.rug.sq1_pos.y] = np.array([self.rug.color, self.rug.id])
        self.board[self.rug.sq2_pos.x, self.rug.sq2_pos.y] = np.array([self.rug.color, self.rug.id])

    def playout(self):
        """Play a random game from the current state.
        Returns the result of the random game."""

        while(True):
            moves = self.legal_moves()

            # If the game is over
            if self.terminal():
                # Victory for player 2
                if self.score() < 0:
                    return -1
                # Victory for player 1
                elif self.score() > 0:
                    return 1
                # Draw
                else:
                    return 0
            
            # The game isn't over: rugs are remaining
            # We play another move chosen randomly
            n = random.randint(0, len(moves)-1)
            self.play(moves[n])

            # Throw the dice for the current player
            dice_result = self.throw_dice()

            # Move the pawn
            self.pawn.move(dice_result)

            # Pay opponent
            # Pay only if the pawn is on an opponent color
            current_square_color = self.board[self.pawn.position.x, self.pawn.position.y][0]
            opponent_player_id = abs(self.current_player.id - 1)
            if current_square_color not in self.current_player.colors:
                amount = 0 #### COMMENT LE NB DE CASES ADJ DE LA COULEUR OU SE TROUVE LE PION
                self.current_player.pay(amount, self.players[opponent_player_id])

            # Change turn 
            self.current_player = self.players[opponent_player_id]
            self.current_color = next(color_cycle)