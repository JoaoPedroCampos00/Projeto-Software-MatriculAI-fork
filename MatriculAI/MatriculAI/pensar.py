materias = [{"cod":"ENG4021","hrs":[{"dia":6,"hi":7,"hf":9}]},{"cod":"ENG4021","hrs":[{"dia":6,"hi":9,"hf":11}]},{"cod":"ENG4021","hrs":[{"dia":6,"hi":11,"hf":13}]},{"cod":"ENG4021","hrs":[{"dia":6,"hi":13,"hf":15}]},{"cod":"MAT4161","hrs":[{"dia":2,"hi":7,"hf":9},{"dia":3,"hi":7,"hf":9},{"dia":4,"hi":7,"hf":9}]},{"cod":"MAT4161","hrs":[{"dia":2,"hi":9,"hf":11},{"dia":3,"hi":9,"hf":11},{"dia":4,"hi":9,"hf":11}]},{"cod":"MAT4161","hrs":[{"dia":2,"hi":11,"hf":13},{"dia":3,"hi":11,"hf":13},{"dia":4,"hi":11,"hf":13}]},{"cod":"MAT4161","hrs":[{"dia":2,"hi":13,"hf":15},{"dia":3,"hi":13,"hf":15},{"dia":4,"hi":13,"hf":15}]},{"cod":"MAT4161","hrs":[{"dia":2,"hi":15,"hf":17},{"dia":3,"hi":15,"hf":17},{"dia":4,"hi":15,"hf":17}]}]

DDS = ["Sab", "Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"];
DDS_M = {"SEG": 2, "TER": 3, "QUA": 4, "QUI": 5, "SEX": 6, "SAB": 7, "DOM": 8};

import json
from pathlib import Path
_db_path = Path(__file__).resolve().parent / "dbPUC.json"
if not _db_path.exists():
    raise FileNotFoundError(f"Arquivo não encontrado: {_db_path}")
with _db_path.open('r', encoding='utf-8') as file:
    turmas_imp_e = json.load(file)

def adicionarTurma(cod, texto, hrs):
    materias.append({cod: cod, hrs: hrs})

def celulaclick(dia, hora, horas_sel):
    horas_sel.append({"dia": dia, "hora": hora})

def estaSelecionado(dia, hora, horas_sel):
    return any(x == {"dia": dia, "hora": hora} for x in horas_sel)

def gethrs(horas_sel):
    hrs = []
    for d in range(2,7):
        ant_sel = False
        for h in range(7,18):
            if(estaSelecionado(d,h, horas_sel)):
                if(not ant_sel):
                    hi = h
                    ant_sel = True
            else:
                if(ant_sel):
                    hrs.append({"dia": d, "hi": hi, "hf": h})
                ant_sel = False
    return hrs

def buscarMat(cod):
    res = []
    turmas = list(filter(lambda x: x[0] == cod,turmas_imp_e))
    for i in turmas:
        hors_i = []
        hs_i = i[8].split("  ")
        for j in hs_i:
            if(j != ""):
                hs_j = j.split(" ")
                hi = hs_j[1].split("-")[0]
                hf = hs_j[1].split("-")[1]
                hors_i.append({"dia": DDS_M[hs_j[0]], "hi": int(hi), "hf": int(hf)})
        texto = ""
        for k in hors_i:
            texto += ("" if texto=="" else " / ")+DDS[int(k["dia"])]+" "+("0" if k["hi"]<10 else "")+str(k["hi"])+"-"+("0" if k["hf"]<10 else "")+str(k["hf"])
        if(not [x for x in res if x == {"cod": cod, "hrtxt": texto, "hrs": hors_i}]):
            res.append({"cod": cod, "hrtxt": texto, "hrs": hors_i})
    return res

def traduzirTexto(horas_sel):
    tex = ""
    for d in range(2,7):
        ant_sel = False
        for h in range(7,18):
            if(estaSelecionado(d,h, horas_sel)):
                if(not ant_sel):
                    tex += (" / " if tex!="" else "")+DDS[d]+" "+("0" if h<10 else "")+str(h)+"-"
                    ant_sel = True
            else:
                if(ant_sel):
                    tex += ("0" if h<10 else "")+str(h)
                ant_sel = False
    return tex

def fab(horario, dias, hs, dia, h):
    for i in horario:
            for t in i["hrs"]:
                tempo = t
                if(overlap(tempo["dia"], tempo["hi"], tempo["hf"], dias[dia], hs[h][0], hs[h][1])):
                    return i["cod"]
    return " "

def renderTabela(horario):
    dias = [2,3,4,5,6]
    hs = [[7,8],[8,9],[9,10],[10,11],[11,12],[12,13],[13,14],[14,15],[15,16],[16,17]]
    tempos = [["" for _ in range(len(dias))] for _ in range(len(hs))]
    for dia in range(len(dias)):
        h = 0
        while h < len(hs):
            tx = '<td'
            span = 1
            fcd = ""
            if(fab(horario, dias, hs, dia, h) != " "):
                tx += ' class="preenchido" '
                fcd = fab(horario, dias, hs, dia, h)
                for i in range(h+1,len(hs)):
                    if(fab(horario, dias, hs, dia, i) == fcd):
                        span += 1
                    else:
                        break
                if(span>1):
                    tx += 'rowspan="' + str(span) + '"'
            tx += ">" + fcd + "</td>"
            tempos[h][dia] = tx
            h += span
    
    HS = ['<td>07-08</td>','<td>08-09</td>','<td>09-10</td>','<td>10-11</td>','<td>11-12</td>','<td>12-13</td>','<td>13-14</td>','<td>14-15</td>','<td>15-16</td>','<td>16-17</td>']
    lns = []
    for h in range(len(tempos)):
        tex = HS[h]
        for dia in tempos[h]:
            tex += dia

        lns.append(tex)
    return lns

#Back End

possibilidades = []
horarios = []
possibilidades_i = 0

def overlap(dia, hi, hf, dia2, hi2, hf2):
    if(dia != dia2):
        return False
    else:
        if(hi2 >= hi and hi2 < hf):
            return True
        elif(hf2 > hi and hf2 <= hf):
            return True
    return False

def testaHor( horario, horarios ):
    for i in horarios:
        for j in i["hrs"]:
            ho = j
            if(overlap(horario["dia"], horario["hi"], horario["hf"], ho["dia"], ho["hi"], ho["hf"])):
                return False
    return True

def testaHorarios(materia, horarios):
    for i in materia["hrs"]:
        if(not testaHor(i, horarios)):
            return False
    return True


def addHora(materia, ino, materias, mats, possibilidades):
    global possibilidades_i
    red = [x for x in materias if x["cod"] == materia]
    for i in red:
        m = i
        if(testaHorarios(m, horarios)):
            horarios.append(m)
            if(ino+1 != len(mats)):
                addHora(mats[ino+1], ino+1, materias, mats, possibilidades)
            else:
                horeste = horarios[:]
                horeste.sort(key=lambda e: e["cod"])
                if(not any(x["hor"] == horeste for x in possibilidades)):
                    possibilidades.append({"hor": horeste, "dist": calcDist(horeste)})
                    #possibilidades.append(horeste)
                    possibilidades_i = possibilidades_i + 1
                    print(possibilidades_i)
            horarios.pop()


def calcDist(horario):
    dias = [2,3,4,5,6]
    hs = [[7,8],[8,9],[9,10],[10,11],[11,12],[12,13],[13,14],[14,15],[15,16],[16,17]]
    
    distTot = 0
    for dia in range(2,7):
        his = [x['hi'] for x in sum([x["hrs"] for x in horario], []) if x['dia'] == dia]
        hfs = [x['hf'] for x in sum([x["hrs"] for x in horario], []) if x['dia'] == dia]
        for i in hfs:
            s = sorted([x for x in his if x >= i])
            distTot += (s[0] - i) if s else 0
    return distTot

print(materias[0]["hrs"][0]["dia"])
print(overlap(6,7,9,6,8,10))
print(overlap(6,7,9,6,9,11))

def testaPossibilidades(mats, materias):
    possibilidades = []
    horarios = []
    # mats = ["ENG4021","MAT4161"]
    addHora(mats[0], 0, materias, mats, possibilidades)
    print(possibilidades)
    possibilidades.sort(key=lambda e: e["dist"])
    print(possibilidades)
    return [x["hor"] for x in possibilidades]