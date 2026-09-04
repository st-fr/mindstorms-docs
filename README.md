# Mindstorms

Documentation for the Mindstorms Party robot-control and networking work at the University of Bayreuth.

## Poster

[Open the A1 poster](poster_robot_network.pdf)

The poster covers:

- EV3 motor control written in Rust
- Differential-drive steering and watchdog stops
- Camera-based path following and collision avoidance
- UDP motion packets and device discovery
- TCP game events
- MQTT commands, acknowledgements and reconnect behavior

## Files

- `poster_robot_network.pdf` - final A1 poster
- `build_robot_network.py` - ReportLab poster generator
- `poster_robot_network_notes.md` - source and implementation notes
- `assets/` - university logo and poster illustrations

## Rebuild

Install ReportLab and run:

```powershell
python build_robot_network.py
```

The script writes `poster_robot_network.pdf` in the repository root.
