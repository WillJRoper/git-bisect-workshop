# git-bisect-workshop

A tiny Game of Life with a bug somewhere in its history. The hands-on half of
a one-hour git workshop. Slides: <https://willjroper.github.io/git-workshop/>.

## Get started

1. Click **Fork** at the top right of this page. Keep the defaults.
2. Clone *your* fork, not this repo:

   ```bash
   git clone https://github.com/YOUR-USERNAME/git-bisect-workshop.git
   cd git-bisect-workshop
   ```

3. Run it:

   ```bash
   python life.py glider
   ```

No local setup? After forking, open your fork in a Codespace (green **Code**
button, **Codespaces** tab) and run the same commands there.

You will need a [GitHub account](https://github.com/signup), `git`, Python 3,
and a way to push to GitHub: `gh auth login`
([GitHub CLI](https://cli.github.com/)) or
[an SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

## The problem

The glider should glide diagonally across the grid forever, wrapping at the
edges. Instead it hits the bottom edge and freezes. Tag `v0.1` definitely
worked:

```bash
git switch --detach v0.1
python life.py glider
git switch main
```

The tests pass at every commit, so nobody noticed. Your job: find the commit
that broke it, fix it, add a test that would have caught it, and open a pull
request.

## The exercise

### 1. Find the culprit with `git bisect`

```bash
git bisect start
git bisect bad                 # the commit you are on is broken
git bisect good v0.1           # this tag worked
```

Git checks out a commit halfway between. Test it:

```bash
python life.py glider --steps 200 --no-animate
```

Five live cells in a glider shape means good, anything else means bad.
Then tell git, and it picks the next commit:

```bash
git bisect good    # or
git bisect bad
```

After about five rounds git prints `<sha> is the first bad commit`. Read
what it changed:

```bash
git show <sha>
git bisect reset               # back to main. Do not skip this.
```

Prefer to automate it? Save this as `check_glider.py` next to `life.py`
(untracked files survive checkouts):

```python
import life
cells = life.place(life.PATTERNS["glider"], 40, 20)
for _ in range(200):
    cells = life.step(cells, 40, 20)
raise SystemExit(0 if len(cells) == 5 else 1)
```

then `git bisect run python check_glider.py` does the whole search.

### 2. Fix it on a branch

```bash
git switch -c fix-glider
# edit life.py
python life.py glider          # flies again?
```

### 3. Add the test that was missing

The existing tests only use patterns that sit still in the middle of the
grid. Add a test to `test_life.py` that exercises the glider crossing an
edge. One idea: on a 40 by 20 grid the glider returns to its starting cells
after 160 generations.

```bash
python -m unittest -v
```

### 4. Commit and push

```bash
git status
git diff
git add life.py test_life.py
git commit -m "Fix glider freezing at the bottom edge"
git push -u origin fix-glider
```

### 5. Open a pull request

GitHub prints a link after the push. Open it, make sure the base is
`WillJRoper/git-bisect-workshop` and `main`, write one or two sentences about what
was wrong, and submit. The tests run automatically on the PR.

## Running the demo

```bash
python life.py --list
python life.py glider --width 60 --height 30 --delay 0.02
python life.py pulsar --steps 30 --no-animate
python -m unittest -v
```

## Contributing

Open an issue or a pull request. Keep commits small, one change each, with a
message that says why. Run the tests before you push.
