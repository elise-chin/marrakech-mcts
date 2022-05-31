import game

# Pawn

def test_pawn_set_position():
    pawn = game.Pawn()
    pawn.set_position(5,5)
    assert pawn.x == 5 and pawn.y == 5

def test_pawn_legal_orientations():
    pawn = game.Pawn()
    orientations = pawn.legal_orientations()
    expected_orientations = [game.NORTH, game.EAST, game.WEST]
    assert orientations == expected_orientations

def test_pawn_move_1():
    pawn = game.Pawn() # (3, 3, N)
    dice = 1

    # NORTH
    pawn.set_position(3, 3)
    pawn.set_orientation(game.NORTH)
    pawn.move(game.NORTH, dice)
    assert pawn.x == 3 and pawn.y == 4 and pawn.orientation == game.NORTH
    
    # EAST
    pawn.set_position(3, 3)
    pawn.set_orientation(game.NORTH)
    pawn.move(game.EAST, dice)
    assert pawn.x == 4 and pawn.y == 3 and pawn.orientation == game.EAST
    
    # WEST
    pawn.set_position(3, 3)
    pawn.set_orientation(game.NORTH)
    pawn.move(game.WEST, dice)
    assert pawn.x == 2 and pawn.y == 3 and pawn.orientation == game.WEST

def test_pawn_move_2():
    pawn = game.Pawn() # (3, 3, N)

    pawn.set_position(0, 0)  
    pawn.set_orientation(game.NORTH)
    pawn.move(game.WEST, dice=1)
    assert pawn.x == 0 and pawn.y == 1 and pawn.orientation == game.NORTH
    
    pawn.set_position(3, 1)
    pawn.set_orientation(game.WEST)
    pawn.move(game.SOUTH, dice=2)
    assert pawn.x == 4 and pawn.y == 1 and pawn.orientation == game.NORTH
    
    pawn.set_position(4, 6)
    pawn.set_orientation(game.SOUTH)
    pawn.move(game.EAST, dice=3)
    print(pawn.x, pawn.y, pawn.orientation)
    assert pawn.x == 6 and pawn.y == 5 and pawn.orientation == game.SOUTH