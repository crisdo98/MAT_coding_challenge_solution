import json
import logging
import time

from haversine import haversine

logger = logging.getLogger('mat_logger')


def get_distance_travelled(lat1, lon1, lat2, lon2):
    coordinates1 = (lat1, lon1)
    coordinates2 = (lat2, lon2)
    return haversine(coordinates1, coordinates2, unit='mi')


def get_elapsed_time(time1, time2):
    return time2 - time1


def calc_speed(lat1, lon1, lat2, lon2, time1, time2, units="mph"):
    elapsed_time = get_elapsed_time(time1, time2)

    miles_travelled = get_distance_travelled(lat1, lon1, lat2, lon2)

    logger.debug("Elapsed time (milliseconds): " + str(elapsed_time) +
                 "; Distance travelled: " + str(miles_travelled))

    factor = 3600000 / elapsed_time
    logger.debug("Factor: " + str(factor))
    speed = miles_travelled * factor
    logger.debug("Speed = " + str(int(speed)) + units.lower())
    return speed


def parse_json(message):
    data = json.loads(str(message.decode('utf-8')))
    car_index = data['carIndex']
    lat = data['location']['lat']
    lon = data['location']['long']
    timestamp = data['timestamp']
    logger.debug("Car: " + str(car_index) + "; Lat: " + str(lat) +
                 "; Lon: " + str(lon) + "; Timestamp: " + str(timestamp))
    return car_index, lat, lon, timestamp


def get_epoch():
    return int(time.time())
