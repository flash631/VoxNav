# VoxNav: Voice→Intent Digital Twin for Differential-Drive Robots

A modern, software-only **digital twin** of Arduino voice-controlled robot. It provides:
- A 2D simulator (pygame) for a differential-drive robot with simple kinematics
- A natural-language **intent parser** for commands like `forward 30 cm`, `left 90`, `go to 6,3`
- A grid-based **A*** path planner with obstacle map loading from YAML
- A HAL-style "motor interface" so your old Arduino `MoveForward/SpinLeft/...` semantics map to the sim
- Tests + GitHub Actions CI

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m voxnav.ui.pygame_app --world examples/worlds/basic_10x10.yaml
```
- Click the window, then press `/` to open the command box. Type: `forward 30 cm` or `left 90` or `goto 8,2`.
- Arrow keys also drive the robot (for quick manual checks).

## Repo layout
```
src/voxnav/
  __init__.py
  control/intents.py         # text→intent parser
  planning/astar.py          # grid A* with 4/8-connectivity
  sim/robot.py               # kinematics + HAL (set_motor, move_cm, turn_deg)
  sim/world.py               # grid world, YAML loader
  ui/pygame_app.py           # pygame visualizer + command console
examples/worlds/basic_10x10.yaml
firmware/Aswin_VoiceRobot.ino
assets/                         # images/pdf for README
tests/test_astar.py
.github/workflows/ci.yml
```

## Features
- **Digital twin**: demonstrate without hardware; add sensors (line, lidar) in software and test algorithms
- **NLP-to-motion**: from voice or typed phrases → structured intents → motion primitives / paths
- **Planning-aware**: `goto x,y` runs A* over a map and follows waypoints with proportional control
- **Reproducible**: deterministic sim loops, unit tests, CI

## Next steps (ideas for issues)
- Integrate offline STT (Vosk/Whisper) and phrase grammar
- Add virtual sensors: line sensors for line-following, range rays for obstacle avoidance (Bug/DWA)
- Record telemetry to CSV + live plots
- Export ROS2 bridge (publish `/cmd_vel` from intents)

---

