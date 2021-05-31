# EdgeVision Testing Task

This is my solution to EdgeVision testing task. The solution contains three components: Sensor, Controller, and
Manipulator. Sensor produces and sends data to Controller at 300 FPS (by default) using JSON API. Controller stores
data and periodically (once per 5 seconds) sends signal to Manipulator over TCP socket. Manipulator accepts commands
and logs them.

## Running in Docker Compose

The easiest way to run the system is the following Docker Compose command:

```bash
docker-compose up --scale sensor=8 [--build]
```

Use `--build` option if you are running the system for the first time or have made some changes to the code.
