import math


class Camera:
    """Groups together all camera-related operations"""
    INITIAL_POS = (0, 0)
    SPEED = 15

    def __init__(self, screen_size):
        """Initializes this instance.

        :param screen_size: The current screen size as a tuple in the
            form (width, height).
        """
        self.x_size, self.y_size = screen_size
        self.half_x_size = self.x_size / 2
        self.half_y_size = self.y_size / 2

        self.x = self.y = None
        self.initial_position = 0, 0
        self.zoom_speed = 0.1
        self.zoom = 1.0
        self.min_zoom, self.max_zoom = 0.1, math.inf

        self.reset()

    def reset(self):
        """Returns the camera to its initial position."""
        self.move_to(*self.initial_position)

    def up(self):
        """Moves the camera upwards."""
        self.move_to(self.x, self.y - Camera.SPEED)

    def down(self):
        """Moves the camera downwards."""
        self.move_to(self.x, self.y + Camera.SPEED)

    def left(self):
        """Moves the camera to the left."""
        self.move_to(self.x - Camera.SPEED, self.y)

    def right(self):
        """Moves the camera to the right."""
        self.move_to(self.x + Camera.SPEED, self.y)

    def move_to(self, x, y):
        """Moves the camera to the initial position.

        :param x: The x position.
        :param y: The y position.
        """
        self.x, self.y = x, y

    def zoom_in(self):
        """Brings the camera closer to the action."""
        self.apply_zoom(+1)

    def zoom_out(self):
        """Moves the camera away."""
        self.apply_zoom(-1)

    def apply_zoom(self, in_or_out):
        """Common part for zoom in and zoom out behaviours.

        :param in_or_out: Whether the action to be performed is to zoom
            in (in_or_out = +1) or zoom out (in_or_out = -1) the camera.
        """
        self.zoom += self.zoom * self.zoom_speed * in_or_out
        self.zoom = min(max(self.zoom, self.min_zoom), self.max_zoom)

    def virtual2screen(self, virtual_coords):
        """Transforms the "virtual" coords into screen coords.

        :param virtual_coords: The virtual coordinates.
        :return: The screen coordinates
        """
        x, y = virtual_coords
        new_x = (x - self.x) / self.zoom + self.half_x_size
        new_y = (y - self.y) / self.zoom + self.half_y_size

        return round(new_x), round(new_y)

    def screen2virtual(self, screen_coords):
        """Transforms the screen coords into virtual ones.

        :param screen_coords: The screen coordinates.
        :return: The virtual coordinates
        """
        x, y = screen_coords
        new_x = ((x - self.half_x_size) * self.zoom) + self.x
        new_y = ((y - self.half_y_size) * self.zoom) + self.y
        return new_x, new_y
