from game import *

# Set up
board = Board()
board.board[3,3] = np.array([RED, 1])
board.board[4,3] = np.array([RED, 1])
board.board[4,2] = np.array([RED, 1])
board.board[5,3] = np.array([RED, 1])
board.board[5,4] = np.array([RED, 1])

rug_red_1 = Rug(RED, Position(0,0), Position(1,0))
rug_blue_1 = Rug(BLUE, Position(1,1), Position(1,2))
rug_blue_2 = Rug(BLUE, Position(1,2), Position(2,2))

dice = 2

def test_pawn_set_position():
    pawn = Pawn()
    pawn.set_position(5,5)
    assert pawn.position.x == 5 and pawn.position.y == 5

def test_pawn_legal_orientations():
    pawn = Pawn()
    orientations = pawn.legal_orientations()
    expected_orientations = [NORTH, EAST, WEST]
    assert orientations == expected_orientations

def test_pawn_move_case_1():
    pawn = Pawn() # (3, 3, N)

    # NORTH
    pawn.set_position(3, 3)
    pawn.set_orientation(NORTH)
    pawn.move(1)
    assert pawn.position.x == 3 and pawn.position.y == 4
    
    # EAST
    pawn.set_position(3, 3)
    pawn.set_orientation(EAST)
    pawn.move(1)
    assert pawn.position.x == 4 and pawn.position.y == 3
    
    # WEST
    pawn.set_position(3, 3)
    pawn.set_orientation(WEST)
    pawn.move(1)
    assert pawn.position.x == 2 and pawn.position.y == 3 

def test_pawn_move_case_2():
    pawn = Pawn() # (3, 3, N)

    # Bottom left corner (0, 0)
    pawn.set_position(0, 0)  
    pawn.set_orientation(WEST)
    pawn.move(dice=1)
    assert pawn.position.x == 0 and pawn.position.y == 0 and pawn.orientation == NORTH
    
    # Top right corner (6, 6)
    pawn.set_position(4, 6)
    pawn.set_orientation(EAST)
    pawn.move(dice=3)
    assert pawn.position.x == 6 and pawn.position.y == 6 and pawn.orientation == SOUTH

    # Bottom side
    pawn.set_position(3, 1)
    pawn.set_orientation(SOUTH)
    pawn.move(dice=2)
    assert pawn.position.x == 4 and pawn.position.y == 0 and pawn.orientation == NORTH
    
    # Right side
    pawn.set_position(4, 2)
    pawn.set_orientation(EAST)
    pawn.move(dice=3)
    assert pawn.position.x == 6 and pawn.position.y == 3 and pawn.orientation == WEST
    
    # Top side
    pawn.set_position(4, 6)
    pawn.set_orientation(NORTH)
    pawn.move(dice=3)
    assert pawn.position.x == 5 and pawn.position.y == 4 and pawn.orientation == SOUTH

    # Left side
    pawn.set_position(1, 4)
    pawn.set_orientation(WEST)
    pawn.move(dice=3)
    assert pawn.position.x == 1 and pawn.position.y == 3 and pawn.orientation == EAST

def test_get_nb_same_color_squares():
    n = board.pawn.get_nb_same_color_squares(board)
    assert n == 5 