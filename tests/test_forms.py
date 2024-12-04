"""Testing forms using pytest"""
import pytest
from django.contrib.auth.models import User
from pets.forms import (
    CustomUserCreationForm, LoginForm, ProductForm, AddPetForm,
    EditPetForm, HealthLogForm, ActivityLogForm, ContactForm
)

@pytest.mark.django_db
def test_custom_user_creation_form_valid_data():
    """Test CustomUserCreationForm with valid data"""
    form = CustomUserCreationForm(data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password1': 'strongpassword123',
        'password2': 'strongpassword123',
    })
    assert form.is_valid()

@pytest.mark.django_db
def test_custom_user_creation_form_invalid_email():
    """Test CustomUserCreationForm with invalid email"""
    form = CustomUserCreationForm(data={
        'username': 'testuser',
        'email': 'invalid-email',
        'password1': 'strongpassword123',
        'password2': 'strongpassword123',
    })
    assert not form.is_valid()

@pytest.mark.django_db
def test_login_form_valid_data():
    """Test LoginForm with valid data"""
    User.objects.create_user(username='testuser', password='strongpassword123')
    form = LoginForm(data={'username': 'testuser', 'password': 'strongpassword123'})
    assert form.is_valid()

@pytest.mark.django_db
def test_login_form_invalid_data():
    """Test LoginForm with invalid data"""
    form = LoginForm(data={'username': 'testuser', 'password': 'wrongpassword'})
    assert not form.is_valid()

@pytest.mark.django_db
def test_product_form_valid_data():
    """Test ProductForm with valid data"""
    form = ProductForm(data={
        'name': 'Test Product',
        'description': 'A great product for pets.',
        'price': '10.99',
    })
    assert form.is_valid()

@pytest.mark.django_db
def test_product_form_invalid_price():
    """Test ProductForm with invalid price"""
    form = ProductForm(data={
        'name': 'Test Product',
        'description': 'A great product for pets.',
        'price': '-5.00',
    })
    assert not form.is_valid()

@pytest.mark.django_db
def test_add_pet_form_valid_data():
    """Test AddPetForm with valid data"""
    form = AddPetForm(data={
        'name': 'Buddy',
        'breed': 'Labrador',
        'age': 3,
        'weight': 20.5,
    })
    assert form.is_valid()

@pytest.mark.django_db
def test_add_pet_form_invalid_data():
    """Test AddPetForm with invalid data"""
    form = AddPetForm(data={
        'name': '',
        'breed': 'Labrador',
        'age': -1,
        'weight': -5.0,
    })
    assert not form.is_valid()

@pytest.mark.django_db
def test_edit_pet_form_valid_data():
    """Test EditPetForm with valid data"""
    form = EditPetForm(data={
        'name': 'Max',
        'breed': 'Beagle',
        'age': 5,
        'weight': 15.5,
    })
    assert form.is_valid()

@pytest.mark.django_db
def test_edit_pet_form_invalid_weight():
    """Test EditPetForm with invalid weight"""
    form = EditPetForm(data={
        'name': 'Max',
        'breed': 'Beagle',
        'age': 5,
        'weight': -10.0,
    })
    assert not form.is_valid()

@pytest.mark.django_db
def test_health_log_form_valid_data():
    """Test HealthLogForm with valid data"""
    form = HealthLogForm(data={
        'record_date': '2023-12-03',
        'weight': 25.5,
        'rabies': 'yes',
        'deworming': 'no',
    })
    assert form.is_valid()

@pytest.mark.django_db
def test_health_log_form_invalid_weight():
    """Test HealthLogForm with invalid weight"""
    form = HealthLogForm(data={
        'record_date': '2023-12-03',
        'weight': -3.0,
        'rabies': 'yes',
        'deworming': 'no',
    })
    assert not form.is_valid()

@pytest.mark.django_db
def test_activity_log_form_valid_data():
    """Test ActivityLogForm with valid data"""
    form = ActivityLogForm(data={
        'activity_date': '2023-12-03',
        'activity_type': 'walk',
        'duration': 30,
    })
    assert form.is_valid()

@pytest.mark.django_db
def test_activity_log_form_invalid_duration():
    """Test ActivityLogForm with invalid duration"""
    form = ActivityLogForm(data={
        'activity_date': '2023-12-03',
        'activity_type': 'play',
        'duration': 0,
    })
    assert not form.is_valid()

def test_contact_form_valid_data():
    """Test ContactForm with valid data"""
    form = ContactForm(data={
        'name': 'John Doe',
        'email': 'johndoe@example.com',
        'subject': 'Inquiry',
        'message': 'I would like to know more about your services.',
    })
    assert form.is_valid()

def test_contact_form_invalid_email():
    """Test ContactForm with invalid email"""
    form = ContactForm(data={
        'name': 'John Doe',
        'email': 'invalid-email',
        'subject': 'Inquiry',
        'message': 'I would like to know more about your services.',
    })
    assert not form.is_valid()
