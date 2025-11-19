materias = [{"cod":"ENG4021","hrs":[{"dia":6,"hi":7,"hf":9}]},{"cod":"ENG4021","hrs":[{"dia":6,"hi":9,"hf":11}]},{"cod":"ENG4021","hrs":[{"dia":6,"hi":11,"hf":13}]},{"cod":"ENG4021","hrs":[{"dia":6,"hi":13,"hf":15}]},{"cod":"MAT4161","hrs":[{"dia":2,"hi":7,"hf":9},{"dia":3,"hi":7,"hf":9},{"dia":4,"hi":7,"hf":9}]},{"cod":"MAT4161","hrs":[{"dia":2,"hi":9,"hf":11},{"dia":3,"hi":9,"hf":11},{"dia":4,"hi":9,"hf":11}]},{"cod":"MAT4161","hrs":[{"dia":2,"hi":11,"hf":13},{"dia":3,"hi":11,"hf":13},{"dia":4,"hi":11,"hf":13}]},{"cod":"MAT4161","hrs":[{"dia":2,"hi":13,"hf":15},{"dia":3,"hi":13,"hf":15},{"dia":4,"hi":13,"hf":15}]},{"cod":"MAT4161","hrs":[{"dia":2,"hi":15,"hf":17},{"dia":3,"hi":15,"hf":17},{"dia":4,"hi":15,"hf":17}]}]

var DDS = ["Sab", "Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"];
let DDS_M = {SEG: 2, TER: 3, QUA: 4, QUI: 5, SEX: 6, SAB: 7, DOM: 8};



def adicionarTurma(cod, hrs):
    materias.append({cod: cod, hrs: hrs})




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


def addHora(materia, ino):
    global possibilidades_i
    red = [x for x in materias if x["cod"] == materia]
    for i in red:
        m = i
        if(testaHorarios(m, horarios)):
            horarios.append(m)
            if(ino+1 != len(mats)):
                addHora(mats[ino+1], ino+1)
            else:
                horeste = horarios[:]
                horeste.sort(key=lambda e: e["cod"])
                if(not any(x == horeste for x in possibilidades)):
                    possibilidades.append(horeste)
                    possibilidades_i = possibilidades_i + 1
                    print(possibilidades_i)
            horarios.pop()


print(materias[0]["hrs"][0]["dia"])
print(overlap(6,7,9,6,8,10))
print(overlap(6,7,9,6,9,11))

possibilidades = []
horarios = []
mats = ["ENG4021","MAT4161"]
possibilidades_i = 0
addHora(mats[0], 0)