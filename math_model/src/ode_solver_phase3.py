import math
import numpy as np
from scipy.integrate import odeint


def dudt(u, t):
    y, dydt = u

    P = sigma * (8 * 9.1032 * 1e3)
    T = T0 - (y - Rd) * 0.0045
    g = G * Md / y**2
    p = p0 * math.e ** (-M * g * (y - Rd) / (R * T))
    ro = p * M / (R * T)
    m = m0 - 1.13 * t * sigma

    dvdt = -(ro / 2) * (dydt**2) * alpha / m + g - P / m

    return [-dydt, dvdt]


Rd = 3.2 * 1e5

# Начальные условия
with open("phase_ends.txt", "r+") as f:
    phase_1_end = float(f.readline().split(", ")[0])
    data = f.readline().split(", ")
    phase_2_end = float(data[0])
    y0 = float(data[1]) + Rd
    vy0 = float(data[2])

beta = 0.13194
sigma = 0.12165
mf = 510 - 1.13 * (phase_2_end - phase_1_end) * beta
M = 43.05 * 1e-3
p0 = 6755
T0 = 252
Md = 4.515427 * 1e21
Vship = 24.190682312 ** (2 / 3)
CDship = 1.1507
alpha = Vship * CDship
R = 8.31
G = 6.674 * 1e-11
m0 = 3.0257 * 1e3 - 1.13 * (phase_2_end - phase_1_end) * beta

# Вектор начальных условий
u0 = [y0, vy0]

# Интервал времени
t = np.linspace(0, 217, 217000)

# Решение системы ОДУ
sol = odeint(dudt, u0, t)

with open("log_model.txt", "a+") as f:
    print("Time, Y, Vy (phase 3)", file=f)
for i in range(len(sol)):
    if not i % 100:
        with open("log_model.txt", "a+") as f:
            print(
                ", ".join(
                    [
                        str(t[i] + phase_2_end),
                        "-",
                        "-",
                        str(sol[i][0] - Rd),
                        str(sol[i][1]),
                    ]
                ),
                file=f,
            )
    if sol[i][0] - Rd <= 0:
        with open("log_model.txt", "a+") as f:
            print(
                ", ".join(
                    [
                        str(t[i] + phase_2_end),
                        "-",
                        "-",
                        str(sol[i][0] - Rd),
                        str(sol[i][1]),
                    ]
                ),
                file=f,
            )
        with open("phase_ends.txt", "a+") as f:
            print(
                ", ".join(
                    [str(t[i] + phase_2_end), str(sol[i][0] - Rd), str(sol[i][1])]
                ),
                file=f,
            )
        break
