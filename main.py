import tkinter as tk
import random
from gamelib import Sprite, GameApp, Text

from dir_consts import *
from maze import Maze

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

UPDATE_DELAY = 33

PACMAN_SPEED = 5


class Pacman(Sprite):
    def __init__(self, app, maze, r, c):
        self.r = r
        self.c = c
        self.maze = maze

        self.direction = DIR_STILL
        self.next_direction = DIR_STILL

        x, y = maze.piece_center(r,c)
        super().__init__(app, 'images/pacman.png', x, y)
        self.state = NormalPacmanState(self)

    def update(self):
        if self.maze.is_at_center(self.x, self.y):
            r, c = self.maze.xy_to_rc(self.x, self.y)

            if self.maze.has_dot_at(r, c):
                self.maze.eat_dot_at(r, c)
                if self.maze.is_movable_direction(r, c, self.next_direction):
                    self.direction = self.next_direction
                else:
                    self.direction = DIR_STILL

                self.state.random_upgrade()

        self.state.move_pacman()

    def set_next_direction(self, direction):
        self.next_direction = direction


class PacmanGame(GameApp):
    def init_game(self):
        self.maze = Maze(self, CANVAS_WIDTH, CANVAS_HEIGHT)

        self.pacman1 = Pacman(self, self.maze, 1, 1)
        self.pacman2 = Pacman(self, self.maze, self.maze.get_height() - 2, self.maze.get_width() - 2)

        self.pacman1_score_text = Text(self, 'P1: 0', 100, 20)
        self.pacman2_score_text = Text(self, 'P2: 0', 600, 20)

        self.elements.append(self.pacman1)
        self.elements.append(self.pacman2)

        self.command_map = {'W': self.get_pacman_next_direction_function(self.pacman1, DIR_UP),
                            #  TODO:
                            #   - add all other commands to the command_map
                            'A': self.get_pacman_next_direction_function(self.pacman1, DIR_LEFT),
                            'S': self.get_pacman_next_direction_function(self.pacman1, DIR_DOWN),
                            'D': self.get_pacman_next_direction_function(self.pacman1, DIR_RIGHT),
                            'I': self.get_pacman_next_direction_function(self.pacman2, DIR_UP),
                            'J': self.get_pacman_next_direction_function(self.pacman2, DIR_LEFT),
                            'K': self.get_pacman_next_direction_function(self.pacman2, DIR_DOWN),
                            'L': self.get_pacman_next_direction_function(self.pacman2, DIR_RIGHT),
                            }

    def pre_update(self):
        pass

    def post_update(self):
        pass

    def on_key_pressed(self, event):
        ch = event.char.upper()
        if ch in self.command_map:
            self.command_map[ch]()

        # TODO:
        #   - check if ch is in self.command_map, if it is in the map, call the function.

    def get_pacman_next_direction_function(self, pacman, next_direction):
        def f():
            pacman.set_next_direction(next_direction)
        return f


class NormalPacmanState:
    def __init__(self, pacman):
        self.pacman = pacman

    def random_upgrade(self):
        if random.random() < 0.1:
            self.pacman.state = SuperPacmanState(self.pacman)

    def move_pacman(self):
        # TODO:
        #   - update the pacman's location with normal speed
        pacman_xy = self.pacman
        pacman_xy.x += PACMAN_SPEED * DIR_OFFSET[pacman_xy.direction][0]
        pacman_xy.y += PACMAN_SPEED * DIR_OFFSET[pacman_xy.direction][1]
        self.counter = 0


class SuperPacmanState:
    def __init__(self, pacman):
        self.pacman = pacman
        self.counter = 0

    def random_upgrade(self):
        pass

    def move_pacman(self):
        # TODO:
        #   - update the pacman's location with super speed
        #   - update the counter, if the counter >= 50, set state back to NormalPacmanState
        pacman_xy = self.pacman
        if self.counter <= 50:
            pacman_xy.x += 2 * PACMAN_SPEED * DIR_OFFSET[pacman_xy.direction][0]
            pacman_xy.y += 2 * PACMAN_SPEED * DIR_OFFSET[pacman_xy.direction][1]
            self.counter += 1
            if self.counter > 50:
                pacman_xy.state = NormalPacmanState(pacman_xy)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Monkey Banana Game")
 
    # do not allow window resizing
    root.resizable(False, False)
    app = PacmanGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
