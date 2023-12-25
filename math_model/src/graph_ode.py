import matplotlib.pyplot as plt
import math
import numpy as np

with open("log_model.txt") as f:
    data = f.read()
    time_array = np.array(
        [float(i.split(", ")[0]) for i in data.split("\n")], dtype="float64"
    )
    height_array = np.array(
        [
            math.hypot(float(i.split(", ")[2]), float(i.split(", ")[4]))
            for i in data.split("\n")
        ],
        dtype="float64",
    )
with open("out (5).csv") as f:
    data = f.read()
    time_array_ksp = np.array(
        [(float(i.split(",")[0]) - 22395729.7388) for i in data.split("\n")],
        dtype="float64",
    )
    height_array_ksp = np.array(
        [float(i.split(",")[3]) for i in data.split("\n")], dtype="float64"
    )

plt.title("Speed (m / sec) / Blue - SciPy / Green - KSP")
plt.xlabel("Time (sec)")
plt.ylabel("Speed (m / sec)")
plt.grid()
plt.plot(time_array, height_array, "b", time_array_ksp, height_array_ksp, "g")
plt.show()
