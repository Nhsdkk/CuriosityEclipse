import time

from shared.krpc_client import KRPCClientSingleton
from logger.src.csv_logger_impl import CsvLogger


if __name__ == "__main__":
    client = KRPCClientSingleton("localhost")
    logger = CsvLogger()
    mars = client.get_celestial_body_by_name("Duna")
    sun = client.get_celestial_body_by_name("Sun")
    try:
        while True:
            current_time = client.get_current_time()
            logger.log("Time", current_time)
            current_altitude = client.get_current_altitude()
            logger.log("Altitude", current_time)
            current_pressure = client.get_current_pressure()
            logger.log("Pressure", current_time)
            print(
                f"Current: time {current_time}"
            )
            time.sleep(1e-3)
    except KeyboardInterrupt as err:
        print(err)
        logger.dump()
