def is_safe(board, col):
    """
    Verifica si es seguro colocar una reina en board[col].
    board es una lista de longitud n, donde board[i] es la fila de la reina en columna i.
    """
    for i in range(col):
        # Misma fila
        if board[i] == board[col]:
            return False
        # Diagonal principal (diferencia de filas == diferencia de columnas)
        if abs(board[i] - board[col]) == abs(i - col):
            return False
    return True

def print_solution(board):
    """
    Imprime el tablero basado en el arreglo board.
    """
    n = len(board)
    for row in range(n):
        line = []
        for col in range(n):
            if board[col] == row:
                line.append("Q")
            else:
                line.append(".")
        print(" ".join(line))
    print()