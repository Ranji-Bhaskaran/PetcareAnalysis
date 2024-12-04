"""Testing urls using pytest"""
import pytest
from django.urls import reverse, resolve
from pets import views

@pytest.mark.parametrize("url_name, view_func, kwargs", [
    ('home', views.home, {}),
    ('register', views.register, {}),
    ('login', views.login_view, {}),
    ('logout', views.logout_view, {}),
    ('dashboard', views.dashboard, {}),
    ('add_pet', views.add_pet, {}),
    ('add_health_log', views.add_health_log, {'pet_id': 1}),
    ('add_activity_log', views.add_activity_log, {'pet_id': 1}),
    ('global', views.global_view, {}),
    ('pet_list', views.pet_list, {}),
    ('products', views.products, {}),
    ('cart', views.cart_view, {}),
    ('add_to_cart', views.add_to_cart, {'product_id': 1}),
    ('remove_from_cart', views.remove_from_cart, {'product_id': 1}),
    ('checkout', views.checkout, {}),
    ('pet_detail', views.pet_detail, {'pet_id': 1}),
    ('edit_pet', views.edit_pet, {'pet_id': 1}),
    ('delete_pet', views.delete_pet, {'pet_id': 1}),
    ('contact', views.contact_view, {}),
    ('confirm_payment', views.payment_page, {}),
    ('adopt_pet', views.adopt_pet, {}),
    ('adoption', views.adoption_page, {}),
])
def test_url_resolves_correctly(url_name, view_func, kwargs):
    """
    Test that each URL resolves to the correct view function.
    """
    url = reverse(url_name, kwargs=kwargs)
    resolved = resolve(url)
    assert resolved.func == view_func
