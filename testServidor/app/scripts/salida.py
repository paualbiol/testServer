# Crea matrices de vecinos más cercanos para sacarla en la web.
def vecinos_matrix(nearest_form, nombres, notas, sele, diff):
    # Distinguir entre cursadas y deseadas.
    notas_curs = []
    notas_des = []
    nombres_curs = []
    nombres_des = []
    list_curs = []
    list_des = []
    for i in range(0, len(notas)):
        if notas[i] >= 0:
            notas_curs.append(notas[i])
            nombres_curs.append(nombres[i])
            list_curs.append(i)
        else:
            notas_des.append(notas[i])
            nombres_des.append(nombres[i])
            list_des.append(i)

    # Crear matriz de más cercanos con las cursadas. 
    nearest_form_curs = []
    for i in range(0, len(nearest_form)):
        aux = [i + 1]
        for j in range(0, len(list_curs)):
            aux.append(nearest_form[i][list_curs[j] + 1])
        # Añadir selectividad.
        aux.append(nearest_form[i][len(nearest_form[i]) - 2])
        nearest_form_curs.append(aux)

    # Crear matriz de más cercanos con las deseadas.
    nearest_form_des = []
    for i in range(0, len(nearest_form)):
        aux = [i + 1]
        for j in range(0, len(list_des)):
            aux.append(nearest_form[i][list_des[j] + 1])
        nearest_form_des.append(aux)
        
    # Unir notas de usuario con los vecinos para las cursadas.
    if sele < 0:
        vecinos_curs = [[''] + nombres_curs] + \
                       [['Tú'] + notas_curs] + nearest_form_curs
    else:
        vecinos_curs = [[''] + nombres_curs + ['Selectividad']] + \
                       [['Tú'] + notas_curs + [sele]] + nearest_form_curs


    # Unir notas de usuario con los vecinos para las deseadas.
    vecinos_des = [[''] + nombres_des] + nearest_form_des

    # Retornar ambas matrices.
    return vecinos_curs, vecinos_des


# Reordenar las notas esperadas como las introdujo el usuario y redondear
# a dos decimales.
def format_notas_esp(nombres_des, l_des, grades, nombres):
    notas_esp = []
    for i in range(0, l_des):
        pos = nombres.index(nombres_des[i])
        notas_esp.append(grades[pos])
        notas_esp[i] = round(notas_esp[i], 2)
    return notas_esp


# Crear matriz de fin de semana.
def format_finde_des(finde_des, nombres_des, l_des):
    finde = [['Asignatura', 'Horas']]
    for i in range(0, l_des):
        if finde_des[i] > 0:
            finde.append([nombres_des[i], finde_des[i]])
    return finde
