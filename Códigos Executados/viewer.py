import cv2
import numpy as np
from google.colab.patches import cv2_imshow


"""
    Aluno: Matheus Xavier Melotti
    Data: 18/10/2023
"""

class MazeViewer:
    START_COLOR = (0, 255, 0)
    GOAL_COLOR = (255, 0, 0)
    EXPANDED_COLOR = (0, 255, 255)
    GENERATED_COLOR = (0, 0, 255)
    PATH_COLOR = (128, 0, 255)

    def __init__(self, labirinto, start, goal, zoom=50, step_time_miliseconds=-1):
        self._labirinto = labirinto
        self._zoom = zoom
        self._step = step_time_miliseconds
        self._start = start
        self._goal = goal

    def update(self, generated=None, expanded=None, path=None, view=True):
        if generated is None:
            generated = []
        if path is None:
            path = []
        if expanded is None:
            expanded = []
        maze_img = np.array(self._labirinto).astype(np.uint8) * 255
        maze_img = 255 - maze_img
        maze_img = cv2.cvtColor(maze_img, cv2.COLOR_GRAY2BGR)

        self._draw_cells(maze_img, path, MazeViewer.PATH_COLOR)

        maze_img[self._start.y, self._start.x] = MazeViewer.START_COLOR
        maze_img[self._goal.y, self._goal.x] = MazeViewer.GOAL_COLOR

        self._draw_cells(maze_img, generated, MazeViewer.GENERATED_COLOR)
        self._draw_cells(maze_img, expanded, MazeViewer.EXPANDED_COLOR)

        maze_img = self._increase_image_size(maze_img, zoom=self._zoom)
        self._draw_grid(maze_img, self._zoom)
        if view:
            cv2_imshow(maze_img)
        cv2.waitKey(self._step)

    @staticmethod
    def pause() -> None:
        cv2.waitKey(-1)

    @staticmethod
    def _increase_image_size(img, zoom=10):
        big_img = np.zeros((img.shape[0] * zoom, img.shape[1] * zoom, 3))

        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                r_st = zoom * i
                r_end = zoom * (i + 1)
                c_st = zoom * j
                c_end = zoom * (j + 1)
                big_img[r_st: r_end, c_st: c_end] = img[i, j]

        return big_img

    @staticmethod
    def _draw_grid(maze_img, zoom):
        for i in range(0, maze_img.shape[1], zoom):
            cv2.line(maze_img, (i, 0), (i, maze_img.shape[0]), color=(0, 0, 0), thickness=1)

        for j in range(0, maze_img.shape[0], zoom):
            cv2.line(maze_img, (0, j), (maze_img.shape[1], j), color=(0, 0, 0), thickness=1)

    @staticmethod
    def _draw_cells(maze_img, cells, color):
        for cell in cells:
            maze_img[cell.y, cell.x] = color
