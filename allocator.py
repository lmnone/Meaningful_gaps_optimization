import os
import datetime
import numpy as np
from minizinc import Instance, Model, Solver
from pymzn import dzn


class MeaningfulGapsSolver:
    def __init__(self, model_path: str = './minizinc'):
        print('loading %s' % model_path)
        self.exec_path = os.path.join(model_path, "meaningful_gaps.mzn")
        self.triangle_solver = Model(self.exec_path)
        self.optimizer = Solver.lookup("gecode")

    def calc(self, intervals_lo: np.array, intervals_hi: np.array, movable: np.array):
        instance = Instance(self.optimizer, self.triangle_solver)

        assert intervals_lo.shape == intervals_hi.shape
        assert movable.shape == intervals_lo.shape

        instance['n_blocks'] = intervals_lo.shape[0]
        instance['intervals_lo'] = intervals_lo
        instance['intervals_hi'] = intervals_hi
        instance['movable'] = movable

        result = instance.solve(intermediate_solutions=False)
        print('found %d solutions' % len(result))
        if result.solution is None:
            return None

        return result.solution.block_2_room, result.solution.shift
