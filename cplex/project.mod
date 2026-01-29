// ** PLEASE ONLY CHANGE THIS FILE WHERE INDICATED **
// In particular, do not change the names of the OPL variables.

int             K = ...;
int 	  P[1..K] = ...;
int 	  R[1..K] = ...;
int 	  A[1..K] = ...;
int 	  C[1..K] = ...;

int             N = ...;
int M[1..N][1..N] = ...;

// Define here your decision variables and
// any other auxiliary OPL variables you need.
// You can run an execute block if needed.

//>>>>>>>>>>>>>>>>
// Ranges
range crossings = 1..N;   // i
range models    = 1..K;   // k
range days      = 1..7;   // d

// Decision variables
dvar boolean x_ik[crossings, models];              // x[i,k]
dvar boolean y_ikd[crossings, models, days];       // y[i,k,d]

// Objective function
dvar float+ z;

// Install cost
dexpr float installCost =
    sum(i in crossings, k in models) P[k] * x_ik[i,k];
// Energy cost
dexpr float energyCost  =
    sum(i in crossings, k in models, d in days) C[k] * y_ikd[i,k,d];
//<<<<<<<<<<<<<<<<

// You can run an execute block if needed.

execute {
  
//>>>>>>>>>>>>>>>>
  cplex.tilim = 1800;    // Time limit: 30 min
  cplex.epgap = 0.01;    // GAP tolerance: 1%
//<<<<<<<<<<<<<<<<    
}

minimize  z;// Write here the objective function.

//>>>>>>>>>>>>>>>>

//<<<<<<<<<<<<<<<<

subject to {

    // Write here the constraints.

    //>>>>>>>>>>>>>>>>
    // Constraint 1: Obj func def
    z == installCost + energyCost;
    
    // Constraint 2: At most one camera per crossing
    forall(i in crossings)
      sum(k in models) x_ik[i,k] <= 1;
      
	// Constraint 3: Coverage of every crossing j on every day d
	forall(j in crossings, d in days)
	  sum(i in crossings, k in models : M[i][j] <= R[k]) y_ikd[i,k,d] >= 1;
	  
    // Constraint 4: Activation only if installed
    forall(i in crossings, k in models, d in days)
      y_ikd[i,k,d] <= x_ik[i,k];
      
    // Constraint 5: A camera of model k cannot operate more than Ak consecutive days
	forall(i in crossings, k in models, d in days)
	  sum(h in 0..A[k]) 
	    y_ikd[i,k, 1 + ((d - 1 + h) mod 7)] 
	  <= A[k];
	  
	// Constraint 6: Minimum 2 days operation period
	forall(i in crossings, k in models, d in 2..6)
	  y_ikd[i,k,d] - y_ikd[i,k,d-1] <= y_ikd[i,k,d+1];

	// Constraint 7: Minimum 2-day operation period (first day)
	forall(i in crossings, k in models)
	  y_ikd[i,k,1] - y_ikd[i,k,7] <= y_ikd[i,k,2];
	
	// Constraint 8: Minimum 2-day operation period (last day)
	forall(i in crossings, k in models)
	  y_ikd[i,k,7] - y_ikd[i,k,6] <= y_ikd[i,k,1];
		  
    //<<<<<<<<<<<<<<<<
}

// You can run an execute block if needed.

execute {

//>>>>>>>>>>>>>>>>

//<<<<<<<<<<<<<<<<
}
