# Main.py
from pathlib import Path
import time

from logger import (
    read_instance,
    print_solution,
    print_covered_matrix,
    read_config, 
    write_solution,    
)

from heuristics.greedy import greedy
from heuristics.localsearch import localsearch
from heuristics.grasp import grasp


# ------------------- CONFIG -------------------
BASE_DIR = Path(__file__).resolve().parent

# Read from config.dat
config = read_config(BASE_DIR / "config.dat")

# PARAMETERS FROM CONFIG.DAT
instance_path   = BASE_DIR / config["instancePath"]
solver          = config.get("solver", "Greedy")
solution_file   = BASE_DIR / config.get("solutionFile", "solutions/solution.sol")
localSearch     = config.get("localSearch", False)
ls_policy       = config.get("policy", "FirstImprovement")
alpha           = config.get("alpha", 0.1) # Default alpha? 0.1?
max_exec_time   = config.get("maxExecTime", 60) # Not sure how to stop when timeout
maxIt  			= config.get("maxIt", 50) # For GRASP


# ------------------- READ DATA -------------------
K, P, R, A, C, N, M = read_instance(instance_path)


# ------------------- SOLVERS EXECUTION -------------------
# ------------------- GREEDY -------------------
if solver == "Greedy" and not localSearch:

    start = time.perf_counter()      # START TIME
    S, covers, cost = greedy(K, P, R, A, C, N, M)
    end = time.perf_counter()        # END TIME

    # Execution time
    exec_time = end - start
    exec_time = exec_time * 1000 # ms
    
    # save solution (even if it is not feasible)
    i = -1 
    alpha = -1 # We are not using iterations for this solver
    write_solution(solution_file, S, covers, cost, exec_time, i, alpha)

    if S is not None:
        print_solution(S)
        # print_covered_matrix(covers, N) # If is feasible this always print the same since eveything is covered, so it is not necessary
        print(f"=== Total cost: === \n{cost}") 
    else:
        print("Not feasible solution was faund for this data")

    print(f"\n=== Execution time:=== \n{exec_time:.6f} ms\n")

# ------------------- GREEDY + LOCAL SEARCH -------------------
elif solver == "Greedy" and localSearch:
    # Selecting policy for local search
    if ls_policy == "FirstImprovement": policy = 0
    elif ls_policy == "BestImprovement": policy = 1
    else: 
        policy = 0
        print("\nError geting the policy, FirstImprovement is going to execute as the default one")
    
    start = time.perf_counter()      # START TIME
    S, _, _ = greedy(K, P, R, A, C, N, M)
    S, covers, cost = localsearch(K, P, R, A, C, N, M, policy, S)
    end = time.perf_counter()        # END TIME

    # Execution time
    exec_time = end - start
    exec_time = exec_time * 1000 # ms

    # save solution (even if it is not feasible)
    i = -1 # We are not using iterations for this solver
    alpha = -1
    write_solution(solution_file, S, covers, cost, exec_time, i, alpha)

    if S is not None:
        print_solution(S)
        # print_covered_matrix(covers, N) # If is feasible this always print the same since eveything is covered, so it is not necessary
        print(f"=== Total cost: === \n{cost}") 
    else:
        print("Not feasible solution was faund for this data")

    print(f"\n=== Execution time:=== \n{exec_time:.6f} ms\n")

# ------------------- GRASP -------------------
elif solver == "GRASP":
    # Selecting policy for local search
    if ls_policy == "FirstImprovement": policy = 0
    elif ls_policy == "BestImprovement": policy = 1
    else: 
        policy = 0
        print("\nError geting the policy, FirstImprovement is going to execute as the default one")

    start = time.perf_counter()      # START TIME
    S, covers, cost = grasp(K, P, R, A, C, N, M, policy, maxIt, alpha) 
    end = time.perf_counter()        # END TIME

    # Execution time
    exec_time = end - start
    exec_time = exec_time * 1000 # ms

    # save solution (even if it is not feasible)
    write_solution(solution_file, S, covers, cost, exec_time, maxIt, alpha)
    
    if S is not None:
        print_solution(S)
        # print_covered_matrix(covers, N) # If is feasible this always print the same since eveything is covered, so it is not necessary
        print(f"=== Total cost: === \n{cost}") 
    else:
        print("Not feasible solution was faund for this data")

    print(f"\n=== Execution time: === \n{exec_time:.6f} ms")
    print(f"\n=== Nº iterations: === \n{maxIt}\n")

else:
    print("The selected solver is not implemented yet :( \nTry another configuration please")
