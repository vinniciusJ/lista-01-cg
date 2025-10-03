import pygame

from typing import List, Tuple, Optional

Color = Tuple[int, int, int]
Point = Tuple[int, int]

INSIDE = 0  # 0000
LEFT = 1  # 0001
RIGHT = 2  # 0010
BOTTOM = 4  # 0100
TOP = 8  # 1000


def draw_line_midpoint(
    surface: pygame.Surface, x1: int, y1: int, x2: int, y2: int, color: Color
) -> None:
    dx = x2 - x1
    dy = y2 - y1

    sign_x = 1 if dx > 0 else -1
    sign_y = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dy > dx:
        dx, dy = dy, dx
        swapped = True
    else:
        swapped = False

    p = 2 * dy - dx
    x, y = x1, y1

    for _ in range(dx + 1):
        pygame.draw.circle(surface, color, (x, y), 1)

        if p >= 0:
            if swapped:
                x += sign_x
            else:
                y += sign_y

            p -= 2 * dx

        if swapped:
            y += sign_y
        else:
            x += sign_x

        p += 2 * dy


def _get_region_code(x: int, y: int, xmin: int, ymin: int, xmax: int, ymax: int) -> int:
    code = INSIDE

    if x < xmin:
        code |= LEFT
    elif x > xmax:
        code |= RIGHT
    if y < ymin:
        code |= TOP
    elif y > ymax:
        code |= BOTTOM

    return code


def cohen_sutherland_clip(
    x1: int, y1: int, x2: int, y2: int, xmin: int, ymin: int, xmax: int, ymax: int
) -> Optional[Tuple[int, int, int, int]]:
    code1 = _get_region_code(x1, y1, xmin, ymin, xmax, ymax)
    code2 = _get_region_code(x2, y2, xmin, ymin, xmax, ymax)
    accepted = False

    while True:
        if code1 == 0 and code2 == 0:
            accepted = True
            break
        elif (code1 & code2) != 0:
            break
        else:
            x, y = 0.0, 0.0
            outside_code = code1 if code1 != 0 else code2

            if outside_code & TOP:
                dy = y2 - y1
                x = x1 + (x2 - x1) * (ymin - y1) / dy if dy != 0 else x1
                y = ymin
            elif outside_code & BOTTOM:
                dy = y2 - y1
                x = x1 + (x2 - x1) * (ymax - y1) / dy if dy != 0 else x1
                y = ymax
            elif outside_code & RIGHT:
                dx = x2 - x1
                y = y1 + (y2 - y1) * (xmax - x1) / dx if dx != 0 else y1
                x = xmax
            elif outside_code & LEFT:
                dx = x2 - x1
                y = y1 + (y2 - y1) * (xmin - x1) / dx if dx != 0 else y1
                x = xmin

            if outside_code == code1:
                x1, y1 = int(x), int(y)
                code1 = _get_region_code(x1, y1, xmin, ymin, xmax, ymax)
            else:
                x2, y2 = int(x), int(y)
                code2 = _get_region_code(x2, y2, xmin, ymin, xmax, ymax)

    if accepted:
        return (x1, y1, x2, y2)
    else:
        return None


def draw_polygon(surface: pygame.Surface, vertices: List[Point], color: Color) -> None:
    num_vertices = len(vertices)

    if num_vertices < 2:
        return

    for i in range(num_vertices):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % num_vertices]

        draw_line_midpoint(surface, p1[0], p1[1], p2[0], p2[1], color)


def fill_polygon_scanline(
    surface: pygame.Surface, vertices: List[Point], color: Color
) -> None:
    if not vertices:
        return

    min_y = min(v[1] for v in vertices)
    max_y = max(v[1] for v in vertices)

    for y in range(min_y, max_y + 1):
        intersections: List[int] = []

        for i in range(len(vertices)):
            p1 = vertices[i]
            p2 = vertices[(i + 1) % len(vertices)]

            if p1[1] > p2[1]:
                p1, p2 = p2, p1

            if y > p1[1] and y <= p2[1] and (p2[1] - p1[1]) != 0:
                x_intersection = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
                intersections.append(int(x_intersection))

        intersections.sort()

        for i in range(0, len(intersections), 2):
            if i + 1 < len(intersections):
                x_start, x_end = intersections[i], intersections[i + 1]

                pygame.draw.line(surface, color, (x_start, y), (x_end, y))
