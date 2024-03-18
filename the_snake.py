from random import choice, randint

import pygame as pg

pg.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (105, 105, 105)

BORDER_COLOR = (173, 255, 47)

APPLE_COLOR = (240, 128, 128)

SNAKE_COLOR = (154, 205, 50)

SPEED = 5

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pg.display.set_caption('Змейка')

clock = pg.time.Clock()


class GameObject:
    """Базовый класс игры."""

    def __init__(self, position=(0, 0), body_color=None):
        """
        Инициализация базовых атрибутов:
            position (tuple): Позиция объекта на игровом поле.
            body_color (tuple): Цвет объекта.
        """
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод отрисовки объекта."""
        raise NotImplementedError('Метод draw должен быть переопределен.')

    def draw_cell(self):
        """Отрисовка одной ячейки на экране."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс яблока, наследуется от GameObject."""

    def __init__(self, occupied_cells=None):
        """Инициализация атрибутов яблока."""
        super().__init__(body_color=APPLE_COLOR)
        if occupied_cells is None:
            occupied_cells = []
        self.occupied_cells = occupied_cells  # Создаем атрибут occupied_cells
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию яблока на игровом поле."""
        while True:
            position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                        randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if position not in self.occupied_cells:
                self.position = position
                break

    def draw(self):
        """Отрисовка яблока на экране."""
        self.draw_cell()


class Snake(GameObject):
    """Класс змейки, наследуется от GameObject."""

    def __init__(self):
        """Инициализация атрибутов змейки."""
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_head = ((head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT)
        if new_head in self.positions[1:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.positions.pop()

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """
        Сбрасывает змейку в исходное состояние
           после столкновения с собой.
        """
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        self.next_direction = None

    def draw(self):
        """Отрисовка змейки на экране."""
        for position in self.positions[:-1]:
            self.position = position
            self.draw_cell()

        head_position = self.get_head_position()
        head_rect = pg.Rect(head_position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная логика игры."""
    snake = Snake()
    occupied_cells = snake.positions[:]
    apple = Apple(occupied_cells)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            occupied_cells = snake.positions[:]
            apple = Apple(occupied_cells)

        if snake.get_head_position() == apple.position:
            snake.length += 1
            occupied_cells.append(apple.position)
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
