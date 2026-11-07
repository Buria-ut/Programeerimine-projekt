# kuupäevade käsitlemiseks
from datetime import datetime
# andmete hoidmiseks json kujul
import json

def loe_failist(fnimi):
    try:
        f=open(fnimi, encoding = 'utf-8')
        andmed = json.load(f)
        for element in andmed:
            element['tahtaeg'] = datetime.strptime(element['tahtaeg'], '%Y-%m-%d').date()
        return andmed
        f.close()
    except FileNotFoundError:
        return []
def salvesta_faili(fnimi, ylesanded):
    kirjed = []
    for ylesanne in ylesanded:
        koopia = ylesanne.copy()
        koopia['tahtaeg'] = koopia ['tahtaeg'].isoformat()
        kirjed.append(koopia)
    f=open(fnimi,'w', encoding='utf-8')
    json.dump(kirjed, f, indent=4)
    f.close()

def lisa_ylesanne(kood, kirjeldus, tahtaeg, maht):
    ylesanne = {
        "kood": kood,
        "kirjeldus": kirjeldus,
        "tahtaeg": tahtaeg,
        "maht": maht
    }
    ylesanded.append(ylesanne)
    salvesta_faili(fnimi, ylesanded)

fnimi = 'ylesanded.txt'
ylesanded = []

def kuva_ylesanded(ylesanded):
    if len(ylesanded) == 0:
        print('\nAktiivseid ülesandeid ei ole, naudi vaba aega!\n')
    else:
        # loendi sorteerimine tähtaja järgi
        ylesanded_sorteeritud = sorted(ylesanded, key=lambda x: x['tahtaeg'])
        for ylesanne in ylesanded_sorteeritud:
            tahtaeg_kuvamiseks = ylesanne['tahtaeg'].strftime('%d.%m.%Y')
            print(f'{tahtaeg_kuvamiseks}: {ylesanne['kood']}, {ylesanne['kirjeldus']}, {ylesanne['maht']} h')     

loe_failist('ylesanded.txt')
while True:
    print('Ülesande lisamiseks sisesta "Lisa"')
    print('Väljumiseks sisesta "Lõpeta"')
    print('Ajakava kuvamiseks sisesta "Kuva"')
    tegevus = input('Vali tegevus: ')
    if tegevus == 'Lõpeta':
        break
    elif tegevus == 'Lisa':
        kood = input('Anna ülesandele unikaalne kood: ')
        kirjeldus = input('Sisesta ülesande kirjeldus: ')
        while True:
            tahtaeg = input('Sisesta ülesande tähtaeg (aaaa-kk-pp): ')
            try:
                tahtaeg_date = datetime.strptime(tahtaeg, '%Y-%m-%d').date()
                if tahtaeg_date >= datetime.now().date():
                    break
                else:
                    print('Sisestatud kuupäev ei tohi olla minevikus. ')
            except ValueError:
                print('Sisestatud kuupäeva formaat on vigane. Sisesta kuupäev kujul aaaa-kk-pp. ')
        while True:
            maht = input('Sisesta ülesande eeldatav maht (tundides): ')
            if maht.isdigit():
                maht_h = int(maht)
                break
            else:
                print('Sisestatud ülesande maht on vigane. Sisesta ülesande maht tundides täisarvuna')
        lisa_ylesanne(kood, kirjeldus, tahtaeg_date, maht_h)      
    elif tegevus == 'Kuva':
        kuva_ylesanded(ylesanded)      
    else:
        print('Vigane sisend. Proovi uuesti')
        
