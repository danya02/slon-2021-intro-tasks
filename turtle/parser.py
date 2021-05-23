import re
from typing import List, Union, Any
import turtle
import io
import traceback

class Parser:
    def __init__(self, turtle: turtle.Turtle):
        """
        Class that parses the command file and controls the turtle.
        
        turtle must be a initialized Turtle instance.
        """
        self.turtle = turtle
        self.stack = [1]
        self.stack_depth = 0

    def execute_stack(self, stack: List[Union[int, str, Any]]) -> None:
        """
        Run all the commands that have been accumulated in the stack.

        stack is a list whose first element is how many times this sequence should be executed,
        and the remaining elements are either commands or lists with the same format.
        """

        turtle = self.turtle
        cmds = {'up': turtle.up, 'down': turtle.down, 'left': turtle.left, 'right': turtle.right, 'paint': turtle.paint}
        for _ in range(stack[0]):
            for command in stack[1:]:
                if isinstance(command, list):
                    self.execute_stack(command)
                elif command in cmds:
                    turtle.before_command_exec(command)
                    try:
                        cmds[command]()
                    finally:
                        turtle.after_command_exec(command)
                else:
                    raise SyntaxError('unknown command while parsing loop stack:', command)                

    def take_line(self, line: str) -> None:
        """
        Accept a line from the command file and do things with it.
        """
        line = line.strip()
        turtle = self.turtle
        turtle.before_read_line(line)
        
        # if this is a basic command and we are not currently consuming commands for a loop, execute it and return.
        cmds = {'up': turtle.up, 'down': turtle.down, 'left': turtle.left, 'right': turtle.right, 'paint': turtle.paint}
        if line in cmds and self.stack_depth == 0:
            turtle.before_command_exec(line)
            try:
                return cmds[line]()
            finally:
                turtle.after_command_exec(line)
        
        # if this is a basic command, but we are in a loop parsing process, then find the innermost loop that we are currently populating and insert the command into it.
        if line in cmds:
            current_loop = self.stack
            for _ in range(self.stack_depth):
                current_loop = current_loop[-1]
            current_loop.append(line)
            return

        # if this is an "end" command, then decrement the loop depth. If this brings us up to the top level, we execute the loops.
        if line == 'end':
            if self.stack_depth <= 0:
                raise SyntaxError('Encountered "end" without matching "N times"')
            self.stack_depth -= 1
            if self.stack_depth == 0:
                self.execute_stack(self.stack)
                self.stack = [1]
            return        

        # if this is a "N times" command, then increment the loop depth and create a list for this depth.
        match = re.match('([0-9]+) times', line)
        if match:
            times = int(match.group(1))
            current_loop = self.stack
            for _ in range(self.stack_depth):
                current_loop = current_loop[-1]
            current_loop.append([times])
            self.stack_depth += 1
            return

        # if line starts with "#", this is a comment and should be ignored
        if line.startswith('#'): return

        raise SyntaxError('Unknown line: '+ repr(line))


    def read_file(self, file: io.TextIOBase) -> None:
        """
        Run the script in the file.
        """
        try:
            for line in file:
                self.take_line(line)
        except turtle.TurtleHaltException:
            print('Turtle halted!')
            traceback.print_exc()
        finally:
            self.turtle.after_script()
