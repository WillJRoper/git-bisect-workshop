"""Conway's Game of Life on a wrapping grid.

Run a named pattern and watch it evolve in the terminal:

    python life.py glider
    python life.py blinker --steps 20 --delay 0.2
"""
import argparse
import os
import random
import time

CLEAR = "cls" if os.name == "nt" else "clear"

OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

PATTERNS = {
    "beacon": {(0, 0), (1, 0), (0, 1), (1, 1), (2, 2), (3, 2), (2, 3), (3, 3)},
    "blinker": {(0, 1), (1, 1), (2, 1)},
    "block": {(0, 0), (1, 0), (0, 1), (1, 1)},
    "glider": {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)},
    "lwss": {(1, 0), (4, 0), (0, 1), (0, 2), (4, 2), (0, 3), (1, 3), (2, 3), (3, 3)},
    "pulsar": {
        (0, 2), (0, 3), (0, 4), (0, 8), (0, 9), (0, 10),
        (2, 0), (2, 5), (2, 7), (2, 12), (3, 0), (3, 5),
        (3, 7), (3, 12), (4, 0), (4, 5), (4, 7), (4, 12),
        (5, 2), (5, 3), (5, 4), (5, 8), (5, 9), (5, 10),
        (7, 2), (7, 3), (7, 4), (7, 8), (7, 9), (7, 10),
        (8, 0), (8, 5), (8, 7), (8, 12), (9, 0), (9, 5),
        (9, 7), (9, 12), (10, 0), (10, 5), (10, 7), (10, 12),
        (12, 2), (12, 3), (12, 4), (12, 8), (12, 9), (12, 10),
    },
    "toad": {(1, 1), (2, 1), (3, 1), (0, 2), (1, 2), (2, 2)},
}


def count_neighbours(alive: set[tuple[int, int]], x: int, y: int, width: int, height: int) -> int:
    """Count the live neighbours of one cell.

    The grid wraps at the edges, so a cell on the left edge neighbours the
    right edge and a cell on the top edge neighbours the bottom.

    Args:
        alive: The set of live cells as (x, y) pairs.
        x: Column of the cell to inspect.
        y: Row of the cell to inspect.
        width: Width of the grid in cells.
        height: Height of the grid in cells.

    Returns:
        The number of live cells among the eight neighbours, 0 to 8.
    """
    return sum(((x + dx) % width, (y + dy) % width) in alive for dx, dy in OFFSETS)


def step(alive: set[tuple[int, int]], width: int, height: int) -> set[tuple[int, int]]:
    """Advance the grid by one generation.

    Applies Conway's rules to every cell: a live cell with two or three live
    neighbours survives, a dead cell with exactly three live neighbours is
    born, everything else is dead in the next generation. The grid wraps
    around at the edges, so it behaves like a torus.

    Args:
        alive: The set of live cells as (x, y) pairs.
        width: Width of the grid in cells.
        height: Height of the grid in cells.

    Returns:
        A new set of live cells for the next generation. The input set is
        not modified.
    """
    new = set()
    for x in range(width):
        for y in range(height):
            n = count_neighbours(alive, x, y, width, height)
            if n == 3 or (n == 2 and (x, y) in alive):
                new.add((x, y))
    return new


def render(alive: set[tuple[int, int]], width: int, height: int) -> str:
    """Draw the grid as text.

    Args:
        alive: The set of live cells as (x, y) pairs.
        width: Width of the grid in cells.
        height: Height of the grid in cells.

    Returns:
        A string with one line per row, a block glyph for each live cell and
        a dot for each dead cell. No trailing newline.
    """
    rows = []
    for y in range(height):
        rows.append("".join("█" if (x, y) in alive else "·" for x in range(width)))
    return "\n".join(rows)


def place(pattern: set[tuple[int, int]], width: int, height: int, x0: int = 1, y0: int = 1) -> set[tuple[int, int]]:
    """Offset a pattern so it sits inside the grid.

    Args:
        pattern: Cells of the pattern as (x, y) pairs relative to its own
            top left corner.
        width: Width of the grid in cells.
        height: Height of the grid in cells.
        x0: Column to place the pattern's left edge at.
        y0: Row to place the pattern's top edge at.

    Returns:
        A new set of cells shifted by (x0, y0).

    Raises:
        ValueError: If any shifted cell falls outside the grid.
    """
    cells = {(x + x0, y + y0) for x, y in pattern}
    if any(x >= width or y >= height for x, y in cells):
        raise ValueError("pattern does not fit in the grid")
    return cells


def main(argv=None):
    """Run the command line interface.

    Parses the arguments, builds the starting grid from a named pattern or a
    random seed, then either animates it in the terminal or prints only the
    final generation.

    Args:
        argv: Command line arguments to parse. Defaults to ``sys.argv[1:]``
            when None.
    """
    parser = argparse.ArgumentParser(description="Conway's Game of Life.")
    parser.add_argument("pattern", nargs="?", choices=sorted(PATTERNS), help="name of the starting pattern")
    parser.add_argument("--seed", type=int, help="start from a random grid with this seed")
    parser.add_argument("--list", action="store_true", help="list the available patterns and exit")
    parser.add_argument("--steps", type=int, default=100, help="generations to run")
    parser.add_argument("--width", type=int, default=40, help="grid width in cells")
    parser.add_argument("--height", type=int, default=20, help="grid height in cells")
    parser.add_argument("--delay", type=float, default=0.1, help="seconds between frames")
    parser.add_argument("--no-animate", action="store_true", help="print only the final grid")
    args = parser.parse_args(argv)

    if args.list:
        print("\n".join(sorted(PATTERNS)))
        return
    if args.seed is not None:
        rng = random.Random(args.seed)
        alive = {(x, y) for x in range(args.width) for y in range(args.height) if rng.random() < 0.3}
    elif args.pattern:
        alive = place(PATTERNS[args.pattern], args.width, args.height)
    else:
        parser.error("give a pattern name or --seed")
    for generation in range(args.steps):
        if not args.no_animate:
            os.system(CLEAR)
            print(render(alive, args.width, args.height))
            print(f"generation {generation}, {len(alive)} alive")
            time.sleep(args.delay)
        alive = step(alive, args.width, args.height)
    if args.no_animate:
        print(render(alive, args.width, args.height))
        print(f"generation {args.steps}, {len(alive)} alive")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
