from typing import Tuple

class Turtle:
    def __init__(self, location=(0,0), battery=1000, paint=float('inf'), repainting_consumes_paint=True, fuel=float('inf')):
        """
        Class representing the state of a turtle and its coordinate plane.

        `location`: starting position of turtle
        `battery`: how many instructions can the turtle execute before halting on next instruction.
        `paint`: how many cells the turtle can paint before halting on next paint instruction.
        `repainting_consumes_paint`: if True, then executing the paint instruction while on a cell that has already been painted also consumes paint.
        `fuel`: how many move instructions can the turtle execute before halting on next move instruction.
        """
        self.loc_x, self.loc_y = location
        self.battery = battery
        self._paint = paint
        self.repainting_consumes_paint = repainting_consumes_paint
        self.fuel = fuel
        self.painted_cells_ord = []
        self.painted_cells_unord = set()


        self.bbox_xmin = None
        self.bbox_xmax = None
        self.bbox_ymin = None
        self.bbox_ymax = None


    def before_read_line(self, line: str) -> None:
        """
        This should be called just before a line from the command file gets parsed.

        line is the line that was just parsed.

        By default, this does nothing.
        """
        pass


    def before_command_exec(self, cmd: str) -> None:
        """
        This should be called before a command is to be executed.

        cmd is the text representation of the command.

        By default, this does nothing.
        """
        pass
    
    def after_command_exec(self, cmd: str) -> None:
        """
        This should be called after a command has just finished being executed, even if it raised an exception.

        cmd is the text representation of the command.

        By default, this does nothing.
        """
        pass

    def after_script(self) -> None:
        """
        This should be called after the script has finished execution.

        By default, this does nothing.
        """
        pass


    @property
    def location(self) -> Tuple[int, int]:
        return (self.loc_x, self.loc_y)

    @location.setter
    def location(self, new: Tuple[int, int]) -> None:
        self.loc_x, self.loc_y = new


    def consume_battery(self) -> None:
        """
        Decrement the battery counter.
        If it is at zero, raise an OutOfBatteryException.
        """
        if self.battery <= 0:
            raise OutOfBatteryException

        self.battery -= 1

    def consume_paint(self) -> None:
        """
        Decrement the paint counter.
        If it is at zero, raise an OutOfPaintException.
        """
        if self._paint <= 0:
            raise OutOfPaintException

        self._paint -= 1
    
    def consume_fuel(self) -> None:
        """
        Decrement the fuel counter.
        If it is at zero, raise an OutOfFuelException.
        """
        if self.fuel <= 0:
            raise OutOfFuelException

        self.fuel -= 1

    def move(self, direction: Tuple[int, int]) -> None:
        """
        Move the turtle in the direction described by the direction vector.

        `direction` must be a tuple of two integers, one of which must be 0 and the other either -1, 0, or 1.
        In other words, it must be a 2D vector with integer coordinates of magnitude 1, or the zero vector.
        If it is not, a ValueError is raised.


        If it is the zero vector, this is a no-op.
        If it is a directed vector, the turtle moves a single step in this direction and decrements its fuel.

        If there is no fuel at command invocation, this raises an OutOfFuelException.
        If there is no battery at command invocation, this raises an OutOfBatteryException.
        """

        if len(direction) != 2:
            raise ValueError('direction must be 2-length')

        direction = tuple(direction)
        if direction == (0, 0):
            return

        if sum( [i*i for i in direction] ) != 1:
            raise ValueError('direction does not have magnitude 1')

        if not all( [isinstance(i, int) for i in direction] ):
            raise ValueError('not all elements of direction are int')

        self.consume_battery()
        self.consume_fuel()       
 
        disp_x, disp_y = direction
        self.loc_x += disp_x
        self.loc_y += disp_y


    up = lambda self: self.move((0, 1))
    down = lambda self: self.move((0, -1))
    left = lambda self: self.move((-1, 0))
    right = lambda self: self.move((1, 0))

    def update_bbox(self, new: Tuple[int, int]) -> bool:
        """
        Update the bounding box variables to fit the new coordinate.

        Return whether the bounding box changed.
        """

        nx, ny = new

        if self.bbox_xmin is None or self.bbox_xmax is None or self.bbox_ymin is None or self.bbox_ymax is None:  # bbox is not initialized.
            self.bbox_xmin, self.bbox_xmax = nx, nx
            self.bbox_ymin, self.bbox_ymax = ny, ny
            return True

        updated = False
        if nx not in range(self.bbox_xmin, self.bbox_xmax + 1):
            updated = True
            self.bbox_xmin = min(self.bbox_xmin, nx)
            self.bbox_xmax = max(self.bbox_xmax, nx)
        
        if ny not in range(self.bbox_ymin, self.bbox_ymax + 1):
            updated = True
            self.bbox_ymin = min(self.bbox_ymin, ny)
            self.bbox_ymax = max(self.bbox_ymax, ny)

        return updated


    def paint(self) -> Tuple[bool, bool]:
        """
        Paint the current location of the turtle.
        If there is no paint at command invocation, this raises an OutOfPaintException.

        Returns a 2-tuple of booleans.
        The first one is whether paint has been consumed by this operation
        (only False when on a previously-painted cell and the turtle is set to not paint pre-painted cells).

        The second one is whether this operation changed the bounds of the visible field
        (in other words, if this point is outside the bounding box of all the previous points).
        """

        self.consume_battery()

        if self.location in self.painted_cells_unord:
            if self.repainting_consumes_paint:
                self.consume_paint()
            return (self.repainting_consumes_paint, False)

        self.consume_paint()

        self.painted_cells_unord.add(self.location)
        self.painted_cells_ord.append(self.location)

        updated_bbox = self.update_bbox(self.location)
        return (True, updated_bbox)



class TurtleHaltException(RuntimeError): pass

class OutOfBatteryException(TurtleHaltException): pass
class OutOfPaintException(TurtleHaltException): pass
class OutOfFuelException(TurtleHaltException): pass
