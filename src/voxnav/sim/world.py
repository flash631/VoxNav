import yaml

class World:
    def __init__(self, width, height, obstacles=None, start=None, goal=None, cell_cm=10.0):
        self.width = width
        self.height = height
        self.obstacles = set(tuple(o) for o in (obstacles or []))
        self.start = start or [0,0,0]
        self.goal = goal or [width-1, height-1]
        self.cell_cm = cell_cm

    @classmethod
    def from_yaml(cls, path):
        with open(path, "r", encoding="utf-8") as f:
            d = yaml.safe_load(f)
        return cls(
            width=d["width"],
            height=d["height"],
            obstacles=d.get("obstacles", []),
            start=d.get("start", [0,0,0]),
            goal=d.get("goal", [d["width"]-1, d["height"]-1]),
            cell_cm=d.get("cell_cm", 10.0)
        )

    def grid(self):
        g = [[0]*self.width for _ in range(self.height)]
        for (x,y) in self.obstacles:
            if 0 <= x < self.width and 0 <= y < self.height:
                g[y][x] = 1
        return g
