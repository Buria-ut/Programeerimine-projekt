""" Õppimise planeerimise rakendus. Autorid: Anna Katlerova, Liisa Alop """

from datetime import date, datetime, timedelta
import json

paevane_limiit = 2
fnimi_ulesanded = 'ulesanded.txt'
fnimi_ajakava = 'ajakava.txt'

def loe_ulesanne_failist(fnimi):
    """ loeb failist json formaadis ülesanded sõnastikku """
    try:
        f=open(fnimi, encoding = 'utf-8')
        massiiv = json.load(f)
        f.close()
        andmed = {}
        for element in massiiv:
            element['tahtaeg'] = datetime.strptime(element['tahtaeg'], '%Y-%m-%d').date()
            andmed[element['kood']] = element
        return andmed
    except:
        return {}
    
def salvesta_ulesanne_faili(fnimi, ulesanded):
    """ kirjutab ülesanded sõnastikust json kujul faili """
    kirjed = []
    for ulesanne in ulesanded.values():
        koopia = ulesanne.copy()
        koopia['tahtaeg'] = koopia ['tahtaeg'].isoformat()
        kirjed.append(koopia)
    f=open(fnimi,'w', encoding='utf-8')
    json.dump(kirjed, f, indent=4, ensure_ascii=False)
    f.close()

def vota_tahtaeg(ulesanne):
    """ tagastab sorteerimiseks ühe ülesande tähtaja """
    return ulesanne['tahtaeg']

def jaga_ajakulu(ulesanne):
    """ jagab ülesande mahu plokkideks, millest igaüks on suurusega kuni paevane_limiit tundi ja tagastab plokkide listi, nt 5 h -> [2, 2, 1] """
    blocks = []
    ajakulu = ulesanne['maht']
    while ajakulu > paevane_limiit:
        ajakulu = ajakulu - paevane_limiit
        blocks.append(paevane_limiit)
    blocks.append(ajakulu)
    return blocks

def koosta_järjekord(ulesanded):
    """ koostab kõigi ülesannete põhjal ajakava sorteerides ülesanded tähtaja järgi ja kirjutab ajakava faili """
    
    # sorteerib ülesanded tähtaja järgi (lähim tähtaeg esimesena)
    ulesanded_loendina = sorted(ulesanded.values(), key=vota_tahtaeg)

    ajakava = {}   # kuupäev -> mida sel päeval teha

    for t in ulesanded_loendina:
        viimane_paev = t["tahtaeg"] - timedelta(days=1)
        paev = date.today()
        for plokk in jaga_ajakulu(t):
            if paev > viimane_paev:
                # kui plokk ei mahu enne tähtaega ära, antakse hoiatus
                print(f'\nHOIATUS: {t["aine"]} {t["kirjeldus"]}: {plokk} h ei mahu tähtajaks ära\n')
            else:
                if paev not in ajakava:
                    ajakava[paev] = []
                ajakava[paev].append(f'{t["aine"]}: {t["kirjeldus"]} - {plokk} h')
            paev = paev + timedelta(days=1)
    # kirjutab faili järgmised 7 päeva, tühjad päevad märgib vabaks
    with open(fnimi_ajakava, 'w', encoding='utf-8') as file:
        for i in range(7):
            paev = date.today() + timedelta(days=i)
            file.write(f'{paev}\n')
            if paev in ajakava:
                for rida in ajakava[paev]:
                    file.write(f'  {rida}\n')
            else:
                file.write('  vaba päev\n')

def loe_jarjekord():
    """loeb ajakava failist ja kuvab selle"""
    try:
        with open(fnimi_ajakava, 'r', encoding='utf-8') as file:
            sisu = file.read().strip()
            if len(sisu) == 0:
                print ('Sul on kõik õpitud.')
            else:
                print(sisu)
    except:
        # faili pole
        print ('Sul on kõik õpitud.')
        
def lisa_ulesanne(kood, aine, kirjeldus, tahtaeg, maht, ulesanded):
    """ lisab ülesande sõnastikku """
    if kood in ulesanded:
        print(f'Koodiga {kood} ülesanne on juba olemas')
        return
    
    ulesanne = {
        "kood": kood,
        "aine": aine,
        "kirjeldus": kirjeldus,
        "tahtaeg": tahtaeg,
        "maht": maht
    }
    
    # lisab ülesande ajutiselt ülesannete nimekirja, et kontrollida ajakava arvutust
    ulesanded[kood] = ulesanne    
    jagamine_onnestus=True
    try:
        koosta_järjekord(ulesanded)
    except:
        # kui tekkis viga, siis eemaldatakse vigane ülesanne
        jagamine_onnestus=False
        ulesanded.pop(kood)
    if jagamine_onnestus==True:
        salvesta_ulesanne_faili(fnimi_ulesanded, ulesanded)
        jaga_ajakulu(ulesanne)
    else:
        print('Ülesande lisamine ei õnnestu, küsi õppejõult pikendust.')
    
def kustuta_ulesanne(ulesanded):
    """ eemaldab ülesande ülesannete sõnastikust """
    kustutatav = input('Sisesta kustutatava ülesande kood: ')
    if kustutatav in ulesanded:
        ulesanded.pop(kustutatav)
        salvesta_ulesanne_faili(fnimi_ulesanded, ulesanded)
        koosta_järjekord(ulesanded)
    else:
        print('Sellise koodiga ülesannet ei leitud.')
                
def kuva_ulesanded(ulesanded):
    """ kuvab ülesanded sorteertitult tähtaja järgi """
    if len(ulesanded) == 0:
        print('\nAktiivseid ülesandeid ei ole, naudi vaba aega!\n')
    else:
        # loendi sorteerimine tähtaja järgi
        ulesanded_sorteeritud = sorted(ulesanded.values(), key=lambda x: x['tahtaeg'])
        for ulesanne in ulesanded_sorteeritud:
            tahtaeg_kuvamiseks = ulesanne['tahtaeg'].strftime('%d.%m.%Y')
            print(f'{tahtaeg_kuvamiseks}: {ulesanne['kood']}, {ulesanne['aine']}, {ulesanne['kirjeldus']}, {ulesanne['maht']} h')     

def main():
    while True:
        # enne iga uut tegevust loetakse failist värsked andmed
        ulesanded = loe_ulesanne_failist(fnimi_ulesanded)
        
        print('Ülesande lisamiseks sisesta "Lisa"')
        print('Ülesande kustutamiseks sisesta "Kustuta"')
        print('Väljumiseks sisesta "Lõpeta"')
        print('Ajakava kuvamiseks sisesta "Kuva"')
        print('Õppimise plaani kuvamiseks sisesta "Plaan"')
        tegevus = input('Vali tegevus: ')
        if tegevus == 'Lõpeta':
            break
        elif tegevus == 'Plaan':
            loe_jarjekord()
        elif tegevus == 'Kustuta':
            kustuta_ulesanne(ulesanded)
        elif tegevus == 'Lisa':
            kood = input('Anna ülesandele unikaalne kood: ')
            aine = input('Sisesta aine: ')
            kirjeldus = input('Sisesta ülesande kirjeldus: ')
            while True:
                tahtaeg = input('Sisesta ülesande tähtaeg (aaaa-kk-pp): ')
                try:
                    tahtaeg_date = datetime.strptime(tahtaeg, '%Y-%m-%d').date()
                    if tahtaeg_date > datetime.now().date():
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
            lisa_ulesanne(kood, aine, kirjeldus, tahtaeg_date, maht_h, ulesanded)      
        elif tegevus == 'Kuva':
            kuva_ulesanded(ulesanded)      
        else:
            print('Vigane sisend. Proovi uuesti')
            
if __name__ == "__main__":
    main()
