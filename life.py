import argparse
import time

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
    parser.add_argument("--steps", type=int, default=100, help="generations to run")
    parser.add_argument("--width", type=int, default=40, help="grid width in cells")
    parser.add_argument("--height", type=int, default=20, help="grid height in cells")
    parser.add_argument("--no-animate", action="store_true", help="print only the final grid")
    args = parser.parse_args(argv)

    alive = set(PATTERNS[args.pattern])
    for _ in range(args.steps):
        if not args.no_animate:
            print("\033[2J\033[H" + render(alive, args.width, args.height))
            time.sleep(0.1)
        alive = step(alive, args.width, args.height)
    if args.no_animate:
        print(render(alive, args.width, args.height))


if __name__ == "__main__":
    main()
