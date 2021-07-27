from pl import PL
from auxiliar import Auxiliar

def read_input():
    """
    Read input and return as list of intergers
    """
    standart_input = input()
    raw_input = standart_input.split(' ')
    int_input = [int(i) for i in raw_input]
    return int_input



# Read input
n, m = read_input()
c_vector = read_input()
A_matrix = []
b_vector = []
for i in range(int(n)):
    line_read = read_input()
    b_element = line_read.pop()
    A_matrix.append(line_read)
    b_vector.append(b_element)

# Transforma em FPI (consequentemente em forma canonica)
# e depois constroi o tableau
pl = PL(A_matrix, b_vector, c_vector, n, m)
pl.build_tableau()
print("ORIGINAL")
pl.print_matrix()
print()

# Verifica necessidade de PL auxiliar:
if not all(b_value >= 0 for b_value in b_vector):
    # Constroi auxiliar
    pl_FPI = pl.get_FPI()
    aux = Auxiliar(pl_FPI['A_matrix'], pl_FPI['b_vector'], pl_FPI['c_vector'], n)
    aux_result = aux.execute(print_flag=True)
    # Verifica termino por inviabilidade
    if aux_result == "inviavel":
        return 0
    # Transfere auxiliar para a original
    pl.transfer_A_matrix(aux.get_aux_tableau())

"""
# Soluciona PL original
pivot_not_finished = True
cnt = 1
while pivot_not_finished:
    print("PIVOT-",cnt," -------------------------------------")
    pivot_not_finished = pl.pivot(print_flag=True)
    print()
    print("Result:", cnt)
    pl.print_matrix()
    print()
    print()
    cnt+=1
pl.get_response()
"""
