import pygame, sys

from checkers.constants import WIDTH, HEIGHT, TILE_SIZE, BLACK, WHITE
from checkers.game import Game
from ai.minimax import minimax, move_ordering
from datetime import datetime

FPS = 30

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_tile_pos(pos):
  x, y = pos
  row = y // TILE_SIZE
  col = x // TILE_SIZE
  return row, col

def main():
  run = True
  doOnce = True
  count = 0
  totalTime, numCuts, numNodes, numStates = [], [], [], []
  killerHeuristic = []

  # CONFIG
  depth = 8
  bool_move_ordering = True

  clock = pygame.time.Clock()
  game = Game(window)
  while run:
    clock.tick(FPS)

    if game.winner() != None:
      print(game.winner() + " wins!")
      run = False
    else:
      if game.turn == WHITE:
        game.find_moveable_pieces()
        if game.moveable_pieces == None:
          game.board.white_rem = 0
          print('No moves left for white!')
          continue
        cuts = nodes = states = 0
        for i in range(count):
          killerHeuristic.pop()
        start_time = datetime.now()
        if bool_move_ordering:
          score, new_board, cuts, nodes, states, killerMoves = move_ordering(game.get_board(), depth, depth, True, float('-inf'), float('inf'), killerHeuristic)
          killerHeuristic += killerMoves
          count = len(killerMoves)
        else:
          score, new_board, cuts, nodes, states = minimax(game.get_board(), depth, depth, True, float('-inf'), float('inf'))
        game.ai_move(new_board)
        end_time = datetime.now()
        time_taken = end_time - start_time
        print(str(time_taken.total_seconds()) + 's\n' + str(states) + ' nodes visited\n' + str(nodes) + ' nodes generated\n' + str(cuts) + ' cutoffs')
        totalTime.append(time_taken.total_seconds())
        numCuts.append(cuts)
        numNodes.append(nodes)
        numStates.append(states)
        doOnce = True

      if game.turn == BLACK and doOnce:
        game.find_moveable_pieces()
        if game.moveable_pieces == None:
          game.board.black_rem = 0
          print('No moves left for black!')
          continue
        doOnce = False

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        row, col = get_tile_pos(pos)
        game.select(row, col)
      
      if event.type == pygame.KEYDOWN:
        pass

    game.update()
  print('Total Move Time by AI: ', sum(totalTime))
  print('Total Nodes Generated:', sum(numNodes))
  print('Total Nodes Visited:', sum(numStates))
  print('Total Beta Cutoffs:', sum(numCuts))
  print('Average Move Time by AI: ', sum(totalTime)/len(totalTime))
  print('Average Nodes Generated:', sum(numNodes)//len(numNodes))
  print('Average Nodes Visited:', sum(numStates)//len(numStates))
  print('Average Beta Cutoffs:', sum(numCuts)//len(numCuts))
  pygame.quit()

if __name__ == '__main__':
  try:
    main()
  except Exception as e:
    print(e)
    sys.exit(0)