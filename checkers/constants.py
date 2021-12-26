import pygame

pygame.init()
pygameInfo = pygame.display.Info()
pygame.quit()

# GUI DISPLAY CONSTANTS
WIDTH = HEIGHT = min(pygameInfo.current_w, pygameInfo.current_h) - min(pygameInfo.current_w, pygameInfo.current_h) * 0.1
ROWS = COLS = 8
TILE_SIZE = WIDTH//COLS

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
LIGHTBROWN = (255, 191, 128)
BROWN = (153, 77, 0)
BLUE = (0, 0, 255)