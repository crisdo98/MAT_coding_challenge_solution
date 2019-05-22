import logging

from utilities.MiscUtils import calc_speed
from utilities.MiscUtils import get_distance_travelled

logger = logging.getLogger('mat_logger')


class CarDataMap:
    leader_chart = []
    temp_chart = []

    def __init__(self, no_of_cars=6):
        self.no_of_cars = no_of_cars - 1
        self.cars = {}
        self.init_cars()
        self.first_pass = True

    def init_cars(self):
        logger.info("*** Initialising car data map ***")
        for key in range(0, self.no_of_cars):
            self.cars[key] = {}

        for c in range(0, self.no_of_cars):
            self.cars[c]['lat1'] = 0.0
            self.cars[c]['lon1'] = 0.0
            self.cars[c]['lat2'] = 0.0
            self.cars[c]['lon2'] = 0.0
            self.cars[c]['time1'] = 0.0
            self.cars[c]['time2'] = 0.0
            self.cars[c]['speed'] = 0.0
            self.cars[c]['distance'] = 0.0
            self.cars[c]['position'] = -1
        logger.debug("Printing car map: " + str(self.cars))

    def update_lat_lon(self, car, lat, lon, time2):
        logger.debug("*** Updating lat lon for car " + str(car))
        self.cars[car]['lat1'] = self.cars[car]['lat2']
        self.cars[car]['lon1'] = self.cars[car]['lon2']
        self.cars[car]['lat2'] = lat
        self.cars[car]['lon2'] = lon
        self.cars[car]['time1'] = self.cars[car]['time2']
        self.cars[car]['time2'] = time2

        if self.cars[car]['lat1'] != 0.0:
            self.update_speed_and_distance(car)
            if car == self.no_of_cars - 1:
                self.update_leader_chart()

    def update_speed_and_distance(self, car):
        lat1 = self.cars[car]['lat1']
        lon1 = self.cars[car]['lon1']
        lat2 = self.cars[car]['lat2']
        lon2 = self.cars[car]['lon2']
        time1 = self.cars[car]['time1']
        time2 = self.cars[car]['time2']

        dist_travelled = get_distance_travelled(lat1, lon1, lat2, lon2)

        speed = calc_speed(lat1, lon1, lat2, lon2, time1, time2)
        logger.debug("Car: " + str(car) + " is travelling at " + str(speed) + "mph")
        self.cars[car]['speed'] = speed

        self.cars[car]['distance'] = self.cars[car]['distance'] + dist_travelled
        logger.debug("Total distance travelled: " + str(self.cars[car]['distance']))

    def update_leader_chart(self):
        CarDataMap.temp_chart.clear()
        try:
            for c in range(0, self.no_of_cars):
                CarDataMap.temp_chart.append((c, self.cars[c]['distance']))

            CarDataMap.temp_chart.sort(key=lambda tup: tup[1], reverse=True)
            self.print_leader_chart()

            if not self.first_pass:
                CarDataMap.leader_chart = CarDataMap.temp_chart.copy()
        except:
            logger.info("Unable to update chart")

        if self.first_pass:
            self.first_pass = False

    def print_leader_chart(self):
        if len(CarDataMap.leader_chart) > 0:
            if str((CarDataMap.temp_chart[0])[0]) != str((CarDataMap.leader_chart[0])[0]):
                logger.info("Car " + str((CarDataMap.temp_chart[0])[0]) + " has taken the lead")
            for c in range(1, len(CarDataMap.leader_chart) - 1):
                before, after = str((CarDataMap.leader_chart[c])[0]), str((CarDataMap.temp_chart[c])[0])
                if before != after:
                    logger.info("Position " + str(c + 1) + " had car " + str((CarDataMap.temp_chart[c])[0]) +
                                " but now car " + str((CarDataMap.leader_chart[c])[0]) + " has this place")
            if str((CarDataMap.temp_chart[self.no_of_cars - 1])[0]) != \
                    str((CarDataMap.leader_chart[self.no_of_cars - 1])[0]):
                logger.info("Car " + str((CarDataMap.temp_chart[self.no_of_cars - 1])[0])
                            + " has fallen into last position")
