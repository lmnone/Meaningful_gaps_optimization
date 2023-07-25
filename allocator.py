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
        self.optimizer = Solver.lookup("chuffed")

    def calc(self, interval_lo: np.array, interval_hi: np.array, movable: np.array):
        instance = Instance(self.optimizer, self.triangle_solver)

        assert interval_lo.shape == interval_hi.shape
        assert movable.shape == interval_lo.shape

        instance['n_blocks'] = interval_lo.shape[0]
        instance['interval_lo'] = interval_lo
        instance['interval_hi'] = interval_hi

        result = instance.solve(intermediate_solutions=False)
        print('found %d solutions' % len(result))
        if result.solution is None:
            return None

        return result.solution.block_2_room, result.solution.shift
