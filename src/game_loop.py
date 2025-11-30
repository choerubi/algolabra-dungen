import os
import sys
import random
import pygame
import rooms
import bowyer_watson
from config import (
    DISPLAY_WIDTH, DISPLAY_HEIGHT,
    DUNGEON_WIDTH, DUNGEON_HEIGHT, TILE_SIZE
)

# pylint: disable=too-many-instance-attributes,too-many-nested-blocks
class GameLoop:
    def __init__(self):
        """A constructor that initializes the game window."""

        self.display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption("Dungeon Generator")

        self.dungeon_surface = pygame.Surface((DUNGEON_WIDTH, DUNGEON_HEIGHT))
        self.dungeon_rect = self.dungeon_surface.get_rect(
            center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2)
        )

        self.dir_name = os.path.dirname(__file__)

        self._load_fonts()
        self._create_buttons()
        self._load_assets()

        self.current_view = 0

        self.generate_new_dungeon = False
        self.rooms = None

        self.bowyer_watson = bowyer_watson.BowyerWatson()

        self.dungeon_surface.fill((37, 19, 26))

    def _load_fonts(self):
        """A method that loads the fonts and renders the title text."""

        font_path = os.path.join(self.dir_name, "assets", "fonts", "PressStart2P-Regular.ttf")
        self.title_font = pygame.font.Font(font_path, 32)
        self.main_font = pygame.font.Font(font_path, 20)

        self.title_text = self.title_font.render("2D DUNGEON GENERATOR", True, (255, 255, 255))
        self.title_position = (DISPLAY_WIDTH // 2 - self.title_text.get_width() // 2, 40)

    def _create_buttons(self):
        """A method that creates the buttons and their text labels."""

        self.generate_button_rect = pygame.Rect(40, 200, 200, 50)
        self.generate_button_text = self.main_font.render("GENERATE", True, (255, 255, 255))
        self.generate_text_rect = self.generate_button_text.get_rect(
            center=self.generate_button_rect.center
        )

        self.exit_button_rect = pygame.Rect(40, 275, 125, 50)
        self.exit_button_text = self.main_font.render("EXIT", True, (255, 255, 255))
        self.exit_text_rect = self.exit_button_text.get_rect(
            center=self.exit_button_rect.center
        )

        self.left_button_rect = pygame.Rect(
            (DISPLAY_WIDTH - DUNGEON_WIDTH) // 2 - 50,
            DISPLAY_HEIGHT // 2 - 50,
            50,
            50
        )
        self.left_button_text = self.title_font.render("<", True, (255, 255, 255))
        self.left_text_rect = self.left_button_text.get_rect(
            center=self.left_button_rect.center
        )

        self.right_button_rect = pygame.Rect(
            (DISPLAY_WIDTH - DUNGEON_WIDTH) // 2 + DUNGEON_WIDTH,
            DISPLAY_HEIGHT // 2 - 50,
            50,
            50
        )
        self.right_button_text = self.title_font.render(">", True, (255, 255, 255))
        self.right_text_rect = self.right_button_text.get_rect(
            center=self.right_button_rect.center
        )

    def _load_assets(self):
        """A method that loads the tile assets."""

        self.floor_tile_1 = pygame.image.load(
            os.path.join(self.dir_name, "assets", "sprite_022.png")
        ).convert()
        self.floor_tile_2 = pygame.image.load(
            os.path.join(self.dir_name, "assets", "sprite_023.png")
        ).convert()

    def start(self):
        """A method that runs the main game loop."""

        while True:
            self._handle_events()

            if self.generate_new_dungeon:
                self._generate_dungeon()
                self.generate_new_dungeon = False

            self._render()

    def _handle_events(self):
        """A method that processes user input and system events."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

                elif self.generate_button_rect.collidepoint(event.pos):
                    self.generate_new_dungeon = True

                elif self.left_button_rect.collidepoint(event.pos):
                    if self.current_view > 0:
                        self.current_view = self.current_view - 1

                elif self.right_button_rect.collidepoint(event.pos):
                    if self.current_view < 1:
                        self.current_view = self.current_view + 1

    def _generate_dungeon(self):
        """A method that generates a new dungeon when the button is pressed."""
        self.current_view = 0

        self.rooms = rooms.generate_rooms(
            grid_width=DUNGEON_WIDTH // TILE_SIZE,
            grid_height=DUNGEON_HEIGHT // TILE_SIZE,
            min_size=2,
            max_size=10,
            max_rooms=12,
            margin=2
        )

    def _draw_rooms(self):
        """A method that draws the rooms onto the dungeon surface."""

        self.dungeon_surface.fill((37, 19, 26))

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

    def _draw_triangulation(self):
        """A method that draws the Delaunay triangulation onto the dungeon surface."""

        room_centers = []

        for room in self.rooms:
            center_x = room.tile_x * TILE_SIZE + room.tile_width * TILE_SIZE // 2
            center_y = room.tile_y * TILE_SIZE + room.tile_height * TILE_SIZE // 2
            room_centers.append((center_x, center_y))

        triangles = self.bowyer_watson.triangulate(room_centers)

        for triangle in triangles:
            for edge in triangle.edges:
                pygame.draw.line(self.dungeon_surface, (57, 255, 20), edge.v1, edge.v2)

    def _render(self):
        """A method that renders the current game frame."""

        self.display.fill((0, 0, 0))
        self.display.blit(self.dungeon_surface, self.dungeon_rect)

        if self.rooms:
            if self.current_view == 0:
                self._draw_rooms()

            if self.current_view == 1:
                self._draw_rooms()
                self._draw_triangulation()

        self._render_ui()
        pygame.display.flip()

    def _render_ui(self):
        """A method that renders the UI of the current game frame."""

        self.display.blit(self.title_text, self.title_position)

        pygame.draw.rect(self.display, (0, 0, 0), self.generate_button_rect)
        self.display.blit(self.generate_button_text, self.generate_text_rect)

        pygame.draw.rect(self.display, (0, 0, 0), self.exit_button_rect)
        self.display.blit(self.exit_button_text, self.exit_text_rect)

        if self.rooms:
            if self.current_view > 0:
                pygame.draw.rect(self.display, (0, 0, 0), self.left_button_rect)
                self.display.blit(self.left_button_text, self.left_text_rect)

            if self.current_view < 1:
                pygame.draw.rect(self.display, (0, 0, 0), self.right_button_rect)
                self.display.blit(self.right_button_text, self.right_text_rect)
