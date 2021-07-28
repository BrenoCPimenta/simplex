from pl import PL
from auxiliar import Auxiliar


def read_input():
    """
    Read input and return as list of float
    """
    standart_input = input()
    raw_input = standart_input.split()
    int_input = [float(i) for i in raw_input]
    return int_input


def run():
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
    pl = PL(A_matrix, b_vector, c_vector, int(n), int(m))
    pl.build_tableau()

    # Verifica necessidade de PL auxiliar:
    if not all(b_value >= 0 for b_value in b_vector):
        # Constroi auxiliar
        pl_FPI = pl.get_FPI()
        aux = Auxiliar(pl_FPI['A_matrix'], pl_FPI['b_vector'], pl_FPI['c_vector'], int(n), int(m))
        aux_result = aux.execute()
        # Verifica termino por inviabilidade
        if aux_result == "inviavel":
            return 0
        # Transfere auxiliar para a original
        pl.transfer_A_matrix(aux.get_aux_tableau())

    # Soluciona PL original
    pivot_not_finished = True
    while pivot_not_finished:
        pivot_not_finished, ilimitada = pl.pivot()
        if ilimitada:
            print("ilimitada")
            base_positions = pl.get_response()
            pl.get_unlimited(base_positions)
            return 0
    print("otima")
    pl.get_objective_value()
    pl.get_response()
    pl.get_optimal_cert()
    return 0


if __name__ == "__main__":
    run()
