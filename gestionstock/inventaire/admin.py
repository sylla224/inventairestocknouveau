from django.contrib import admin

from inventaire.models import Magasin, Enterprise, Product,Location, TypeEnterprise

admin.site.register(Magasin)
admin.site.register(Enterprise)
admin.site.register(Product)
admin.site.register(Location)
admin.site.register(TypeEnterprise)