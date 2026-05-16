from itertools import combinations

def encode_alo(variables):
    """
    At Least One: Trả về 1 clause duy nhất chứa tất cả các biến.
    """
    return [variables]

def encode_amo_binomial(variables):
    """
    At Most One (Binomial Encoding)
    O(n^2) clauses, 0 biến phụ.
    """
    clauses = []
    for xi, xj in combinations(variables, 2):
        clauses.append([-xi, -xj])
    return clauses

def encode_amo_sequential_counter(variables, start_aux):
    """
    At Most One (Sequential Counter Encoding)
    O(n) clauses, n-1 biến phụ.
    Trả về: (danh_sách_clauses, chỉ_số_biến_phụ_tiếp_theo_cho_hệ_thống)
    """
    n = len(variables)
    if n <= 1:
        return [], start_aux

    clauses = []
    s = [start_aux + i for i in range(n - 1)]
    next_start_aux = start_aux + n - 1

    clauses.append([-variables[0], s[0]])
    for i in range(1, n - 1):
        xi = variables[i]
        si = s[i]
        si_minus_1 = s[i - 1]

        clauses.append([-xi, si])
        clauses.append([-si_minus_1, si])
        clauses.append([-xi, -si_minus_1]) 

    clauses.append([-variables[n - 1], -s[n - 2]])

    return clauses, next_start_aux

if __name__ == "__main__":
    from pysat.solvers import Minisat22

    vars_list = [1, 2, 3, 4]
    
    solver = Minisat22()
    
    solver.add_clause(encode_alo(vars_list)[0])
    
    amo_clauses, next_aux = encode_amo_sequential_counter(vars_list, start_aux=5)
    for clause in amo_clauses:
        solver.add_clause(clause)
        
    print(f"Số biến phụ đã dùng: {next_aux - 5}")
    print(f"Các mệnh đề AMO tạo ra: {amo_clauses}")
    
    
    is_sat = solver.solve()
    if is_sat:
        model = solver.get_model()
        original_vars_assignment = [v for v in model if abs(v) <= 4]
        print(f"SAT! Nghiệm của biến gốc: {original_vars_assignment}")
    else:
        print("UNSAT!")