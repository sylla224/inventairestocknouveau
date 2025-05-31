from django.contrib import admin

from inventaire.models import Store, Enterprise, Product,Location, TypeEnterprise

admin.site.register(Store)
admin.site.register(Enterprise)
admin.site.register(Product)
admin.site.register(Location)
admin.site.register(TypeEnterprise)