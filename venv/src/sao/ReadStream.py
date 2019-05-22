import logging

import paho.mqtt.client as mqtt
from data.CarDataMap import CarDataMap
from utilities.MiscUtils import parse_json

logger = logging.getLogger('mat_logger')


class ReadStream:

    def __init__(self, host: str = 'localhost', port: int = 1883, topic: str = 'carCoordinates'):
        self._msg_count = 0
        self._topic = topic
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(host, port, 60)
        self.cdm = CarDataMap()

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        self.client.loop_forever()

        # create a map of car data information

    def get_client(self):
        return self.client

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        data = parse_json(msg.payload)
        self.cdm.update_lat_lon(data[0], data[1], data[2], data[3])
        self.msg_count += 1
        if self.msg_count % 20 == 0:
            logger.debug(data)

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        logger.info("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(self._topic)
