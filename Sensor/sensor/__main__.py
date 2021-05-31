import logging
import os
from datetime import datetime
import random
from math import cos

import pygame
import requests

FPS = int(os.environ.get('SENSOR_FPS', 300))
FRAME_RATE = 1. / FPS

try:
    SERVICE_ADDRESS = os.environ['SENSOR_SERVICE_ADDRESS']
except KeyError as exc:
    print(f'ERROR: missing environment variable {exc}')
    exit(-1)

AMPLITUDE = random.choice((-3, -2, -1, 1, 2, 3))
PHASE = random.choice((-1.5, -1, -0.75, 0, 0.75, 1, 1.5))
ANGULAR_FREQUENCY = random.choice((1, 2, 3))


def oscillation(counter):
    return AMPLITUDE * cos(ANGULAR_FREQUENCY * counter + PHASE)


def main_loop() -> None:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    logger.propagate = False
    # Using pygame library just for controlling the frame rate is a total
    # overkill but it gets the job done better than custom code. And I consider
    # the frame rate to be important for this task.
    clock = pygame.time.Clock()
    # And let's hope the app will not go long enough for the counter to become
    # too large.
    counter = 0
    error_cooldown = 0
    while True:
        counter += 1
        if counter % FPS == 0:
            logger.debug('Current frame rate: %.2f', clock.get_fps())
        try:
            response = requests.post(
                SERVICE_ADDRESS,
                json={
                    'datetime': datetime.now().strftime('%Y%m%dT%H%M%S'),
                    'payload': oscillation(counter / FPS),
                }
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            # We do not want to get 300+ messages per second if something went
            # wrong but we sure want to know in case it did.
            if error_cooldown <= 0:
                logger.error('Exception occurred when sending data: %s',
                             repr(exc))
                error_cooldown = FPS
        finally:
            error_cooldown = max(error_cooldown - 1, 0)
        clock.tick(FPS)


pygame.init()

try:
    main_loop()
except KeyboardInterrupt:
    pygame.quit()
