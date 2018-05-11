import pandas as pd
from app.scripts import vecinos as vc


# Dada una posición, devuelve el inicio del siguiente alumno (con CODEX distinto).
# Devuelve -1 si no quedan más alumnos.
def next(pos, df):
    aux = pos # Para no modificar pos.
    codex = df['CODEX'].iloc[aux]
    while aux < len(df):
        if df['CODEX'].iloc[aux] != codex: return aux
        aux += 1
    return -1


# Crea una matriz con todos los alumnos que tienen nota en codas.
# La matrix tiene la forma (con primer fila de cabecera):
# | CODEX/CODASS | CODASS1 | CODASS2 | ... | CODASSN | SELE |
# |    CODEX     |   NF1   |   NF2   | ... |   NFN   |  NS  |
# Donde CODASS1...CODASSN son los códigos de codas.
def create_matrix(df, codas, sele):
    df = df[df['CODASS'].isin(codas)] # Primer filtrado.
    df.reset_index(drop = True)

    pos = 0
    matrix = [['CODEX/CODASS'] + codas + ['SELE']]
    while True:
        npos = next(pos, df)
        if npos == -1: return matrix
        # Optimización usando que df está ordenado.
        notas = df[pos:npos]['NF'].values.tolist()
        if len(notas) == len(codas):
            codex = df['CODEX'].iloc[pos]
            if sele < 0:
                matrix.append([codex] + notas)
            else:
                sele_aux = df['SELE'].iloc[pos]
                matrix.append([codex] + notas + [sele_aux])
        pos = npos


# Retorna vector con las notas predichas para las asignaturas de asigs2.
def predict_grades(nearest, codas, notas, matrix, k, diff, sele):
    # Posible error por falta de alumnos 'compatibles'.
    if len(nearest) < k: k = len(nearest)
    # Corrección de error si no hay ningún alumno 'compatible'.
    if k == 0: return 0

    # Predicción de notas.
    grades = [0]*len(codas)
    for j in range(0, len(codas)):
        # Si es una asignatura no cursada, calculo la media.
        if notas[j] < 0:
            for i in range(0, k):
                grades[j] += matrix[nearest[i][1]][j + 1]
            grades[j] /= k
            grades[j] += diff
            if grades[j] < 0: grades[j] = 0 # No permitir notas negativas.
            if grades[j] > 10: grades[j] = 10 # No permitir notas mayores que 10.
    return grades


# Precondición: asigs2 está ordenado de manera creciente (mismo orden que matriz).
def predictor_main(codas, notas, k, l_curs, sele):
    # Abrir fichero con todos los datos (está ordenado).
    df = pd.read_csv('app/databases/data.csv')

    # Crear la matriz.
    matrix = create_matrix(df, codas, sele)

    # Vector con los k vecinos más cercanos y diferencia.
    nearest, diff, nearest_form = vc.k_nearest_neighbors(k, matrix, notas, \
                                                         l_curs, sele)

    # Predecir notas.
    grades = predict_grades(nearest, codas, notas, matrix, k, diff, sele)

    return grades, nearest_form, diff
