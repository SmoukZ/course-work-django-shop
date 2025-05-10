from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('category/<slug:category_slug>', views.catalog,
         name='catalog_by_category'),
    path('products/<slug:slug>/', views.product_detail,
         name='product_detail')
    
]
