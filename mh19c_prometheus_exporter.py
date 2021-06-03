import time

import mh_z19
from prometheus_client import Gauge
from prometheus_client import start_http_server, Summary

REQUEST_TIME = Summary('request_processing_seconds',
                       'Time spent processing request')
gauge_co2 = Gauge('atmosphere_mainroom_co2', "Main room CO2 level")
gauge_temperature = Gauge('atmosphere_mainroom_temperature',
                          "Main room temperature")


@REQUEST_TIME.time()
def process_request(wait_second: int):
    sensor_values = mh_z19.read_all()
    gauge_co2.set(sensor_values['co2'])
    gauge_temperature.set(sensor_values['temperature'])

    time.sleep(wait_second)


if __name__ == '__main__':
    start_http_server(8000)
    while True:
        process_request(300)
