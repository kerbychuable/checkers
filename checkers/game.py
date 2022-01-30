import pygame
from .constants import BLACK, WHITE, BLUE, TILE_SIZE, RED
from checkers.board import Board

class Game:
  def __init__(self, window):
    self.window = window
    self.init()

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
      self.selected = None # Unselect the piece
      self.valid_moves = {}
      if not result: # Not a valid tile to move on
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
  
  def ai_move(self, board):
    self.board = board
    self.end_turn()
  
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
      pygame.draw.circle(self.window, BLUE, (col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 8)

  def update(self):
    # self.board.ascii_draw()
    self.board.draw(self.window)
    if self.selected:
      pygame.draw.circle(self.window, RED, (self.selected.x, self.selected.y), (TILE_SIZE // 2 - TILE_SIZE * 0.08), 5) # Highlight the selected piece
      self.draw_valid_moves(self.valid_moves)
    pygame.display.update()