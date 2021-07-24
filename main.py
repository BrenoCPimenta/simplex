def read_input():
    """
    Read input and return as list of intergers
    """
    standart_input = input()
    raw_input = standart_input.split(' ')
    int_input = [int(i) for i in raw_input]
    return int_input


n, m = read_input()
cost_vector = read_input()
restrictions = []
for i in range(int(n)):
    restrictions.append(read_input())
