import pygame
from .constants import BROWN, LIGHTBROWN, ROWS, COLS, TILE_SIZE, BLACK, WHITE
from .piece import Piece

class Board:
  def __init__(self):
    self.board = []
    self.black_rem = self.white_rem = 12
    self.black_kings = self.white_kings = 0
    self.new_board()

  def new_board(self):
    for row in range(ROWS):
      self.board.append([])
      for col in range(COLS):
        if col % 2 == ((row + 1) % 2): # Check if on a brown tile
          if row < 3: # White side
            self.board[row].append(Piece(row, col, WHITE))
          elif row > 4: # Black side
            self.board[row].append(Piece(row, col, BLACK))
          else: # Empty tiles
            self.board[row].append(0)
        else: # On a light brown tile (should be empty)
          self.board[row].append(0)

  def draw_tiles(self, window): # Draw outline (grid)
    window.fill(BROWN)
    for row in range(ROWS):
      for col in range(row % 2, COLS, 2):
        pygame.draw.rect(window, LIGHTBROWN, (row * TILE_SIZE, col * TILE_SIZE, TILE_SIZE, TILE_SIZE)) # x, y, width, height

  def draw(self, window): # Draw pieces on the board
    self.draw_tiles(window)
    for row in range(ROWS):
      for col in range(COLS):
        piece = self.board[row][col]
        if piece != 0:
          piece.draw(window)
  
  def get_piece(self, row, col): # check a tile and return the state
    return self.board[row][col]

  def get_all_pieces(self, color):
    pieces = []
    for row in self.board: # check each row
      for tile in row: # check each tile (column)
        if tile != 0 and tile.color == color: # check if there is a piece and it belongs to the active player
          pieces.append(tile)
    return pieces

  def winner(self): # Check for game winner
    if self.white_rem <= 0:
      return "Black"
    elif self.black_rem <= 0:
      return "White"
    return None

  def remove(self, pieces): # Remove a piece from the board (eaten)
    for piece in pieces:
      if piece != 0:
        self.board[piece.row][piece.col] = 0
        if piece.color == BLACK:
          self.black_rem -= 1
        else:
          self.white_rem -= 1

  def move(self, piece, row, col):
    self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col] # Update board
    piece.move(row, col) # Update piece's internal knowledge of its location

    if row == ROWS-1 or row == 0: # piece reached the end
      piece.set_king()
      if piece.color == BLACK:
        self.black_kings += 1
      else:
        self.white_kings += 1

  def get_valid_moves(self, piece):
    moves = {}
    left = piece.col - 1
    right = piece.col + 1
    row = piece.row

    if piece.color == BLACK or piece.king: # Move up
      moves.update(self.traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
      moves.update(self.traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
    if piece.color == WHITE or piece.king: # Move down
      moves.update(self.traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
      moves.update(self.traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

    return moves
  
  def traverse_left(self, start, stop, step, color, left, jumped=[]):
    moves = {}
    last = []

    for curr_row in range(start, stop, step):
      if left < 0: # Reached the edge of the board
        break

      current = self.board[curr_row][left] # Get piece in the new coordinates

      if current == 0: # Empty tile
        if jumped and not last: # Prevent additional move after jumping (except if there is another piece to jump over)
          break
        elif jumped: # Jumped over a piece
          moves[(curr_row, left)] = last + jumped
        else: # Moved to an empty tile only
          moves[(curr_row, left)] = last

        if last: # Jumped over enemy piece, check for possible additional jumps
          if step == -1: # Moving up
            row = max(curr_row - 3, -1)
          else: # Moving down
            row = min(curr_row + 3, ROWS)
          moves.update(self.traverse_left(curr_row + step, row, step, color, left - 1, jumped=last))
          moves.update(self.traverse_right(curr_row + step, row, step, color, left + 1, jumped=last))
        break # prevent additional move (move 2 empty tiles in 1 turn)
      elif current.color == color: # Own piece
        break # Ignore, not a valid move
      else:
        last = [current] # Enemy piece
      
      left -= 1
    
    return moves

  def traverse_right(self, start, stop, step, color, right, jumped=[]):
    moves = {}
    last = []

    for curr_row in range(start, stop, step):
      if right >= COLS: # Reached the edge of the board
        break

      current = self.board[curr_row][right] # Get piece in the new coordinates

      if current == 0: # Empty tile
        if jumped and not last: # Prevent additional move after jumping (except if there is another piece to jump over)
          break
        elif jumped: # Jumped over a piece
          moves[(curr_row, right)] = last + jumped
        else: # Moved to an empty tile only
          moves[(curr_row, right)] = last

        if last: # Jumped over enemy piece, check for possible additional jumps
          if step == -1: # Moving up
            row = max(curr_row - 3, -1)
          else: # Moving down
            row = min(curr_row + 3, ROWS)
          moves.update(self.traverse_left(curr_row + step, row, step, color, right - 1, jumped=last))
          moves.update(self.traverse_right(curr_row + step, row, step, color, right + 1, jumped=last))
        break # prevent additional move (move 2 empty tiles in 1 turn)
      elif current.color == color: # Own piece
        break # Ignore, not a valid move
      else:
        last = [current] # Enemy piece
      
      right += 1
    
    return moves

  def evaluate(self):
    return self.white_rem - self.black_rem + (self.white_kings * 0.5 - self.black_kings * 0.5)