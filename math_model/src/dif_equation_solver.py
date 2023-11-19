from typing import Union
import math
import numpy as np
import matplotlib.pyplot as plt


class Equation:
    def __init__(
        self,
        r0: Union[float, int] = 0,
        requested_flight_time: Union[float, int] = 311.3,
        h: Union[float, int] = 1e-5,
        k_fuel: Union[float, int] = 1510.84,
        mass_of_spaceship_with_fuel: Union[float, int] = 539_287,
        c_x: Union[float, int] = 0.5,
        volume: Union[float, int] = 706.86,
        pressure_0: Union[float, int] = 1e5,
        p_thrust: Union[float, int] = 9.271 * 1e6,
        temperature_0: Union[float, int] = 293,
    ):
        """
        Initialization of spaceship specifications

        :param r0: Height from sea level at the start expressed in meters
        :param requested_flight_time: Needed flight time expressed in seconds
        :param h: Step between two values in approximations
        :param k_fuel: Fuel usage constant expressed in kilograms / second (const)
        :param mass_of_spaceship_with_fuel: Full fuel mass + mass of spaceship without fuel expressed in kilograms
        :param c_x: Coefficient of aerodynamic drag (const)
        :param volume: Volume of spaceship expressed in metres ^ 3
        :param pressure_0: Air pressure on start expressed in pascals
        :param p_thrust: Thrust force expressed in newtons
        :param temperature_0: Air temperature on start expressed in kelvin degrees
        """
        self.G = 6.6743 * 1e-11
        self.EarthMass = 5.9742 * 1e24
        self.R = 8.31
        self.EarthRadius = 6.371 * 1e6
        self.AirMolarMass = 28.98 * 1e-3
        self.c_x = c_x
        self.h = h
        self.k_fuel = k_fuel
        self.p_thrust = p_thrust
        self.fullyFueledSpaceshipMass = mass_of_spaceship_with_fuel
        self.r0 = r0
        self.r1 = (
            (
                self.p_thrust / self.find_mass(self.h)
                - self.G * self.EarthMass / self.EarthRadius**2
            )
            * self.h**2
            / 2
        )
        self.volume = volume
        self.pressure_0 = pressure_0
        self.n = int(requested_flight_time / self.h)
        self.temperature_0 = temperature_0

    def find_mass(self, current_flight_time: Union[float, int]) -> Union[float, int]:
        """
        Finding mass of the spaceship at given flight time

        :param current_flight_time: Moment of flight expressed in seconds
        :return: Mass at given flight time expressed in kilograms
        """
        temporary_mass = (
            self.fullyFueledSpaceshipMass - self.k_fuel * current_flight_time
        )
        return temporary_mass if temporary_mass > 37_736 else 37_736

    def find_g(self, r: Union[float, int]) -> Union[float, int]:
        """
        Finding acceleration of free fall on given height

        :param r: Height expressed in meters
        :return: Acceleration of free fall on given height expressed in meters / second ^ 2
        """
        return self.G * self.EarthMass / (self.EarthRadius + r) ** 2

    def find_temperature(self, r: Union[float, int]) -> Union[float, int]:
        """
        Finding air temperature on given height

        :param r: Height expressed in meters
        :return: Air temperature expressed in kelvin degrees
        """
        temporary_temperature = self.temperature_0 - 0.003 * r
        return 173 if temporary_temperature < 173 else temporary_temperature

    def find_pressure(self, r: Union[float, int]) -> Union[float, int]:
        """
        Finding air pressure on given height

        :param r: Height expressed in meters
        :return: Air pressure expressed in pascals
        """
        return self.pressure_0 * math.e ** (
            -self.AirMolarMass
            * self.find_g(r)
            * r
            / (self.R * self.find_temperature(r))
        )

    def find_ro(self, r: Union[float, int]) -> Union[float, int]:
        """
        Finding air density on given height

        :param r: Height expressed in meters
        :return: Air density expressed in kilograms / metre ^ 3
        """
        return (
            self.find_pressure(r)
            * self.AirMolarMass
            / (self.R * self.find_temperature(r))
        )

    def fi(
        self, r: Union[float, int], current_flight_time: Union[float, int]
    ) -> Union[float, int]:
        temp_thrust = self.p_thrust / self.find_mass(current_flight_time)
        if current_flight_time > 311.3:
            return -self.G * self.EarthMass / (self.EarthRadius + r) ** 2
        else:
            return temp_thrust - self.G * self.EarthMass / (self.EarthRadius + r) ** 2

    def w(
        self, r: Union[float, int], current_flight_time: Union[float, int]
    ) -> Union[float, int]:
        if r > 100_000:
            return 0
        return (
            -self.c_x
            * self.volume ** (2 / 3)
            * self.find_ro(r)
            / (2 * self.find_mass(current_flight_time))
        )

    def find_roots_neat_approximation(
        self,
        current_flight_time: Union[float, int],
        r_i_minus1: Union[float, int],
        r_i: Union[float, int],
    ) -> tuple[Union[float, int, complex], Union[float, int, complex]]:
        # Написать про то, что считается уравнение вида ax^2 + bx + c = 0
        w_i, fi_i = self.w(r_i, current_flight_time), self.fi(r_i, current_flight_time)
        a = w_i / 4
        b = -1 - r_i_minus1 * w_i / 2
        c = 2 * r_i - r_i_minus1 + w_i * r_i_minus1**2 / 4 + self.h**2 * fi_i
        return np.roots(np.array([a, b, c]))

    def find_root_rough_approximation(
        self,
        current_flight_time: Union[float, int],
        r_i_minus1: Union[float, int],
        r_i: Union[float, int],
    ) -> Union[float, int]:
        w_i, fi_i = self.w(r_i, current_flight_time), self.fi(r_i, current_flight_time)
        return 2 * r_i - r_i_minus1 + self.h**2 * fi_i + w_i * (r_i - r_i_minus1) ** 2

    def get_next_r(
        self,
        current_flight_time: int,
        r_i_minus1: Union[float, int],
        r_i: Union[float, int],
    ) -> Union[float, int]:
        roots = tuple(
            item
            for item in self.find_roots_neat_approximation(
                current_flight_time, r_i_minus1, r_i
            )
            if item >= 0 and type(item) is not complex
        )
        x = self.find_root_rough_approximation(current_flight_time, r_i_minus1, r_i)
        return min(roots, key=lambda q: abs(q - x))

    def solve(self) -> None:
        r_0 = self.r0
        r_1 = self.r1
        abscissa_array = np.zeros(self.n + 2, dtype="float64")
        ordinate_array = np.zeros(self.n + 2, dtype="float64")
        ordinate_array[1] = r_1

        for i in np.arange(1, self.n + 1):
            current_flight_time = i * self.h
            abscissa_array[i] = current_flight_time
            ordinate = self.get_next_r(current_flight_time, r_i_minus1=r_0, r_i=r_1)
            ordinate_array[i + 1] = ordinate
            if not i % 100000:
                with open("rocket_flight_stats.txt", "a+") as file:
                    print(
                        f"Time: {current_flight_time:.5f} s, Height: {ordinate:.5f} m, "
                        f"Speed: {(ordinate - r_0) / (2 * self.h):.5f} m / s, "
                        f"Acceleration: {(ordinate - 2 * r_1 + r_0) / self.h ** 2:.5f} m / s ^ 2",
                        file=file,
                    )
            r_0, r_1 = r_1, ordinate
        abscissa_array[-1] = (self.n + 1) * self.h

        plt.title("Height (time) m / s")
        plt.xlabel("Time (s)")
        plt.ylabel("Height (m)")
        plt.grid()
        plt.plot(abscissa_array, ordinate_array)
        plt.show()


trier = Equation(requested_flight_time=400)
trier.solve()
