
'''
CASE I
'''
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
import numpy as np

df2 = pd.read_csv("AccidentDetail.csv",sep=',')


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

#en commentaire parce que useless pour l'instant
'''
    for col in  df.columns - ['lieu_1_nomv','lieu_2_nomv','date','carr','coordonnees','adresse','code_postal','com','7541','heure']:
    print col,' \n',set(df[col])
    print '\n'
    '''

#scrapping nombre d'habitant par arondissement
languages=range(1,21)
dfHab=pd.DataFrame({'arondissement' : languages, 'habitant': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]})

page = requests.get("http://www.insee.fr/fr/ppp/bases-de-donnees/recensement/populations-legales/departement.asp?dep=75").text
doc  = html.fromstring(page)
d = {}
for i in range(1,21) :
    element = doc.xpath('//*[@id="col-centre"]/table[2]/tbody/tr['+str(i)+']/td[5]')[0]
    print("Arrondissement " + str(i) + ", " + element.text_content().replace(" ",""))
    value = ""
    for j in element.text_content():
        if(j.isnumeric()):
            value += j
    d[i] = value
    dfHab["habitant"][int(i)-1] = int(value)

print dfHab
dfHab.plot('arondissement','habitant',kind="bar",title="Nombre d'habitant par arrondissement",color='green')

heures=range(0,24)
lh = []
for h in heures:
    lh.append(df2[str(h)].sum())
dfHeure = pd.DataFrame({"heure" : heures, "accidents": lh})
print dfHeure

dfHeure.plot('heure', 'accidents')
plt.xticks(np.arange(0, 24, 1.0))
plt.show()

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

'''

CASE IV
'''

labels ='Cyclo', 'VU', 'Bicy', 'Bus', 'Moto', 'Poids_lourd', 'VL', 'Scoot'

#la somme de chaque accident par type et le total
totalCyclo = dfStat['Cyclo'].sum(axis=0)
totalVU = dfStat['VU'].sum(axis=0)
totalBicy = dfStat['Bicy'].sum(axis=0)
totalBus = dfStat['Bus'].sum(axis=0)
totalMoto = dfStat['Moto'].sum(axis=0)
totalPL = dfStat['Poids_lourd'].sum(axis=0)
totalVL = dfStat['VL'].sum(axis=0)
totalScoot = dfStat['Scoot'].sum(axis=0)
total = totalCyclo + totalVU + totalBicy + totalBus + totalMoto + totalPL + totalVL + totalScoot

#la taille en pourcentage
sizes = [totalVU/total, totalBicy/total, totalBus/total, totalMoto/total, totalMoto/total, totalPL/total, totalVL/total, totalScoot/total]

#couleurs pour chaque part
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'red', 'orange', 'purple', 'green']
#le split
explode = (0, 0, 0, 0, 0, 0, 0.1, 0)

plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')

'''

CASE V
'''

fig = plt.figure()
ax = fig.gca()

#les camemberts
ax.pie(sizes, explode=(0, 0, 0, 0, 0, 0, 0, 0), labels=['','','','','','','',''], colors=colors,
       autopct='', shadow=True, startangle=90,
       radius=0.40, center=(0, 0), frame=True)

ax.pie(np.random.random(8), explode=(0, 0, 0, 0, 0, 0, 0, 0), labels=labels, colors=colors,
       autopct='', shadow=True, startangle=90,
       radius=0.40, center=(1, 1), frame=True)

ax.pie(np.random.random(8), explode=(0, 0, 0, 0, 0, 0, 0, 0), labels=['','','','','','','',''], colors=colors,
       autopct='', shadow=True, startangle=90,
       radius=0.40, center=(0, 1), frame=True)

ax.pie(np.random.random(8), explode=(0, 0, 0, 0, 0, 0, 0, 0), labels=['','','','','','','',''], colors=colors,
       autopct='', shadow=True, startangle=90,
       radius=0.40, center=(1, 0), frame=True)

ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_xticklabels(["2012", "2013"])
ax.set_yticklabels(["Paris", "La Ferté-Gaucher"])
ax.set_xlim((-0.5, 1.5))
ax.set_ylim((-0.5, 1.5))

#Set aspect ratio
ax.set_aspect('equal')

plt.show()