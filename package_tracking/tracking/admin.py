from django.contrib import admin
from .models import Store, Employee, Package, Delivery

admin.site.register(Store)
admin.site.register(Employee)
admin.site.register(Package)
admin.site.register(Delivery)
