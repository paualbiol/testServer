# Da formato a los vecinos más cercanos de matriz (sin primera fila).
# | CODEX | NOMBRE1 | NOMBRE2 | ... | NOMBREN | SELE |
# |   C   |   NF1   |   NF2   | ... |   NFN   |  NS  |
# Selectividad solo si ha sido introducida por usuario.
def format_nearest(nearest, matrix):
    nearest_form = []
    for i in range(0, len(nearest)):
        nearest_form += [matrix[nearest[i][1]] + [round(nearest[i][0], 2)]]
    return nearest_form


# Calcula distancia entre usuario y alumno (dada su fila en matriz).
def distance(row, notas, matrix, sele):
    distance = 0
    for j in range(0, len(notas)):
        if notas[j] >= 0: # Solo sumo para notas1 (las que son >= 0)
            # La primera columna tiene el CODEX.
            distance += pow(notas[j] - matrix[row][j + 1], 2)
    # Si el usuario me ha proporcionado sele.
    if sele >= 0: distance += pow(sele - matrix[row][len(notas) + 1], 2)
    return distance


# Cálculo de la media de diferencias de notas (con signo) entre usuario y vecinos.
def differences(notas, nearest, k, matrix, l_curs):
    if l_curs == 0: return 0 # Caso especial si ninguna nota se introduce.
    # Posible error por falta de alumnos 'compatibles'.
    if len(nearest) < k: k = len(nearest)
    # Corrección de error si no hay ningún alumno 'compatible'.
    if k == 0: return 0

    # Cálculo de diferencia total.
    diff_tot = 0
    for i in range(0, k):
        row = nearest[i][1]
        diff = 0
        for j in range(0, len(notas)):
            if notas[j] >= 0:
                diff += notas[j] - matrix[row][j + 1]
        diff_tot += diff/l_curs
    return diff_tot/k


# Retorna vector con las filas (en la matriz) de los k vecinos más cercanos.
# Devuelve la diferencia total media (con signo) a sus k vecinos más cercanos.
def k_nearest_neighbors(k, matrix, notas, l_curs, sele):
    # Calculo todas las distancias.
    nearest = []
    for row in range(1, len(matrix)):
        nearest.append([distance(row, notas, matrix, sele), row])

    # Me quedo con los k vecinos más cercanos.
    nearest.sort()
    nearest = nearest[0:k]

    # Calculo diferencia media total.
    diff = differences(notas, nearest, k, matrix, l_curs)

    # Doy formato de matriz al vector nearest.
    nearest_form = format_nearest(nearest, matrix)

    return nearest, diff, nearest_form
