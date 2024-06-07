from django.urls import path
from .views import pickup_package, deliver_package, index

urlpatterns = [
    path('package/<int:package_id>/pickup/<int:store_id>/', pickup_package, name='pickup_package'),
    path('package/<int:package_id>/deliver/<int:store_id>/', deliver_package, name='deliver_package'),
    path('', index, name='index'),
]
