# Import key functions/classes from modules to make them accessible at the package level
from .data_generation import simulate_data
from .model import train_model
from .visualization import plot_data

# Define what gets imported when using `from tipper_truck_model import *`
__all__ = [
    "simulate_data" "train_model",
    "evaluate_model",
    "plot_data",
]
