import os
import pygame
from config import (
    DISPLAY_WIDTH, DISPLAY_HEIGHT,
    POPUP_WIDTH, POPUP_HEIGHT
)

# pylint: disable=too-many-instance-attributes,too-many-positional-arguments
class InputBox:
    def __init__(self, box_x, box_y, box_width, box_height, text=""):
        """A constructor that initializes an input box in the popup window."""

        self.box_active = False
        self.invalid_input = False

        self.box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        self.text = text

        dir_name = os.path.dirname(__file__)
        font_path = os.path.join(dir_name, "assets", "fonts", "PressStart2P-Regular.ttf")
        self.main_font = pygame.font.Font(font_path, 16)

    def handle_events(self, event):
        """A method that processes user input and system events."""

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.box_rect.collidepoint(event.pos):
                self.box_active = True
            else:
                self.box_active = False

        if event.type == pygame.KEYDOWN:
            if self.box_active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]

                elif event.unicode.isdigit():
                    self.text += event.unicode

    def draw_box(self, window):
        """A method that draws the input box onto the popup window."""

        if self.invalid_input:
            color = (220, 20, 60)
        else:
            color = (255, 255, 255)
        pygame.draw.rect(window, color, self.box_rect)

        box_text = self.main_font.render(self.text, True, (0, 0, 0))
        window.blit(box_text, (self.box_rect.x + 5, self.box_rect.y + 10))

    def get_input_value(self):
        """A method that returns the value the user submitted."""

        return int(self.text) if self.text else 0

class InputPopup:
    def __init__(self):
        """A constructor that initializes the popup window."""

        self.popup_active = False

        self.popup_rect = pygame.Rect(
            (DISPLAY_WIDTH - POPUP_WIDTH) // 2,
            (DISPLAY_HEIGHT - POPUP_HEIGHT) // 2,
            POPUP_WIDTH,
            POPUP_HEIGHT
        )

        self.min_size = InputBox(self.popup_rect.x + 295, self.popup_rect.y + 50, 105, 35, "3")
        self.max_size = InputBox(self.popup_rect.x + 295, self.popup_rect.y + 100, 105, 35, "10")
        self.max_rooms = InputBox(self.popup_rect.x + 295, self.popup_rect.y + 150, 105, 35, "12")

        self.input_boxes = [self.min_size, self.max_size, self.max_rooms]

        dir_name = os.path.dirname(__file__)
        font_path = os.path.join(dir_name, "assets", "fonts", "PressStart2P-Regular.ttf")
        self.main_font = pygame.font.Font(font_path, 16)
        self.button_font = pygame.font.Font(font_path, 20)

        self.min_size_text = self.main_font.render("MIN ROOM SIZE:", True, (255, 255, 255))
        self.max_size_text = self.main_font.render("MAX ROOM SIZE:", True, (255, 255, 255))
        self.max_rooms_text = self.main_font.render("ROOM AMOUNT:", True, (255, 255, 255))

        self.done_button_rect = pygame.Rect(
            self.popup_rect.x + (POPUP_WIDTH // 2 - 200 // 2),
            self.popup_rect.y + 220,
            200,
            50
        )
        self.done_button_text = self.button_font.render("DONE", True, (255, 255, 255))
        self.done_text_rect = self.done_button_text.get_rect(
            center=self.done_button_rect.center
        )

    def open(self):
        """A method that opens the popup window."""

        self.popup_active = True

    def handle_events(self, event):
        """A method that processes user input and system events."""

        if self.popup_active:
            for box in self.input_boxes:
                box.handle_events(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.done_button_rect.collidepoint(event.pos):
                    return self._close()

        return None

    def _close(self):
        """A method that validates the input values and closes the popup window
            if all input values are valid."""

        for box in self.input_boxes:
            box.invalid_input = False

        min_size = self.min_size.get_input_value()
        max_size = self.max_size.get_input_value()
        max_rooms = self.max_rooms.get_input_value()

        if min_size > max_size:
            self.min_size.invalid_input = True
            self.max_size.invalid_input = True

        if not 3 <= min_size <= 10:
            self.min_size.invalid_input = True
        if not 3 <= max_size <= 10:
            self.max_size.invalid_input = True
        if not 3 <= max_rooms <= 15:
            self.max_rooms.invalid_input = True

        if not any(
            [self.min_size.invalid_input,
            self.max_size.invalid_input,
            self.max_rooms.invalid_input]
        ):
            self.popup_active = False
            return min_size, max_size, max_rooms

        return None

    def draw_window(self, display):
        """A method that draws the popup window onto the main display."""

        if self.popup_active:
            # Add an overlay that dims everything but the popup window
            overlay = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            display.blit(overlay, (0, 0))

            pygame.draw.rect(display, (37, 19, 26), self.popup_rect)

            for box in self.input_boxes:
                box.draw_box(display)

            display.blit(self.min_size_text, (self.popup_rect.x + 55, self.popup_rect.y + 60))
            display.blit(self.max_size_text, (self.popup_rect.x + 55, self.popup_rect.y + 110))
            display.blit(self.max_rooms_text, (self.popup_rect.x + 55, self.popup_rect.y + 160))

            pygame.draw.rect(display, (37, 19, 26), self.done_button_rect)
            display.blit(self.done_button_text, self.done_text_rect)
