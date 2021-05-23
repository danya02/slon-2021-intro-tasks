from turtle import Turtle
import uuid
import pygame
from typing import Callable, Tuple

class DebugTurtle(Turtle):
    """
    Turtle that prints its internal state on exit and reports every command as it happens.
    """
    def before_read_line(self, line: str) -> None:
        print('Reading line', line)

    def before_command_exec(self, cmd: str) -> None:
        print('Running command', cmd)

    def after_command_exec(self, cmd: str) -> None:
        print('Finished running', cmd)

    def after_script(self) -> None:
        print('Script ended')
        for key in self.__dict__:
            print(key, ':\t', self.__dict__[key])

class SimpleTurtle(Turtle):
    """
    Turtle that prints how many cells have been painted after script finishes.
    """
    def after_script(self) -> None:
        print('Script ended')
        print('Painted', len(self.painted_cells_unord), 'cells')


class PygameRenderingTurtle(Turtle):
    """
    Turtle that draws the state of the field into an image file.
    """
    def __init__(self, *args, bg_color='black', stroke_color='white', x_color='red', y_color='green', origin_color='blue', origin_radius=10, turtle_color='yellow', turtle_radius=10, file='img.png', **kwargs):
        """
        All colors are arguments for pygame.Color.

        bg_color: Default color for pixels that do not have any special features.
        stroke_color: Color for pixels which the turtle has painted.
        x_color: Color for the horizontal axis.
        y_color: Color for the vertical axis.
        origin_color: Color for the point at the origin.
        origin_radius: The origin is marked with a circle of what radius?
        turtle_color: Color for the point where the turtle is.
        turtle_radius: The turtle is marked with a circle of what radius?
        file: Which file to save the image to when the script ends?
        """

        self.bg_color = bg_color
        self.stroke_color = stroke_color
        self.x_color = x_color
        self.y_color = y_color
        self.origin_color = origin_color
        self.origin_radius = origin_radius
        self.turtle_color = turtle_color
        self.turtle_radius = turtle_radius
        self.file = file
        super().__init__(*args, **kwargs)

    @property
    def bbox(self) -> pygame.Rect:
        """Bounding box, as a pygame.Rect."""
        return pygame.Rect(self.bbox_xmin, self.bbox_ymax, self.bbox_xmax-self.bbox_xmin, self.bbox_ymax-self.bbox_ymin)

    def draw_coordinate_grid(self, surf: pygame.Surface, turtle_to_screen: Callable[ [Tuple[int, int]], Tuple[int, int] ]) -> None:
        """
        Draw the two axes and the origin.
        """
        for y in range(-self.bbox.height*2, self.bbox.height*2, 2):
            surf.set_at(turtle_to_screen((0, y)), pygame.Color(self.y_color))
        
        for x in range(-self.bbox.width*2, self.bbox.width*2, 2):
            surf.set_at(turtle_to_screen((x, 0)), pygame.Color(self.x_color))

        pygame.draw.circle(surf, pygame.Color(self.origin_color), turtle_to_screen((0, 0)), self.origin_radius)

    def draw_turtle_pos(self, surf: pygame.Surface, turtle_to_screen: Callable[ [Tuple[int, int]], Tuple[int, int] ]) -> None:
        """
        Draw the turtle's current position.
        """
        pygame.draw.circle(surf, pygame.Color(self.turtle_color), turtle_to_screen(self.location), self.turtle_radius)

    def render_to_surface(self, surf: pygame.Surface) -> Callable[ [Tuple[int, int]], Tuple[int, int] ]:
        """
        Draw the current painted cells as pixels of this surface.

        Return a function that maps turtle-space coordinates to screen-space coordinates.
        """
        surf.fill(pygame.Color(self.bg_color))
        V = pygame.math.Vector2
        bbox = self.bbox
        original_tl = V(bbox.topleft)
        bbox.topleft = (0,0)
        displacement = original_tl - V((0, 0))
        x_axis = V(1, 0)
        displacement.reflect_ip(x_axis)  # because cartesian system has Y going up, but Pygame has Y going down. 
        disx, disy = map(int, displacement)

        def turtle_to_screen(point):
            x, y = point
            x = -x
            x += (bbox.width - disx)
            y += (bbox.height - disy)
            return (x, y)

        for point in self.painted_cells_ord:
            point = turtle_to_screen(point)
            surf.set_at(point, pygame.Color(self.stroke_color))

        return turtle_to_screen

    def after_script(self) -> None:
        if self.painted_cells_ord == []:
            print('No cells painted, nothing to render!')
            return

        pygame.init()
        
        bbox = self.bbox
        surf = pygame.Surface((bbox.width+1, bbox.height+1))

        tts = self.render_to_surface(surf)
        self.draw_coordinate_grid(surf, tts)
        self.draw_turtle_pos(surf, tts)

        pygame.image.save(surf, self.file)


class PygameInteractiveTurtle(PygameRenderingTurtle):
    """
    Turtle that draws its field onto a Pygame display as the field is being drawn.
    """
    def __init__(self, *args, framerate=60, steps_between_frames=100, **kwargs):
        """
        framerate: how many screen updates per second are desired?
        steps_between_frames: how many commands can the turtle execute before another screen update?
        """
        self.framerate = framerate
        self.steps_between_frames = steps_between_frames
        
        pygame.init()
        self.steps_without_draw = 0
        self.clock = pygame.time.Clock()
        self.screen = None
        super().__init__(*args, **kwargs)

    def render_to_screen(self) -> None:
        """
        Draw the current state of the turtle's world to the Pygame display, updating its size if needed.
        """
        if len(self.painted_cells_ord) == 0: return
        if self.screen is None or self.screen.get_size() != self.bbox.size:
            # screen size is outdated, creating new screen
            self.screen = pygame.display.set_mode( (self.bbox.width+1, self.bbox.height+1) )
        tts = self.render_to_surface(self.screen)
        self.draw_coordinate_grid(self.screen, tts)
        self.draw_turtle_pos(self.screen, tts)
        pygame.display.flip()
        pygame.event.pump()

    def after_command_exec(self, cmd: str) -> None:
        """If enough commands have passed without a screen update, update the screen."""
        self.steps_without_draw += 1
        if self.steps_without_draw >= self.steps_between_frames:
            self.steps_without_draw = 0
            self.render_to_screen()
            self.clock.tick(self.framerate)

    def after_script(self) -> None:
        super().after_script()
        print('Script ended')
        if self.screen is None:
            return
        print('Press the quit button to quit')
        while 1:
            ev = pygame.event.wait()
            if ev.type == pygame.QUIT:
                return
            pygame.event.pump()


