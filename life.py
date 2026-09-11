"""Conway's Game of Life on a wrapping grid.

Run a named pattern and watch it evolve in the terminal:

    python life.py glider
    python life.py blinker --steps 20 --delay 0.2
"""
import argparse
import time

OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

PATTERNS = {
    "block": {(0, 0), (1, 0), (0, 1), (1, 1)},
    "blinker": {(0, 1), (1, 1), (2, 1)},
    "glider": {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)},
    "toad": {(1, 1), (2, 1), (3, 1), (0, 2), (1, 2), (2, 2)},
    "beacon": {(0, 0), (1, 0), (0, 1), (1, 1), (2, 2), (3, 2), (2, 3), (3, 3)},
    "lwss": {(1, 0), (4, 0), (0, 1), (0, 2), (4, 2), (0, 3), (1, 3), (2, 3), (3, 3)},
}


def count_neighbours(alive: set[tuple[int, int]], x: int, y: int, width: int, height: int) -> int:
    """Count the live neighbours of (x, y), wrapping at the edges."""
    return sum(((x + dx) % width, (y + dy) % width) in alive for dx, dy in OFFSETS)


def step(alive: set[tuple[int, int]], width: int, height: int) -> set[tuple[int, int]]:
    """Advance the grid by one generation and return the new live cells.

    The grid wraps around at the edges, so it behaves like a torus.
    """
    new = set()
    for x in range(width):
        for y in range(height):
            n = count_neighbours(alive, x, y, width, height)
            if n == 3 or (n == 2 and (x, y) in alive):
                new.add((x, y))
    return new


def render(alive: set[tuple[int, int]], width: int, height: int) -> str:
    """Return the grid as a block of text, one row per line."""
    rows = []
    for y in range(height):
        rows.append("".join("█" if (x, y) in alive else "·" for x in range(width)))
    return "\n".join(rows)


def place(pattern: set[tuple[int, int]], width: int, height: int, x0: int = 1, y0: int = 1) -> set[tuple[int, int]]:
    """Return a copy of the pattern shifted to start at (x0, y0)."""
    cells = {(x + x0, y + y0) for x, y in pattern}
    if any(x >= width or y >= height for x, y in cells):
        raise ValueError("pattern does not fit in the grid")
    return cells


def main(argv=None):
    parser = argparse.ArgumentParser(description="Conway's Game of Life.")
    parser.add_argument("pattern", help="name of the starting pattern")
    parser.add_argument("--steps", type=int, default=100, help="generations to run")
    parser.add_argument("--width", type=int, default=40, help="grid width in cells")
    parser.add_argument("--height", type=int, default=20, help="grid height in cells")
    parser.add_argument("--delay", type=float, default=0.1, help="seconds between frames")
    parser.add_argument("--no-animate", action="store_true", help="print only the final grid")
    args = parser.parse_args(argv)

    alive = place(PATTERNS[args.pattern], args.width, args.height)
    for generation in range(args.steps):
        if not args.no_animate:
            print("\033[2J\033[H" + render(alive, args.width, args.height))
            print(f"generation {generation}, {len(alive)} alive")
            time.sleep(args.delay)
        alive = step(alive, args.width, args.height)
    if args.no_animate:
        print(render(alive, args.width, args.height))
        print(f"generation {args.steps}, {len(alive)} alive")


if __name__ == "__main__":
    main()
