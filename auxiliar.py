class Auxiliar():

    def __init__(self, A_matrix, b_vector, c_vector, num_rows, num_variables):
        self.A_matrix = A_matrix
        self.b_vector = b_vector
        self.c_vector = c_vector
        self.num_rows = num_rows
        self.num_variables = num_variables

    def execute(self, print_flag=False):
        """
        Creates aux tableau and manages it execution
        """

        self.aux_tableau = []
        firstline = []
        # Adiciona primeira linha
        for i in range(len(self.c_vector)):
            firstline.append(0)
        for i in range(self.num_rows):
            firstline.append(1) # colunas da auxiliar
        firstline.append(0) # valor objetivo
        self.aux_tableau.append(firstline)
        # Adiciona A e trata linhas com b negativo
        for i in range(self.num_rows):
            if self.b_vector[i+1] < 0:
                mult = -1
            else:
                mult = 1
            line = []
            for j in range(len(self.A_matrix[0])):
                line.append(self.A_matrix[i][j]*mult)
            self.aux_tableau.append(line)

        # Adiciona novas colunas e vetor b ao tableau auxiliar:
        for i in range(1, self.num_rows+1):
            for j in range(1, self.num_rows+1):
                if i == j:
                    self.aux_tableau[i].append(1)
                else:
                    self.aux_tableau[i].append(0)
            if self.b_vector[i] < 0:
                self.aux_tableau[i].append(self.b_vector[i]*-1)
            else:
                self.aux_tableau[i].append(self.b_vector[i])

        # Colocando em forma canonica
        # (Subtraindo outras linhas na primeira)
        for i in range(1, len(self.aux_tableau)):
            for j in range(len(self.aux_tableau[0])):
                self.aux_tableau[0][j] = self.aux_tableau[0][j] - self.aux_tableau[i][j]

        if print_flag:
            print()
            print("AUXILIAR")
            self.aux_print_matrix()

        # Pivoteando:
        need_pivot = True
        while need_pivot:
            # Busca pivot
            keep_pivot, pivot_line, pivot_column = self.aux_select_pivot()

            # Verifica parada
            if not keep_pivot:
                if round(self.aux_tableau[0][-1], 0) < 0:
                    print("inviavel")
                    start_range = self.num_variables
                    end_range = len(self.A_matrix[0])
                    for i in range(start_range, end_range):
                        print(round(self.aux_tableau[0][i], 7), end=" ")
                    return "inviavel"
                else:
                    need_pivot = False
                    continue
            # Pivoteia
            self.aux_pivot(pivot_line, pivot_column)
        return "viavel"

    def aux_select_pivot(self, print_flag=False):
        """
        Finds the line and the column
        of the pivot element
        """
        # Selecionando um valor negativo em C
        pivot_column = -1
        for i in range(len(self.aux_tableau[0])-1): # -1 para nao usar valor objetivo
            if self.aux_tableau[0][i] < 0:
                pivot_column = i
                break

        # Verificação de parada
        if pivot_column == -1:
            return (False, 0, 0)

        if print_flag:
            print("    |Column to pivot: ", pivot_column)
            print("    |Value in C: ", self.aux_tableau[0][pivot_column])
            print("    |Possible pivots:")

        # Calculando os limites
        possible_pivots = []
        lines = len(self.aux_tableau)
        for i in range(1, lines):
            numerator = abs(self.aux_tableau[i][-1])
            denominator = self.aux_tableau[i][pivot_column]
            if numerator == 0 or denominator == 0:
                continue

            limit = numerator/denominator
            if limit > 0:
                if print_flag:
                    print("    |    ", numerator, "/", denominator, "=", limit)
                possible_pivots.append((i, limit))
        # Verifica se não há possíveis pivots
        if len(possible_pivots) == 0:
            return (False, 0, 0)
        # Pegando o maior valor que o x selecionado pode tomar:
        # Ordena as tuplas e pega o index na primeira tupla
        possible_pivots.sort(key=lambda tup: tup[1])
        pivot_line = possible_pivots[0][0]
        if print_flag:
            print("    |Chosen pivot: ", possible_pivots[0][1])
        return (True, pivot_line, pivot_column)

    def aux_pivot(self, pivot_line, pivot_column):
        pivot = self.aux_tableau[pivot_line][pivot_column]

        # Regularizar linha do pivot
        if pivot != 1:
            self.aux_tableau[pivot_line] = [i*(1/pivot) for i in self.aux_tableau[pivot_line]]
            pivot = self.aux_tableau[pivot_line][pivot_column]

        # Regularizando as outras linhas
        for this_line in range(len(self.aux_tableau)):
            if this_line != pivot_line:
                value_reference = self.aux_tableau[this_line][pivot_column]
                if value_reference != 0:
                    new_line = []
                    for i in range(len(self.aux_tableau[0])):
                        new_line.append(self.aux_tableau[this_line][i] - (value_reference*self.aux_tableau[pivot_line][i]))
                    self.aux_tableau[this_line] = new_line

    def get_aux_tableau(self):
        return self.aux_tableau

    def aux_print_matrix(self):
        for i, line in enumerate(self.aux_tableau):
            print("    |",end="")
            if i == 0:
                sep = "_"
            else:
                sep = " "
            for value in line:
                space = self.aux_get_space(value)
                print(sep*space, round(value,3), end=" ")
            print()

    def aux_get_space(self, i):
        if i > 9:
            space = 2
        elif i >= 0:
            space = 3
        elif i < -9:
            space = 1
        elif i < 0:
            space = 2
        return space
