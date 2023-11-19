from .src.dif_equation_solver import Equation

if __name__ == "__main__":
    trier = Equation(requested_flight_time=400)
    trier.solve()
