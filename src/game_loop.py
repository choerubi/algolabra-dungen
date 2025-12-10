import os
import sys
import pygame
import rooms
import bowyer_watson
import prim
import a_star
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
        self.triangles = None
        self.mst_edges = None
        self.extra_edges = None
        self.tiles = None

        self.bowyer_watson = bowyer_watson.BowyerWatson()
        self.prim = prim.Prim()
        self.a_star = a_star.AStar()

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

        self.floor_tile = pygame.image.load(
            os.path.join(self.dir_name, "assets", "sprite_022.png")
        ).convert()
        self.path_tile = pygame.image.load(
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
                    if self.current_view < 4:
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

        room_centers = []

        for room in self.rooms:
            center_x = room.tile_x * TILE_SIZE + room.tile_width * TILE_SIZE // 2
            center_y = room.tile_y * TILE_SIZE + room.tile_height * TILE_SIZE // 2
            room_centers.append((center_x, center_y))

        self.triangles = self.bowyer_watson.triangulate(room_centers)

        self.prim.get_vertices(self.triangles)
        self.mst_edges = self.prim.create_mst()

        self.extra_edges = prim.add_random_edges(15, self.mst_edges, self.triangles, self.rooms)

        self._get_free_tiles()

    def _draw_rooms(self):
        """A method that draws the rooms onto the dungeon surface."""

        for room in self.rooms:
            for i in range(room.tile_width):
                for j in range(room.tile_height):
                    tile_x = room.tile_x + i
                    tile_y = room.tile_y + j

                    tile_rect = pygame.Rect(
                        tile_x * TILE_SIZE,
                        tile_y * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )

                    self.dungeon_surface.blit(self.floor_tile, tile_rect)

    def _draw_triangulation(self):
        """A method that draws the Delaunay triangulation onto the dungeon surface."""

        for triangle in self.triangles:
            for edge in triangle.edges:
                pygame.draw.line(self.dungeon_surface, (57, 255, 20), edge.v1, edge.v2)

    def _draw_mst(self):
        """A method that draws the Minimum Spanning Tree onto the dungeon surface."""

        for edge in self.mst_edges:
            pygame.draw.line(self.dungeon_surface, (57, 255, 20), edge.v1, edge.v2)

    def _draw_extra_edges(self):
        """A method that draws the Minimum Spanning Tree with the extra edges
            onto the dungeon surface."""

        for edge in self.extra_edges:
            pygame.draw.line(self.dungeon_surface, (57, 255, 20), edge.v1, edge.v2)

    def _get_free_tiles(self):
        """A method that finds all free tiles that are not blocked by rooms."""

        # Initialize all tiles as zeros (free tiles)
        tile_height = DUNGEON_HEIGHT // TILE_SIZE
        tile_width = DUNGEON_WIDTH // TILE_SIZE
        self.tiles = [[0 for col in range(tile_height)] for row in range(tile_width)]

        # Mark tiles inside rooms as ones (occupied tiles)
        for room in self.rooms:
            for i in range(room.tile_width):
                for j in range(room.tile_height):
                    tile_x = room.tile_x + i
                    tile_y = room.tile_y + j
                    self.tiles[tile_x][tile_y] = 1

    def _draw_paths(self):
        """A method that draws the A* paths onto the dungeon surface."""

        for edge in self.mst_edges.union(self.extra_edges):
            tile_x1 = edge.v1[0] // TILE_SIZE
            tile_y1 = edge.v1[1] // TILE_SIZE
            start_pos = tile_x1, tile_y1

            tile_x2 = edge.v2[0] // TILE_SIZE
            tile_y2 = edge.v2[1] // TILE_SIZE
            goal_pos = tile_x2, tile_y2

            path = self.a_star.find_path(start_pos, goal_pos, self.tiles)

            for tile_x, tile_y in path:
                tile_rect = pygame.Rect(
                        tile_x * TILE_SIZE,
                        tile_y * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )

                if self.tiles[tile_x][tile_y] == 0:
                    self.dungeon_surface.blit(self.path_tile, tile_rect)

# pylint: disable=too-many-statements
    def _render(self):
        """A method that renders the current game frame."""

        self.display.fill((0, 0, 0))
        self.dungeon_surface.fill((37, 19, 26))

        if self.rooms:
            if self.current_view >= 0:
                self._draw_rooms()

            if self.current_view == 1:
                self._draw_triangulation()

            if self.current_view == 2:
                self._draw_mst()

            if self.current_view == 3:
                self._draw_mst()
                self._draw_extra_edges()

            if self.current_view == 4:
                self._draw_paths()

        self.display.blit(self.dungeon_surface, self.dungeon_rect)
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

            if self.current_view < 4:
                pygame.draw.rect(self.display, (0, 0, 0), self.right_button_rect)
                self.display.blit(self.right_button_text, self.right_text_rect)
