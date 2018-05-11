import pandas as pd


# Dado un vector de CODASS, devuelve un vector con los nombres de las asignaturas.
def decoder(codass):
    df = pd.read_csv('app/databases/asignaturas.csv')
    df = df[df['CODASS'].isin(codass)]
    df = df.reset_index(drop = True)
    names = []
    for i in range(0, len(df)):
        names += df[df['CODASS'] == names[i]]['NOMBRE'].values.tolist()
    return names


# Dado un vector de nombres de asignaturas, devuelve un vector con los CODASS.
def encoder(names):
    df = pd.read_csv('app/databases/asignaturas.csv')
    df = df[df['NOMBRE'].isin(names)]
    df = df.reset_index(drop = True)
    codass = []
    for i in range(0, len(df)):
        codass += df[df['NOMBRE'] == names[i]]['CODASS'].values.tolist()
    return codass
