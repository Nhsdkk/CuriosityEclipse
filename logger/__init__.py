from shared.krpc_client import FuelType
from logger.src.csv_logger_impl import CsvLogger
from logger.src.ksp_data_repository import KspDataRepository


if __name__ == "__main__":
    ksp_data_repository = KspDataRepository("localhost", 1000, 1001)
    logger = CsvLogger()
    print("Started")
    while True:
        try:
            current_time = ksp_data_repository.get_current_time()
            logger.log("Time", current_time)
            current_altitude = ksp_data_repository.get_current_altitude()
            logger.log("Altitude", current_altitude)
            current_pressure = ksp_data_repository.get_current_pressure()
            logger.log("Pressure", current_pressure)
            current_velocity = ksp_data_repository.get_current_velocity()
            logger.log("Velocity", current_velocity)
            current_solid_fuel_resource = ksp_data_repository.get_fuel_amount(
                FuelType.SOLID_FUEL
            )
            logger.log("SolidFuel", current_solid_fuel_resource)
            current_liquid_fuel_resource = ksp_data_repository.get_fuel_amount(
                FuelType.LIQUID_FUEL
            )
            logger.log("LiquidFuel", current_liquid_fuel_resource)
            current_temp = ksp_data_repository.get_current_temperature()

            logger.log("Temperature", current_temp)
            current_angle = ksp_data_repository.get_current_angle()
            logger.log("Angle", current_angle)
            # print(f"Current: time {current_time}")
        except KeyboardInterrupt as err:
            print(err)
            logger.dump()
