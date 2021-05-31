import json
import logging
import socket


logging.basicConfig(level=logging.INFO)

server = socket.create_server(('0.0.0.0', 8088))
server.listen(1)

try:
    while True:
        controller, address = server.accept()
        logging.debug('New connection')
        controller.setblocking(True)
        controller.settimeout(10)
        try:
            input_buffer = str()
            while True:
                logging.debug('Waiting for data')
                data = controller.recv(256)
                if not data:
                    break
                input_buffer += data.decode('utf-8')
                logging.debug('Current input buffer: %s', input_buffer)
                if '}' in input_buffer:
                    end_of_message = input_buffer.index('}') + 1
                    message = input_buffer[:end_of_message]
                    logging.info('Message received: %s', message)
                    json_data = json.loads(message)
                    input_buffer = input_buffer[end_of_message:]
        except OSError:
            logging.exception('Got OSError')
except KeyboardInterrupt:
    server.close()
