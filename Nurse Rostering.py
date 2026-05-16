from pysat.solvers import Minisat22

def encode_amk_sc(variables, k, start_aux):
    n = len(variables)
    if k >= n:
        return [], start_aux, []
    if k == 0:
        return [[-v] for v in variables], start_aux, []

    clauses = []
    s = {}
    aux_id = start_aux

    for i in range(1, n):
        for j in range(1, k + 1):
            s[(i, j)] = aux_id
            aux_id += 1

    clauses.append([-variables[0], s[(1, 1)]])
    for j in range(2, k + 1):
        clauses.append([-s[(1, j)]])

    for i in range(1, n - 1):
        xi = variables[i]
        
        clauses.append([-xi, s[(i + 1, 1)]])
        clauses.append([-s[(i, 1)], s[(i + 1, 1)]])
        
        for j in range(2, min(i + 1, k) + 1):
            clauses.append([-xi, -s[(i, j - 1)], s[(i + 1, j)]])
            clauses.append([-s[(i, j)], s[(i + 1, j)]])
            
        clauses.append([-xi, -s[(i, k)]])

    clauses.append([-variables[n - 1], -s[(n - 1, k)]])

    output_states = [s[(n - 1, j)] for j in range(1, k + 1)] if n > 1 else []
    
    return clauses, aux_id, output_states

def encode_ladder_amk_2_windows(x_start, shared_block, x_end, k, start_aux):
    clauses = []
    block_clauses, next_aux, shared_out_states = encode_amk_sc(shared_block, k, start_aux)
    clauses.extend(block_clauses)
    
    if len(shared_out_states) >= k:
        s_k = shared_out_states[k - 1]
        clauses.append([-x_start, -s_k])
        clauses.append([-x_end, -s_k])
        
    if len(shared_out_states) > k:
        s_k_plus_1 = shared_out_states[k]
        clauses.append([-s_k_plus_1])
        
    return clauses, next_aux

def encode_nrp_alsc_ladder(x_start, shared_block, x_end, w, k, start_aux):
    max_false_days = w - k
    
    neg_x_start = -x_start
    neg_shared_block = [-v for v in shared_block]
    neg_x_end = -x_end
    
    return encode_ladder_amk_2_windows(
        neg_x_start, 
        neg_shared_block, 
        neg_x_end, 
        max_false_days, 
        start_aux
    )

def test_nrp():
    solver = Minisat22()
    w = 3
    k = 2
    x_start = 1
    shared_block = [2, 3]
    x_end = 4
    start_aux = 5
    
    clauses, _ = encode_nrp_alsc_ladder(x_start, shared_block, x_end, w, k, start_aux)
    for clause in clauses:
        solver.add_clause(clause)
        
    solver.add_clause([-1])
    solver.add_clause([-2])
    
    print("NRP Ladder (W=3, K=2) with x1=False, x2=False result:", solver.solve())
    solver.delete()

if __name__ == "__main__":
    test_nrp()