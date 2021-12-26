from .constants import BLACK, WHITE, GREY, TILE_SIZE
import pygame

class Piece:
  PADDING = 15 # Piece padding
  OUTLINE = 2 # Outline width

  def __init__(self, row, col, color):
    self.row = row
    self.col = col
    self.color = color
    self.king = False
    self.x = 0
    self.y = 0
    self.set_pos()

    def set_pos(self):
      self.x = TILE_SIZE * self.col + TILE_SIZE // 2
      self.y = TILE_SIZE * self.row + TILE_SIZE // 2

    def set_king(self):
      self.king = True
    
    def draw(self, window):
      circRadius = TILE_SIZE // 2 - PADDING
      pygame.draw.circle(window, GREY, (self.x, self.y), circRadius + OUTLINE) # Draw piece outline
      pygame.draw.circle(window, self.color, (self.x, self.y), circRadius) # Draw piece
      # if self.king: # King piece
      #   win.blit()

    def move(self, row, col):
      self.row = row
      self.col = col
      self.set_pos()
    
    def __repr__(self):
      return str(self.color)