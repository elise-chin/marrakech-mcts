import game

def test_pawn_set_position():
    pawn = game.Pawn()
    pawn.set_position(5,5)
    assert pawn.position.x == 5 and pawn.position.y == 5

def test_pawn_legal_orientations():
    pawn = game.Pawn()
    orientations = pawn.legal_orientations()
    expected_orientations = [game.NORTH, game.EAST, game.WEST]
    assert orientations == expected_orientations

def test_pawn_move_case_1():
    pawn = game.Pawn() # (3, 3, N)
    dice = 1

    # NORTH
    pawn.set_position(3, 3)
    pawn.set_orientation(game.NORTH)
    pawn.move(game.NORTH, dice)
    assert pawn.position.x == 3 and pawn.position.y == 4 and pawn.orientation == game.NORTH
    
    # EAST
    pawn.set_position(3, 3)
    pawn.set_orientation(game.NORTH)
    pawn.move(game.EAST, dice)
    assert pawn.position.x == 4 and pawn.position.y == 3 and pawn.orientation == game.EAST
    
    # WEST
    pawn.set_position(3, 3)
    pawn.set_orientation(game.NORTH)
    pawn.move(game.WEST, dice)
    assert pawn.position.x == 2 and pawn.position.y == 3 and pawn.orientation == game.WEST

def test_pawn_move_case_2():
    pawn = game.Pawn() # (3, 3, N)

    # Bottom left corner (0, 0)
    pawn.set_position(0, 0)  
    pawn.set_orientation(game.NORTH)
    pawn.move(game.WEST, dice=1)
    assert pawn.position.x == 0 and pawn.position.y == 0 and pawn.orientation == game.NORTH
    
    # Top right corner (6, 6)
    pawn.set_position(4, 6)
    pawn.set_orientation(game.SOUTH)
    pawn.move(game.EAST, dice=3)
    assert pawn.position.x == 6 and pawn.position.y == 6 and pawn.orientation == game.SOUTH

    # Bottom side
    pawn.set_position(3, 1)
    pawn.set_orientation(game.WEST)
    pawn.move(game.SOUTH, dice=2)
    assert pawn.position.x == 4 and pawn.position.y == 0 and pawn.orientation == game.NORTH
    
    # Right side
    pawn.set_position(4, 2)
    pawn.set_orientation(game.SOUTH)
    pawn.move(game.EAST, dice=3)
    assert pawn.position.x == 6 and pawn.position.y == 3 and pawn.orientation == game.WEST
    
    # Top side
    pawn.set_position(4, 6)
    pawn.set_orientation(game.EAST)
    pawn.move(game.NORTH, dice=3)
    assert pawn.position.x == 5 and pawn.position.y == 4 and pawn.orientation == game.SOUTH

    # Left side
    pawn.set_position(1, 4)
    pawn.set_orientation(game.SOUTH)
    pawn.move(game.WEST, dice=3)
    assert pawn.position.x == 1 and pawn.position.y == 3 and pawn.orientation == game.EAST
    