from .greedy import greedy
from .localsearch import localsearch
from .aux_functions import initCandidates, is_solution, evaluate_quality, feseability, totalCost, compute_covered
import random


def RCL(Candidates, covered, P, E, qmax, qmin, alpha):
    # Init empty list
    rcl = [] 

    for c in Candidates:
        # Gain: how much can I cover?
        c_covered = c["covers"] - covered
        gain = len(c_covered)

        # Cost: how much do I cost?
        purchaseCost  = P[c["k"]]
        operatingCost = E[c["k"]] * sum(c["pattern"])
        cost = purchaseCost + operatingCost

        q = gain/cost # Quality
        threshold = qmax-alpha*(qmax-qmin) # q(c)≥ qmax-α(qmax-qmin)

        if q >= threshold:
            # RCLmax← {c∊C | q(c)≥ qmax-α(qmax-qmin)}
            rcl.append(c)

    return rcl


def doConstructionPhase(K, P, R, A, E, N, M, alpha):
    # ---------- Init as greedy ----------
    C = initCandidates(K, R, A, N, M)
    S = []                  
    covered = set()         

    
    # ---------- Greedy loop ----------
    while (not is_solution(covered, N)) and C: # While is not ture

        # Evaluate q(c,S) for each c ∈ C
        best_c, qmax, _, qmin = evaluate_quality(C, covered, P, E)
        
        if best_c is None:
            break # No possible candidate --> stop
        
        # Create Restricted Candidate List (RLC) and add them to the partial solution S
        rcl = RCL(C, covered, P, E, qmax, qmin, alpha)
        
        if not rcl and best_c is not None:
            rcl.append(best_c)
        elif not rcl:
            break  # If no candidate stop

        random_c = random.choice(rcl)
        S.append(random_c)            
        covered |= random_c["covers"]  

        # Update C (feasibilidad)
        C = feseability(C, random_c)

    
    # Uncovered --> this is only to print later in order to check what crossings were not able to be covered at days d
    all_pairs = {(j, d) for j in range(N) for d in range(7)}
    uncovered = all_pairs - covered


    # If any solution reached
    if not is_solution(covered, N):
        # print("GRASP constructive did not find a feasible solution. Crossings that still need to be covered: ", uncovered)
        return None, None, None
    
    # If solution reached
    else:
        total_cost = totalCost(S, P, E)
        # print("Feasible Greedy!")
        return S, covered, total_cost 
    


def grasp(K, P, R, A, E, N, M, ls, policy, maxIt, alpha):
    
    # Init param
    Sbest = None
    best_covers = None
    best_cost = float("inf")

    for i in range(maxIt):
        # Construction phase above (slightly diffrent from greedy)
        S, covers, cost = doConstructionPhase(K, P, R, A, E, N, M, alpha)
        
        # If no feasible solution in this iteration, try next one
        if S is None:
            continue

        if ls:
            S, covers, cost = localsearch(K, P, R, A, E, N, M, policy, S)
        
        # Save the best solution
        if cost < best_cost:
            Sbest = S
            best_cost = cost
            best_covers = covers 
    
    if Sbest is None:
        print("GRASP could not find any feasible solution :(")
        return None, None, None
    else:
        return Sbest, best_covers, best_cost
