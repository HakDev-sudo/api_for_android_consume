from django.urls import path
from .views import esp32_data
from . import views


urlpatterns = [
    #para recibir los datos del esp32
    path('api/rfid', esp32_data, name='rfid_receive'),

    # Esta url es para consumir la api rest
    path('api/', views.IndexApi.as_view(), name='api'),
    # for product
    path('api/productos', views.ProductApi.as_view(), name='api-productos'),
    path('api/producto/<int:id>', views.ProductDetailApi.as_view(), name='api-producto'),

    # for categories

    path('api/categorias', views.CategoryApi.as_view(), name='api-categorias'),
    path('api/categoria/<int:id>', views.CategoryDetailApi.as_view(), name="api-categoria"),

    # for UID RFID
    path('api/uid', views.UIDApi.as_view(), name='api-uid'),
    path('api/uid/<int:id>', views.UIDDetailApi.as_view(), name='api-uid-detail'),
    
    # Rutas para NFC
    path('api/nfc', views.NFCApi.as_view(), name='api-nfc'),
    path('api/nfc/<int:id>', views.NFCDetailApi.as_view(), name='api-nfc-detail'),

    # Rutas para movimientos de stock
    path('api/stockmovements', views.StockMovementApi.as_view(), name='api-stockmovements'),
    path('api/stockmovement/<int:id>', views.StockMovementDetailApi.as_view(), name='api-stockmovement-detail'),

]