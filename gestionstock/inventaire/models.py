from django.db import models
from account.models import CustomUser
from django.conf import settings


"""
Il y a de l'anglais et français mélangé
Utilise le snake_case pour les attributs
"""

class TypeEnterprise(models.Model):
    nom = models.CharField(max_length=100 )

    def __str__(self):
        return self.nom


MOVEMENT_CHOICES = [
    ('1', "Vente"),
    ('2', "Location"),
]


class Enterprise(models.Model):
    nom = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    type_enterprise = models.ForeignKey(TypeEnterprise, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) # Donc une entreprise appartient à un utilisateur ok

    def __str__(self):
        return f"{self.nom}-{self.type_enterprise.nom}"

    def __repr__(self):
        return Enterprise(self.nom, self.address, self.type_enterprise)

class Store(models.Model): ## Mettre Store à la place de Magasin
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    id_number = models.CharField(max_length=50)
    entreprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)


class AccountStore(models.Model): ## Ici je ferais du coup AccountStore
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.ForeignKey("account.Role", on_delete=models.CASCADE) # ou ManyToMany s'il y a plusieurs roles possibles
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.store.nom} - {self.user.email}"


class Product(models.Model):
    sku = models.CharField("SKU", max_length=100)
    nom = models.CharField("Nom", max_length=100)
    description = models.TextField("Description")
    prix = models.IntegerField("Prix", default=0)
    seuil_alert = models.IntegerField("Alert", default=0)
    stock = models.IntegerField("Stock", default=0)

    def __str__(self):
        return f"Produit: {self.nom} de {self.sku} à un seuil alert {self.seuil_alert}"

    def __repr__(self):
        return Product(self.sku, self.nom, self.description, self.prix, self.seuil_alert)

class StoreProduct(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Location(models.Model):
    produit_location = models.ForeignKey(Product, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    # ajouter le user
    date_location = models.DateTimeField(auto_now=True)
    nom = models.CharField("Nom", max_length=100)
    users = models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name="Utilisateurs")
    adresse = models.CharField("Adresse", max_length=100)

    # type = models.CharField("Type", max_length=100)
    def __str__(self):
        return f"{self.produit_location}-{self.date_location}"


# class Stock:
#     produit_stock = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantite = models.IntegerField("Quantite", default=0)


class Mouvement(models.Model):
    type_mouvement = models.CharField(max_length=20, choices=MOVEMENT_CHOICES)
    produit = models.ForeignKey(Product, on_delete=models.CASCADE)
    lieu = models.CharField("Lieu", max_length=100)
    date_created = models.DateTimeField(auto_now=True)
    raison = models.TextField("Raison")

    def __str__(self):
        return f"{self.produit}-{self.type_mouvement}"
