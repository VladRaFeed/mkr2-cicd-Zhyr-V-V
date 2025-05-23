from django.urls import path
from . import views

urlpatterns = [
    path('gallery/', views.gallery_view, name='gallery'),
    path('image/<int:image_id>/', views.image_detail, name='image_detail'),
]