# Logs

## 10/06/22

__DONE__

In `game.py`:

- Creation of counters (starting at 1) for each color, automatically incremented when we instanciate a new Rug of a particular color. For example:
  - Rug(RED, ...) -> 1
  - Rug(BLUE, ...) -> 1
  - Rug(RED, ...) -> 2
- `Move.valid()`
  - if-else statements because there is a hierarchy of errors. We need to satisfy a certain condition before checking the next condition. For example, need to check if the new orientation of the pawn is valid before checking if the rug is well placed, since it depends on the pawn orientation
  - 4 nested methods for clarity
- Creation of a `Position` class 
  - Why? Because we needed to check if a position (x,y) was inside or outside the board several times. It is a simple *if* statement (`x < 0 or x > 6 or y < 0 or y > 6`). We write it as a method of the class.
  - Changes in `Pawn` class. From `self.x`, `self.y` to `self.position` and then we can refer to the coordinates with`self.position.x` and `self.position.y`. Modifications in all methods accordingly.
  - In `Rug` class, we keep the position of the first and second squares separately
- `Board` class
  - `self.board` from a 2D-matrix to a 3D-matrix to assign to each square of the board an array([rug_color, rug_id]), where rug_color=0 means empty square. 
  
__TODO__

- [x] Test `Pawn.move()` --> 11/06/22
- [ ] Test `Move.valid()`
- [ ] How to deal with the dice?