import sys

import pygame

from camera import Camera
from gui import Gui
from universe import Universe


class Mouse:
    """Listed with some ids of mouse clicks."""
    WHEEL_DOWN = 4
    WHEEL_UP = 5


class Simulation:
    """Simulates the Conway's Game of Life on an infinite universe."""

    def __init__(self):
        """Initializes this instance."""
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.xsize, self.ysize = pygame.display.get_surface().get_size()

        self.universe = Universe()

        self.running = False
        self.speed = 100

        self.camera = Camera(screen_size=(self.xsize, self.ysize))
        self.gui = Gui(simulation=self)

    def run(self):
        """Runs the whole simulation loop."""
        i = 1
        while True:
            if i % self.speed == 0:
                self.universe.step()
                i = 1

            self.input()
            self.gui.update()

            pygame.display.flip()
            if self.running:
                i += 1

    def input(self):
        """Checks the user input for any actions to perform."""
        # Whether or not to exit the application
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.exit()

        # Whether or not to reset the simulation
        if pygame.key.get_pressed()[pygame.K_DELETE]:
            self.reset()

        # WASD movement around the map
        if pygame.key.get_pressed()[pygame.K_w]:
            self.camera.up()
        if pygame.key.get_pressed()[pygame.K_a]:
            self.camera.left()
        if pygame.key.get_pressed()[pygame.K_s]:
            self.camera.down()
        if pygame.key.get_pressed()[pygame.K_d]:
            self.camera.right()

        # Creation and deletion of cells
        l_click, _, r_click = pygame.mouse.get_pressed()
        if l_click:
            self.universe.add(self.gui.screen2cell(pygame.mouse.get_pos()))
        if r_click:
            self.universe.remove(self.gui.screen2cell(pygame.mouse.get_pos()))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Pause and resume simulation
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    self.pause_or_resume()
                # Speed up the simulation
                if event.key == pygame.K_PLUS:
                    self.speed_up()
                # Decelerate the simulation
                if event.key == pygame.K_MINUS:
                    self.slow_down()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Apply zoom in
                if event.button == Mouse.WHEEL_UP:
                    self.camera.zoom_in()
                # Apply zoom out
                if event.button == Mouse.WHEEL_DOWN:
                    self.camera.zoom_out()

    def speed_up(self):
        """Accelerates the simulation by decreasing the frequency."""
        self.speed = max(1, self.speed - 1)

    def slow_down(self):
        """Accelerates the simulation by augmenting the frequency."""
        self.speed = min(500, self.speed + 1)

    def pause_or_resume(self):
        """Pause the simulation if it was running or vice versa."""
        self.running = not self.running

    def reset(self):
        """Leaves the simulation in the initial state."""
        self.running = False
        self.camera.reset()
        self.universe.reset()

    @staticmethod
    def exit():
        """Exits the simulation."""
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    simulation = Simulation()
    simulation.run()
