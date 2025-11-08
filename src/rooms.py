import random
import pygame
from config import TILE_SIZE

class Room:
    """A class to represent a room consisting of tiles."""

    def __init__(self, tile_x, tile_y, tile_width, tile_height):
        """A constructor that initializes a room in tile units.

        Args:
            tile_x: Top-left x-coordinate of the room in tile units.
            tile_y: Top-left y-coordinate of the room in tile units.
            tile_width: Room width in tile units.
            tile_height: Room height in tile units.
        """

        self.tile_x = tile_x
        self.tile_y = tile_y
        self.tile_width = tile_width
        self.tile_height = tile_height

        # Convert tile coordinates into pixel coordinates
        self.room_rect = pygame.Rect(
            tile_x * TILE_SIZE,
            tile_y * TILE_SIZE,
            tile_width * TILE_SIZE,
            tile_height * TILE_SIZE
        )

def generate_rooms(grid_width, grid_height, min_size, max_size, max_rooms, margin):
    """A method that randomly generates rooms on a grid.

    Args:
        grid_width: Dungeon width in tile units.
        grid_height: Dungeon height in tile units.

        min_size: Minimum room size in tile units.
        max_size: Maximum room size in tile units.

        max_rooms: Number of rooms to try to place.
        margin: Minimum number of empty tiles around each room.

    Returns:
        A list of Room objects with valid placements.
    """

    rooms = []

    tries = 0
    max_tries = max_rooms * 50 # Cap the number of tries to prevent infinite loops

    while len(rooms) < max_rooms and tries < max_tries:
        tile_width = random.randint(min_size, max_size)
        tile_height = random.randint(min_size, max_size)

        tile_x = random.randint(margin, grid_width - tile_width - margin)
        tile_y = random.randint(margin, grid_height - tile_height - margin)

        new_room = Room(tile_x, tile_y, tile_width, tile_height)

        # Check if the new room overlaps with any existing rooms
        rect_with_margin = new_room.room_rect.inflate(
            2 * margin * TILE_SIZE, 2 * margin * TILE_SIZE
        )

        overlaps = False
        for room in rooms:
            if rect_with_margin.colliderect(room.room_rect):
                overlaps = True
                break

        # Generate room if no collisions were found
        if overlaps is False:
            rooms.append(new_room)

        tries += 1

    return rooms
