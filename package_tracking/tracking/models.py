from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import generate_qr_code
from django.conf import settings


class Store(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    qr_code = models.ImageField(upload_to='store_qr_codes/', blank=True, null=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Package(models.Model):
    description = models.CharField(max_length=255)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='package_qr_codes/', blank=True, null=True)

    def __str__(self):
        return f"Package {self.id} - {self.description}"


class Delivery(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    from_store = models.ForeignKey(Store, related_name='delivery_from', on_delete=models.CASCADE)
    to_store = models.ForeignKey(Store, related_name='delivery_to', on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delivery of {self.package} by {self.employee} from {self.from_store} to {self.to_store} at {self.timestamp}"


# Add this to Store model
@receiver(post_save, sender=Store)
def create_store_qr_code(sender, instance, created, **kwargs):
    if created:
        qr_code = generate_qr_code(f"{settings.BASE_URL}/store/{instance.id}/pickup/")
        instance.qr_code.save(f"store_{instance.id}_qr.png", qr_code)


# Add this to Package model
@receiver(post_save, sender=Package)
def create_package_qr_code(sender, instance, created, **kwargs):
    if created:
        qr_code = generate_qr_code(f"{settings.BASE_URL}/package/{instance.id}/pickup/")
        instance.qr_code.save(f"package_{instance.id}_qr.png", qr_code)
