# Mindstorms

Public documentation for the Mindstorms Party bachelor project at the University of Bayreuth.

## Project poster

[View the final A1 poster](poster_robot_network.pdf)

The poster explains the robot-control system, collision avoidance, steering, and communication between the AR app, desktop application, and EV3 robots.

## System overview

| Component | Role |
| --- | --- |
| AR App | Unity joystick and game interface |
| Desktop | Camera tracking, route planning, collision avoidance, and path following |
| EV3 robot | Rust-based motor execution, status reporting, and safety checks |

## Network communication

### UDP

Compact binary motion packets keep control latency low. The AR app and desktop send fresh speed-and-turn commands to the robot at 20 Hz. UDP broadcasts discover robots on the local network, while heartbeats refresh their addresses and report state.

### TCP

The AR app and desktop exchange structured JSON game events over TCP. These messages carry events such as shop actions and shared game-state updates.

### MQTT

MQTT carries commands that require acknowledgements, including distance moves, turns, stops, and status requests. Clients reconnect automatically and restore their subscriptions after a connection loss.

## Autonomous driving

The desktop plans routes with Dijkstra and uses grid-based A* when another robot blocks the route. A coordinator resolves path conflicts and can move a parked robot away from an occupied destination.

ArUco markers provide each robot's position and heading. A camera homography converts image coordinates to centimetres. The path follower selects a lookahead target, calculates the heading error, and adjusts forward speed and turn rate until the robot reaches its destination.

## EV3 control and safety

The EV3 software runs natively in Rust. Separate workers receive UDP data, control the motors, process MQTT commands, and send heartbeats.

- A 150 ms watchdog stops continuous motion when drive packets stop arriving.
- A stale camera pose causes the desktop to command zero motion after 400 ms.
- An MQTT stop request interrupts an active distance or turn command.
