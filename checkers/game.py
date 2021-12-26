import pygame
from .constants import BLACK, WHITE, BLUE, TILE_SIZE
from checkers.board import Board

class Game:
  def __init__(self, window):
    self.window = window

  def init(self):
    self.board = Board()
    self.turn = BLACK
    self.selected = None
    self.valid_moves = {}

  def winner(self):
    return self.board.winner()

  def reset(self):
    self.init()

  def select(self, row, col):
    if self.selected: # A piece is already selected, try to move to selected tile
      result = self.move(row, col) # Move the piece
      if not result: # Not a valid tile to move on
        self.selected = None # Unselect the piece
        self.select(row, col) # Select the tile clicked and check if a piece exists
    
    piece = self.board.get_piece(row, col)
    if piece != 0 and piece.color == self.turn: # Check if active player's piece is selected
      self.selected = piece
      self.valid_moves = self.board.get_valid_moves(piece) # Get the piece's valid moves
      return True # A piece has been selected
    return False # Active player did not select its own piece

  def move(self, row, col):
    piece = self.board.get_piece(row, col)
    if self.selected and piece == 0 and (row, col) in self.valid_moves: # Active player is trying to move its piece to an empty tile
      self.board.move(self.selected, row, col)
      jumped = self.valid_moves[(row, col)]
      if jumped:
        self.board.remove(jumped)
      self.end_turn()
    else:
      return False
    return True

  def end_turn(self):
    self.valid_moves = {}
    if self.turn == BLACK:
      self.turn = WHITE
    else:
      self.turn = BLACK
  
  def get_board(self):
    return self.board

  def draw_valid_moves(self, moves):
    for move in moves:
      row, col = move
      pygame.draw.circle(self.window, BLUE, (col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 4)

  def update(self):
    self.board.draw(self.window)
    self.draw_valid_moves(self.valid_moves)
    pygame.display.update()