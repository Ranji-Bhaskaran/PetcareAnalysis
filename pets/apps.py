""" Config for Pets-App"""
from django.apps import AppConfig

class PetsConfig(AppConfig):
    """ App attributes and defaults are configured here """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pets'
