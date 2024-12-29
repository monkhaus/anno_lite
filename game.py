import pygame
import sys
import time

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_SIZE = 40
ROWS, COLS = SCREEN_HEIGHT // GRID_SIZE, SCREEN_WIDTH // GRID_SIZE
BACKGROUND_COLOR = (200, 200, 200)
GRID_COLOR = (150, 150, 150)
FONT_COLOR = (0, 0, 0)

# Colors for buildings
COLORS = {
    "woodcutter": (139, 69, 19),
    "sawmill": (205, 133, 63),
    "house": (100, 149, 237),
}

# Resource production rates (in seconds)
PRODUCTION_TIMERS = {
    "woodcutter": 3,
    "sawmill": 5,
}

# Initialize screen and font
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Production Chain Game")
font = pygame.font.Font(None, 24)

# Game state
grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
resources = {"wood": 0, "planks": 0}
buildings = []
selected_building = None

class Building:
    def __init__(self, row, col, building_type):
        self.row = row
        self.col = col
        self.type = building_type
        self.timer = PRODUCTION_TIMERS.get(building_type, 0)
        self.last_production_time = time.time()

    def produce(self):
        current_time = time.time()
        if current_time - self.last_production_time >= self.timer:
            if self.type == "woodcutter":
                resources["wood"] += 1
            elif self.type == "sawmill" and resources["wood"] > 0:
                resources["wood"] -= 1
                resources["planks"] += 1
            self.last_production_time = current_time

# Draw grid
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)
            if grid[row][col]:
                pygame.draw.rect(screen, COLORS[grid[row][col]], rect)

# Draw HUD
def draw_hud():
    wood_text = font.render(f"Wood: {resources['wood']}", True, FONT_COLOR)
    planks_text = font.render(f"Planks: {resources['planks']}", True, FONT_COLOR)
    instructions_text = font.render("Press W for Woodcutter, S for Sawmill, H for House, then Click to Place", True, FONT_COLOR)
    selected_text = font.render(f"Selected: {selected_building if selected_building else 'None'}", True, FONT_COLOR)
    screen.blit(wood_text, (10, 10))
    screen.blit(planks_text, (10, 40))
    screen.blit(instructions_text, (10, 70))
    screen.blit(selected_text, (10, 100))

# Main game loop
def main():
    global selected_building
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    selected_building = "woodcutter"
                elif event.key == pygame.K_s:
                    selected_building = "sawmill"
                elif event.key == pygame.K_h:
                    selected_building = "house"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                col, row = x // GRID_SIZE, y // GRID_SIZE
                if grid[row][col] is None and selected_building:
                    if selected_building == "house":
                        if resources["planks"] >= 5:
                            resources["planks"] -= 5
                            grid[row][col] = selected_building
                    else:
                        grid[row][col] = selected_building
                        buildings.append(Building(row, col, selected_building))

        # Update buildings
        for building in buildings:
            building.produce()

        draw_grid()
        draw_hud()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
