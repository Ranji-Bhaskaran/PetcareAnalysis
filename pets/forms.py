""" Forms file """
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import (
    MinLengthValidator,
    RegexValidator,
    MinValueValidator,
    MaxValueValidator)
from .models import Pet, HealthLog, ActivityLog, ACTIVITY_CHOICES, Product

# Define the constants for the regex pattern and messages
ALPHABETIC_SPACE_REGEX = r'^[a-zA-Z ]+$'
VALID_NAME_MESSAGE = "Enter a valid name"
POSITIVE_WEIGHT_MESSAGE = "Weight must be positive"

class CustomUserCreationForm(UserCreationForm):
    """ Custom Register form """
    email = forms.EmailField(
        required=True,
        validators=[RegexValidator(r'^[\w\.-]+@[\w\.-]+\.\w+$',
        message="Enter a valid email address")]
    )

    class Meta:
        """ fields for register form """
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    """Custom login form """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        validators=[MinLengthValidator(3)]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        validators=[MinLengthValidator(8)]
    )

class ProductForm(forms.ModelForm):
    """ Custom Product form for accessories """
    class Meta:
        """ Fields for product form """
        model = Product
        fields = ['name', 'description', 'price', 'image']
        widgets = {
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }
    name = forms.CharField(
        validators=[MinLengthValidator(2),
        RegexValidator(ALPHABETIC_SPACE_REGEX, message="Enter a valid product name")]
    )
    description = forms.CharField(
        validators=[MinLengthValidator(10)]
    )
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01, message="Price must be at least 0.01")]
    )

class AddPetForm(forms.ModelForm):
    """Form for adding a new pet"""
    class Meta:
        """ Fields for adding pet form """
        model = Pet
        fields = ['name', 'breed', 'age', 'weight', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Pet Name'}),
            'breed': forms.TextInput(attrs={'placeholder': 'Breed'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Age'}),
            'weight': forms.NumberInput(attrs={'placeholder': 'Weight (kg)'}),
            'image': forms.ClearableFileInput(),
        }
    name = forms.CharField(
        validators=[MinLengthValidator(2),
        RegexValidator(ALPHABETIC_SPACE_REGEX, message=VALID_NAME_MESSAGE)]
    )
    breed = forms.CharField(
        validators=[MinLengthValidator(3)]
    )
    age = forms.IntegerField(
        validators=[MinValueValidator(0),
        MaxValueValidator(30, message="Enter a realistic age for a pet")]
    )
    weight = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.1, message=POSITIVE_WEIGHT_MESSAGE)]
    )

class EditPetForm(forms.ModelForm):
    """Form for editing an existing pet"""
    class Meta:
        """ Fields for edit pet form """
        model = Pet
        fields = ['name', 'breed', 'age', 'weight']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Pet Name'}),
            'breed': forms.TextInput(attrs={'placeholder': 'Breed'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Age'}),
            'weight': forms.NumberInput(attrs={'placeholder': 'Weight (kg)'}),
        }
    name = forms.CharField(
        validators=[MinLengthValidator(2),
        RegexValidator(ALPHABETIC_SPACE_REGEX, message=VALID_NAME_MESSAGE)]
    )
    breed = forms.CharField(
        validators=[MinLengthValidator(3)]
    )
    age = forms.IntegerField(
        validators=[MinValueValidator(0),
        MaxValueValidator(30, message="Enter a realistic age for a pet")]
    )
    weight = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.1, message=POSITIVE_WEIGHT_MESSAGE)]
    )

class HealthLogForm(forms.ModelForm):
    """Form for recording health logs of pets"""
    class Meta:
        """ Fields for health log """
        model = HealthLog
        fields = ['record_date', 'weight', 'rabies', 'deworming']
        widgets = {
            'record_date': forms.DateInput(attrs={'type': 'date'}),
            'weight': forms.NumberInput(attrs={'placeholder': 'Weight (kg)'}),
            'rabies': forms.Select(
                choices=[('yes', 'Yes'),
                ('no', 'No')],
                attrs={'placeholder': 'Rabies Vaccination'}),
            'deworming': forms.Select(
                choices=[('yes', 'Yes'),
                ('no', 'No')],
                attrs={'placeholder': 'De-worming Tablet'}),
        }
    weight = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.1, message=POSITIVE_WEIGHT_MESSAGE)]
    )

class ActivityLogForm(forms.ModelForm):
    """Form for recording activity logs of pets"""
    class Meta:
        """ FIelds for activity log """
        model = ActivityLog
        fields = ['activity_date', 'activity_type', 'duration']
        widgets = {
            'activity_date': forms.DateInput(attrs={'type': 'date'}),
            'activity_type': forms.Select(choices=ACTIVITY_CHOICES),
            'duration': forms.NumberInput(attrs={'placeholder': 'Duration (minutes)'}),
        }
    duration = forms.IntegerField(
        validators=[MinValueValidator(1, message="Duration must be at least 1 minute")]
    )

class ContactForm(forms.Form):
    """Form for contact messages"""
    name = forms.CharField(
        max_length=100,
        validators=[RegexValidator(ALPHABETIC_SPACE_REGEX, message=VALID_NAME_MESSAGE)],
        widget=forms.TextInput(attrs={'placeholder': 'Your Name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}),
        validators=[RegexValidator(r'^[\w\.-]+@[\w\.-]+\.\w+$',
        message="Enter a valid email address")]
    )
    subject = forms.CharField(
        max_length=200,
        validators=[MinLengthValidator(5, message="Subject should be descriptive")],
        widget=forms.TextInput(attrs={'placeholder': 'Subject'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Your Message'}),
        validators=[MinLengthValidator(10, message="Message should be at least 10 characters")]
    )
