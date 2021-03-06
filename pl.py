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
        self.num_original_variables = num_original_variables
        self.num_rows = num_rows

    def build_tableau(self):
        """
        Standardize matrix and vector
        values ​​to match the tableau
        """
        # Multiplica o c por menos 1
        self.c_vector = [i*-1 for i in self.c_vector]
        # Adiciona o valor ótimo no b
        self.b_vector.insert(0, 0)

    def pivot(self, print_flag=False):
        """
        Pivot the tableau and verify for
        unlimited possibility
        """
        keep_pivot, pivot_line, pivot_column, ilimitada = self.select_pivot()

        if not keep_pivot:
            if ilimitada:
                return(True, True)
            else:
                return (False, False)

        pivot = self.A_matrix[pivot_line][pivot_column]

        # Regularizar linha do pivot
        if pivot != 1:
            self.A_matrix[pivot_line] = [i*(1/pivot) for i in self.A_matrix[pivot_line]]
            self.b_vector[pivot_line+1] = self.b_vector[pivot_line+1]*(1/pivot)
            pivot = self.A_matrix[pivot_line][pivot_column]

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

        return (True, False)

    def select_pivot(self, print_flag=False):
        """
        Finds the line and the column
        of the pivot element
        """
        # Selecionando um valor negativo em C
        pivot_column = -1
        for i, value in enumerate(self.c_vector):
            if value < 0:
                pivot_column = i
                break

        # Verificação de parada
        if pivot_column == -1:
            return (False, 0, 0, False)

        if print_flag:
            print("Column to pivot: ", pivot_column)
            print("Value in C: ", self.c_vector[pivot_column])
            print("Possible pivots:")

        # Calculando os limites
        possible_pivots = []
        unlimited_cnt = 0
        lines = len(self.A_matrix)
        for i in range(lines):
            numerator = self.b_vector[i+1] # +1 por conta do valor objetivo
            denominator = self.A_matrix[i][pivot_column]

            if denominator <= 0:
                unlimited_cnt += 1

            if numerator == 0 or denominator == 0:
                continue

            limit = numerator/denominator
            if limit > 0:
                if print_flag:
                    print("    ", numerator, "/", denominator, "=",limit)
                possible_pivots.append((i,limit))
        # Verifica se é limitada
        if unlimited_cnt == len(self.A_matrix):
            return (False, 0, 0, True)
        # Pegando o maior valor que o x selecionado pode tomar:
        # Ordena as tuplas e pega o index na primeira tupla
        possible_pivots.sort(key=lambda tup: tup[1])
        pivot_line = possible_pivots[0][0]
        if print_flag:
            print("Chosen pivot: ", possible_pivots[0][1])
        return (True, pivot_line, pivot_column, False)


    def print_matrix(self):
        """
        Print tableau
        """
        for i in self.c_vector:
            space = self.get_space(i)
            print("_"*space, round(i,1) , end =" ")
        space = self.get_space(self.b_vector[0])
        print("|", "_"*space, round(self.b_vector[0],1))
        for i,line in enumerate(self.A_matrix):
            for value in line:
                space = self.get_space(value)
                print(" "*space, round(value,1), end =" ")
            space = self.get_space(self.b_vector[i+1])
            print("|", " "*space, round(self.b_vector[i+1], 1))

    def get_space(self, i):
        """
        Get number of spaces
        for pretty print tableau
        """
        if i > 9:
            space = 2
        elif i >= 0:
            space = 3
        elif i < -9:
            space = 1
        elif i < 0:
            space = 2
        return space

    def get_objective_value(self):
        """
        returns objective value
        """
        print(round(self.b_vector[0], 7)) # Valor objetivo

    def get_response(self):
        """
        Find the bases and print them
        and return their positions so
        that can be used to unlimited cert.
        """
        base_columns = []
        base_rows = []
        line_num = len(self.A_matrix)
        for i in range(self.num_original_variables):
            xi_value = 0
            # Verifica coluna
            num_zero = 0
            num_one = 0
            one_position = 0
            for j in range(line_num):
                value = self.A_matrix[j][i]
                if value == 0:
                    num_zero += 1
                elif value == 1:
                    num_one += 1
                    one_position = j
            if num_one == 1 and num_zero == (line_num-1):
                xi_value = self.b_vector[one_position+1]
                base_columns.append(i)
                base_rows.append(one_position)
            print(round(xi_value, 7), end=" ")
        print()
        return (base_columns, base_rows)

    def get_optimal_cert(self):
        """
        Print optimality certificate
        """
        for value in self.c_vector[self.num_original_variables :]:
            print(round(value, 7), end=" ")

    def get_FPI(self):
        """
        Returns tableau separated
        by specific parts
        """
        return {
            'A_matrix': self.A_matrix,
            'b_vector': self.b_vector,
            'c_vector': self.c_vector
        }

    def transfer_A_matrix(self, aux_tableau):
        """
        Uses pivoted lines from the aux PL
        """
        for i in range(len(self.A_matrix)):
            for j in range(len(self.A_matrix[0])):
                self.A_matrix[i][j] = aux_tableau[i+1][j] # +1 pois nao conta a primeira linha do tableau
        for i in range(1, len(self.b_vector)):
            self.b_vector[i] = aux_tableau[i][-1]

    def get_unlimited(self, base_positions):
        """
        Finds and prints unlimited certificate
        """
        # Busca a coluna com valores negativos
        for i, value in enumerate(self.c_vector):
            if value < 0:
                unl_column = i
                break
        for i in range(self.num_original_variables):
            if i == unl_column:
                print(1, end=" ")
            elif i in base_positions[0]:
                line_index = base_positions[0].index(i)
                line = base_positions[1][line_index]
                value = -1*self.A_matrix[line][unl_column]
                print(round(value, 7), end=" ")
            else:
                print(0, end=" ")
