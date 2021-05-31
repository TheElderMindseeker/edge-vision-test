import asyncio
import json
import logging
import random
from collections import defaultdict

from aiohttp import web


routes = web.RouteTableDef()


async def control_manipulator(app):
    sensor_data = app['sensor_data']
    while True:
        logging.info('Control manipulator')
        size = sum(len(array) for array in sensor_data.values())
        logging.info('Total messages: %d', size)
        signal_sum = 0
        for time_stamp in sorted(sensor_data.keys()):
            partial_sum = sum(sensor_data[time_stamp])
            signal_sum = signal_sum / 2 + partial_sum
        logging.debug('Signal sum: %f', signal_sum)
        try:
            _, writer = await asyncio.open_connection('manipulator', 8088)
            logging.debug('Connected successfully')
            message = {
                'datetime': list(sensor_data.keys())[-1],
                'status': 'up' if signal_sum > 0 else 'down',
            }
            message_dump = json.dumps(message, indent=None, separators=(',', ':'))
            logging.info('Sending message: %s', message_dump)
            writer.write(message_dump.encode('utf-8'))
            await writer.drain()
            logging.debug('Message sent')
            writer.close()
            await writer.wait_closed()
            logging.debug('Socket closed')
        except Exception as exc:
            logging.error(repr(exc))
        sensor_data.clear()
        await asyncio.sleep(5)


async def start_background_task(app):
    app['control_task'] = asyncio.create_task(control_manipulator(app))


async def cleanup_background_task(app):
    app['control_task'].cancel()
    await app['control_task']


@routes.post('/data')
async def accept_data(request: web.Request):
    if request.content_type != 'application/json':
        raise web.HTTPBadRequest
    sensor_data = request.app['sensor_data']
    json_data = await request.json()
    sensor_data[json_data['datetime']].append(json_data['payload'])
    return web.Response(text='OK')


logging.basicConfig(level=logging.DEBUG)
logging.debug('Started')
app = web.Application()
app.add_routes(routes)
app['sensor_data'] = defaultdict(list)
app.on_startup.append(start_background_task)
app.on_cleanup.append(cleanup_background_task)
