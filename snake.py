"""一个基于 Tkinter 的简易贪吃蛇游戏。

运行方式：
    python3 snake.py

按键说明：
    ↑ ↓ ← → : 控制方向
    R        : 游戏结束后重新开始
    Esc      : 退出
"""

from __future__ import annotations

import random
import tkinter as tk
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int


class SnakeGame:
    GRID_SIZE = 20
    CELL_SIZE = 25
    WIDTH = GRID_SIZE * CELL_SIZE
    HEIGHT = GRID_SIZE * CELL_SIZE
    SPEED_MS = 120

    BG_COLOR = "#111827"
    SNAKE_COLOR = "#10b981"
    HEAD_COLOR = "#34d399"
    FOOD_COLOR = "#ef4444"
    TEXT_COLOR = "#f9fafb"

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("贪吃蛇")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            self.root,
            width=self.WIDTH,
            height=self.HEIGHT,
            bg=self.BG_COLOR,
            highlightthickness=0,
        )
        self.canvas.pack()

        self.score_var = tk.StringVar(value="分数: 0")
        score_label = tk.Label(
            self.root,
            textvariable=self.score_var,
            font=("Arial", 12, "bold"),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
            padx=8,
            pady=6,
        )
        score_label.pack(fill=tk.X)

        self.direction = Point(1, 0)
        self.next_direction = self.direction
        self.snake: list[Point] = []
        self.food = Point(0, 0)
        self.score = 0
        self.game_over = False

        self.root.bind("<Up>", lambda _e: self.set_direction(Point(0, -1)))
        self.root.bind("<Down>", lambda _e: self.set_direction(Point(0, 1)))
        self.root.bind("<Left>", lambda _e: self.set_direction(Point(-1, 0)))
        self.root.bind("<Right>", lambda _e: self.set_direction(Point(1, 0)))
        self.root.bind("<r>", lambda _e: self.restart())
        self.root.bind("<R>", lambda _e: self.restart())
        self.root.bind("<Escape>", lambda _e: self.root.destroy())

        self.restart()

    def restart(self) -> None:
        center = self.GRID_SIZE // 2
        self.snake = [Point(center - 1, center), Point(center, center), Point(center + 1, center)]
        self.direction = Point(1, 0)
        self.next_direction = self.direction
        self.score = 0
        self.game_over = False
        self.place_food()
        self.draw()
        self.update_loop()

    def set_direction(self, new_dir: Point) -> None:
        if self.game_over:
            return
        if new_dir.x == -self.direction.x and new_dir.y == -self.direction.y:
            return
        self.next_direction = new_dir

    def place_food(self) -> None:
        empty = [
            Point(x, y)
            for x in range(self.GRID_SIZE)
            for y in range(self.GRID_SIZE)
            if Point(x, y) not in self.snake
        ]
        self.food = random.choice(empty) if empty else Point(-1, -1)

    def move(self) -> None:
        if self.game_over:
            return

        self.direction = self.next_direction
        head = self.snake[-1]
        new_head = Point(head.x + self.direction.x, head.y + self.direction.y)

        out_of_bounds = (
            new_head.x < 0
            or new_head.y < 0
            or new_head.x >= self.GRID_SIZE
            or new_head.y >= self.GRID_SIZE
        )

        hit_self = new_head in self.snake
        if out_of_bounds or hit_self:
            self.game_over = True
            return

        self.snake.append(new_head)

        if new_head == self.food:
            self.score += 1
            self.score_var.set(f"分数: {self.score}")
            self.place_food()
        else:
            self.snake.pop(0)

    def draw_cell(self, p: Point, color: str) -> None:
        x1 = p.x * self.CELL_SIZE
        y1 = p.y * self.CELL_SIZE
        x2 = x1 + self.CELL_SIZE
        y2 = y1 + self.CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=self.BG_COLOR)

    def draw(self) -> None:
        self.canvas.delete("all")

        if self.food.x >= 0:
            self.draw_cell(self.food, self.FOOD_COLOR)

        for i, segment in enumerate(self.snake):
            color = self.HEAD_COLOR if i == len(self.snake) - 1 else self.SNAKE_COLOR
            self.draw_cell(segment, color)

        if self.game_over:
            self.canvas.create_text(
                self.WIDTH // 2,
                self.HEIGHT // 2,
                text="游戏结束\n按 R 重开",
                fill=self.TEXT_COLOR,
                font=("Arial", 24, "bold"),
                justify=tk.CENTER,
            )

    def update_loop(self) -> None:
        self.move()
        self.draw()
        if not self.game_over:
            self.root.after(self.SPEED_MS, self.update_loop)

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    SnakeGame().run()
