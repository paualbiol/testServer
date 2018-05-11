# Cálculo de media de las notas cursadas.
def mean(notas_curs, l_curs):
    if l_curs == 0: return -1
    mean = 0
    for i in range(0, l_curs):
        mean += notas_curs[i]
    mean /= l_curs
    return mean

                   
# Convierte rendimiento a notas deseadas.
def rend_main(rend, l_des, notas_des, notas_curs, l_curs):
    # Rendimiento mínimo.
    if rend == 'min':
        notas_des = [-5]*l_des
        return notas_des
    
    # Sin rendimiento (notas deseadas introducidas manualmente).
    if rend == 'man':
        return notas_des

    media = mean(notas_curs, l_curs)
    # Rendimiento medio.
    if rend == 'med':
        if l_curs == 0: notas_des = [11]*l_des
        elif media >= 5:
            notas_des = [-media]*l_des
        else:
            notas_des = [-5]*l_des
        return notas_des
    
    # Rendimiento máximo.
    if rend == 'max':
        if l_curs == 0: notas_des = [11]*l_des
        elif media*1.1 >= 5 and media*1.1 <= 10:
            notas_des = [-media*1.1]*l_des
        elif media*1.1 >= 5:
            notas_des = [-10]*l_des
        else:
            notas_des = [5*1.1]*l_des
        return notas_des
