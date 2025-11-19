from django.shortcuts import render, redirect
from django.urls import reverse

DDS = ["Sab", "Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"];
DDS_M = {"SEG": 2, "TER": 3, "QUA": 4, "QUI": 5, "SEX": 6, "SAB": 7, "DOM": 8};

turmas = []

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
        'turmas': turmas                # os resultados da pesquisa
    }
    

    return render(request, 'MatriculAI/matricula.html', contexto)

def addTurma(request):
    cod = request.POST.get('cod')
    cod = cod.upper()
    pesquisar = request.POST.get('pesquisar')

    if(not cod==''):
        if(pesquisar=='pesquisar'):
            #pesquisa no DB da PUC
            turmas.append({"cod": cod, "hrtxt": "pesquisei!"})
        else:
            #le os quadradinhos
            horas_sel = []
            for key, value in request.POST.items():
                if(value == 'on'):
                    print(key)
                    celulaclick(int(key.split("/")[0]),int(key.split("/")[1]), horas_sel)
            turmas.append({"cod": cod, "hrtxt": traduzirTexto(horas_sel)})
    return redirect(reverse('matricula'))

def celulaclick(dia, hora, horas_sel):
    horas_sel.append({"dia": dia, "hora": hora})

def traduzirTexto(horas_sel):
    tex = ""
    for d in range(2,7):
        ant_sel = False;
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

def estaSelecionado(dia, hora, horas_sel):
    return any(x == {"dia": dia, "hora": hora} for x in horas_sel)