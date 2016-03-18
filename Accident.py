
'''
CASE I
'''
import pandas as pd

df = pd.read_csv("accidentologie.csv",sep=';')
#remplit les colonnes vides ('nan') avec des chaines vides
df = df.fillna('')
#On supprime les colonnes inutiles
df.__delitem__('segm')
df.__delitem__('dept')
df.__delitem__('lieu_1_nomv')
df.__delitem__('lieu_2_nomv')
df.__delitem__('adresse')
df.__delitem__('coordonnees')
df = df.replace(['Scoo<=50','Scoo>125', 'Scoo50-125', 'Moto50-125', 'Moto>125', 'Voi', 'Car', 'PL<=7,5', 'PL>7,5', 'PLRem'],['Scoot','Scoot', 'Scoot', 'Moto', 'Moto', 'Voiture', 'Voiture','Poids_lourd','Poids_lourd','Poids_lourd'])
df = df.rename(columns={'vehicule_1_cadmin': 'Type_de_vehicule', 'com':'Arrondissement', })
df.head(10)


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

#dict of dataframe, datafram pour chaque arrondissement
dicoDfCodePostaux = {}
for code in codes:
    dicoDfCodePostaux[code] = df.loc[df['code_postal']==code]

#ajout arrondissement pour aider la viz
dfStat = pd.DataFrame({'code_postal':codes,'nb_accident':[len(d) for d in dicoDfCodePostaux.values()]})
dfStat['arrondissement'] = dfStat.apply(lambda row: int(str(row['code_postal'])[-2:]),axis=1)
dfStat = dfStat.sort(['arrondissement'], ascending=True)

#groupement pour avoir nombre d'accident par type de vehicule et par code postal
grouped = df.groupby(['code_postal','Type_de_vehicule'])
#print grouped.groups
vehicules = set(df['Type_de_vehicule'])

#Ajout ddes informations
for col in vehicules:
    l = []
    if col in ["Voiture","TRSem","TR","Q>50","Tram","Q<=50","Engin"]:
        continue
    for arr in dfStat['code_postal'].tolist():
        try:
            l.append(len(grouped.groups[arr,col]))
        except Exception,e:
            l.append(0)

    dfStat[col] = l


#dataframe avec avec code postaux et accidents
print dfStat

#si vous voulez un csv
csvname ="dataArrondissementForD3js.csv"
dfStat.to_csv(csvname,index=False)
