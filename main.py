"""
QuadTree - Computer Graphics 1, Programming Assignment 1
Pure Python 3 + tkinter (standard library only, no external libraries).

Run:  python quadtree.py

Quadrant numbering (as in the assignment picture):
        IV | I
        ---+---
        III| II
"""
import random
import tkinter as tk

SIZE = 640          # side of the square drawing area (pixels)
CAPACITY = 1        # max points stored in one leaf
MAX_DEPTH = 12      # protects against (almost) identical points
QUAD_NAMES = ["I", "II", "III", "IV"]   # child index 0..3
RANDOM_COUNT = 50   # number of points made by "Generate random points" (> 10)

# Colours
C_BG, C_GRID, C_POINT = "#f1fafa", "#7fd1cc", "#2563eb"
C_INSIDE, C_SEL = "#f59e0b", "#9333ea"
C_RECT, C_PATH = "#f9a8d4", "#e9d5ff"


class QuadNode:
    """One node of the QuadTree = one axis-aligned square of the drawing area."""

    def __init__(self, x, y, size, depth):
        self.x, self.y, self.size, self.depth = x, y, size, depth  # x, y = top-left
        self.points = []       # points stored here (only leaves hold points)
        self.children = None   # None for a leaf, else list [I, II, III, IV]

    def child_index(self, p):
        """Index of the child square that contains point p (canvas y grows downwards)."""
        mx, my = self.x + self.size / 2, self.y + self.size / 2
        right, lower = p[0] >= mx, p[1] >= my
        if right and not lower:
            return 0   # I   upper right
        if right and lower:
            return 1   # II  lower right
        if not right and lower:
            return 2   # III lower left
        return 3       # IV  upper left

    def subdivide(self):
        """Split this leaf into 4 equal squares and push its points down."""
        h, d = self.size / 2, self.depth + 1
        self.children = [
            QuadNode(self.x + h, self.y, h, d),       # I
            QuadNode(self.x + h, self.y + h, h, d),   # II
            QuadNode(self.x, self.y + h, h, d),       # III
            QuadNode(self.x, self.y, h, d),           # IV
        ]
        old, self.points = self.points, []
        for p in old:
            self.insert(p)

    def insert(self, p):
        """Insert point p = (x, y); splits leaves when they overflow."""
        if self.children:
            self.children[self.child_index(p)].insert(p)
        elif len(self.points) < CAPACITY or self.depth >= MAX_DEPTH:
            self.points.append(p)
        else:
            self.subdivide()
            self.insert(p)

    def query(self, x1, y1, x2, y2, out):
        """Collect points inside rectangle (x1,y1)-(x2,y2); skips squares that miss it."""
        if (self.x > x2 or self.x + self.size < x1 or
                self.y > y2 or self.y + self.size < y1):
            return out
        for p in self.points:
            if x1 <= p[0] <= x2 and y1 <= p[1] <= y2:
                out.append(p)
        if self.children:
            for c in self.children:
                c.query(x1, y1, x2, y2, out)
        return out

    def path_to(self, p):
        """List of (node, name) from the root down to the leaf containing p."""
        path, cur = [(self, "root")], self
        while cur.children:
            i = cur.child_index(p)
            cur = cur.children[i]
            path.append((cur, QUAD_NAMES[i]))
        return path


class App:
    """User interface + state (set B, tree Q, selection)."""

    def __init__(self, win):
        self.win = win
        win.title("QuadTree")
        self.root = QuadNode(0, 0, SIZE, 0)   # the quadtree Q
        self.points = []                      # the set B
        self.mode = tk.StringVar(value="add") # "add" | "path" | "rect"
        self.selected = None                  # selected point (path mode)
        self.path = []                        # nodes on the path to it
        self.rect = None                      # (x1, y1, x2, y2)
        self.inside = set()                   # points inside R
        self.start = None                     # drag start

        # --- canvas ---
        self.cv = tk.Canvas(win, width=SIZE, height=SIZE, bg=C_BG,
                            highlightthickness=1, highlightbackground=C_GRID)
        self.cv.pack(side="left", padx=8, pady=8)
        self.cv.bind("<ButtonPress-1>", self.on_press)
        self.cv.bind("<B1-Motion>", self.on_drag)
        self.cv.bind("<ButtonRelease-1>", lambda e: setattr(self, "start", None))

        # --- side panel ---
        panel = tk.Frame(win)
        panel.pack(side="left", fill="y", padx=8, pady=8)
        for text, val in [("Add points (click)", "add"),
                          ("Path to a point (click a point)", "path"),
                          ("Select rectangle (drag)", "rect")]:
            tk.Radiobutton(panel, text=text, variable=self.mode, value=val,
                           indicatoron=False, width=28, pady=6,
                           command=self.on_mode).pack(pady=2)
        tk.Button(panel, text="Generate random points", width=28, pady=6,
                  command=self.add_random).pack(pady=(14, 2))
        tk.Button(panel, text="Clear area", width=28, pady=6,
                  command=self.clear).pack(pady=2)
        tk.Label(panel, text="IV. | I.\n---------\nIII. | II.",
                 font=("Courier", 14)).pack(pady=14)
        self.info = tk.Label(panel, text="Click in the square to add points.",
                             wraplength=210, justify="left")
        self.info.pack(pady=6)
        tk.Label(panel, justify="left", wraplength=210,
                 text="blue = point, orange = inside R, purple = selected; pink = rectangle R").pack()
        self.draw()

    # ---------- events ----------
    def on_mode(self):
        """Mode changed: forget old selection and rectangle."""
        self.reset_selection()
        self.start = None
        self.info.config(text={"add": "Click in the square to add points.",
                               "path": "Click a point to see its path in Q.",
                               "rect": "Drag to draw rectangle R."}[self.mode.get()])
        self.draw()

    def on_press(self, e):
        m, mode = (e.x, e.y), self.mode.get()
        if mode == "add":
            self.reset_selection()
            self.points.append(m)
            self.root.insert(m)
            self.info.config(text="Points in B: %d" % len(self.points))
        elif mode == "path":
            p = self.nearest(m)
            if p is None:
                self.info.config(text="Click closer to a point.")
            else:
                self.selected = p
                self.path = self.root.path_to(p)
                names = " -> ".join(name for _, name in self.path)
                self.info.config(text="Path: " + names + " -> point")
        else:  # rect
            self.reset_selection()
            self.start = m
            self.update_rect(m)
        self.draw()

    def on_drag(self, e):
        if self.mode.get() == "rect" and self.start:
            self.update_rect((e.x, e.y))
            self.draw()

    # ---------- logic ----------
    def update_rect(self, m):
        """Rectangle from drag start to m; highlight points inside via quadtree query."""
        x1, x2 = sorted((self.start[0], m[0]))
        y1, y2 = sorted((self.start[1], m[1]))
        self.rect = (x1, y1, x2, y2)
        self.inside = set(self.root.query(x1, y1, x2, y2, []))
        self.info.config(text="Points inside R: %d of %d" %
                         (len(self.inside), len(self.points)))

    def nearest(self, m):
        """Closest point to m within 12 px, else None."""
        best, bd = None, 12 * 12
        for p in self.points:
            d = (p[0] - m[0]) ** 2 + (p[1] - m[1]) ** 2
            if d < bd:
                best, bd = p, d
        return best

    def reset_selection(self):
        self.selected, self.path, self.rect, self.inside = None, [], None, set()

    def add_random(self):
        self.reset_selection()
        for _ in range(RANDOM_COUNT):
            p = (random.randint(2, SIZE - 2), random.randint(2, SIZE - 2))
            self.points.append(p)
            self.root.insert(p)
        self.info.config(text="Points in B: %d" % len(self.points))
        self.draw()

    def clear(self):
        """Empty both B and Q."""
        self.root = QuadNode(0, 0, SIZE, 0)
        self.points = []
        self.reset_selection()
        self.info.config(text="Area cleared.")
        self.draw()

    # ---------- drawing ----------
    def draw_node(self, n):
        self.cv.create_rectangle(n.x, n.y, n.x + n.size, n.y + n.size, outline=C_GRID)
        if n.children:
            for c in n.children:
                self.draw_node(c)

    def draw(self):
        cv = self.cv
        cv.delete("all")
        # shaded squares on the path to the selected point
        for n, _ in self.path:
            cv.create_rectangle(n.x, n.y, n.x + n.size, n.y + n.size,
                                fill=C_PATH, outline="")
        # selection rectangle R
        if self.rect:
            cv.create_rectangle(*self.rect, fill=C_RECT, outline="#db2777")
        # quadtree squares
        self.draw_node(self.root)
        for n, _ in self.path:
            cv.create_rectangle(n.x + 1, n.y + 1, n.x + n.size - 1, n.y + n.size - 1,
                                outline=C_SEL, width=2)
        # points: normal / inside R / selected
        for p in self.points:
            if p == self.selected:
                col, r = C_SEL, 6
            else:
                col, r = (C_INSIDE if p in self.inside else C_POINT), 3
            cv.create_oval(p[0] - r, p[1] - r, p[0] + r, p[1] + r, fill=col, outline="")


if __name__ == "__main__":
    window = tk.Tk()
    App(window)
    window.mainloop()
