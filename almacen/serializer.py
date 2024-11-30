from rest_framework import serializers
from .models import Product, Category, RFID, NFC, StockMovement

class ProductSerializer(serializers.ModelSerializer):
    stock = serializers.ReadOnlyField()
    class Meta:
        model = Product
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class NFCSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NFC
        fields = '__all__'

class RFIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFID
        fields = '__all__'

class StockMovementSerializer(serializers.ModelSerializer):
    # Opcional: se pueden mostrar los datos relacionados de los modelos `Product` y `NFC`
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    NFC_tag = serializers.PrimaryKeyRelatedField(queryset=NFC.objects.all(), allow_null=True)

    class Meta:
        model = StockMovement
        fields = '__all__'
