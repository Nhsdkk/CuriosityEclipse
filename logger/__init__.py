import time

from shared.krpc_client import KRPCClientSingleton, FuelType
from logger.src.csv_logger_impl import CsvLogger


if __name__ == "__main__":
    client = KRPCClientSingleton("localhost")
    logger = CsvLogger()
    pr = 305.90346835177905
    pr_alt = 86.72108320347033

    summ = 0
    i = 0
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
            current_temp = client.get_current_temperature()
            if current_altitude >= 70_000:
                logger.log("Temperature", current_temp)
            print(f"Current: time {current_time}")
    except KeyboardInterrupt as err:
        print(err)
        logger.dump()
