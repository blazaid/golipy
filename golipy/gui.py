import os
from pathlib import Path

import pygame


class Gui:
    """Comprises the entire user interface behaviour."""
    FONT_SIZE = 30
    BOX_W = 54
    BOX_H = 54
    GAP_FACTOR = .9

    BG_COLOR = 0x05, 0x44, 0x5e
    CELL_COLOR = 0xd4, 0xf1, 0xf4
    TEXT_COLOR = 0x75, 0xe6, 0xda
    SELECT_COLOR = 0x18, 0x9a, 0xb4

    PATH = Path(os.path.abspath(__file__)).parent

    def __init__(self, simulation):
        """Initializes this instance.

        :param simulation: The simulation to which this interface
            belongs.
        """
        self.font = pygame.font.Font(
            Gui.PATH / 'resources' / 'fonts' / 'FiraCode-Light.ttf',
            Gui.FONT_SIZE
        )

        self.simulation = simulation
        self.screen = simulation.screen
        self.camera = simulation.camera
        self.universe = simulation.universe

        self.cell_width = Gui.BOX_W * Gui.GAP_FACTOR
        self.cell_height = Gui.BOX_H * Gui.GAP_FACTOR
        self.h_gap = (Gui.BOX_W - self.cell_width) / 2
        self.v_gap = (Gui.BOX_H - self.cell_height) / 2

    def update(self):
        """Updates all the graphical stuff, namely universe and HUD."""
        self.screen.fill(Gui.BG_COLOR)
        self.draw_universe()
        self.draw_hud()

    def draw_universe(self):
        """Draw all cells belonging to the simulated universe."""
        for x, y in self.universe.cells:
            screen_x, screen_y = self.camera.virtual2screen((
                x * Gui.BOX_W + self.h_gap,
                y * Gui.BOX_H + self.v_gap
            ))
            pygame.draw.rect(self.screen, Gui.CELL_COLOR, (
                screen_x, screen_y,
                self.zoom(self.cell_width), self.zoom(self.cell_height)
            ), 0)

    def draw_hud(self):
        """Draw all contextual information of the simulation."""
        virt_x, virt_y = self.camera.screen2virtual(pygame.mouse.get_pos())
        coord_x, coord_y = self.camera.virtual2screen((
            virt_x // Gui.BOX_W * Gui.BOX_W + self.h_gap,
            virt_y // Gui.BOX_H * Gui.BOX_H + self.v_gap
        ))

        # Define the messages to display
        msg_speed = self.font.render(
            f'Simulation speed: {100. / self.simulation.speed:.2f} Hz',
            True, Gui.TEXT_COLOR
        )
        msg_cells_no = self.font.render(
            f'Cells No.: {self.universe.size}',
            True, Gui.TEXT_COLOR
        )
        msg_gen = self.font.render(
            f'Current generation: {self.universe.generation}',
            True, Gui.TEXT_COLOR
        )

        # Draw the square cursor
        pygame.draw.rect(self.screen, Gui.SELECT_COLOR, (
            coord_x, coord_y,
            self.zoom(self.cell_width), self.zoom(self.cell_height)
        ), 0)
        # Draw the messages
        for i, msg in enumerate((msg_speed, msg_cells_no, msg_gen)):
            x = Gui.FONT_SIZE
            y = Gui.FONT_SIZE * (i + 1) + i * Gui.FONT_SIZE / 2
            self.screen.blit(msg, (x, y))

    def zoom(self, value):
        """Transforms a value by scaling using the current zoom.

        :param value: The original value.
        :return: The zoomed value.
        """
        return round(value / self.camera.zoom)

    def screen2cell(self, coords):
        """Converts the given coords to their corresponding cell.

        :param coords: The coordinates to be processed.
        :return: The exact cell value where the coordinates lie.
        """
        x, y = self.camera.screen2virtual(coords)
        return x // Gui.BOX_W, y // Gui.BOX_H
