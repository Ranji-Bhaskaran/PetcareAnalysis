"""Testing views using pytest"""
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from pets.models import Pet, Product, ActivityLog
from django.utils.timezone import now
from decimal import Decimal

@pytest.mark.django_db
def test_home_view(client):
    """Test rendering of the home page."""
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'pets/home.html' in [template.name for template in response.templates]

@pytest.mark.django_db
def test_register_view(client):
    """Test user registration view."""
    response = client.post(reverse('register'), {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password1': 'strongpassword123',
        'password2': 'strongpassword123',
    })
    assert response.status_code == 302
    assert User.objects.filter(username='newuser').exists()

@pytest.mark.django_db
def test_login_view(client, django_user_model):
    """Test user login view."""
    user = django_user_model.objects.create_user(username='testuser', password='strongpassword123')
    response = client.post(reverse('login'), {'username': 'testuser', 'password': 'strongpassword123'})
    assert response.status_code == 302
    assert response.url == reverse('pet_list')

@pytest.mark.django_db
def test_logout_view(client, django_user_model):
    """Test user logout view."""
    user = django_user_model.objects.create_user(username='testuser', password='strongpassword123')
    client.login(username='testuser', password='strongpassword123')
    response = client.get(reverse('logout'))
    assert response.status_code == 302
    assert response.url == reverse('home')

@pytest.mark.django_db
def test_pet_list_view(client, django_user_model):
    """Test pet list view."""
    user = django_user_model.objects.create_user(username='testuser', password='password')
    pet = Pet.objects.create(owner=user, name="Buddy", breed="Labrador", age=5, weight=25.0)
    client.login(username='testuser', password='password')
    response = client.get(reverse('pet_list'))
    assert response.status_code == 200
    assert pet.name in response.content.decode()

@pytest.mark.django_db
def test_add_pet_view(client, django_user_model):
    """Test adding a new pet."""
    user = django_user_model.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')
    response = client.post(reverse('add_pet'), {
        'name': 'Buddy',
        'breed': 'Labrador',
        'age': 5,
        'weight': 25.0,
    })
    assert response.status_code == 302
    assert Pet.objects.filter(name='Buddy').exists()

@pytest.mark.django_db
def test_edit_pet_view(client, django_user_model):
    """Test editing an existing pet."""
    user = django_user_model.objects.create_user(username='testuser', password='password')
    pet = Pet.objects.create(owner=user, name="Buddy", breed="Labrador", age=5, weight=25.0)
    client.login(username='testuser', password='password')
    response = client.post(reverse('edit_pet', args=[pet.id]), {
        'name': 'Buddy Updated',
        'breed': 'Golden Retriever',
        'age': 6,
        'weight': 30.0,
    })
    assert response.status_code == 302
    pet.refresh_from_db()
    assert pet.name == 'Buddy Updated'

@pytest.mark.django_db
def test_delete_pet_view(client, django_user_model):
    """Test deleting an existing pet."""
    user = django_user_model.objects.create_user(username='testuser', password='password')
    pet = Pet.objects.create(owner=user, name="Buddy", breed="Labrador", age=5, weight=25.0)
    client.login(username='testuser', password='password')
    response = client.post(reverse('delete_pet', args=[pet.id]))
    assert response.status_code == 302
    assert not Pet.objects.filter(id=pet.id).exists()

@pytest.mark.django_db
def test_products_view(client, django_user_model):
    """Test viewing products."""
    user = django_user_model.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')

    product = Product.objects.create(name="Dog Food", description="Healthy dog food", price=Decimal('25.50'))

    response = client.get(reverse('products'))
    assert response.status_code == 200
    assert product.name in response.content.decode()
@pytest.mark.django_db
def test_cart_view(client):
    """Test viewing the cart."""
    product = Product.objects.create(name='Dog Food', description="Healthy dog food", price=Decimal('25.50'))
    session = client.session
    session['cart'] = [product.id]
    session.save()
    response = client.get(reverse('cart'))
    assert response.status_code == 200
    assert product.name in response.content.decode()

@pytest.mark.django_db
def test_add_to_cart_view(client):
    """Test adding a product to the cart."""
    product = Product.objects.create(name="Dog Food", description="Healthy dog food", price=Decimal('25.50'))
    response = client.get(reverse('add_to_cart', args=[product.id]))
    assert response.status_code == 302
    assert client.session['cart'] == [product.id]

@pytest.mark.django_db
def test_remove_from_cart_view(client):
    """Test removing a product from the cart."""
    product = Product.objects.create(name="Dog Food", description="Healthy dog food", price=Decimal('25.50'))
    session = client.session
    session['cart'] = [product.id]
    session.save()
    response = client.get(reverse('remove_from_cart', args=[product.id]))
    assert response.status_code == 302
    assert product.id not in client.session['cart']

@pytest.mark.django_db
def test_checkout_view(client, django_user_model):
    """Test checkout view."""
    user = django_user_model.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')

    product = Product.objects.create(name='Dog Food', description="Healthy dog food", price=Decimal('25.50'))
    session = client.session
    session['cart'] = [product.id]
    session.save()
    response = client.get(reverse('checkout'))
    assert response.status_code == 200
    assert '25.50' in response.content.decode()