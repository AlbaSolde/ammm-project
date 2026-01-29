# AMMM_MIRI-Project

This project aims to use ILP, Greedy and GRASP algorithms in order to solve instances of the linear system described in `project.pdf`.

Each method will then be compared on accuracy and execution time to identify the best one.

## Collaborators

Alba Soldevilla González, Thomas Aubertier

## Project Structure

```
.
├── InstanceGenerator/
│   ├── config.dat
│   └── instanceGenerator.py
│
├── algorithms/
│   ├── heuristics/
│   │   ├── aux_functions.py
│   │   ├── grasp.py
│   │   ├── greedy.py
│   │   ├── greedy_solver.py
│   │   └── localsearch.py
│   ├── instances/
│   │   ├── ...
│   ├── solutions/
│   │   ├── ...
│   ├── Main.py
│   ├── config.dat
│   ├── logger.py
│
├── cplex/
│   ├── project.mod
│   ├── test.dat
│   └── README
│
├── README.md
│
└── project.pdf
```


## 1. Instance Generation

The folder `InstanceGenerator` contains the tools used to generate synthetic input instances.

### Configuration

The file `InstanceGenerator/config.dat` defines the characteristics and size of the generated instances (e.g., number of crossings, number of camera models, parameter ranges, etc.).

All generated `.dat` files are stored by default in:

    algorithms/instances/

This path can be changed inside the instance generator script or its configuration file.

### Running the instance generator

    python InstanceGenerator/instanceGenerator.py

(or `python3`)

## 2. Algorithms

All heuristic methods are implemented in:

    algorithms/heuristics/

The available algorithms are:

- **Greedy constructive heuristic**
- **Local Search**
- **GRASP**

Input instances are read from:

    algorithms/instances/

Solutions are written to:

    algorithms/solutions/

These folders can be customised through the main configuration file.

## 3. Solver Configuration

The file `algorithms/config.dat` contains all settings required to run the solver, including:

- selection of the algorithm (Greedy, Local Search, GRASP)
- input and output file names and paths
- Local Search policy (First Improvement or Best Improvement)
- GRASP parameters (alpha, maximum iterations)
- paths for instances and solutions

### Running the solver

    python algorithms/Main.py

(or `python3`)

The solver automatically loads all parameters from `algorithms/config.dat`.

## 4. ILP Model (CPLEX)

The folder `cplex/` contains the exact ILP formulation of the problem:

- `project.mod`  → ILP model
- `test.dat`     → example instance

Note : It does not contains the CPLEX project. It must be created separately.
