from copy import deepcopy
from checkers.constants import BLACK, WHITE, RED, TILE_SIZE
import pygame

cuts = nodes = states = 0
killer_moves = []

def simulate_move(piece, coordinates, board, jumped):
  board.move(piece, coordinates[0], coordinates[1])
  if jumped: # Piece/s jumped over
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

def minimax(board, depth, root_depth, maximizer, alpha, beta):
  if depth == 0 or board.winner() != None: # Reached last node | someone won
    return board.evaluate(), board

  global cuts
  global nodes
  global states

  if depth == root_depth:
    cuts = nodes = states = 0

  best_move = None
  if maximizer: # AI's turn
    maxScore = float('-inf')
    moves = get_all_moves(board, WHITE)
    nodes += len(moves)

    for move in moves:
      states += 1
      score = minimax(move, depth-1, root_depth, False, alpha, beta)[0] # Only get the score
      maxScore = max(maxScore, score)
      alpha = max(alpha, maxScore)
      if maxScore == score:
        best_move = move
      if beta <= alpha:
        cuts += 1
        break
    return maxScore, best_move, cuts, nodes, states
  else: # Player's turn
    minScore = float('inf')
    moves = get_all_moves(board, BLACK)
    nodes += len(moves)

    for move in moves:
      states += 1
      score = minimax(move, depth-1, root_depth, True, alpha, beta)[0] # Only get the score
      minScore = min(minScore, score)
      beta = min(beta, minScore)
      if minScore == score:
        best_move = move
      if beta <= alpha:
        cuts += 1
        break

    return minScore, best_move, cuts, nodes, states

def move_ordering(board, depth, root_depth, maximizer, alpha, beta, best_moves):
  if depth == 0 or board.winner() != None: # Reached last node | someone won
    return board.evaluate(), board

  global cuts
  global nodes
  global states
  global killer_moves

  if depth == root_depth:
    cuts = nodes = states = 0
    killer_moves = best_moves
    
  best_move = None
  if maximizer: # AI's turn
    maxScore = float('-inf')
    moves = get_all_moves(board, WHITE)
    nodes += len(moves)

    for move in moves:
      states += 1
      score = move_ordering(move, depth-1, root_depth, False, alpha, beta, killer_moves)[0] # Only get the score
      maxScore = max(maxScore, score)
      alpha = max(alpha, maxScore)
      if maxScore == score:
        best_move = move
      if beta <= alpha:
        cuts += 1
        killer_moves.append({
          "hash": hash(move),
          "move": move,
          "score": score,
          "depth": depth
        })
        break
    return maxScore, best_move, cuts, nodes, states, killer_moves
  else: # Player's turn
    minScore = float('inf')
    moves = get_all_moves(board, BLACK)
    hashed_moves = []

    for move in moves:
      hashed_moves.append(hash(move))

    for killer_move in killer_moves: # remove non-valid killer moves and those not in the same depth search
      if killer_move['move'] not in hashed_moves or killer_move['depth'] != depth: # Compare hash value of board objects
        killer_moves.remove(killer_move)

    if killer_moves:
      sort = sorted(killer_moves, key = lambda move: move['score'], reverse=True)
      move = sort.pop()
      if move['move'] in moves:
        moves.remove(move['move']) # Place move as first iterable
      moves.insert(0, move['move'])

      if len(sort) > 0: # Place 2nd best killer move
        move_2 = sort.pop()
        if move_2['move'] in moves:
          moves.remove(move_2['move'])
        moves.insert(1, move_2['move'])

    nodes += len(moves)

    for move in moves:
      states += 1
      score = move_ordering(move, depth-1, root_depth, True, alpha, beta, killer_moves)[0] # Only get the score
      minScore = min(minScore, score)
      beta = min(beta, minScore)
      if minScore == score:
        best_move = move
      if beta <= alpha:
        cuts += 1
        killer_moves.append({
          "hash": hash(move),
          "move": move,
          "score": score,
          "depth": depth
        })
        break

    return minScore, best_move, cuts, nodes, states, killer_moves