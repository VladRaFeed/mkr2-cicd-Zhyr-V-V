import pytest
from django.urls import reverse
from gallery.models import Category
from django.test import Client

@pytest.mark.django_db
def test_gallery_view_status_code(client):
    """Перевіряє, чи в’юха повертає статус 200."""
    response = client.get('/gallery/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_gallery_view_template(client):
    """Перевіряє, чи використовується правильний шаблон."""
    response = client.get('/gallery/')
    assert 'gallery.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_gallery_view_empty_categories(client):
    """Перевіряє контекст, коли категорій немає."""
    response = client.get('/gallery/')
    assert response.status_code == 200
    assert len(response.context['categories']) == 0

@pytest.mark.django_db
def test_gallery_view_with_categories(client):
    """Перевіряє контекст із кількома категоріями."""
    Category.objects.create(name="Category 1")
    Category.objects.create(name="Category 2")
    response = client.get('/gallery/')
    assert response.status_code == 200
    assert len(response.context['categories']) == 2
    assert Category.objects.get(name="Category 1") in response.context['categories']
    assert Category.objects.get(name="Category 2") in response.context['categories']

@pytest.mark.django_db
def test_gallery_view_url(client):
    """Перевіряє доступність в’юхи через URL."""
    url = reverse('gallery')  # Припускаємо, що в urls.py в’юха прив’язана до імені 'gallery'
    response = client.get(url)
    assert response.status_code == 200
    assert 'gallery.html' in [t.name for t in response.templates]