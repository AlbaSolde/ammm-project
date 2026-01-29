from itertools import product
# ============================== INIT CANDIDATES =====================================
def initCandidates(K, R, A, N, M):

    C = []

    # Get all the combinations about the days per week the camera k can operate
    # Where A_k == maximum consecutive days, and minimum = 2
    patterns = [generate_patterns(A_k) for A_k in A] # Here we cover Constraints 4,5,6,7 (from the report)

    for i in range(N):              # crossing
        for k in range(K):          # modelo
            for p in patterns[k]:   # pattern of days
                covers = set()
                # For each j that has to be covered
                for j in range(N):
                    # Check if the distnace is lower/equal than the range of the camera model
                    if M[i][j] <= R[k]:
                        # We look for what days the camera is ON
                        for d in range(7):
                            if p[d] == 1:
                                # If the camera k at crossing i can cover crossing j at day d, then we have a candidate
                                covers.add((j, d))

                # Constraint 2: Coverage of every crossing on every day by at least one operating camera
                if covers:
                    # We add as candidate as: at crossing i, camera k, during schedule p, can cover "covers"
                    C.append({"i": i, "k": k, "pattern": p, "covers": covers})
    return C


# ============================== GENERADOR DE Y =====================================
def generate_patterns(A_k):

    valid = []

    for bits in product([0, 1], repeat=7):  # For all the combination of 7 bits
        pattern = list(bits)

        # Find consecutive days and put them in blocks
        blocks = []
        current = 0
        for d in range(7):
            if pattern[d] == 1:
                # Counter of consecutive days
                current += 1
            else:
                # Once we have a 0, we add the counter to the block list
                if current > 0:
                    blocks.append(current)
                    current = 0
        # For he last case of conescutive days
        if current > 0:
            blocks.append(current)

        # If we did not add any block we skip and try new pattern
        if not blocks:
            continue

        # Constraint 6/7: Cyclic Week --> check Monday and Sunday in case its consecutive
        if pattern[0] == 1 and pattern[-1] == 1 and len(blocks) >= 2: # We need a minimum of two blocks in order to fusion
            blocks[0] += blocks[-1]   # Add consecutive days
            blocks.pop()              # remove last block (the one that includes Sunday) since we added it to the first one


        # Constraint 5: Minimum 2-day operation period:
        if any(b < 2 for b in blocks):
            continue

        # Constraint 4: A camera of model k cannot operate more than Ak consecutive days:
        if any(b > A_k for b in blocks):
            continue

        # If the pattern is valid we added it to the valid list
        valid.append(pattern)

    return valid



# ============================== EVALUATE (+ SELECTION) FUNCTION =====================================
def evaluate_quality(Candidates, covered, P, E):
    best_c = None
    best_q = -1.0

    worst_c = None
    worst_q = float("inf") # Not sure if this is a good init value

    for c in Candidates:
        # c: How many crossings (j,d) can I cover (from the left crossings)?
        new_covered = c["covers"] - covered # covers I can minus the ones that are already covered

        gain = len(new_covered)
        if gain == 0:
            continue

        # Cost of this new candidate: purchase + energy * operational days
        purchaseCost  = P[c["k"]]
        operatingCost = E[c["k"]] * sum(c["pattern"])
        cost = purchaseCost + operatingCost

        q = gain / cost   # quality: we measure the quality of the candidate by dividing its gain by its total cost

        if q > best_q:
            # We select the best candidate c --> the one with better quality q
            best_q = q
            best_c = c
        if q < worst_q: # This is used for GRASP
            worst_q = q
            worst_c = c

    return best_c, best_q, worst_c, worst_q



# ============================== IS SOLUTION FUNCTION =====================================
def is_solution(covered, N):
    # Check if per each crossing (j) is covered each day d
    for j in range(N):
      for d in range(7):
          if (j, d) not in covered: # If there is a combination missing, then we have not find any solution yet
              return False
    return True



# ============================== FESEABILITY/UPDATE_CANDIDATE FUNCTION =====================================
def feseability(C, best_c):
  # Constraint 1: At least one camera per crossing
  i_taken = best_c["i"]
  new_C = []
  for c in C:
      if c is best_c:
          # Discard since it is already in the solution set S
          continue
      if c["i"] == i_taken:
          # Since we have installed a camera at crossing i (and following Constraint 1),
          # we have to discard the rest of camera that can be placed at i
          continue
      new_C.append(c)
  return new_C


# ========== TOTAL COST ===========
def totalCost(S, P, E):
    total_cost = 0.0
    for c in S:
        purchaseCost = P[c["k"]]
        operatingCost = E[c["k"]] * sum(c["pattern"])
        total_cost += purchaseCost + operatingCost
    return total_cost

# ============================ AUX FUNCTIONS FOR LOCAL SEARCH ============================================
def compute_covered(S):
    covered = set()
    for c in S:
        covered |= c["covers"]
    return covered

# Compare cameras: We do not want to add the same camera that is already in S
def is_same_camera(c1, c2):
    return (
        c1["i"] == c2["i"] and
        c1["k"] == c2["k"] and
        c1["pattern"] == c2["pattern"]
    )

# Funtion to know check if adding c_in and remove c_out respects the first Constraint
# Constraint 1: At most 1 camera per crossing
def valid_crossing_constraint(S_without, c_in):
    used_crossings = {c["i"] for c in S_without}
    return c_in["i"] not in used_crossings




