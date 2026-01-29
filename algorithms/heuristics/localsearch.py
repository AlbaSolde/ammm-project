from .aux_functions import initCandidates, is_solution, totalCost, compute_covered, is_same_camera, valid_crossing_constraint

# ================================== LOCAL SEARCH ===========================================================
def localsearch(K, P, R, A, E, N, M, policy, S):
    """
    policy == 0 --> First Improvement
    policy == 1 --> Best Improvement
    """
    if S is None:
        # Greedy did not find any solution
        return None, None, None

    # All possible candidates
    C_all = initCandidates(K, R, A, N, M)

    # Apply fi when policy == 0, bi otherwise
    fi = (policy == 0)
    bi = (policy == 1)

    improved = True
    while improved:
        improved = False
        current_cost = totalCost(S, P, E)

        # Init for Best Improvement
        best_delta = 0.0    # delata only will be meaningful if it is greater than zero
        best_move = None  # to save best choice of movement over the candidates that can be removed and added (c_out, c_in) 

        # Go over each s (i,k)
        for c_out, _ in enumerate(S):
            # Remove camera
            S_without = S[:c_out] + S[c_out+1:]

            # For all possible candidates
            for c_in in C_all:
                # If c_in is equal to c, we can SKIP since it is the camera that we removed
                if any(is_same_camera(c_in, s) for s in S):
                    continue

                # Check constraint so we can now if the new possible s respects it, if not, SKIP
                if not valid_crossing_constraint(S_without, c_in):
                    continue

                # New S (Neighbour solution)
                S_neigh = S_without + [c_in]

                # lets see if we cover all the crossings during all the days of the week
                covered_neigh = compute_covered(S_neigh)

                # Is it a solution? If not, SKIP
                if not is_solution(covered_neigh, N):
                    continue

                # Compute cost
                new_cost = totalCost(S_neigh, P, E)
                delta = current_cost - new_cost  # there is an improvement if delta > 0

                # Not improving, SKIP 
                if delta <= 0:
                    continue

                # ---- FIRST IMPROVEMENT ----
                if fi:
                    S = S_neigh
                    improved = True
                    break  # leave inner for (we do not care about the rest of candidates)
                
                # ---- BEST IMPROVEMENT ----
                else:  # bi 
                    if delta > best_delta: # we just check over all possible candidates that have feasible solutions and see if its cost is better than the current one
                        best_delta = delta
                        best_move = (c_out, c_in)

            if fi and improved:
                break # We neither care about the other possible S by removing another c_out

        # If we are in BestImprovement we apply the best move (if exists)
        if bi and best_move is not None:
            c_out, c_in = best_move
            S = S[:c_out] + S[c_out+1:] + [c_in] # From S remove c_out and add c_in
            improved = True

    # Once there is nothing else to be improved --> leave while
    final_covered = compute_covered(S)
    final_cost = totalCost(S, P, E)

    return S, final_covered, final_cost
