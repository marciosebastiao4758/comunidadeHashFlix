from django.shortcuts import render, reverse, redirect
from .models import Filme, Usuario
from .forms import CriarContaForm, FormHomePage
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
# def homepage(request):
#     return render(request, "homepage.html")

# Create your views here.
class Homepage(FormView):
    template_name = "homepage.html"
    form_class = FormHomePage

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated: #usuario esta autenticado:
            # redireciona para a homefilmes
            return redirect('filme:homefilmes')
        else:
            return super().get(request, *args, **kwargs) # redireciona para a homepage

        def get_success_url(self):
            email = self.request.GET.get("email")
            usuarios = Usuario.objects.filter(email=email)
            if usuarios:
                return reverse("filme:login")
            else:
                return reverse("filme:criarconta")

# urls - views - html
# def homefilmes(request):
#     context = {}
#     lista_filmes = Filme.objects.all()
#     context["lista_filmes"] = lista_filmes
#     return render(request, "homefilmes.html", context)

class Homefilmes(LoginRequiredMixin, ListView):
    template_name = "homefilmes.html"
    model = Filme
    # object_list -> lista de filmes  do modelo

class Detalhesfilme(LoginRequiredMixin, DetailView):
    template_name = "detalhesfilme.html"
    model = Filme
    # object -> um item do nosso modelo

    def get(self,request, *args, **kwargs):
        # descobrir qual filme ele está acessando
        filme = self.get_object()
        # somar 1 nas visulizações daquele filme
        filme.vizualizacoes += 1
        # salvar
        filme.save()
        usuario = request.user
        usuario.filmes_vistos.add(filme)
        return super().get(request, *args, **kwargs) # Redireciona o usuário para a url final

    def get_context_data(self, **kwargs):
        context = super(Detalhesfilme, self).get_context_data(**kwargs)
        filmes_relacionados = Filme.objects.filter(categoria=self.get_object().categoria)[0:5]
        context["filmes_relacionados"] = filmes_relacionados
        return context

class PesquisaFilme(LoginRequiredMixin, ListView):
    template_name = "pesquisa.html"
    model = Filme

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get("query")
        if termo_pesquisa:
            object_list = self.model.objects.filter(titulo__icontains=termo_pesquisa)
            return object_list
        else:
            return None


class Paginaperfil(LoginRequiredMixin, UpdateView):
    template_name = "editarperfil.html"
    model = Usuario
    fields = ["first_name", "last_name", "email"]

    def get_success_url(self):
        return reverse("filme:homefilmes")


class Criarconta(FormView):
    template_name = "criarconta.html"
    form_class = CriarContaForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("filme:login")





