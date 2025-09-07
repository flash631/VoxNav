from heapq import heappush, heappop

def astar(grid, start, goal, diag=False):
    """
    grid: 2D list of 0 (free) / 1 (obstacle)
    start, goal: (x, y)
    diag: 8-connected if True
    Returns list of (x, y) from start to goal (inclusive) or [] if no path
    """
    w, h = len(grid[0]), len(grid)
    def neighbors(x, y):
        steps = [(-1,0),(1,0),(0,-1),(0,1)]
        if diag:
            steps += [(-1,-1),(-1,1),(1,-1),(1,1)]
        for dx, dy in steps:
            nx, ny = x+dx, y+dy
            if 0 <= nx < w and 0 <= ny < h and grid[ny][nx] == 0:
                yield nx, ny, 1.4 if dx!=0 and dy!=0 else 1.0
    def h(a,b): return abs(a[0]-b[0])+abs(a[1]-b[1])
    openq = []
    g = {start: 0.0}
    came = {}
    heappush(openq, (h(start, goal), 0.0, start))
    closed = set()
    while openq:
        _, gcost, node = heappop(openq)
        if node in closed: 
            continue
        if node == goal:
            # reconstruct
            path = [node]
            while node in came:
                node = came[node]
                path.append(node)
            return list(reversed(path))
        closed.add(node)
        for nx, ny, wgt in neighbors(*node):
            nn = (nx, ny)
            ng = gcost + wgt
            if nn in closed: 
                continue
            if ng < g.get(nn, 1e18):
                g[nn] = ng
                came[nn] = node
                heappush(openq, (ng + h(nn, goal), ng, nn))
    return []
