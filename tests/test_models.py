"""Testing models using pytest"""
import pytest
from django.contrib.auth.models import User
from datetime import date
from pets.models import Pet, HealthLog, ActivityLog, Product, Contact

@pytest.fixture
def user():
    """Fixture for creating a test user"""
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def pet(user):
    """Fixture for creating a test pet"""
    return Pet.objects.create(owner=user, name='Buddy', breed='Golden Retriever', age=3, weight=30)

@pytest.mark.django_db
def test_pet_model(user):
    """Test creating and retrieving a Pet instance"""
    pet = Pet.objects.create(owner=user, name='Buddy', breed='Golden Retriever', age=3, weight=30)
    assert str(pet) == 'Buddy'
    assert pet.owner == user
    assert pet.age == 3
    assert pet.weight == 30

@pytest.mark.django_db
def test_health_log_model(pet):
    """Test creating and retrieving a HealthLog instance"""
    health_log = HealthLog.objects.create(
        pet=pet, record_date=date.today(), weight=30, rabies='yes', deworming='no'
    )
    assert str(health_log) == f"Health Log for {pet.name} on {health_log.record_date}"
    assert health_log.rabies == 'yes'
    assert health_log.deworming == 'no'

@pytest.mark.django_db
def test_activity_log_model(pet):
    """Test creating and retrieving an ActivityLog instance"""
    activity_log = ActivityLog.objects.create(
        pet=pet, activity_date=date.today(), activity_type='walk', duration=30
    )
    assert str(activity_log) == f"{pet.name} - walk"
    assert activity_log.duration == 30

@pytest.mark.django_db
def test_product_model():
    """Test creating and retrieving a Product instance"""
    product = Product.objects.create(
        name='Pet Collar', description='A durable collar for pets.', price=15
    )
    assert str(product) == 'Pet Collar'
    assert product.price == 15

@pytest.mark.django_db
def test_contact_model():
    """Test creating and retrieving a Contact instance"""
    contact = Contact.objects.create(
        name='John Doe', email='johndoe@example.com', subject='Inquiry', message='Need more info about pet food.'
    )
    assert str(contact) == 'John Doe - Inquiry'
    assert contact.email == 'johndoe@example.com'
    assert contact.subject == 'Inquiry'
