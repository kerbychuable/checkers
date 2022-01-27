from copy import deepcopy
from checkers.constants import BLACK, WHITE, RED, TILE_SIZE
import pygame

def draw_simulation(game, board, piece, valid_moves):
  board.draw(game.window)
  pygame.draw.circle(game.window, RED, (piece.x, piece.y), (TILE_SIZE // 2 - TILE_SIZE * 0.08), 5) # Highlight the selected piece
  game.draw_valid_moves(valid_moves.keys())
  pygame.display.update()
  pygame.time.delay(50)

def simulate_move(piece, coordinates, board, game, jumped):
  board.move(piece, coordinates[0], coordinates[1])
  if jumped: # Piece jumped over enemy piece
    board.remove(jumped)
  return board

def get_all_moves(board, color, game):
  moves = []
  for piece in board.get_all_pieces(color): # Get all pieces of active player
    valid_moves = board.get_valid_moves(piece)
    for move, jumped in valid_moves.items():
      # draw_simulation(game, board, piece, valid_moves)
      use_board = deepcopy(board) # Deep copy the board to avoid changing it in the "live" environment
      use_piece = use_board.get_piece(piece.row, piece.col)  # Get the piece to be moved on the temporary board rather than the actual to prevent changes
      new_board = simulate_move(use_piece, move, use_board, game, jumped) # Simulate the piece's move on the copied board
      moves.append(new_board)
  return moves

def minimax(board, depth, ai, game, alpha, beta):
  if depth == 0 or board.winner() != None: # Reached last node | someone won
    return board.evaluate(), board

  if ai: # AI's turn
    maxScore = float('-inf')
    best_move = None
    moves = get_all_moves(board, WHITE, game)
    moves_len = len(moves) - 1
    print('ai ' + str(moves_len))
    for index, move in enumerate(moves):
      score = minimax(move, depth-1, False, game, alpha, beta)[0] # Only get the score
      maxScore = max(maxScore, score)
      alpha = max(alpha, maxScore)
      if maxScore == score:
        best_move = move
      if index == moves_len and maxScore == '-inf':
        best_move = move
      if beta <= alpha:
        break
    return maxScore, best_move
  else: # Player's turn
    minScore = float('inf')
    best_move = None
    moves = get_all_moves(board, BLACK, game)
    moves_len = len(moves) - 1
    print('player ' + str(moves_len))
    for index, move in enumerate(moves):
      score = minimax(move, depth-1, True, game, alpha, beta)[0] # Only get the score
      minScore = min(minScore, score)
      beta = min(beta, minScore)
      if minScore == score:
        best_move = move
      if index == moves_len and minScore == 'inf':
        best_move = move
      if alpha <= beta:
        break

    return minScore, best_move

def minimax_no_ab(board, depth, ai, game):
  if depth == 0 or board.winner() != None: # Reached last node | someone won
    return board.evaluate(), board

  if ai: # AI's turn
    maxScore = float('-inf')
    best_move = None
    moves = get_all_moves(board, WHITE, game)
    moves_len = len(moves) - 1
    print('ai ' + str(moves_len))
    for index, move in enumerate(moves):
      score = minimax_no_ab(move, depth-1, False, game)[0] # Only get the score
      maxScore = max(maxScore, score)
      if maxScore == score:
        best_move = move
      if index == moves_len and maxScore == '-inf':
        best_move = move
    return maxScore, best_move
  else: # Player's turn
    minScore = float('inf')
    best_move = None
    moves = get_all_moves(board, BLACK, game)
    moves_len = len(moves) - 1
    print('player ' + str(moves_len))
    for index, move in enumerate(moves):
      score = minimax_no_ab(move, depth-1, True, game)[0] # Only get the score
      minScore = min(minScore, score)
      if minScore == score:
        best_move = move
      if index == moves_len and minScore == 'inf':
        best_move = move

    return minScore, best_move