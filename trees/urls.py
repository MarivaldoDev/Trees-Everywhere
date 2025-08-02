from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'trees'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='trees/login.html'), name='login'),
    path('my-trees/', views.MyTreesView.as_view(), name='my_trees'),
    path('add-tree/', views.AddTreeView.as_view(), name='add_tree'),
    path('tree/<int:pk>/', views.TreeDetailView.as_view(), name='tree_detail'),
    path('account-trees/', views.AccountTreesView.as_view(), name='account_trees'),
    path('api/my-trees/', views.UserPlantedTreesAPI.as_view(), name='api_my_trees'),
]

