from .src.dif_equation_solver import Equation
from .src.graph_generator import GraphGenerator

if __name__ == "__main__":
    trier = Equation(requested_flight_time=400)
    t_values, h_values = trier.solve()
    GraphGenerator.create_height_graph(t_values, h_values)
