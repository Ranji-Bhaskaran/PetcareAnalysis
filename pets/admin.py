""" This is the Admin config for storing all the models """
from django.contrib import admin
from .models import Pet, HealthLog, ActivityLog, Product  # Import the Product model

class PetAdmin(admin.ModelAdmin):
    """ This is the admin config for Adding Pets """
    list_display = ('name', 'breed', 'age', 'weight', 'owner')
    search_fields = ('name', 'breed')
    list_filter = ('owner', 'age')

class HealthLogAdmin(admin.ModelAdmin):
    """ This is the admin config for Adding HealthLogs """
    list_display = ('pet', 'record_date', 'weight')
    search_fields = ('pet__name', 'description')
    list_filter = ('pet', 'record_date')
    ordering = ('-record_date',)

class ActivityLogAdmin(admin.ModelAdmin):
    """ This is the admin config for Adding ActivityLogs """
    list_display = ('pet', 'activity_date', 'activity_type', 'duration')
    search_fields = ('pet__name', 'activity_type')
    list_filter = ('pet', 'activity_date')
    ordering = ('-activity_date',)

class ProductAdmin(admin.ModelAdmin):
    """ This is the admin config for Adding Products """
    list_display = ('name', 'description', 'price')  # Add fields to display
    search_fields = ('name', 'description')  # Add searchable fields
    list_filter = ('name',)  # Add filters if necessary
    ordering = ('name',)  # Order by name

# Register models with their respective admin classes
admin.site.register(Pet, PetAdmin)
admin.site.register(HealthLog, HealthLogAdmin)
admin.site.register(ActivityLog, ActivityLogAdmin)
admin.site.register(Product, ProductAdmin)  # Register the Product model
