from voxnav.planning.astar import astar

def test_astar_simple():
    grid = [
        [0,0,0],
        [1,1,0],
        [0,0,0],
    ]
    path = astar(grid, (0,0), (2,2))
    assert path[0] == (0,0) and path[-1] == (2,2)
    # ensure it routes around obstacle
    assert (1,0) in path or (0,1) in path
