import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from gallery.models import Category, Image
from django.test import Client
import datetime

@pytest.mark.django_db
def test_gallery_view_status_code(client):
    """Перевіряє, чи в’юха gallery_view повертає статус 200."""
    response = client.get('/gallery/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_gallery_view_template(client):
    """Перевіряє, чи в’юха gallery_view використовує правильний шаблон."""
    response = client.get('/gallery/')
    assert 'gallery.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_gallery_view_empty_categories(client):
    """Перевіряє контекст gallery_view, коли категорій немає."""
    response = client.get('/gallery/')
    assert response.status_code == 200
    assert len(response.context['categories']) == 0

@pytest.mark.django_db
def test_gallery_view_with_categories(client):
    """Перевіряє контекст gallery_view із кількома категоріями."""
    Category.objects.create(name="Category 1")
    Category.objects.create(name="Category 2")
    response = client.get('/gallery/')
    assert response.status_code == 200
    assert len(response.context['categories']) == 2
    assert Category.objects.get(name="Category 1") in response.context['categories']
    assert Category.objects.get(name="Category 2") in response.context['categories']

@pytest.mark.django_db
def test_gallery_view_url(client):
    """Перевіряє доступність gallery_view через URL."""
    url = reverse('gallery')
    response = client.get(url)
    assert response.status_code == 200
    assert 'gallery.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_image_detail_status_code(client):
    """Перевіряє, чи в’юха image_detail повертає статус 200 для існуючого зображення."""
    image = Image.objects.create(
        title="Test Image",
        image=SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
        created_date=datetime.date(2025, 5, 23),
        age_limit=18
    )
    response = client.get(f'/image/{image.id}/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_image_detail_template(client):
    """Перевіряє, чи в’юха image_detail використовує правильний шаблон."""
    image = Image.objects.create(
        title="Test Image",
        image=SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
        created_date=datetime.date(2025, 5, 23),
        age_limit=18
    )
    response = client.get(f'/image/{image.id}/')
    assert 'image_detail.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_image_detail_context(client):
    """Перевіряє, чи в’юха image_detail передає правильний об’єкт зображення в контекст."""
    image = Image.objects.create(
        title="Test Image",
        image=SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
        created_date=datetime.date(2025, 5, 23),
        age_limit=18
    )
    response = client.get(f'/image/{image.id}/')
    assert response.status_code == 200
    assert response.context['image'] == image
    assert response.context['image'].title == "Test Image"

@pytest.mark.django_db
def test_image_detail_not_found(client):
    """Перевіряє, чи в’юха image_detail повертає 404 для неіснуючого зображення."""
    response = client.get('/image/999/')
    assert response.status_code == 404

@pytest.mark.django_db
def test_image_detail_url(client):
    """Перевіряє доступність в’юхи image_detail через URL."""
    image = Image.objects.create(
        title="Test Image",
        image=SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
        created_date=datetime.date(2025, 5, 23),
        age_limit=18
    )
    url = reverse('image_detail', args=[image.id])
    response = client.get(url)
    assert response.status_code == 200
    assert 'image_detail.html' in [t.name for t in response.templates]