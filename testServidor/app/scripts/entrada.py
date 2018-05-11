from flask import request
from app.scripts import codificador as cd


# Quitar filas ocupadas al inicio y al final.
def format_horario(horario_inp):
    # Encontrar comienzo de filas no vacías.
    ini = 0
    finished = False
    while ini < len(horario_inp):
        for j in range(0, len(horario_inp[0])):
            if horario_inp[ini][j] == -2:
                finished = True
        if finished: break
        ini += 1

    # Encontrar fin de filas no vacías
    fin = len(horario_inp) - 1
    finished = False
    while fin >= 0:
        for j in range(0, len(horario_inp[0])):
            if horario_inp[fin][j] == -2:
                finished = True
        if finished: break
        fin -= 1

    # Crear vector formateado.
    horario = []
    for i in range(ini, fin):
        horario.append(horario_inp[i])

    return horario, 9 + ini


# Convertir input de la web en input válido para el programa.
def convert_input(notas_curs_todas, nombres_des, rend, notas_des, horario):
    # Variables puestas como 'default'.
    nombres_curs_todas = ['Álgebra Lineal', 'Cálculo I', 'Mecánica Fundamental', 
                          'Química I', 'Fundamentos de Informática', 'Cálculo II',
                          'Geometría','Termodinámica Fundamental', 'Química II',
                          'Expresión Gráfica']
    k = 12

    # Notas introducidas por el usuario.
    sele = notas_curs_todas[0]
    l_curs = 0
    notas_curs = []
    nombres_curs = []
    for i in range(1, len(notas_curs_todas)):
        if notas_curs_todas[i] >= 0:
            notas_curs.append(notas_curs_todas[i])
            nombres_curs.append(nombres_curs_todas[i - 1])
            l_curs += 1
    codas_curs = cd.encoder(nombres_curs)

    # Asignaturas para hacer horario.
    l_des = len(nombres_des)
    codas_des = cd.encoder(nombres_des)

    # Unir todo el input y ordenarlo simultáneamente por CODASS.
    codas = codas_curs + codas_des
    # Guardar las notas deseadas negativas (para identificarlas después).
    for i in range(0, len(notas_des)):
        notas_des[i] *= -1
        # Para no tener problemas con el 0 lo guardo como -1111.
        if notas_des[i] == 0: notas_des[i] = -1111 
        notas = notas_curs + notas_des
        nombres = nombres_curs + nombres_des
    if len(codas) > 0:
        codas, notas, nombres = (list(t) for t in \
                                 zip(*sorted(zip(codas, notas, nombres))))

    # Quitar filas ocupadas al inicio y al final.
    horario, hora_ini = format_horario(horario)
    l_horario = len(horario)
    
    # Retornar todo lo necesario.
    return sele, l_curs, l_des, nombres_des, notas_des, codas, nombres, notas, \
        k, horario, rend, notas_curs, l_horario, hora_ini


# Leer notas cursadas desde la web.
def leer_cursadas():
    sele = request.form['input_sele']
    algebra = request.form['input_algebra']
    calcul1 = request.form['input_calcul1']
    info1 = request.form['input_info1']
    mec_fon = request.form['input_MecFon']
    quim1 = request.form['input_quim1']
    calc2 = request.form['input_calcul2']    
    expre = request.form['input_expre']
    geo = request.form['input_geo']
    quim2 = request.form['input_quim2']
    termo = request.form['input_termo']

    # Convertir notas a lista.
    notas_curs_todas = [sele, algebra, calcul1, info1, mec_fon, quim1, calc2, \
                        expre, geo, quim2, termo]
    for i in range(0, len(notas_curs_todas)):
        if notas_curs_todas[i] == '':
            notas_curs_todas[i] = -1
        notas_curs_todas[i] = float(notas_curs_todas[i])

    return notas_curs_todas
