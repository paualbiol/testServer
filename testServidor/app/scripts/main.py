import pandas as pd
from app.scripts import entrada as ent
from app.scripts import salida as sal
from app.scripts import predictor as pr
from app.scripts import horas as hr
from app.scripts import generador as gn
from app.scripts import rendimiento as rd
from app.scripts import terminal as ter


def main(notas_curs_todas, rend, nombres_des, notas_des, horario):
    # Convertir input de la web en input válido para el programa.
    sele, l_curs, l_des, nombres_des, notas_des, codas, nombres, notas, k, \
        horario, rend, notas_curs, l_horario, hora_ini = \
        ent.convert_input(notas_curs_todas, nombres_des, rend, notas_des, horario)
    
    # Predecir notas.
    grades, nearest_form, diff = pr.predictor_main(codas, notas, k, l_curs, sele)

    # Posible error si no hay ningún alumno 'commpatible' con usuario.
    if len(nearest_form) == 0:
        print('\n Ningún alumno compatible! \n')
        return

    # Reordenar las notas esperadas como las introdujo el usuario y redondear
    # a dos decimales.
    notas_esp = sal.format_notas_esp(nombres_des, l_des, grades, nombres)

    # Crear vector de medias y de creditos para asignaturas deseadas.
    df = pd.read_csv('app/databases/asignaturas.csv')
    df = df[df['NOMBRE'].isin(nombres_des)]
    df = df.reset_index(drop = True)
    notas_med = []
    creds = []
    for i in range(0, len(nombres_des)):
        notas_med += df[df['NOMBRE'] == nombres_des[i]]['NM'].values.tolist()
        creds += df[df['NOMBRE'] == nombres_des[i]]['CR'].values.tolist()

    # Obtener horas deseadas según rendimiento.
    notas_des = rd.rend_main(rend, l_des, notas_des, notas_curs, l_curs)

    # Obtener horas de estudio.
    horas = hr.hours_main(notas_des, notas_esp, notas_med, l_des, creds)

    # Generar horario.
    finde_des, nombres_hor, horario_des, \
        horario, ini = gn.generator_main(horas, nombres_des, horario)
    hora_ini += ini
    # Si el horario está vacío, poner hora de inicio a las 9.
    if hora_ini == 23:
        hora_ini = 9
    
    # Imprimir resultados por terminal.
    ter.print_results(nombres_des, notas_des, l_des, notas_esp, nombres, \
               nearest_form, notas, diff, horas, horario_des, finde_des, \
               sele, notas_med, creds, rend)

    # Crear matriz de vecinos más cercanos.
    vecinos_curs, vecinos_des = sal.vecinos_matrix(nearest_form, nombres, \
                                                   notas, sele, diff)

    # Crear matriz de fin de semana.
    finde = sal.format_finde_des(finde_des, nombres_des, l_des)

    # Retornar todo lo necesario para generar el output.
    return horario, hora_ini, nombres_hor, vecinos_curs, vecinos_des, \
        notas_esp, nombres_des, finde, notas_des, notas_med, horas, creds
