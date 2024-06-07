from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Package, Store, Employee, Delivery
from .serializers import PackageSerializer, DeliverySerializer
from django.shortcuts import render
from .models import Delivery


def index(request):
    deliveries = Delivery.objects.all()
    return render(request, 'index.html', {'deliveries': deliveries})


@api_view(['POST'])
def pickup_package(request, package_id, store_id):
    try:
        package = Package.objects.get(id=package_id)
        store = Store.objects.get(id=store_id)
        employee = request.user.employee

        if package.store != store:
            return Response({'error': 'Package is not at this store'}, status=status.HTTP_400_BAD_REQUEST)

        delivery = Delivery.objects.create(package=package, employee=employee, from_store=store)
        return Response(DeliverySerializer(delivery).data, status=status.HTTP_201_CREATED)
    except Package.DoesNotExist:
        return Response({'error': 'Package not found'}, status=status.HTTP_404_NOT_FOUND)
    except Store.DoesNotExist:
        return Response({'error': 'Store not found'}, status=status.HTTP_404_NOT_FOUND)
    except Employee.DoesNotExist:
        return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def deliver_package(request, package_id, store_id):
    try:
        package = Package.objects.get(id=package_id)
        store = Store.objects.get(id=store_id)
        employee = request.user.employee

        delivery = Delivery.objects.filter(package=package, to_store__isnull=True).first()
        if not delivery or delivery.employee != employee:
            return Response({'error': 'No ongoing delivery found for this package'}, status=status.HTTP_400_BAD_REQUEST)

        delivery.to_store = store
        delivery.save()
        return Response(DeliverySerializer(delivery).data, status=status.HTTP_200_OK)
    except Package.DoesNotExist:
        return Response({'error': 'Package not found'}, status=status.HTTP_404_NOT_FOUND)
    except Store.DoesNotExist:
        return Response({'error': 'Store not found'}, status=status.HTTP_404_NOT_FOUND)
    except Employee.DoesNotExist:
        return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
