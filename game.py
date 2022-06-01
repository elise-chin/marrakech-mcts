import numpy as np

#Orientations of the pawn
NORTH = (0, 1)
SOUTH = (0, -1)
EAST = (1, 0)
WEST = (-1, 0)


#U turns (demi tour) of the pawn
u_turn = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
}

class Board(object):
    def __init__(self, size=7):
        self.board = np.zeros((size, size))
        self.pawn = Pawn() #initialized in (3,3)
        pass

    def legal_moves(self):
        # Only legal orientations of the pawn ?
        
        #Also where we can place the rug ?
        return self.pawn.legal_orientations()

    def score(self):
        #Sum of the coins
        #+ number of squares of the boards of the player's colors
        #We can think the score as points(player1) - points(player2)
        #Such that if it's positive player 1 wins, if negative player 2 wins   
        pass

    def terminal(self):
        #If there are no more rugs
        pass

    def play(self):
        # 1. Position the pawn

        # 2. Throw the dice
        # 3. Move the pawn 
        # 4. If the pawn arrives in an opponent's rug, pay 
        # 5. Place a rug 
        pass

    def playout(self):
        """Play a random game from the current state.
        Returns the result of the random game."""
        while(True):
            #The game is over
            if self.terminal():
                #victory for player 2
                if self.score() < 0:
                    return -1
                #victory for player 1
                elif self.score() > 0:
                    return 1
                #equality
                else:
                    return 0
            
            #Non terminal : rugs are remaining
        pass


class Pawn(object):
    def __init__(self):
        #The pawn start at the center of the board
        self.x = 3
        self.y = 3
        self.orientation = NORTH
    
    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_orientation(self, orientation):
        self.orientation = orientation

    def legal_orientations(self):
        #The pawn cannot make a u turn
        orientations = [NORTH, SOUTH, EAST, WEST]
        orientations.remove(u_turn[self.orientation])
        return orientations

    def reorient(self, new_orientation):
        #What's the difference between this and set_orientation ?
        if new_orientation in self.legal_orientations():
            self.orientation = new_orientation
            #What if it is not legal ? I don't understand this part

    def move(self, new_orientation, dice):
        # 1. Position the pawn
        self.reorient(new_orientation)

        # 2. Move the pawn according to the new orientation and the dice's result

        #   Case 1: pawn does not go out from the board
        self.x = self.x + self.orientation[0] * dice 
        self.y = self.y + self.orientation[1] * dice 

        #   Case 2: pawn goes out from the board (implementation brute-force)
        if self.x < 0 or self.x > 6 or self.y < 0 or self.y > 6: 
            # Count the number of steps left after moving out of the board
            # Place the pawn at the limit of the board
            if self.orientation == NORTH:
                steps_left = self.y - 6
                self.y = 6
            elif self.orientation == EAST:
                steps_left = self.x - 6
                self.x = 6
            elif self.orientation == SOUTH:
                steps_left = -self.y
                self.y = 0
            elif self.orientation == WEST:
                steps_left = -self.x
                self.x = 0

            # Place the pawn after it has moved out from the board 
            #It counts as a step
            self.move_in_board() #modifies position and orientation
            steps_left = steps_left - 1
            
            # Move the pawn according its new orientation and the number of steps left
            self.x = self.x + self.orientation[0] * steps_left 
            self.y = self.y + self.orientation[1] * steps_left

    def move_in_board(self):
        # Bottom left corner (0,0)
        #to read again by mathilde
        if (self.x, self.y) == (0,0) and self.orientation == SOUTH:
            self.orientation = EAST
        elif (self.x, self.y) == (0,0) and self.orientation == WEST:
            self.orientation = NORTH
        # Bottom side (y = 0)
        elif self.orientation == SOUTH:
            self.x = self.x + 1 if self.x % 2 == 1 else self.x - 1
            self.orientation = NORTH
        # Right side (x = 6)
        elif self.orientation == EAST:
            self.y = self.y + 1 if self.y % 2 == 0 else self.y - 1
            self.orientation = WEST
        # Top right corner (6,6)
        elif (self.x, self.y) == (6,6) and self.orientation == EAST:
            self.orientation = SOUTH
        elif (self.x, self.y) == (6,6) and self.orientation == NORTH:
            self.orientation = WEST
        # Top side (y = 6)
        elif self.orientation == NORTH:
            self.x = self.x + 1 if self.x % 2 == 1 else self.x - 1
            self.orientation = SOUTH
        # Left side (x = 0)
        elif self.orientation == WEST:
            self.y = self.y + 1 if self.y % 2 == 0 else self.y - 1
            self.orientation = EAST

        
    
class Player(object):
    def __init__(self, id):
        self.id = id
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
            

class Rug(object):
    def __init__(self, id, color):
        self.id = id
        self.color = color
