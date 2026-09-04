# Mindstorms Party Documentation

This repository contains the public project documentation for the Mindstorms Party bachelor project at the University of Bayreuth. It covers the desktop application, AR app, EV3 robot software, autonomous driving, and communication between the components.

## Documentation

### System and integration manual

**[Open the system manual](manual.pdf)** - 24 pages

The manual explains how the complete system works. It covers:

- Desktop architecture and module responsibilities
- Camera tracking, coordinate systems, and board navigation
- Route planning, path following, and multi-robot collision avoidance
- UDP, TCP, and MQTT communication
- Robot discovery, session handling, and timing constants
- AR app scenes, networking, input, and game flow
- Cross-component interactions and logging

Start here for an architectural overview or to understand how information moves through the project.

### Desktop API reference

**[Open the Doxygen reference](doxygen.pdf)** - 360 pages

This generated reference documents the C++ desktop application in detail, including classes, namespaces, files, functions, and data structures. Use it when looking up a specific implementation or interface.

### Robot and networking poster

**[Open the A1 project poster](poster_robot_network.pdf)**

The poster provides a one-page visual overview of robot control, collision avoidance, steering, safety behavior, and the UDP, TCP, and MQTT channels connecting the AR app, desktop, and EV3 robots.

## Main components

| Component | Technology | Responsibility |
| --- | --- | --- |
| Desktop application | C++23, Qt6, OpenCV | Tracking, game logic, planning, collision avoidance, and path following |
| AR app | Unity and C# | Joystick control, AR board view, and game interface |
| EV3 robot | Rust on ev3dev | Motor execution, command handling, watchdog stops, and status reporting |

For a guided explanation, read the system manual first. Use the Doxygen reference for implementation details and the poster for a compact visual summary.
