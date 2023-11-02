from typing import Any
from django import http
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, reverse
from .forms import CriarContaForm
from .models import Filme, Usuario
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class Homepage(TemplateView):
    template_name = "homepage.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('filme:homefilmes')
        else:
            return super().get(request, *args, **kwargs)


class Homefilmes(LoginRequiredMixin, ListView):
    template_name = "homefilmes.html"
    model = Filme


class Detalhesfilme(LoginRequiredMixin, DetailView):
    template_name = "detalhesfilme.html"
    model = Filme

    def get(self, request, *args, **kwargs):
        # Descobrir qual filme que ele está acessando
        filme = self.get_object()
        # Somar 1 nas visualizações do filme
        filme.visualizacoes += 1
        # Salvar
        filme.save()

        # Colocando filme selecionado nos filmes visualizados pelo usuário
        usuario = request.user
        usuario.filmes_vistos.add(filme)

        return super().get(request, *args, **kwargs) # Redireciona o cara para o link final

    def get_context_data(self, **kwargs):
        context =  super(Detalhesfilme, self).get_context_data(**kwargs)

        # Filtrar a tabela de filmes que tenham a mesma categoria do filme selecionado
        filmes_relacionados = Filme.objects.filter(categoria=self.get_object().categoria)[0:10]
        context['filmes_relacionados'] = filmes_relacionados
        return context


class Pesquisafilme(LoginRequiredMixin, ListView):
    template_name = "pesquisafilme.html"
    model = Filme

    # Editando object_list
    def get_queryset(self):
        pesquisa = self.request.GET.get("query")
        if pesquisa:
            object_list = self.model.objects.filter(titulo__icontains = pesquisa)
            return object_list
        else: 
            return None


class Paginaperfil(LoginRequiredMixin, UpdateView):
    template_name = "editarperfil.html"
    model = Usuario
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('filme:homefilmes')


class Criarconta(FormView):
    template_name = "criarconta.html"
    form_class = CriarContaForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('filme:login')

# def homepage(request):
#     return render(request, "homepage.html")

# def homefilmes(request):
#     context = {}
#     lista_filmes = Filme.objects.all()
#     context['lista_filmes'] = lista_filmes
#     return render(request, "homefilmes.html", context)