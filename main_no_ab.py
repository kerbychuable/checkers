import pygame, sys

from checkers.constants import WIDTH, HEIGHT, TILE_SIZE, BLACK, WHITE
from checkers.game import Game
from ai.minimax import minimax_no_ab
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
  clock = pygame.time.Clock()
  game = Game(window)
  while run:
    clock.tick(FPS)

    if game.winner() != None:
      print(game.winner() + " wins!")
      # run = False

    if game.turn == WHITE:
      start_time = datetime.now()
      score, new_board = minimax_no_ab(game.get_board(), 3, True, game)
      # print(score)
      game.ai_move(new_board)
      end_time = datetime.now()
      time_taken = end_time - start_time
      print(str(time_taken.total_seconds()))

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
  pygame.quit()

if __name__ == '__main__':
  try:
    main()
  except Exception as e:
    print(e)
    sys.exit(0)