import math
from dataclasses import dataclass

@dataclass
class RobotState:
    x: float   # in cm
    y: float
    heading_deg: float  # 0 = +x; ccw positive

class Robot:
    def __init__(self, wheelbase_cm=12.0, speed_cm_s=10.0):
        self.wheelbase_cm = wheelbase_cm
        self.speed = speed_cm_s
        self.state = RobotState(10.0, 10.0, 0.0)
    # HAL-like API
    def move_cm(self, cm: float):
        # simple straight-line move in heading
        rad = math.radians(self.state.heading_deg)
        self.state.x += cm * math.cos(rad)
        self.state.y -= cm * math.sin(rad)  # y-up in grid; screen uses y-down
    def turn_deg(self, deg: float):
        self.state.heading_deg = (self.state.heading_deg + deg) % 360.0
    def goto_waypoints(self, waypoints, cell_cm=10.0):
        # follow cell centers with proportional heading control
        for (cx, cy) in waypoints:
            tx = (cx+0.5)*cell_cm
            ty = (cy+0.5)*cell_cm
            dx = tx - self.state.x
            dy = self.state.y - ty  # invert
            ang = math.degrees(math.atan2(dy, dx))
            turn = (ang - self.state.heading_deg + 540) % 360 - 180
            self.turn_deg(turn)
            dist = math.hypot(dx, dy)
            self.move_cm(dist)
