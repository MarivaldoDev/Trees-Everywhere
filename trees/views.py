from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .forms import PlantedTreeForm
from .models import PlantedTree, User


class MyTreesView(LoginRequiredMixin, ListView):
    model = PlantedTree
    template_name = "trees/my_trees.html"
    context_object_name = "trees"

    def get_queryset(self):
        return PlantedTree.objects.filter(user=self.request.user)


class AddTreeView(LoginRequiredMixin, CreateView):
    model = PlantedTree
    form_class = PlantedTreeForm
    template_name = "trees/add_tree.html"
    success_url = reverse_lazy("trees:my_trees")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TreeDetailView(LoginRequiredMixin, DetailView):
    model = PlantedTree
    template_name = "trees/tree_detail.html"
    context_object_name = "tree"

    def dispatch(self, request, *args, **kwargs):
        tree = self.get_object()
        if tree.user != request.user:
            return HttpResponseForbidden("Você não pode ver essa árvore.")
        return super().dispatch(request, *args, **kwargs)


class AccountTreesView(LoginRequiredMixin, ListView):
    model = PlantedTree
    template_name = "trees/account_trees.html"
    context_object_name = "trees"

    def get_queryset(self):
        user_accounts = self.request.user.accounts.all()
        related_users_ids = User.objects.filter(accounts__in=user_accounts).values_list(
            "id", flat=True
        )
        return PlantedTree.objects.filter(user__id__in=related_users_ids)


class UserPlantedTreesAPI(LoginRequiredMixin, View):
    def get(self, request):
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
