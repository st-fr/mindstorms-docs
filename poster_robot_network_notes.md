# Robot control and network poster

A1 portrait, 594 x 841 mm. Original vector illustrations; based on the supplied local `mindstorms-party-main` snapshot, reviewed 2026-09-04. The old poster and sources are preserved.

## Build

Run `python build_robot_network.py` with ReportLab installed. The builder uses Segoe UI and DejaVu Sans Mono from `C:/Windows/Fonts` on Windows. It writes `poster_robot_network.pdf`. Paragraph height checks catch overflow. Source graphic coordinates are scaled to A1; all diagrams remain vector graphics.

## Evidence used

Paths below are relative to the supplied project, not this poster repository.

- `ev3-control-rs/src/main.rs`, `state.rs`: four workers, shared mutex/condition variable, precision-move channel.
- `ev3-control-rs/src/config.rs`, `udp_rx.rs`, `heartbeat.rs`, `protocol.rs`: UDP 7778 / 7779, 1 Hz heartbeat, binary frame layouts, robot ID filtering and last-arriving setpoint storage.
- `ev3-control-rs/src/motor.rs`: B/C motors, 10 ms fallback tick, 150 ms continuous-drive watchdog, differential-drive mixing, joint saturation scaling, 56 mm wheel diameter and 126 mm axle spacing.
- `ev3-control-rs/src/mqtt.rs`: QoS 1, command and status topics, command IDs, completion ACKs, interruptible precision moves; beep is ACK-only.
- `desktop-app/src/robot_controller/robot_controller.cpp`: 50 ms republish period, 100 ms desktop release debounce, 3000 ms no-status timeout, 30000 ms precision-move ACK timeout; relative moves are turn -> ACK -> drive_for -> ACK.
- `desktop-app/src/robot_controller/robot_fleet.cpp`: robot addressing from heartbeat source IP.
- `desktop-app/src/collision_avoidance/collision_planner.cpp`, `playboard_graph.cpp`, `desktop-app/src/pathfinding/path_planner.cpp`: Dijkstra board routes, grid A*, checked corner smoothing, parked obstacles, occupied-target relocation, higher-ID yielding. Avoidance begins below 25 cm for watched path pairs and clears above 40 cm. If still closing below 12 cm, the yielder holds.
- `desktop-app/src/path_follower/path_follower.cpp`, `.hpp`, `desktop-app/follower_params.json`: lookahead plus heading PID, slowing into corners and near goals, pulse-and-settle turns (250/400 ms), calibration scaling; selected defaults are 20 cm lookahead, 150 mm/s maximum and 3 cm follower arrival radius.
- `desktop-app/src/map/mapwindow.cpp`: ArUco pose-to-board homography, live path-following integration and 400 ms stale-pose zero-drive rule.
- `desktop-app/src/app/main.cpp`, `communication/socket.cpp`, `communication/message_processing.cpp`, `items/shop.cpp`: TCP 1234, asynchronous network thread, JSON type dispatch, shop_buy / shop_open.
- `ar-app/Assets/Scripts/InputHandler.cs`, `Ev3UdpClient.cs`: direct phone-to-EV3 UDP, 50 ms default interval, four-byte drive packets and 150 ms zero-drive release burst.
- `desktop-app/src/mini_games/splatoon.cpp` plus Unity `Splatoon/JoystickSender.cs`, `GridReciever.cs`: minigame UDP ports 12346 input and 12345 grid output.

## Deliberate accuracy choices

The old project README and parts of shared/protocol.md mix legacy and current designs. Implementation took precedence: robot payloads are binary; phone joystick traffic is direct UDP; Rust replaces the Python brick controller. Phone scene settings can override the default transmission rate. The header's robot is a conceptual schematic, not a physical hardware photograph; route drawings are explanatory schematics, not benchmark results.

MQTT QoS 1 is at least once, not exactly once. The current Rust handler does not deduplicate command IDs. Stop sets an interrupt flag and its immediate ACK is not proof that the wheels have already halted; the poster does not make that claim. The brake payload option is not acted on in the Rust stop handler. TCP framing is inconsistent (closing brace inbound, newline outbound), and the inbound implementation can mishandle nested or coalesced JSON. Beep sound is still TODO. These are implementation gaps, not features to advertise as complete.

Collision avoidance belongs to desktop-planned motion. The direct phone joystick bypasses that planner. The 150 ms watchdog governs continuous drive, not the duration of precision moves. Distance and timing values shown are code defaults, not measured safety or performance guarantees.

## Validation

Rendered with Poppler and visually inspected at 2400 px height. Verified one A1 page, extracted text, and the QR hyperlink destination. No runtime robot tests or hardware benchmarks were performed for this poster task.

## Reconnection and broadcasts

MQTT reconnection and restored subscriptions are verified in desktop-app/src/mqtt_client/client.cpp (Mosquitto 1-10 s exponential backoff, subscription replay) and ev3-control-rs/src/mqtt.rs (rumqttc reconnect and subscribe on ConnAck). TCP broadcasts are application-level fan-out to connected clients via socket.cpp and items/shop.cpp. Robot heartbeat discovery uses unicast UDP to the configured desktop; robot_fleet.cpp refreshes each robot address from the sender IP. The supplied Unity TCPClient.cs has no automatic reconnect loop, so the poster attributes reconnection to MQTT.

## User clarification: UDP device discovery

The user clarified that the intended discovery mechanism is a network-level UDP broadcast. The poster now shows this explicitly and labels TCP as game events. No discovery port, sender, or wire format was supplied, so none is assigned in the diagram. This discovery statement comes from the user's project knowledge; the previously inspected snapshot separately contains unicast robot heartbeats and application-level TCP fan-out.

