import time

from shared.krpc_client import KRPCClientSingleton

if __name__ == "__main__":
    client = KRPCClientSingleton("localhost")
    earth_radius = client.get_celestial_body_radius()

    while True:
        current_time = client.get_current_time()
        current_altitude = client.get_current_altitude()
        current_pressure = client.get_current_pressure()
        print(
            f"Current: time {current_time} / altitude {current_altitude} / "
            f"pressure {current_pressure} / earth radius {earth_radius}"
        )
        time.sleep(1)
