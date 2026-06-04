from random import choice, randint

import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

START_POSITION = (
    SCREEN_WIDTH // 2,
    SCREEN_HEIGHT // 2
)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

DIRECTION_MAP = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT,
}

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 10

pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=START_POSITION, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw_cell(self, position, color=None, border=True):
        """Отрисовывает одну ячейку игрового поля."""
        if color is None:
            color = self.body_color

        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)

        if border:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Метод отрисовки объекта."""
        raise NotImplementedError(
            'Метод draw() должен быть реализован в дочернем классе.'
        )


class Apple(GameObject):
    """Класс яблока."""

    def __init__(
        self,
        occupied_positions=None,
        position=START_POSITION,
        body_color=APPLE_COLOR
    ):
        super().__init__(position, body_color)

        if occupied_positions is None:
            occupied_positions = []

        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Устанавливает случайную позицию яблока."""
        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )

            if position not in occupied_positions:
                self.position = position
                break

    def draw(self):
        """Отрисовывает яблоко."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(
        self,
        position=START_POSITION,
        body_color=SNAKE_COLOR
    ):
        super().__init__(position, body_color)
        self.reset(RIGHT)

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки."""
        if new_direction:
            self.direction = new_direction

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction

        new_head_position = (
            (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head_position)
        self.last = self.positions.pop()

    def grow(self):
        """Увеличивает длину змейки на один сегмент."""
        if self.last:
            self.positions.append(self.last)
            self.last = None

    def reset(self, direction=None):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [self.position]
        self.direction = direction or choice((UP, DOWN, LEFT, RIGHT))
        self.last = None

    def draw(self):
        """Отрисовывает змейку."""
        self.draw_cell(self.get_head_position())

        if self.last:
            self.draw_cell(
                self.last,
                BOARD_BACKGROUND_COLOR,
                border=False
            )


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш."""
    new_direction = None

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit

            new_direction = DIRECTION_MAP.get(
                (game_object.direction, event.key)
            )

    return new_direction


def main():
    """Запускает основной игровой цикл."""
    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)

    while True:
        clock.tick(SPEED)

        new_direction = handle_keys(snake)

        snake.update_direction(new_direction)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position(snake.positions)

        elif snake.get_head_position() in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(snake.positions)

        apple.draw()
        snake.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
