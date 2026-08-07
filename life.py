OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

PATTERNS = {
    "block": {(0, 0), (1, 0), (0, 1), (1, 1)},
    "blinker": {(0, 1), (1, 1), (2, 1)},
}


def step(alive, width, height):
    """Advance the grid by one generation and return the new live cells."""
    new = set()
    for x in range(width):
        for y in range(height):
            n = sum((x + dx, y + dy) in alive for dx, dy in OFFSETS)
            if n == 3 or (n == 2 and (x, y) in alive):
                new.add((x, y))
    return new
