def read_input():
    """
    Read input and return as list of intergers
    """
    standart_input = input()
    raw_input = standart_input.split(' ')
    int_input = [int(i) for i in raw_input]
    return int_input


class PL():
    def __init__(self, A_matrix, b_vector, c_vector, num_rows, num_original_variables):
        for i in range(num_rows):
            c_vector.append(0)
            for j in range(num_rows):
                if i == j:
                    A_matrix[i].append(1)
                else:
                    A_matrix[i].append(0)
        self.A_matrix = A_matrix
        self.b_vector = b_vector
        self.c_vector = c_vector

    def build_tableau(self):
        # Multiplica o c por menos 1
        self.c_vector = [i*-1 for i in self.c_vector]
        # Adiciona o valor ótimo no b
        self.b_vector.insert(0, 0)

    def pivot(self):
        pivot_line, pivot_column = self.select_pivot()

        if (pivot_line, pivot_column) == (False, False):
            return True

        pivot = self.A_matrix[pivot_line][pivot_column]

        # Regularizar linha do pivot
        if pivot != 1:
            self.A_matrix[pivot_line] = [i*(1/pivot) for i in self.A_matrix[pivot_line]]
            self.b_vector[pivot_line+1] = self.b_vector[pivot_line+1]*(1/pivot)
            pivot = self.A_matrix[pivot_line][pivot_column]

        num_lines = len(self.A_matrix) + 1

        # Regularizando vetor de custo (primeira linha do Tableau)
        value_reference = self.c_vector[pivot_column]
        if value_reference != 0:
            new_c = []
            for i in range(len(self.A_matrix[0])):
                new_c.append(self.c_vector[i] - (value_reference*self.A_matrix[pivot_line][i]))
            self.c_vector = new_c
            # Faz a conta também para o valor objetivo, pois está na primeira linha do tableau
            self.b_vector[0] = self.b_vector[0] - (value_reference*self.b_vector[pivot_line + 1])

        # Regularizando as outras linhas
        for this_line in range(len(self.A_matrix)):
            if this_line != pivot_line:
                value_reference = self.A_matrix[this_line][pivot_column]
                if value_reference != 0:
                    new_line = []
                    for i in range(len(self.A_matrix[0])):
                        new_line.append(self.A_matrix[this_line][i] - (value_reference*self.A_matrix[pivot_line][i]))
                    self.A_matrix[this_line] = new_line
                    # Faz a conta também para o valor objetivo, pois está na primeira linha do tableau
                    self.b_vector[this_line+1] = self.b_vector[this_line+1] - (value_reference*self.b_vector[pivot_line + 1])

        return False


    def select_pivot(self):
        """
        Finds the line and the column
        of the pivot element
        """
        # Selecionando um valor negativo em C
        pivot_column = -1
        for i,value in enumerate(self.c_vector):
            if value < 0:
                pivot_column = i
                break

        # Verificação de parada
        if pivot_column == -1:
            return (False, False)

        # Calculando os limites
        possible_pivots = []
        lines = len(self.A_matrix)
        for i in range(lines):
            numerator = self.b_vector[i+1] # +1 por conta do valor objetivo
            denominator = self.A_matrix[i][pivot_column]
            if numerator == 0 or denominator == 0:
                continue
            possible_pivots.append((i,(numerator/denominator)))
        # Verifica se não há possíveis pivots
        if len(possible_pivots) == 0:
            return (False, False)
        # Pegando o maior valor que o x selecionado pode tomar:
        # Ordena as tuplas e pega o index na primeira tupla
        possible_pivots.sort(key=lambda tup: tup[0])
        pivot_line = possible_pivots[0][0]
        return (pivot_line, pivot_column)


    def print_matrix(self):
        for i in self.c_vector:
            space = self.get_space(i)
            print("_"*space, i , end =" ")
        space = self.get_space(self.b_vector[0])
        print("|", "_"*space, self.b_vector[0])
        for i,line in enumerate(self.A_matrix):
            for value in line:
                space = self.get_space(value)
                print(" "*space, value, end =" ")
            space = self.get_space(self.b_vector[i+1])
            print("|", " "*space, self.b_vector[i+1])

    def get_space(self, i):
            if i > 9:
                space = 2
            elif i >= 0:
                space = 3
            elif i < -9:
                space = 1
            elif i < 0:
                space = 2
            return space




n, m = read_input()
c_vector = read_input()
A_matrix = []
b_vector = []
for i in range(int(n)):
    line_read = read_input()
    b_element = line_read.pop()
    A_matrix.append(line_read)
    b_vector.append(b_element)

pl = PL(A_matrix, b_vector, c_vector, n, m)
pl.build_tableau()
pl.print_matrix()
print()
print()
pl.pivot()
pl.print_matrix()
