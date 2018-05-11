from app.scripts import codificador as cd


# Imprimir por pantalla bien una matriz (de Stack Overflow).
def print_matrix(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print ('\n'.join(table))

    
# Imprimir por pantalla bien una matriz (de Stack Overflow).
def print_matrix_small(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print ('\n'.join(table))


# Programa para leer el input desde input_file.txt
def read(name):
    # Abrir fichero.
    input_file = open(name, 'r')

    # Leer todas las líneas del fichero como string.
    lines = input_file.readlines()

    # Guardar la nota de selectividad.
    sele = float(lines[19])

    # Guardar en vector asignaturas ya cursadas con notas.
    nombres_curs = []
    notas_curs = []
    # Diferencio entre el número de asignaturas cursadas introducido y el real.
    l_curs_int = int(lines[22])
    l_curs = l_curs_int
    for i in range(0, l_curs):
        nombre = lines[24 + 2*i]
        nota = float(lines[25 + 2*i])
        if nota != -1:
            nombre = nombre[0:len(nombre) - 1]
            nombres_curs.append(nombre)
            notas_curs.append(nota)
        else: l_curs -= 1
        codas_obt = cd.encoder(nombres_curs)

    # Guardar rendimiento.
    rend = int(lines[26 + 2*l_curs_int])

    # Guardar en vector asignaturas para hacer horario con nota deseada.
    l_des = int(lines[29 + 2*l_curs_int])
    nombres_des = []
    notas_des = []
    for i in range(0, l_des):
        nombre = lines[31 + 2*l_curs_int + 2*i]
        nombre = nombre[0:len(nombre) - 1]
        nombres_des.append(nombre)
        nota = float(lines[32 + 2*l_curs_int + 2*i])
        notas_des.append(nota)
    codas_des = cd.encoder(nombres_des)
        
    # Número de vecinos más cercanos.
    k = int(lines[33 + 2*l_curs_int + 2*l_des])
            
    # Restricciones de horario.
    l_horario = int(lines[36 + 2*l_curs_int + 2*l_des])
    horario = []
    for i in range(0, l_horario):
        aux = [0, 0, 0, 0, 0]
        for j in range(0, 5):
            aux[j] = int(lines[38 + 2*l_curs_int + 2*l_des + i][3*j:3*j + 2])
        horario.append(aux)
        
    # Unir todo el input y ordenarlo simultáneamente por CODASS.
    codas = codas_obt + codas_des
    # Guardar las notas deseadas negativas (para identificarlas después).
    for i in range(0, len(notas_des)):
        notas_des[i] *= -1
        # Para no tener problemas con el 0 lo guardo como -11.
        if notas_des[i] == 0: notas_des[i] = -11 
    notas = notas_curs + notas_des
    nombres = nombres_curs + nombres_des
    if len(codas) > 0:
        codas, notas, nombres = (list(t) for t in \
                                 zip(*sorted(zip(codas, notas, nombres))))

    # Retornar todo lo necesario.
    return sele, l_curs, l_des, nombres_des, notas_des, codas, nombres, notas, \
        k, horario, rend, notas_curs, l_horario
        

# Programa que genera el output del programa.
def print_results(nombres_des, notas_des, l_des, notas_esp, nombres, \
               nearest_form, notas, diff, horas, horario, finde_des, \
               sele, notas_med, creds, rend):
    # Imprimir por pantalla los vecinos más cercanos.
    print('\n', '\t'*7, 'VECINOS MÁS CERCANOS', '\n'*2)
    # Quitar las notas deseadas de la tabla.
    notas_sin = []
    for i in range(0, len(notas)):
        if notas[i] < 0:
            notas_sin.append('')
        else:
            notas_sin.append(notas[i])
    if sele < 0:
        nearest_form = [['CODEX'] + nombres + ['DISTANCIA'], \
                        ['']*(len(nombres) + 2)] + [['TÚ'] + notas_sin + \
                        ['diff = ' + str(round(diff, 2))]] \
                       + [['']*(len(nombres) + 2)] + nearest_form
    else:
        nearest_form = [['CODEX'] + nombres + ['SELE'] + ['DISTANCIA'], \
                        ['']*(len(nombres) + 3)] + [['TÚ'] + notas_sin + [sele] + \
                        ['diff = ' + str(round(diff, 2))]] \
                       + [['']*(len(nombres) + 3)] + nearest_form
    # Acortar nombres para que entren en pantalla.
    for j in range(0, len(nearest_form[0])):
        nearest_form[0][j] = nearest_form[0][j][0:5]
    print_matrix_small(nearest_form)

    # Imprimir por pantalla tabla con datos diversos.
    print('\n'*3, '\t'*7, 'EJECUCIÓN DEL PROGRAMA', '\n'*2)
    aux2 = [['ASIGNATURA', 'NOTA ESPERADA', 'NOTA DESEADA', 'NOTA MEDIA', \
             'CRÉDITOS', 'HORAS'], \
                ['', '', 'rend = ' + str(rend), '', '', '']]
    for i in range(0, l_des):
        aux2.append([nombres_des[i], round(notas_esp[i], 2), \
                     -round(notas_des[i], 2), round(notas_med[i], 2), \
                     creds[i], horas[i]])
    print_matrix(aux2)

    # Imprimir por pantalla el horario en tabla.
    print('\n'*3, '\t'*7, 'HORARIO DE ESTUDIO', '\n\n')
    horario = [['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES'], \
               ['', '', '', '', '']] + horario
    print_matrix(horario)

    # Vector con las horas del fin de semana.
    print('\n'*3, '\t'*7, 'FIN DE SEMANA: ', '\n'*2)
    aux3 = [['ASIGNATURA', 'HORAS'],['', '']]
    for i in range(0, l_des):
        aux3.append([nombres_des[i], finde_des[i]])
    print_matrix(aux3)

    # Imprimir distribución de horas.
    print('\n'*2)
    horas_total = 0
    for i in range(0, l_des):
        horas_total += horas[i]
    horas_finde = 0
    for i in range(0, l_des):    
        horas_finde += finde_des[i]
    horas_semana = horas_total - horas_finde
    aux4 = [['DISTRIBUCIÓN DE HORAS:', ''], ['', ''], ['Semana:', horas_semana], \
            ['Fin de semana:', horas_finde], ['Total:', horas_total]]
    print_matrix(aux4)

    print()
