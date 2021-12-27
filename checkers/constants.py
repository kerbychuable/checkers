import pygame

pygame.init()
pygameInfo = pygame.display.Info()
pygame.quit()

# GUI DISPLAY CONSTANTS
WIDTH = HEIGHT = (min(pygameInfo.current_w, pygameInfo.current_h) - int(min(pygameInfo.current_w, pygameInfo.current_h) * 0.1)) // 8 * 8 # Ensure window is in proper size for grid
ROWS = COLS = 8
TILE_SIZE = WIDTH//COLS

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
LIGHTBROWN = (255, 206, 158)
BROWN = (209, 139, 71)
BLUE = (0, 0, 255)
RED = (255, 0, 0)