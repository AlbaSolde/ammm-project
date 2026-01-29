import os
import random
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

input_file_default = os.path.join(BASE_DIR, "config.dat")
output_file_default = os.path.join(BASE_DIR, "..", "algorithms", "instances", "test.dat") # Output file path


# Variables
var_names = ["K", "P", "R", "A", "C", "N", "M"]
var_types = ["int", "vec", "vec", "vec", "vec", "int", "mat"]


def read_data(file_name):
    res = []
    with open(file_name, 'r') as file:
        lines = [line.rstrip() for line in file]

        for line in lines:
            spl = line.split('=')
            if len(spl) != 0:
                try:
                    value = int(spl[1].replace(' ','').replace(';',''))
                    res.append(value)
                except:
                    pass
    return res

def gen_data(var_data):
    K, N, MinPrice, MaxPrice, MinCost, MaxCost, MinAutonomy, MaxAutonomy, MinRangeCam, MaxRangeCam, MinRangeCross, MaxRangeCross = var_data
    P = gen_vector(K, MinPrice, MaxPrice, is_int=True)     # precios int
    R = gen_vector(K, MinRangeCam, MaxRangeCam, is_int=True)
    A = gen_vector(K, MinAutonomy, MaxAutonomy, is_int=True)
    C = gen_vector(K, MinCost, MaxCost, is_int=True)       # costes int
    M = gen_matrix(N, MinRangeCross, MaxRangeCross, is_int=True)

    # Orden final: K, P, R, A, C, N, M
    var_values = [K, P, R, A, C, N, M]
    return var_values


def gen_value(min, max):
    return min + random.random()*(max - min)

def gen_vector(n, min, max, is_int=False):
    vect = [0 for i in range(n)]
    rr = max - min
    for i in range(n):
        if is_int:
            vect[i] = random.randint(min, max)
        else:
            vect[i] = round(min + random.random()*rr,2)

    return vect

def gen_matrix(n, min, max, is_int=False):
    matrix = [[0 for i in range(n)] for j in range(n)]
    rr = max - min
    for r in range(n):
        matrix[r][r] = 0
        for c in range(r):
            if is_int:
                matrix[r][c] = random.randint(min, max)
            else:
                matrix[r][c] = round(min + random.random()*rr,2)
            matrix[c][r] = matrix[r][c]
                
    return matrix
            
def write_data(file_name, var_values):
    with open(file_name, 'w') as file:
        for i,v in enumerate(var_names):
            if var_types[i] == "int":
                file.write(v+" = "+str(var_values[i])+";\n")
            elif var_types[i] == "vec":
                file.write(v+" = [")
                for e in var_values[i]:
                    file.write(" "+str(e))
                file.write(" ];\n")
            elif var_types[i] == "mat":
                file.write(v+" = [\n")
                for r in var_values[i]:
                    file.write("[")
                    for e in r:
                        file.write(" "+str(e))
                    file.write(" ]\n")
                file.write(" ];\n")
            file.write("\n")
                
                           
def main():

    if len(sys.argv) >= 2:
        input_file = sys.argv[1]
    else:
        input_file = input_file_default

    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        output_file = output_file_default

    print("\33[0;93m" + f"Generating instance from [{input_file}] :")

    inp = read_data(input_file)
    print("Parsed values from config:", inp, "len =", len(inp)) 

    if len(inp) != 12:
        raise ValueError(f"Config file {input_file} should contain 12 integer values, found {len(inp)}")

    var_values = gen_data(inp)
    write_data(output_file, var_values)

    print("\33[1;32m" + f"Instance successfully saved in [{output_file}] !\33[0m")


if __name__ == "__main__":

    main()
