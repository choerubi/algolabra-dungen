import os
import sys
import random
import pygame
import rooms
from config import (
    DISPLAY_WIDTH, DISPLAY_HEIGHT,
    DUNGEON_WIDTH, DUNGEON_HEIGHT, TILE_SIZE
)

class GameLoop:
    def __init__(self):
        """A constructor that initializes the game window."""

        self.display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption("2D Dungeon Generator")

        self.dungeon_surface = pygame.Surface((DUNGEON_WIDTH, DUNGEON_HEIGHT))
        self.dungeon_rect = self.dungeon_surface.get_rect(
            center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2)
        )

        dir_name = os.path.dirname(__file__)
        self.floor_tile_1 = pygame.image.load(
            os.path.join(dir_name, "assets", "sprite_022.png")
        ).convert()
        self.floor_tile_2 = pygame.image.load(
            os.path.join(dir_name, "assets", "sprite_023.png")
        ).convert()

        self.rooms = rooms.generate_rooms(
            grid_width=DUNGEON_WIDTH // TILE_SIZE,
            grid_height=DUNGEON_HEIGHT // TILE_SIZE,
            min_size=2,
            max_size=10,
            max_rooms=10,
            margin=2
        )

        self._draw_rooms()

    def start(self):
        """A method that runs the main game loop."""

        while True:
            self._handle_events()
            self._render()

    def _handle_events(self):
        """A method that processes user input and system events."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def _draw_rooms(self):
        """A method that draws the rooms onto the dungeon surface."""

        self.dungeon_surface.fill((255, 255, 255))

        # Draw the rooms
        for room in self.rooms:
            for i in range(room.tile_width):
                for j in range(room.tile_height):
                    tile_x = room.tile_x + i # x-coordinate of the specific tile inside the room
                    tile_y = room.tile_y + j # y-coordinate of the specific tile inside the room

                    # Convert tile coordinates into pixel coordinates
                    tile_rect = pygame.Rect(
                        tile_x * TILE_SIZE,
                        tile_y * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )

                    floor_tile = random.choice([self.floor_tile_1, self.floor_tile_2])
                    self.dungeon_surface.blit(floor_tile, tile_rect)

    def _render(self):
        """A method that renders the current game frame."""

        self.display.fill((0, 0, 0))

        self.display.blit(self.dungeon_surface, self.dungeon_rect)

        pygame.display.flip()
