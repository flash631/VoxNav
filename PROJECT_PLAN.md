# Project Plan — VoxNav Digital Twin

## Objective
Turn the legacy Arduino voice robot into a **modern, software-only** project that demonstrates voice/NLP → intent → motion planning in a 2D simulator (digital twin).

## Problem it solves (modern framing)
- Rapidly prototype **voice-guided mobile robots** without hardware
- Test **navigation policies** (goto cells, obstacle avoidance) with repeatability
- Provide an **educational sandbox** for HRI (Human–Robot Interaction) + planning

## Roadmap (milestones)
**M0 – Initial release (you are here)**
- ✅ Pygame simulator, grid worlds, A* planner
- ✅ Intent parser for `forward/back cm`, `left/right deg`, `goto x,y`
- ✅ Unit tests + CI; include original .ino & assets

**M1 – Sensors & telemetry**
- [ ] Simulated line sensors + follow-line primitive
- [ ] Range-ray “lidar” for obstacle avoidance
- [ ] CSV telemetry + replay script

**M2 – Speech**
- [ ] Offline STT (Vosk/Whisper) CLI wrapper → intents
- [ ] Small phrase grammar + hotkeys to toggle mic in UI

**M3 – Controls & planning**
- [ ] PID for straighter tracking; smooth turn-in-place vs arc turns
- [ ] Waypoint follower with tolerance; 8-connected A* option
- [ ] D* Lite or Theta* for better paths

**M4 – Integrations**
- [ ] ROS2 bridge (`/cmd_vel`, `/odom` stubs)
- [ ] Web UI (FastAPI + simple canvas map)
- [ ] Dockerfile + devcontainer.json

## Issues to open (starter list)
- chore: add devcontainer + Dockerfile
- feat: line sensors & follow-line
- feat: range sensor and reactive avoidance
- feat: Vosk STT integration
- feat: CSV telemetry & plots
- perf: decouple sim step from render FPS
- docs: GIFs of example worlds

## Architecture (high level)
```
text/voice → intents.py → (move_cm / turn_deg / goto) → robot.py (HAL)
                                       │
                                       └─ planning/astar.py → world grid
UI (pygame_app) ↔ world.py (map) ↔ robot state (x,y,heading)
```
