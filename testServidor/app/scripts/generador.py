# Quitar filas vacías del principio o final.
def format_horario(horario_inp):
    # Encontrar comienzo de filas no vacías.
    ini = 0
    finished = False
    while ini < len(horario_inp):
        for j in range(0, len(horario_inp[0])):
            if horario_inp[ini][j] >= 0:
                finished = True
        if finished: break
        ini += 1

    # Encontrar fin de filas no vacías
    fin = len(horario_inp) - 1
    finished = False
    while fin >= 0:
        for j in range(0, len(horario_inp[0])):
            if horario_inp[fin][j] >= 0:
                finished = True
        if finished: break
        fin -= 1

    # Crear vector formateado.
    horario = []
    for i in range(ini, fin + 1):
        horario.append(horario_inp[i])

    return horario, ini


# Función de comparación para el ordenamiento por selección.
def comp(a, b):
    if a%2 == 0:
        if b%2 == 0:
            if a <= b: return True
            return False
        return True
    else:
        if b%2 == 0: return False
        if a <= b: return True
        return False

        
# Ordenamiento por selección.
def sort(u, v, w):
    n = len(u)
    for i in range(0, n):
        min = u[i]
        posMin = i
        for j in range(i + 1, n):
            if comp(u[j], min):
                min = u[j]
                posMin = j
        u[i], u[posMin] = u[posMin], u[i]
        v[i], v[posMin] = v[posMin], v[i]
        w[i], w[posMin] = w[posMin], w[i]        


# Primera asignación de horas al fin de semana.
def update_finde(hours):
    n = len(hours)
    finde = [0]*n
  
    ht = 0
    for i in range(0, n): ht += hours[i]
    hf = int((ht*2)/7)

    if hf%2 != 0: hf -= 1
    
    i = n - 1
    while hf > 0:
        hf -= 2
        hours[i] -= 2
        finde[i] += 2
        i -= 1
        # Si me he salido de la lista, vuelvo a comenzar.
        if i < 0: i = n - 1
        
    return finde
        

# Añadir 1 hours de estudio de asig en day.
def put1(asig, day, horario):
    for i in range(0, len(horario)):
        if horario[i][day] == -2:
            horario[i][day] = asig
            return True
    return False


# Añadir 2 hours de estudio de asig en day.
def put2(asig, day, horario):
    for i in range(0, len(horario) - 1):
        if horario[i][day] == -2 and horario[i + 1][day] == -2:
            horario[i][day] = horario[i + 1][day] = asig
            return True
    return False;


# Retorna verdadero si un día está completo.
def complete(horario, day):
    n = len(horario)
    for i in range(0, n):
        if horario[i][day] == -2: return False
    return True


# Devuelve el día con menos hours de estudio no completo.
def next_minimum_uncomplete(horario, hras_est_dia):
    minDay = -1
    for day in range(0, 5):
        if not complete(horario, day) and \
           (minDay == -1 or hras_est_dia[day] < hras_est_dia[minDay]):
            minDay = day
    return minDay


def distribute(hours, horario, finde):
    hras_est_dia = [0]*5
    n = len(hours) # Número de asignaturas.
  
    # En grupos de 2 hours.
    # Secuencia: Lunes, Miércoles, Viernes, Martes, Jueves.
    sec = [0, 2, 4, 1, 3]
    j = 0  # Iterador para la secuencia de días.
    for asig in range(0, n):
        exit = 0
        while hours[asig] > 1 and exit < 5:
            if j > 4: j = 0
            if put2(asig, sec[j], horario):
                hours[asig] -= 2
                hras_est_dia[sec[j]] += 2
            else: exit += 1
            j += 1

    # Para que no se quede una asignatura con más de 4 hours para el fin de semana.
    for asig in range(0, n):
        bug = 0 # Para evitar bucle infinito.
        while hours[asig] + finde[asig] > 4 and bug < 3:
            bug += 1
            day = next_minimum_uncomplete(horario, hras_est_dia)
            if day != -1 and put1(asig, day, horario):
                hours[asig] -= 1
                hras_est_dia[day] += 1

    # De 1 hora en 1 hora. Comenzando por los días con menos hours de estudio.
    for asig in range(0, n):
        finished = False
        while hours[asig] > 0 and not finished:
            day = next_minimum_uncomplete(horario, hras_est_dia)
            if day == -1: finished = True
            elif put1(asig, day, horario):
                hours[asig] -= 1
                hras_est_dia[day] += 1

    # Guardando las hours no asignadas en vector fin de semana.
    for i in range(0, n):
        finde[i] += hours[i]
        hours[i] = 0

        
def generator_main(horas, nombres_des, horario):
    # Creo copia del vector de horas y de nombres, para no sobreescribirlo.
    hours = list(horas)
    nombres = list(nombres_des)
    
    # Ejecución del generador.
    sort(hours, nombres, [0]*len(hours))
    finde = update_finde(hours)
    sort(hours, nombres, finde)
    distribute(hours, horario, finde)

    # Quitar filas vacías del principio o final.
    horario, ini = format_horario(horario)

    horario_des = []
    for i in range(0, len(horario)):
        horario_des.append([])
        for j in range(0, len(horario[0])):
            horario_des[i].append(horario[i][j])

    # Convirtiendo el horario codificado, a horario con nombres.
    for i in range(0, len(horario)):
        for j in range(0, 5):
            k = horario[i][j]
            if k >= 0: horario_des[i][j] = nombres[k]
            elif k == -1: horario_des[i][j] = '-----------------'
            else: horario_des[i][j] = ''

    # Reordenando el vector finde, como nombres_des.
    finde_des = []
    for i in range(0, len(finde)):
        pos = nombres.index(nombres_des[i])
        finde_des.append(finde[pos])

    return finde_des, nombres, horario_des, horario, ini
