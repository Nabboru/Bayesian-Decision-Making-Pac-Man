CELL_WIDTH = 20
CELL_HEIGHT = 24
GREY = (105,105,105)
DARK_BLUE = (0,0,205)
BLACK = (0,0,0)
WHITE = (255, 255, 255)
CORAL = (240,128,128)
NAVY = (35, 57, 93)
SEA_GREEN = (46,139,87)
ROYAL_BLUE = (65,105,225)
COLOURS = [WHITE, GREY, CORAL, SEA_GREEN, ROYAL_BLUE]
AGENTS_COLOURS = ['pink', 'yellow', 'red', 'blue']
WORSTCASE_RATIO = 0.52
EPSILON = 2 * (WORSTCASE_RATIO - 0.5)
DELTA = 0.1
X = 0.975
MEAN = WORSTCASE_RATIO
Z_SCORE = (X - MEAN) / DELTA