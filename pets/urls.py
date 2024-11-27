""" Urls for routing to specific pages with views """
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_pet/', views.add_pet, name='add_pet'),  # Add a new pet
    #Health log Url
    path('add_health_log/<int:pet_id>/', views.add_health_log, name='add_health_log'),
    #Activity log Url
    path('add_activity_log/<int:pet_id>/', views.add_activity_log, name='add_activity_log'),
    path('global/', views.global_view, name='global'),
    path('pets/', views.pet_list, name='pet_list'),  # List of all pets
    # pet products --------------------------------------------------------
    path('products/', views.products, name='products'),
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    #-----------------------------------------------------------------------------------------
    path('pet/<int:pet_id>/', views.pet_detail, name='pet_detail'),  # Detailed view of a single pet
    path('pet/<int:pet_id>/edit/', views.edit_pet, name='edit_pet'),  # Edit pet details
    path('pets/delete/<int:pet_id>/', views.delete_pet, name='delete_pet'), # Delete pet
    path('contact/', views.contact_view, name='contact'),  # Contact form
    path('confirm_payment/', views.payment_page, name='confirm_payment'),
    path('adopt_pet/', views.adopt_pet, name='adopt_pet'),
    path('adoption/', views.adoption_page, name='adoption'),
]
