import pygame
import sys

from typing import List, Tuple, Optional
from . import algorithms as ga

WINDOW_WIDTH: int = 800
WINDOW_HEIGHT: int = 600
BG_COLOR: Tuple[int, int, int] = (255, 255, 255)  # Branco
DRAW_COLOR: Tuple[int, int, int] = (0, 0, 0)  # Preto
FILL_COLOR: Tuple[int, int, int] = (100, 100, 255)  # Azul claro
CLIPPED_COLOR: Tuple[int, int, int] = (255, 0, 0)  # Vermelho
CLIP_WINDOW_COLOR: Tuple[int, int, int] = (0, 255, 0)  # Verde

Point = Tuple[int, int]


def main() -> None:
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Computação gráfica: Lista 01")

    my_polygon: List[Point] = [
        (600, 100),
        (750, 200),
        (700, 350),
        (550, 300),
        (500, 150),
    ]

    lines_to_clip: List[Tuple[Point, Point]] = [
        ((50, 50), (250, 250)),  # Totalmente dentro
        ((10, 150), (80, 280)),  # Parcialmente dentro
        ((150, 30), (150, 350)),  # Atravessando verticalmente
        ((300, 100), (400, 150)),  # Totalmente fora
        ((30, 300), (350, 300)),  # Totalmente fora (abaixo)
    ]

    clip_window: pygame.Rect = pygame.Rect(100, 100, 200, 150)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BG_COLOR)

        ga.fill_polygon_scanline(screen, my_polygon, FILL_COLOR)
        ga.draw_polygon(screen, my_polygon, DRAW_COLOR)

        pygame.draw.rect(screen, CLIP_WINDOW_COLOR, clip_window, 2)

        pygame.draw.circle(screen, (255, 165, 0), (400, 500), 50)
        ga.draw_line_midpoint(screen, 50, 450, 300, 550, (128, 0, 128))

        for line in lines_to_clip:
            p1, p2 = line

            ga.draw_line_midpoint(screen, p1[0], p1[1], p2[0], p2[1], (200, 200, 200))

            clip_result: Optional[Tuple[int, int, int, int]] = ga.cohen_sutherland_clip(
                p1[0],
                p1[1],
                p2[0],
                p2[1],
                clip_window.left,
                clip_window.top,
                clip_window.right,
                clip_window.bottom,
            )

            if clip_result:
                x1_c, y1_c, x2_c, y2_c = clip_result
                ga.draw_line_midpoint(screen, x1_c, y1_c, x2_c, y2_c, CLIPPED_COLOR)

        pygame.display.flip()


if __name__ == "__main__":
    main()
