import time

from shared.krpc_client import KRPCClientSingleton, FuelType
from logger.src.csv_logger_impl import CsvLogger


if __name__ == "__main__":
    client = KRPCClientSingleton("localhost")
    logger = CsvLogger()
    try:
        while True:
            current_time = client.get_current_time()
            logger.log("Time", current_time)
            current_altitude = client.get_current_altitude()
            logger.log("Altitude", current_altitude)
            current_pressure = client.get_current_pressure()
            logger.log("Pressure", current_pressure)
            current_velocity = client.get_current_velocity()
            logger.log("Velocity", current_velocity)
            current_solid_fuel_resource = client.get_fuel_amount(FuelType.SOLID_FUEL)
            logger.log("SolidFuel", current_solid_fuel_resource)
            current_liquid_fuel_resource = client.get_fuel_amount(FuelType.LIQUID_FUEL)
            logger.log("LiquidFuel", current_liquid_fuel_resource)
            print(f"Current: time {current_time}")
            time.sleep(1e-3)
    except KeyboardInterrupt as err:
        print(err)
        logger.dump()
