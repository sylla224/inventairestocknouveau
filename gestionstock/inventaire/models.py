from django.db import models
from account.models import EnterpriseUser
from django.conf import settings




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
    User = models.ForeignKey(EnterpriseUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom}-{self.type_enterprise.nom}"

    def __repr__(self):
        return Enterprise(self.nom, self.address, self.type_enterprise)

class Magasin(models.Model):
    nom = models.CharField(max_length=100)
    addresse = models.CharField(max_length=200)
    idnumber = models.CharField(max_length=50)
    entrepriseId = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    adminMagsin = models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name="Utilisateurs")


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
        return Product(self.SKU, self.nom, self.description, self.prix, self.seuil_alert)

class MagasinProduit(models.Model):
    magasinId = models.ForeignKey(Magasin, on_delete=models.CASCADE)
    produitId = models.ForeignKey(Product, on_delete=models.CASCADE)

class Location(models.Model):
    produit_location = models.ForeignKey(Product, on_delete=models.CASCADE)
    magasinId = models.ForeignKey(Magasin, on_delete=models.CASCADE)
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
    datecreated = models.DateTimeField(auto_now=True)
    raison = models.TextField("Raison")

    def __str__(self):
        return f"{self.produit}-{self.type_mouvement}"
