import unittest
from rooms import Room, generate_rooms
from config import TILE_SIZE

class TestRoom(unittest.TestCase):
    def test_room_stores_correct_values(self):
        room = Room(tile_x=5, tile_y=6, tile_width=7, tile_height=8)

        self.assertEqual(room.tile_x, 5)
        self.assertEqual(room.tile_y, 6)
        self.assertEqual(room.tile_width, 7)
        self.assertEqual(room.tile_height, 8)

        self.assertEqual(room.room_rect.x, 5 * TILE_SIZE)
        self.assertEqual(room.room_rect.y, 6 * TILE_SIZE)
        self.assertEqual(room.room_rect.width, 7 * TILE_SIZE)
        self.assertEqual(room.room_rect.height, 8 * TILE_SIZE)

class TestGenerateRooms(unittest.TestCase):
    def test_rooms_within_bounds(self):
        grid_width = 40
        grid_height = 30

        rooms = generate_rooms(
            grid_width=grid_width,
            grid_height=grid_height,
            min_size=2,
            max_size=10,
            max_rooms=10,
            margin=2
        )

        for room in rooms:
            self.assertGreaterEqual(room.tile_x, 0)
            self.assertGreaterEqual(room.tile_y, 0)
            self.assertLessEqual(room.tile_x + room.tile_width, grid_width)
            self.assertLessEqual(room.tile_y + room.tile_height, grid_height)

    def test_no_room_overlaps(self):
        rooms = generate_rooms(
            grid_width=40,
            grid_height=30,
            min_size=2,
            max_size=10,
            max_rooms=10,
            margin=2
        )

        for i, room_a in enumerate(rooms):
            for room_b in rooms[i + 1:]:
                self.assertFalse(room_a.room_rect.colliderect(room_b.room_rect))

    def test_no_infinite_room_generation(self):
        max_rooms = 10

        rooms = generate_rooms(
            grid_width=40,
            grid_height=30,
            min_size=2,
            max_size=10,
            max_rooms=max_rooms,
            margin=2
        )

        self.assertLessEqual(len(rooms), max_rooms)
