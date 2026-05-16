import math
from pysat.solvers import Glucose3

class LadderAMKEncoder:
    def __init__(self, solver, start_var_id):
        self.solver = solver
        self.current_var_id = start_var_id

    def _build_sc_block(self, block_vars, k, is_amk_block):
        n = len(block_vars)
        R = {}
        
        for i in range(1, n + 1):
            R[i] = {}
            for j in range(1, min(i, k) + 1):
                R[i][j] = self.current_var_id
                self.current_var_id += 1

        if n == 0:
            return R

        for i in range(1, n):
            self.solver.add_clause([-block_vars[i-1], R[i][1]])

        for i in range(2, n + 1):
            for j in range(1, min(i - 1, k) + 1):
                self.solver.add_clause([-R[i-1][j], R[i][j]])

        for i in range(2, n + 1):
            for j in range(2, min(i, k) + 1):
                self.solver.add_clause([-block_vars[i-1], -R[i-1][j-1], R[i][j]])

        for i in range(1, min(n, k) + 1):
            self.solver.add_clause([block_vars[i-1], -R[i][i]])

        for i in range(2, n + 1):
            for j in range(2, min(i, k) + 1):
                self.solver.add_clause([R[i-1][j-1], -R[i][j]])

        for i in range(2, n + 1):
            for j in range(1, min(i - 1, k) + 1):
                self.solver.add_clause([block_vars[i-1], R[i-1][j], -R[i][j]])

        if is_amk_block:
            for i in range(k + 1, n + 1):
                self.solver.add_clause([-block_vars[i-1], -R[i-1][k]])

        return R

    def _connect_blocks(self, r_left, r_right, overlap, k):
        for i in range(1, overlap + 1):
            j_left = i
            j_right = overlap - i + 1
            
            if j_left not in r_left or j_right not in r_right:
                continue
                
            for p in range(1, k + 1):
                req_left = k - p + 1
                req_right = p
                
                if req_left <= min(j_left, k) and req_right <= min(j_right, k):
                    left_var = r_left[j_left][req_left]
                    right_var = r_right[j_right][req_right]
                    self.solver.add_clause([-left_var, -right_var])

    def encode(self, variables, w, k):
        n = len(variables)
        num_areas = math.ceil(n / w)
        
        forward_blocks = {}
        backward_blocks = {}

        for area_idx in range(num_areas):
            start_idx = area_idx * w
            end_idx = min(start_idx + w, n)
            area_vars = variables[start_idx:end_idx]

            if area_idx != 0:
                forward_blocks[area_idx] = self._build_sc_block(area_vars, k, True)

            if area_idx != num_areas - 1:
                backward_blocks[area_idx] = self._build_sc_block(area_vars[::-1], k, False)

        for area_idx in range(num_areas - 1):
            if area_idx in backward_blocks and (area_idx + 1) in forward_blocks:
                self._connect_blocks(
                    backward_blocks[area_idx],
                    forward_blocks[area_idx + 1],
                    w - 1,
                    k
                )
        
        return self.current_var_id

def ladder_amk():
    solver = Glucose3()
    n = 10
    w = 4
    k = 2
    variables = list(range(1, n + 1))
    
    encoder = LadderAMKEncoder(solver, start_var_id=11)
    encoder.encode(variables, w, k)
    
    solver.add_clause([3])
    solver.add_clause([4])
    solver.add_clause([5])
    
    result = solver.solve()
    print("SAT" if result else "UNSAT")
    solver.delete()

if __name__ == "__main__":
    ladder_amk()