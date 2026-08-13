import argparse

OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

PATTERNS = {
    "block": {(0, 0), (1, 0), (0, 1), (1, 1)},
    "blinker": {(0, 1), (1, 1), (2, 1)},
    "glider": {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)},
}


def step(alive, width, height):
    """Advance the grid by one generation and return the new live cells.

    The grid wraps around at the edges, so it behaves like a torus.
    """
    new = set()
    for x in range(width):
        for y in range(height):
            n = sum(((x + dx) % width, (y + dy) % height) in alive for dx, dy in OFFSETS)
            if n == 3 or (n == 2 and (x, y) in alive):
                new.add((x, y))
    return new


def render(alive, width, height):
    """Return the grid as a block of text, one row per line."""
    rows = []
    for y in range(height):
        rows.append("".join("#" if (x, y) in alive else "." for x in range(width)))
    return "\n".join(rows)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Conway's Game of Life.")
    parser.add_argument("pattern", help="name of the starting pattern")
    parser.add_argument("--steps", type=int, default=10, help="generations to run")
    args = parser.parse_args(argv)

    width, height = 20, 10
    alive = set(PATTERNS[args.pattern])
    for _ in range(args.steps):
        alive = step(alive, width, height)
    print(render(alive, width, height))


if __name__ == "__main__":
    main()
