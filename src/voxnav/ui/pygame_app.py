import argparse, pygame, sys
from ..sim.robot import Robot
from ..sim.world import World
from ..control.intents import parse_intent
from ..planning.astar import astar

CELL = 40

def draw_grid(screen, world):
    screen.fill((240,240,240))
    for y in range(world.height):
        for x in range(world.width):
            rect = pygame.Rect(x*CELL, y*CELL, CELL, CELL)
            pygame.draw.rect(screen, (210,210,210), rect, 1)
    for (x,y) in world.obstacles:
        pygame.draw.rect(screen, (120,120,120), pygame.Rect(x*CELL, y*CELL, CELL, CELL))
    gx, gy = world.goal
    pygame.draw.rect(screen, (180,255,180), pygame.Rect(gx*CELL, gy*CELL, CELL, CELL))

def draw_robot(screen, robot):
    x = robot.state.x / world.cell_cm * CELL
    y = robot.state.y / world.cell_cm * CELL
    pygame.draw.circle(screen, (0,0,0), (int(x), int(y)), 8)
    # heading line
    import math
    rad = math.radians(robot.state.heading_deg)
    hx = x + 14 * math.cos(rad)
    hy = y - 14 * math.sin(rad)
    pygame.draw.line(screen, (0,0,0), (x,y), (hx,hy), 2)

def console_draw(screen, text, active):
    s = pygame.Surface((screen.get_width(), 30), pygame.SRCALPHA)
    s.fill((255,255,255,220))
    screen.blit(s, (0, screen.get_height()-30))
    font = pygame.font.SysFont(None, 22)
    msg = ("> " + text) if active else "Press / to type a command (e.g., 'forward 30 cm', 'left 90', 'goto 8,2')"
    img = font.render(msg, True, (0,0,0))
    screen.blit(img, (8, screen.get_height()-25))

def apply_intent(robot, world, intent):
    if intent.kind == "move_cm":
        robot.move_cm(intent.value)
    elif intent.kind == "turn_deg":
        robot.turn_deg(intent.value)
    elif intent.kind == "goto":
        grid = world.grid()
        path = astar(grid, (int(robot.state.x//world.cell_cm), int(robot.state.y//world.cell_cm)), intent.target, diag=False)
        if path:
            robot.goto_waypoints(path[1:], cell_cm=world.cell_cm)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--world", default="examples/worlds/basic_10x10.yaml")
    args = parser.parse_args()
    global world
    world = World.from_yaml(args.world)
    pygame.init()
    screen = pygame.display.set_mode((world.width*CELL, world.height*CELL))
    clock = pygame.time.Clock()
    robot = Robot()
    robot.state.x = (world.start[0]+0.5) * world.cell_cm
    robot.state.y = (world.start[1]+0.5) * world.cell_cm
    robot.state.heading_deg = world.start[2]
    typing = False
    buf = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit(0)
                if event.key == pygame.K_SLASH and not typing:
                    typing = True; buf=""; continue
                if typing:
                    if event.key == pygame.K_RETURN:
                        from ..control.intents import parse_intent
                        intent = parse_intent(buf)
                        if intent:
                            apply_intent(robot, world, intent)
                        buf = ""
                        typing = False
                    elif event.key == pygame.K_BACKSPACE:
                        buf = buf[:-1]
                    else:
                        if event.unicode:
                            buf += event.unicode
                else:
                    # manual control with arrow keys
                    if event.key == pygame.K_UP: robot.move_cm(10)
                    if event.key == pygame.K_DOWN: robot.move_cm(-10)
                    if event.key == pygame.K_LEFT: robot.turn_deg(15)
                    if event.key == pygame.K_RIGHT: robot.turn_deg(-15)
        draw_grid(screen, world)
        draw_robot(screen, robot)
        console_draw(screen, buf, typing)
        pygame.display.flip()
        clock.tick(30)
