
from numpy import ndarray

class SimData:
    """Sim data class. Stores and validates simulation results."""
    def __init__(self):
        self._sim_data: ndarray = None

    @property
    def sim_data(self):
        return self._sim_data
    
    @sim_data.setter    
    def sim_data(self, sim_data: ndarray):
        if not isinstance(sim_data, ndarray):
            raise ValueError("Monte Carlo simulation data must be of type numpy.ndarray")
        self._sim_data = sim_data