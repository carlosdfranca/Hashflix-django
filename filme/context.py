from .models import Filme

#Lista de Filmes mais recentes
def lista_filmes_frequentes(request):
    lista_filmes = Filme.objects.all().order_by("-data_criacao")[0:8]
    return {"lista_filmes_recentes": lista_filmes}


# Lista de Filmes em alta
def lista_filmes_emalta(request):
    lista_filmes = Filme.objects.all().order_by("-visualizacoes")[0:8]
    return {"lista_filmes_emalta": lista_filmes}


# Filme de destaque
def filme_destaque(request):
    filmes = Filme.objects.order_by("-data_criacao")
    if filmes:
        filme = filmes[0]
    else:
        filme = None
    return {"filme_destaque": filme}