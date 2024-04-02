################### COLOURS
BLUE = '#006BA2'
CYAN = '#3EBCD2'
GREEN = '#379A8B'
YELLOW = '#EBB434'
OLIVE = '#B4BA39'
PURPLE = '#9A607F'
RED = '#DB444B'
GOLD = '#D1B07C'
GREY =  '#758D99'
BLUE_LIGHT = '#98DAFF'
BLUE_DARK = '#00588D'
CYAN_LIGHT = '#6FE4FB'
CYAN_DARK = '#005F73'
GREEN_LIGHT = '#86E5D4'
GREEN_DARK = '#005F52'
YELLOW_LIGHT = '#FFCB4D'
YELLOW_DARK = '#714C00'
OLIVE_LIGHT = '#D7DB5A'
OLIVE_DARK = '#4C5900'
PURPLE_LIGHT = '#FFC2E3'
PURPLE_DARK = '#78405F'
RED_LIGHT = '#FFA39F'
RED_DARK = '#A81829'
GOLDLIGHT = '#F2CF9A'
GOLD_DARK = '#674E1F'


food = {
"🧁 pasticceria": ['q4__4', 'q5__4', 'freq_past', 'cam_past'],
"🍬 dolci": ['q4__5', 'q5__5', 'freq_dol', 'cam_dol'],
"🍩 biscotti": ['q4__6', 'q5__6', 'freq_bis', 'cam_bis'],
"🍔 merendine": ['q4__7', 'q5__7', 'freq_mer', 'cam_mer'],
"☕ caffè": ['q4__8', 'q5__8', 'freq_caf', 'cam_caf'],
"🍵 tè": ['q4__9', 'q5__9', 'freq_te', 'cam_te'],
"🍫 cioccolato": ['q4__10', 'q5__10', 'freq_cioc', 'cam_cioc'],
}

metrics_mapping = {
    'stile': ['stili alimentari','Stili alimentari'],
    'q4__4': ['Frequenza acquisto: pasticceria', 'Frequenza acquisto: pasticceria (torte pronte, muffin, crostate, ecc.)'],
    'q4__5': ['Frequenza acquisto: dolci', 'Frequenza acquisto: dolci da ricorrenza italiani (panettoni, pandori, colombe, ecc.)'],
    'q4__6': ['Frequenza acquisto: biscotti','Frequenza acquisto: biscotti'] ,
    'q4__7': ['Frequenza acquisto: merendine', 'Frequenza acquisto: merendine'],
    'q4__8': ['Frequenza acquisto: caffè', 'Frequenza acquisto: caffè'],
    'q4__9': ['Frequenza acquisto: tè e infusi', 'Frequenza acquisto: tè e infusi'],
    'q4__10': ['Frequenza acquisto: cioccolato', 'Frequenza acquisto: cioccolato, cioccolatini, praline'],
    'q5__4': ['Cambiamenti frequenza: pasticceria', 'Cambiamenti frequenza: pasticceria (torte pronte, muffin, crostate, ecc.)'],
    'q5__5': ['Cambiamenti frequenza: dolci', 'Cambiamenti frequenza: dolci da ricorrenza italiani (panettoni, pandori, colombe, ecc.'] ,
    'q5__6': ['Cambiamenti frequenza: biscotti', 'Cambiamenti frequenza: biscotti'],
    'q5__7': ['Cambiamenti frequenza: merendine', 'Cambiamenti frequenza: merendine'],
    'q5__8': ['Cambiamenti frequenza: caffè', 'Cambiamenti frequenza: caffè'],
    'q5__9': ['Cambiamenti frequenza: tè e infusi', 'Cambiamenti frequenza: tè e infusi'],
    'q5__10': ['Cambiamenti frequenza: cioccolato', 'Cambiamenti frequenza: cioccolato, cioccolatini, praline'],
}

order_frequenza = [
        'ogni giorno', '2-3/sett', '1/sett', 
        '2-3/mese', '1/mese', "raro", 
        ][::-1]

order_cambiamento = [
           "Molto +", "Poco +", "Uguale", 
            "Poco -", "Molto -", 
        ][::-1]

order_stile = [
    'Territorialisti',
    'Ristoriani',
    'Salutisti',
    'Industriariani',
    'Esterofili',
    'Salubristi',
    'Sregolati',
    'Edonisti',
    'Essenzialisti',
    'Localivori',
    'Eticisti',
    'Estetizzanti',
    'Nessuno stile',
][::-1]