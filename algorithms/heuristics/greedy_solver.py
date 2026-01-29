from .aux_functions import (
    init_C,
    feseability,
    evaluate_quality,
    is_solution,
    totalCost,
)

def greedy(K, purchaseCost, R, A, energyCost, N, M):

  # ---------- 1) Init Candidates ----------
  C = init_C(K, R, A, N, M)

  # ---------- 2) Init solution set S ----------
  S = []                     # chosen cameras
  covered = set()            # pares (j,d) ya cubiertos - crossings j cubiertos los dias d

  
  # ---------- 3) Greedy loop ----------
  while (not is_solution(covered, N)) and C: # While is not ture

      # Evaluate q(c,S) for each c ∈ C
      best_c = evaluate_quality(C, covered, purchaseCost, energyCost)
      
      if best_c is None:
          break # No possible candidate --> stop

      
      # ---------- 4) Add best candidate to S ----------
      # Constraint 3: Activation only if installed
      # Installed cuando añadimos a la solución, y la activación ya viene implicita en patterns que tiene c
      S.append(best_c)              # update set solutions S
      covered |= best_c["covers"]   # update covered 

      
      # ---------- 5) Update C (feasibilidad) ----------
      C = feseability(C, best_c)

 
  # Uncovered --> this is only to print later in order to check what crossings were not able to be covered at days.
  all_pairs = {(j, d) for j in range(N) for d in range(7)}
  uncovered = all_pairs - covered

  # ---------- 6) Return results ----------
  # If any solution reached
  if not is_solution(covered, N):
      print("Greedy did not find a feasible solution. Crossings that still need to be covered: ", uncovered)
      return None, None, None
  
  # If solution reached
  else:
      total_cost = totalCost(S, purchaseCost, energyCost)

      print("Feasible Greedy!")
      return S, covered, total_cost 

