from pysat.solvers import Minisat22

def solve_cnf():
    solver = Minisat22()
    
    solver.add_clause([1, 2])
    solver.add_clause([-1, 2])
    solver.add_clause([-2, 3])
    
    is_sat = solver.solve()
    
    if is_sat:
        print("SAT")
        print(solver.get_model())
    else:
        print("UNSAT")

if __name__ == "__main__":
    solve_cnf()