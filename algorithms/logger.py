
import re
from pathlib import Path


# ESTE ARCHIVO SOLO ES PARA LEER/PRINTEAR/ESCRIBIR LA INFORMACIÓN    
from pathlib import Path

def read_config(path):
    params = {}
    path = Path(path)

    with path.open("r") as f:
        for line in f:
            # quitar comentarios
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            if "=" not in line:
                continue

            name, value = line.split("=", 1)
            name = name.strip()
            value = value.strip().rstrip(";").strip()

            # detectar tipo
            # strings entre comillas
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            # booleanos
            elif value.lower() in ("true", "false"):
                value = value.lower() == "true"
            else:
                # int o float si se puede
                try:
                    if "." in value:
                        value = float(value)
                    else:
                        value = int(value)
                except ValueError:
                    
                    pass

            params[name] = value

    return params


from pathlib import Path

def write_solution(solution_path, S, covered, cost, time, i, alpha):
    """
    Escribe una solución en formato (estilo OPL):
       x = [...];
       y = [...];
       total_cost = ...;
    """
    solution_path = Path(solution_path)

    # Crear carpeta si no existe
    solution_path.parent.mkdir(parents=True, exist_ok=True)

    with solution_path.open("w") as f:
        if S is None:
            f.write("# No feasible solution found\n")
            return

        # Write

        for c in S:
            f.write(f"Crossing {c['i']} , with camera model {c['k']},\noperates days: {c['pattern']},\ncovers (j, d): {c['covers']}\n\n")


        if alpha != -1:
            f.write(f"Alpha = {alpha};\n")
            f.write(f"Iterations = {i};\n")   


        # Coste total
        f.write(f"Total cost = {cost};\n")
        f.write(f"Execution time = {time};\n")


# READ FILE
def _parse_scalar(name: str, text: str) -> int:
    """Busca:  name = 123;"""
    m = re.search(rf"\b{name}\s*=\s*([-+]?\d+)\s*;", text)
    if not m:
        raise ValueError(f"Scalar '{name}' not found in .dat file")
    return int(m.group(1))


def _parse_vector(name: str, text: str):
    """Busca: name = [ 1 2 3 ];  y devuelve [1,2,3]."""
    m = re.search(
        rf"\b{name}\s*=\s*\[\s*([-\d\s\.]+?)\s*\];",
        text,
        flags=re.DOTALL,
    )
    if not m:
        raise ValueError(f"Vector '{name}' not found in .dat file")

    raw = m.group(1)
    tokens = raw.replace("\n", " ").split()
    vals = [float(t) if "." in t else int(t) for t in tokens]
    return vals


def _parse_matrix(name: str, text: str):
    """Busca:
        name = [
          [ 0 1 2 ]
          [ 3 4 5 ]
        ];
       y devuelve [[0,1,2],[3,4,5]]
    """
    m = re.search(
        rf"\b{name}\s*=\s*\[\s*(.*?)\s*\];",
        text,
        flags=re.DOTALL,
    )
    if not m:
        raise ValueError(f"Matrix '{name}' not found in .dat file")

    body = m.group(1)
    rows_raw = re.findall(r"\[\s*([-\d\s\.]+?)\s*\]", body)
    if not rows_raw:
        raise ValueError(f"No rows found for matrix '{name}'")

    matrix = []
    for row in rows_raw:
        tokens = row.replace("\n", " ").split()
        vals = [float(t) if "." in t else int(t) for t in tokens]
        matrix.append(vals)
    return matrix


def read_instance(path: str):
    """
    Lee un archivo .dat estilo OPL y devuelve:
    K, P, R, A, C, N, M

    Donde:
      - K, N son enteros
      - P, R, A, C son tuplas de enteros
      - M es una tupla de tuplas (matriz NxN)
    """
    with open(path, "r") as f:
        text = f.read()

    K = _parse_scalar("K", text)
    N = _parse_scalar("N", text)
    P = _parse_vector("P", text)
    R = _parse_vector("R", text)
    A = _parse_vector("A", text)
    C = _parse_vector("C", text)
    M = _parse_matrix("M", text)

    P = tuple(P)
    R = tuple(R)
    A = tuple(A)
    C = tuple(C)
    M = tuple(tuple(row) for row in M)

    return K, P, R, A, C, N, M

# PRINT FUNCTIONS
def print_covered_matrix(covered, N):
    print("=== Coverd matrix (j × d) ===")
    for j in range(N):
        fila = [1 if (j,d) in covered else 0 for d in range(7)]
        print(f"Crossing {j}: {fila}")
    print()


def print_solution(S):
    print("=== Installed Cameras (S) ===")
    for idx, c in enumerate(S):
        i = c["i"]
        k = c["k"]
        pattern = c["pattern"]
        covers = c["covers"]
        print(f"Camera {idx+1}: crossing {i}, model {k}, operational days {pattern}. \nCovers the crossings (j,d) {covers}\n")
    print()
