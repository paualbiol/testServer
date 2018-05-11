# Conversión de notas a horas de estudio.
def hours_main(notas_des, notas_esp, notas_med, l_des, creds):
    # Descodificar las notas deseadas de 0 (están guardadas como -1111).
    for i in range(0, l_des):
        if notas_des[i] == -1111:
            notas_des[i] = 0

    # Calcular horas (las notas deseadas son todas negativas).
    hours = []
    for i in range(0, l_des):
        # Para la media, es necesario estudiar 0.8*n_creditos horas a la semana.
        hours.append(creds[i]*0.8)
        # Multiplico por factor de corrección dependiendo de la nota deseada.
        # Evito el rápido crecimiento de la exponencial.
        if -notas_des[i] - notas_esp[i] < 2:
            hours[i] *= pow(1.12, 1.7*(-notas_des[i] - notas_esp[i]))
        elif -notas_des[i] - notas_esp[i] < 4:
            hours[i] *= pow(1.12, 1.1*(-notas_des[i] - notas_esp[i]))
        elif -notas_des[i] - notas_esp[i] < 6:
            hours[i] *= pow(1.12, 0.9*(-notas_des[i] - notas_esp[i]))
        else:
            hours[i] *= pow(1.12, 0.7*(-notas_des[i] - notas_esp[i]))
        # Factores de corrección para notas muy bajas.
        if -notas_des[i] <= 1:
            hours[i] = 0
        elif -notas_des[i] <= 1.5:
            hours[i] *= 0.5
        elif -notas_des[i] <= 2:
            hours[i] *= 0.75
        # Redondear la nota al entero más cercano.
        hours[i] = int(round(hours[i], 0))
        # No permitir horas por encima de 25.
        if hours[i] >= 25:
            hours[i] = 25
        
    return hours
