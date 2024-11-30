from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
import uuid
import os
from django.utils.text import slugify

# Función para generar la ruta de subida de imágenes de categorías
def upload_to_category(instance, filename):
    # Obtener la extensión del archivo original
    ext = filename.split('.')[-1]

    # Crear un nombre basado en el nombre de la categoría
    filename = f"{slugify(instance.name)}-{uuid.uuid4().hex[:8]}.{ext}"

    # Guardar la imagen en la carpeta "categories_images"
    return os.path.join('categories_images', filename)

# Función para generar la ruta de subida de imágenes de usuarios
def upload_to_user(instance, filename):
    # Obtener la extensión del archivo original
    ext = filename.split('.')[-1]

    # Crear un nombre basado en el nombre del usuario
    filename = f"{slugify(instance.name)}-{uuid.uuid4().hex[:8]}.{ext}"

    # Guardar la imagen en la carpeta "users_images"
    return os.path.join('users_images', filename)

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to=upload_to_category, null=True, blank=True)

    def __str__(self):
        return self.name

class RFID(models.Model):
    id_tagr = models.CharField(max_length=50, unique=True)
    id_esp32 = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    fecha_llegada = models.DateField(null=True, blank=True)
    fecha_asignado = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.id_tagr
    

def upload_to_producto(instance, filename):
    # Obtener la extensión del archivo original
    ext = filename.split('.')[-1]
    
    # Crear un nombre basado en el nombre del producto
    filename = f"{slugify(instance.name)}-{uuid.uuid4().hex[:8]}.{ext}"
    
    # Guardar la imagen en la carpeta "imagenes"
    return os.path.join('imagenes', filename)
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to=upload_to_producto, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)  # Protege la categoría
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Llama al método `save` original para guardar el objeto y la imagen
        super().save(*args, **kwargs)

        # Redimensionar la imagen si existe
        if self.img:
            with Image.open(self.img.path) as img:
                # Convierte a modo RGB si es necesario (para evitar errores con ciertos formatos)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                # Redimensiona la imagen manteniendo la proporción
                img.thumbnail((800, 800))

                # Guarda la imagen redimensionada
                img.save(self.img.path)
    @property
    def stock(self):
        # Calcula el stock sumando las entradas y restando las salidas en los movimientos
        entradas = self.stockmovements.filter(movement_type="entrada").count()
        salidas = self.stockmovements.filter(movement_type="salida").count()
        return entradas - salidas

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    img = models.ImageField(upload_to=upload_to_user, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Transacction(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ' - ' + self.product.name
    

class NFC(models.Model):
    id_tag = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=50)
    fecha_asignado = models.DateField()
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='rfid_set')
    def __str__(self):
        return self.id_tag


# Usamos un receptor de señal para crear automáticamente un movimiento de stock tipo "entrada"
@receiver(post_save, sender=NFC)
def crear_movimiento_stock_entrada(sender, instance, created, **kwargs):
    # Solo crea una entrada si se ha asignado un producto y es una nueva asignación
    if instance.product and created:
        StockMovement.objects.create(
            product=instance.product,
            NFC_tag=instance,
            quantity=1,  # Ajustable si se asigna más de una unidad por NFC
            movement_type="entrada",
            description="Asignación automática de etiqueta NFC al producto"
        )

class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='stockmovements')
    NFC_tag = models.ForeignKey(NFC, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField()  # Cantidad de unidades afectadas
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.movement_type} - {self.product.name} - {self.quantity}'
