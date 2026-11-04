from datetime import date, timedelta

paevane_limiit = 2
tasks = []

while True:
    aine = input('Sisesta aine: ')
    if aine == 'stop':
        break
    ul = input('Sisesta ülesanne: ')
    paev_tekst = input('Sisesta tähtaeg (p.k.a): ')
    ajakulu = float(input('Sisesta ajakulu tundides: '))

    osad = paev_tekst.split('.')
    task = {"aine": aine, "ülesanne": ul,"tähtaeg": date(int(osad[2]), int(osad[1]), int(osad[0])),"ajakulu": ajakulu}
    tasks.append(task)

def vota_tahtaeg(ulesanne):
    return ulesanne['tähtaeg']

def jagame_ajakulu(ulesanne):
    blocks = []
    ajakulu = ulesanne['ajakulu']
    while ajakulu > paevane_limiit:
        ajakulu = ajakulu - paevane_limiit
        blocks.append(paevane_limiit)
    blocks.append(ajakulu)
    return blocks

tasks.sort(key=vota_tahtaeg)

ajakava = {}   # kuupäev -> mida sel päeval teha

for t in tasks:
    viimane_paev = t["tähtaeg"] - timedelta(days=1)
    paev = date.today()
    for blok in jagame_ajakulu(t):
        if paev > viimane_paev:
            print(f'HOIATUS: {t["aine"]} {t["ülesanne"]}: {blok} h ei mahu tähtajaks ära')
        else:
            if paev not in ajakava:
                ajakava[paev] = []
            ajakava[paev].append(f'{t["aine"]}: {t["ülesanne"]} - {blok} h')
        paev = paev + timedelta(days=1)

with open('ajakava.txt', 'w', encoding='utf-8') as file:
    for i in range(7):
        paev = date.today() + timedelta(days=i)
        file.write(f'{paev}\n')
        if paev in ajakava:
            for rida in ajakava[paev]:
                file.write(f'  {rida}\n')
        else:
            file.write('  vaba päev\n')
