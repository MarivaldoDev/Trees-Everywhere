from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .forms import PlantedTreeForm
from .models import PlantedTree, User


def home(request):
    return render(request, "trees/home.html")


class MyTreesView(LoginRequiredMixin, ListView):
    """Mostra uma lista de árvores plantadas pelo usuário autenticado."""

    model = PlantedTree
    template_name = "trees/my_trees.html"
    context_object_name = "trees"

    def get_queryset(self):
        """Filtra as árvores apenas do usuário logado."""
        return PlantedTree.objects.filter(user=self.request.user)

    def handle_no_permission(self):
        return redirect("trees:login")


class AddTreeView(LoginRequiredMixin, CreateView):
    """Permite que o usuário adicione uma nova árvore."""

    model = PlantedTree
    form_class = PlantedTreeForm
    template_name = "trees/add_tree.html"
    success_url = reverse_lazy("trees:my_trees")

    def form_valid(self, form):
        """Antes de salvar o formulário, associa o usuário logado à árvore."""
        form.instance.user = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        return redirect("trees:login")


class TreeDetailView(LoginRequiredMixin, DetailView):
    """A árvore deve pertencer ao usuário logado."""

    model = PlantedTree
    template_name = "trees/tree_detail.html"
    context_object_name = "tree"

    def dispatch(self, request, *args, **kwargs):
        """Verifica se a árvore pertence ao usuário. Se não, retorna um erro 403 (Forbidden)."""
        tree = self.get_object()
        if tree.user != request.user:
            return HttpResponseForbidden("Você não pode ver essa árvore.")
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return redirect("trees:login")


class AccountTreesView(LoginRequiredMixin, ListView):
    """Mostra as árvores plantadas por usuários de contas relacionadas.
    Pode ser usada quando um usuário tem acesso a várias contas (ex: administrador de contas múltiplas).
    """

    model = PlantedTree
    template_name = "trees/account_trees.html"
    context_object_name = "trees"

    def get_queryset(self):
        """Recupera IDs de usuários relacionados por conta. Retorna árvores plantadas por esses usuários."""
        user_accounts = self.request.user.accounts.all()
        related_users_ids = User.objects.filter(accounts__in=user_accounts).values_list(
            "id", flat=True
        )
        return PlantedTree.objects.filter(user__id__in=related_users_ids)

    def handle_no_permission(self):
        return redirect("trees:login")


class UserPlantedTreesAPI(LoginRequiredMixin, View):
    """Retorna uma lista de árvores do usuário em formato JSON. View do tipo API, não usa templates."""

    def get(self, request):
        """Serializa os dados da árvore (espécie, localização e data) para JSON."""
        trees = PlantedTree.objects.filter(user=request.user)
        data = [
            {
                "plant": tree.plant.name,
                "latitude": float(tree.latitude),
                "longitude": float(tree.longitude),
                "planted_at": tree.planted_at.isoformat(),
            }
            for tree in trees
        ]
        return JsonResponse(data, safe=False)

    def handle_no_permission(self):
        return redirect("trees:login")
