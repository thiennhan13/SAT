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

def encode_alk_sc(variables, k, start_aux):
    n = len(variables)
    max_false = n - k
    negated_vars = [-v for v in variables]
    return encode_amk_sc(negated_vars, max_false, start_aux)

def test_alk():
    solver = Minisat22()
    variables = [1, 2, 3, 4]
    k = 2
    
    clauses, _, _ = encode_alk_sc(variables, k, 5)
    for clause in clauses:
        solver.add_clause(clause)
        
    solver.add_clause([-1])
    solver.add_clause([-2])
    solver.add_clause([-3])
    
    print("ALK (k=2) with 3 False variables result:", solver.solve())
    solver.delete()

if __name__ == "__main__":
    test_alk()