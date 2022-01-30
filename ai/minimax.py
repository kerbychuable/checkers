from copy import deepcopy
from checkers.constants import BLACK, WHITE, RED, TILE_SIZE
import pygame

def simulate_move(piece, coordinates, board, jumped):
  board.move(piece, coordinates[0], coordinates[1])
  if jumped: # Piece jumped over enemy piece
    board.remove(jumped)
  return board

def get_all_moves(board, color):
  moves = []
  for piece in board.get_all_pieces(color): # Get all pieces of active player
    valid_moves = board.get_valid_moves(piece)
    for move, jumped in valid_moves.items():
      use_board = deepcopy(board) # Deep copy the board to avoid changing it in the "live" environment
      use_piece = use_board.get_piece(piece.row, piece.col)  # Get the piece to be moved on the temporary board rather than the actual to prevent changes
      new_board = simulate_move(use_piece, move, use_board, jumped) # Simulate the piece's move on the copied board
      moves.append(new_board)
  return moves

def minimax(board, depth, maximizer, alpha, beta):
  if depth == 0 or board.winner() != None: # Reached last node | someone won
    return board.evaluate(), board

  best_move = None
  if maximizer: # AI's turn
    maxScore = float('-inf')
    moves = get_all_moves(board, WHITE)
    for move in moves:
      score = minimax(move, depth-1, False, alpha, beta)[0] # Only get the score
      maxScore = max(maxScore, score)
      alpha = max(alpha, maxScore)
      if maxScore == score:
        best_move = move
      if beta <= alpha:
        break
    return maxScore, best_move
  else: # Player's turn
    minScore = float('inf')
    moves = get_all_moves(board, BLACK)
    for move in moves:
      score = minimax(move, depth-1, True, alpha, beta)[0] # Only get the score
      minScore = min(minScore, score)
      beta = min(beta, minScore)
      if minScore == score:
        best_move = move
      if alpha <= beta:
        break

    return minScore, best_move