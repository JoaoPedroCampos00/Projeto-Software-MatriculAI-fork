from django.shortcuts import render, redirect
from django.urls import reverse
from MatriculAI.pensar import celulaclick, traduzirTexto, estaSelecionado, buscarMat, renderTabela, testaPossibilidades, gethrs

DDS = ["Sab", "Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"];
DDS_M = {"SEG": 2, "TER": 3, "QUA": 4, "QUI": 5, "SEX": 6, "SAB": 7, "DOM": 8};

turmas = []
horarios = []
horarios_i = 0
result = ["<td>07-08</td>"+"<td></td>"*5,
       "<td>08-09</td>"+"<td></td>"*5,
       "<td>09-10</td>"+"<td></td>"*5,
       "<td>10-11</td>"+"<td></td>"*5,
       "<td>11-12</td>"+"<td></td>"*5,
       "<td>12-13</td>"+"<td></td>"*5,
       "<td>13-14</td>"+"<td></td>"*5,
       "<td>14-15</td>"+"<td></td>"*5,
       "<td>15-16</td>"+"<td></td>"*5,
       "<td>16-17</td>"+"<td></td>"*5]
pag = 1
tot = 1

def home(request):
    '''
    View function for home page of site.
    Renders the home.html template.
    '''
    return render(request, 'MatriculAI/home.html')

def paginaDuvidas(request):

    return render(request, 'MatriculAI/pagina-duvidas.html')

def paginaLogin(request):

    return render(request, 'MatriculAI/login.html')

def paginaCadastro(request):

    return render(request, 'MatriculAI/criarConta.html')

def matricula(request):

    contexto = {
        'turmas': turmas,                # os resultados da pesquisa
        'res': result,
        'pag': pag,
        'tot': tot,
        'en':  "" if tot > 1 else "disabled"
    }
    
    return render(request, 'MatriculAI/matricula.html', contexto)

def addTurma(request):
    cod = request.POST.get('cod')
    cod = cod.upper()
    pesquisar = request.POST.get('pesquisar')

    if(not cod==''):
        if(pesquisar=='pesquisar'):
            #pesquisa no DB da PUC
            res = buscarMat(cod)
            for r in res:
                turmas.append(r)

        else:
            #le os quadradinhos
            horas_sel = []
            for key, value in request.POST.items():
                if(value == 'on'):
                    print(key)
                    celulaclick(int(key.split("/")[0]),int(key.split("/")[1]), horas_sel)
            hrs = gethrs(horas_sel)
            turmas.append({"cod": cod, "hrs": hrs, "hrtxt": traduzirTexto(horas_sel)})
    return redirect(reverse('matricula'))

def testarPossibilidades(request):
    
    horario = [{"cod": "ENG4021", "hrs": [{"dia": 5, "hi": 9, "hf": 11},{"dia": 6, "hi": 7, "hf": 9}] }]
    global horarios
    global horarios_i
    mats = [x["cod"] for x in turmas]
    mats = list(set(mats))
    horarios = testaPossibilidades(mats,turmas)
    horarios_i = 0

    return proxTabela(request)

def proxTabela(request):

    i = request.POST.get("pg")
    if(not i):
        i = 0
    else:
        i = int(i)

    global result
    global horarios
    global horarios_i
    horarios_i = (horarios_i+i)%len(horarios)
    result = renderTabela(horarios[horarios_i])
    print(result)
    global pag
    global tot
    pag = horarios_i+1
    tot = len(horarios)
    print(horarios[horarios_i])
    return redirect(reverse('matricula')+'#cont_tab')