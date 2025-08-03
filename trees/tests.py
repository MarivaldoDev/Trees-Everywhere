from django.test import Client, TestCase
from django.urls import reverse

from .models import Account, Plant, PlantedTree, User


class TreeTestCase(TestCase):
    def setUp(self):
        # Contas
        self.acc1 = Account.objects.create(name="Conta 1")
        self.acc2 = Account.objects.create(name="Conta 2")

        # Usuários
        self.user1 = User.objects.create_user(username="user1", password="123")
        self.user2 = User.objects.create_user(username="user2", password="123")
        self.user3 = User.objects.create_user(username="user3", password="123")

        # Associação usuário-conta
        self.user1.accounts.add(self.acc1)
        self.user2.accounts.add(self.acc1)
        self.user3.accounts.add(self.acc2)

        # Planta
        self.plant = Plant.objects.create(name="Ipê")

        # Árvores plantadas
        self.tree1 = self.user1.plant_tree(self.plant, -10.0, -50.0)
        self.tree2 = self.user2.plant_tree(self.plant, -11.0, -51.0)
        self.tree3 = self.user3.plant_tree(self.plant, -12.0, -52.0)

    def login(self, username):
        self.client = Client()
        self.client.login(username=username, password="123")

    def test_my_trees_view(self):
        self.login("user1")
        response = self.client.get(reverse("trees:my_trees"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ipê")
        self.assertContains(response, "-10.0")
        self.assertNotContains(response, "-11.0")

    def test_forbidden_other_user_tree(self):
        self.login("user1")
        url = reverse("trees:tree_detail", args=[self.tree3.pk])  # árvore do usuário3
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_account_trees_view(self):
        self.login("user1")
        response = self.client.get(reverse("trees:account_trees"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "-10.0")  # user1
        self.assertContains(response, "-11.0")  # user2
        self.assertNotContains(response, "-12.0")  # user3

    def test_plant_tree_method(self):
        tree = self.user1.plant_tree(self.plant, -22.0, -47.0)
        self.assertEqual(tree.user, self.user1)
        self.assertEqual(tree.latitude, -22.0)

    def test_plant_trees_method(self):
        data = [
            (self.plant, (-1.0, -1.0)),
            (self.plant, (-2.0, -2.0)),
        ]
        trees = self.user2.plant_trees(data)
        self.assertEqual(len(trees), 2)
        self.assertEqual(trees[0].latitude, -1.0)
