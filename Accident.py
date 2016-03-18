
'''
CASE I
'''

import pandas as pd

df = pd.read_csv("accidentologie.csv",sep=';')
#remplit les colonnes vides ('nan') avec des chaines vides
df = df.fillna('')
#supprime la colonne segm
df.__delitem__('segm')
df = df.replace(['Scoo<=50','Scoo>125', 'Scoo50-125', 'Moto50-125', 'Moto>125', 'Voi', 'Car'],['Scoot','Scoot', 'Scoot', 'Moto', 'Moto', 'Voiture', 'Voiture'])
df = df.rename(columns={'vehicule_1_cadmin': 'Type_de_vehicule'})
df.head()


'''
CASE II

'''

#en commentaire parce que useless pour l'instant
'''
for col in  df.columns - ['lieu_1_nomv','lieu_2_nomv','date','carr','coordonnees','adresse','code_postal','com','7541','heure']:
    print col,' \n',set(df[col])
    print '\n'
'''


'''

CASE III
'''

#classement par code postal
df.sort_values(['code_postal'])

#visualisation des codes postaux possible
codes=df['code_postal'].unique().tolist()
print codes

#dict of dataframe, datafram pour chaque arrondissement
dicoDfCodePostaux = {}
for code in codes:
    dicoDfCodePostaux[code] = df.loc[df['code_postal']==code]

dfStat = pd.DataFrame({'code_postal':codes,'nb_accident':[len(d) for d in dicoDfCodePostaux.values()]})
dfStat['arrondissement'] = dfStat.apply(lambda row: int(str(row['code_postal'])[-2:]),axis=1)
#dataframe avec avec code postaux et accidents
print dfStat

#si vous voulez un csv
csvname ="dataForD3js.csv"
dfStat.to_csv(csvname)
