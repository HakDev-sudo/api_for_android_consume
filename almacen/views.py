from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Product, Category, RFID, NFC, StockMovement
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .serializer import ProductSerializer, CategorySerializer, NFCSerializer, StockMovementSerializer, RFIDSerializer 
from django.shortcuts import get_object_or_404
from rest_framework import status
import boto3
import os

# create view for the index page
# create a view for pruducts page
# create a view for the product detail page
# create a view for the cart page
# create a view for the checkout page
# create a view for the login page
# create a view for the registration page
# create a view for the profile page
# create a view dashboard page

# creating view api for to consume the api rest of the rfid
class IndexApi(APIView):
    def get(self, request):
        context = {
            'message': 'API en línea, listo para trabajar'
        }
        return Response(context)
    
# creating view api for to products of the rfid

class ProductApi(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

# creating view api for to product detail of the rfid

class ProductDetailApi(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

# creating view api for to category of the rfid

class CategoryApi(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

# creating view api for to category detail of the rfid

class CategoryDetailApi(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

# creating view api for to UID of the rfid

class UIDApi(ListCreateAPIView):
    queryset = RFID.objects.all()
    serializer_class = RFIDSerializer
    lookup_field = 'id'

# creating view api for to UID detail of the rfid

class UIDDetailApi(RetrieveUpdateDestroyAPIView):
    queryset = RFID.objects.all()
    serializer_class = RFIDSerializer
    lookup_field = 'id'

@csrf_exempt
def esp32_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rfid_uid = data.get('message')
            print(f"RFID UID recibido: {rfid_uid}")
            RFID.objects.create(id_tag=rfid_uid)
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'failed', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'}, status=400)

# Vista para listar y crear NFC
class NFCApi(ListCreateAPIView):
    queryset = NFC.objects.all()
    serializer_class = NFCSerializer
    lookup_field = 'id'

# Vista para obtener, actualizar y eliminar un NFC específico
class NFCDetailApi(RetrieveUpdateDestroyAPIView):
    queryset = NFC.objects.all()
    serializer_class = NFCSerializer
    lookup_field = 'id'

# Vista para listar y crear movimientos de stock
class StockMovementApi(ListCreateAPIView):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    lookup_field = 'id'

# Vista para obtener, actualizar y eliminar un movimiento de stock específico
class StockMovementDetailApi(RetrieveUpdateDestroyAPIView):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    lookup_field = 'id'