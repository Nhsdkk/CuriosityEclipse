from typing import Union
import math
import numpy as np
import matplotlib.pyplot as plt


class Equation:
    def __init__(
        self,
        r0: Union[float, int] = 0,
        time: Union[float, int] = 300,
        # u: Union[float, int] = 1.83211
        h: Union[float, int] = 1e-5,
        k: Union[float, int] = 1510.84,
        m_of: Union[float, int] = 539287,
        c: Union[float, int] = 0.5,
        v: Union[float, int] = 706.86,
        p0: Union[float, int] = 1e5,
        p_thrust: Union[float, int] = 9271000,
        temperature0: Union[float, int] = 293,
    ):
        """


        :param r0:
        :param time:
        :param h:
        :param k:
        :param m_of:
        :param c:
        :param v:
        :param p0:
        :param p_thrust:
        :param temperature0:
        """
        self.G = 6.6743 * 1e-11
        self.m_earth = 5.9742 * 1e24
        self.R = 8.31
        self.R_earth = 6371000
        self.M = 28.97 * 1e-3
        self.h = h
        self.k = k
        self.p_thrust = p_thrust
        self.m_of = m_of
        self.r0 = r0
        self.r1 = (
            self.h**2
            * (
                self.p_thrust / self.find_m(self.h)
                - self.G * self.m_earth / self.R_earth**2
            )
            / 2
        )
        self.c = c
        self.v = v
        self.p0 = p0
        self.n = int(time / self.h)
        self.temperature0 = temperature0

    def find_m(self, t: Union[float, int]) -> Union[float, int]:
        return self.m_of - self.k * t

    def find_g(self, r: Union[float, int]) -> Union[float, int]:
        return self.G * self.m_earth / (self.R_earth + r) ** 2

    def find_temperature(self, r: Union[float, int]) -> Union[float, int]:
        temp_temperature = self.temperature0 - 0.003 * r
        return 173 if temp_temperature < 173 else temp_temperature

    def find_p(self, r: Union[float, int]) -> Union[float, int]:
        return self.p0 * math.e ** (
            -self.M * self.find_g(r) * r / (self.R * self.find_temperature(r))
        )

    def find_ro(self, r: Union[float, int]) -> Union[float, int]:
        return self.find_p(r) * self.M / (self.R * self.find_temperature(r))

    def fi(self, r: Union[float, int], t: Union[float, int]) -> Union[float, int]:
        return -self.G * self.m_earth / (
            self.R_earth + r
        ) ** 2 + self.p_thrust / self.find_m(t)

    def w(self, r: Union[float, int], t: Union[float, int]) -> Union[float, int]:
        return -self.c * self.v ** (2 / 3) * self.find_ro(r) / (2 * self.find_m(t))

    def find_roots_good_approximation(
        self,
        t: Union[float, int],
        r_i_minus1: Union[float, int],
        r_i: Union[float, int],
    ) -> tuple[Union[float, int, complex], Union[float, int, complex]]:
        w_i, fi_i = self.w(r_i, t), self.fi(r_i, t)
        a = w_i / 4
        b = -1 - r_i_minus1 * w_i / 2
        c = 2 * r_i - r_i_minus1 + w_i * r_i_minus1**2 / 4 + self.h**2 * fi_i
        return np.roots(np.array([a, b, c]))

    def find_root_bad_approximation(
        self,
        t: Union[float, int],
        r_i_minus1: Union[float, int],
        r_i: Union[float, int],
    ) -> Union[float, int]:
        w_i, fi_i = self.w(r_i, t), self.fi(r_i, t)
        return 2 * r_i - r_i_minus1 + self.h**2 * fi_i + w_i * (r_i - r_i_minus1) ** 2

    def get_next_rs(
        self, t: int, r_i_minus1: Union[float, int], r_i: Union[float, int]
    ) -> tuple[Union[float, int], Union[float, int]]:
        roots = self.find_roots_good_approximation(t, r_i_minus1, r_i)
        if len(roots) == 1:
            x1, x2 = roots, roots
        else:
            x1, x2 = roots

        roots = tuple(
            item for item in [x1, x2] if item >= 0 and type(item) is not complex
        )
        x = self.find_root_bad_approximation(t, r_i_minus1, r_i)
        return x, min(roots, key=lambda q: abs(q - x))

    def solve(self) -> str:
        r_0 = self.r0
        r_1 = self.r1
        r_difference_sum = 0
        iterations = self.n
        abscissa_array = np.zeros(self.n + 2, dtype="float64")
        ord_array_1 = np.zeros(self.n + 2, dtype="float64")
        ord_array_2 = np.zeros(self.n + 2, dtype="float64")
        ord_array_1[1], ord_array_2[1] = r_1, r_1

        for i in np.arange(1, self.n + 1):
            t = i * self.h
            abscissa_array[i] = t
            ord1, ord2 = self.get_next_rs(t, r_i_minus1=r_0, r_i=r_1)
            ord_array_1[i + 1], ord_array_2[i + 1] = ord1, ord2
            if not i % 100000:
                print(
                    f"Время: {t:.5f} с, Высота: {ord2:.5f} м, Скорость: {(ord2 - r_0) / (2 * self.h):.5f} м / с, "
                    f"Ускорение: {(ord2 - 2 * r_1 + r_0) / self.h ** 2:.5f} м / c ^ 2"
                )
            r_0, r_1 = r_1, ord2
            r_difference_sum += r_1 - r_0

        plt.title("Approximations y1, y2")
        plt.xlabel("t")
        plt.ylabel("y1, y2")
        plt.grid()
        plt.plot(abscissa_array, ord_array_1, abscissa_array, ord_array_2)
        plt.show()

        return f"r(t) ~ {r_difference_sum / iterations}t"


trier = Equation()
print(trier.solve())
