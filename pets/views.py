"""Views for the Pet application, 
handling user interactions with pet profiles, 
activity logs, and contact form.
"""
# Standard library imports
import io
import json
import base64
from datetime import timedelta
from decimal import Decimal, ROUND_DOWN

# Third-party library imports
import matplotlib.pyplot as plt
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.utils import timezone

# Local application/library imports
from .utils import send_sms
from .models import Pet, ActivityLog, Product
from .forms import (
    CustomUserCreationForm,
    LoginForm,
    AddPetForm,
    EditPetForm,
    ProductForm,
    ContactForm,
    HealthLogForm,
    ActivityLogForm,
)
from .telegram import send_adoption_message

def home(request):
    """Render the home page."""
    return render(request, 'pets/home.html')


def register(request):
    """ Register form and view """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
        messages.error(request, 'Please correct the error below.')

    form = CustomUserCreationForm()
    return render(request, 'pets/register.html', {'form': form})

def login_view(request):
    """Authenticate and log in the user."""
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('pet_list')
            messages.error(request, "Invalid username or password.")
    form = LoginForm()
    return render(request, 'pets/login.html', {'form': form})


@login_required
def logout_view(request):
    """Log out the current user and redirect to the home page."""
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

# No method restriction
@login_required
def pet_list(request): # Sensitive
    """List pets owned by the user along with weekly activity summaries."""
    pets = Pet.objects.filter(owner=request.user)
    one_week_ago = timezone.now() - timedelta(days=7)
    pet_data = []

    for pet in pets:
        activities = ActivityLog.objects.filter(pet=pet, activity_date__gte=one_week_ago)
        activity_summary = {'walk': 0, 'play': 0, 'groom': 0}
        for activity in activities:
            if activity.activity_type in activity_summary:
                activity_summary[activity.activity_type] += activity.duration

        labels = list(activity_summary.keys())
        sizes = list(activity_summary.values())
        chart_message = "No activity this week" if all(value == 0 for value in sizes) else None

        if chart_message is None:
            plt.figure(figsize=(6, 6))
            plt.pie(
                sizes,
                labels=labels,
                colors=['#4CAF50', '#FF9800', '#2196F3'],
                autopct='%1.1f%%',
                startangle=140)
            plt.title(f"Weekly Activity Summary for {pet.name}")
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            image_data = base64.b64encode(buf.getvalue()).decode('utf-8')
            buf.close()
            plt.close()
        else:
            image_data = None

        pet_data.append({
            'pet': pet,
            'weekly_activity': activity_summary,
            'chart': image_data,
            'chart_message': chart_message
        })

    return render(request, 'pets/pet_list.html', {'pet_data': pet_data})

# No method restriction
@login_required
def pet_detail(request, pet_id): # Sensitive
    """Display details of a specific pet with a weekly activity summary chart."""
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    one_week_ago = timezone.now() - timedelta(days=7)
    activities = ActivityLog.objects.filter(pet=pet, activity_date__gte=one_week_ago)
    activity_summary = {'walk': 0, 'play': 0, 'groom': 0}
    for activity in activities:
        if activity.activity_type in activity_summary:
            activity_summary[activity.activity_type] += activity.duration
    labels = list(activity_summary.keys())
    sizes = list(activity_summary.values())
    sizes = [1e-9 if value == 0 else value for value in sizes]
    plt.figure(figsize=(6, 6))
    plt.pie(
        sizes,
        labels=labels,
        colors=['#4CAF50', '#FF9800', '#2196F3'],
        autopct='%1.1f%%',
        startangle=140)
    plt.title(f"Weekly Activity Summary for {pet.name}")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close()

    return render(request, 'pets/pet_detail.html', {
        'pet': pet,
        'chart': image_data,
    })


@login_required
def add_pet(request):
    """Add a new pet to the user's pet list."""
    if request.method == 'POST':
        form = AddPetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            messages.success(request, "Pet added successfully!")
            return redirect('pet_list')
    form = AddPetForm()
    return render(request, 'pets/add_pet.html', {'form': form})


@login_required
def edit_pet(request, pet_id):
    """Edit details of an existing pet"""
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    if request.method == 'POST':
        form = EditPetForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, "Pet details updated successfully!")
            return redirect('pet_list')
    else:
        form = EditPetForm(instance=pet)

    return render(request, 'pets/edit_pet.html', {'form': form, 'pet': pet})


@login_required
def delete_pet(request, pet_id):
    """Delete an existing pet"""
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    if request.method == 'POST':
        pet.delete()
        messages.success(request, "Pet deleted successfully!")
        return redirect('pet_list')
    return render(request, 'pets/delete_pet.html', {'pet': pet})


@login_required
def dashboard(request):
    """Dashboard view displaying pet details and forms for adding new records"""
    pets = Pet.objects.filter(owner=request.user)
    pet_form = AddPetForm()
    health_log_form = HealthLogForm()
    activity_log_form = ActivityLogForm()

    context = {
        'pets': pets,
        'pet_form': pet_form,
        'health_log_form': health_log_form,
        'activity_log_form': activity_log_form,
    }
    return render(request, 'pets/dashboard.html', context)


@login_required
def add_health_log(request, pet_id):
    """Add a health log entry for a pet"""
    pet = get_object_or_404(Pet, pk=pet_id)
    if request.method == 'POST':
        form = HealthLogForm(request.POST)
        if form.is_valid():
            health_log = form.save(commit=False)
            health_log.pet = pet
            health_log.save()
            messages.success(request, "Health log added successfully!")
            return redirect('dashboard')
    else:
        form = HealthLogForm()

    return render(request, 'pets/add_health_log.html', {'form': form, 'pet': pet})


@login_required
def add_activity_log(request, pet_id):
    """View to add an activity log entry"""
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    if request.method == 'POST':
        form = ActivityLogForm(request.POST)
        if form.is_valid():
            activity_log = form.save(commit=False)
            activity_log.pet = pet
            activity_log.save()
            messages.success(request, "Activity log added successfully!")
            return redirect('dashboard')
    else:
        form = ActivityLogForm()

    return render(request, 'pets/add_activity_log.html', {'form': form, 'pet': pet})


def global_view(request):
    """Search for pets globally"""
    query = request.GET.get('q', '')
    if query:
        global_pets = (
            Pet.objects.filter(name__icontains=query) |
            Pet.objects.filter(breed__icontains=query)
        )
    else:
        global_pets = Pet.objects.all()
    # Check if there are no results based on the query
    no_results = not global_pets.exists()

    # Return context with query so 'Clear Search' button works properly
    return render(request, 'pets/global.html', {
        'global_pets': global_pets,
        'query': query,  # Pass the query variable
        'no_results': no_results,
    })

@login_required
def products(request):
    """ Function to display all accessories """
    all_products = Product.objects.all()
    form = ProductForm()

    # Retrieve the cart from the session
    cart = request.session.get('cart', [])
    # Fetch products that are currently in the cart
    cart_products = Product.objects.filter(id__in=cart)

    if request.method == 'POST' and request.user.is_staff:
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')  # Redirect after saving

    return render(request, 'pets/products.html', {
        'products': all_products,
        'form': form,
        'cart_products': cart_products  # Pass cart products to the template
    })

def cart_view(request):
    """ Function to view cart page """
    cart = request.session.get('cart', [])  # Retrieve cart from session
    cart_items = Product.objects.filter(id__in=cart)

    # Calculate total price, ensuring each item.price is treated as Decimal
    total_price = sum(
        Decimal(item.price) for item in cart_items) if cart_items else Decimal('0.00')

    # Define tax and admin fee
    tax_rate = Decimal('0.10')  # Tax rate as Decimal
    admin_fee = Decimal('5.00')  # Admin fee as Decimal

    # Calculate tax amount
    tax_amount = (total_price * tax_rate).quantize(
        Decimal('0.00'), rounding=ROUND_DOWN)

    # Calculate final total
    final_total = (total_price + tax_amount + admin_fee).quantize(
        Decimal('0.00'), rounding=ROUND_DOWN)

    return render(request, 'pets/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price.quantize(
            Decimal('0.00'), rounding=ROUND_DOWN),  # Ensure total price is also quantized
        'tax_amount': tax_amount,
        'admin_fee': admin_fee,
        'final_total': final_total
    })

# Function to add a product to the cart
def add_to_cart(request, product_id):
    """ Function to add product to cart """
    cart = request.session.get('cart', [])
    if product_id not in cart:
        cart.append(product_id)
        request.session['cart'] = cart  # Save updated cart in session
    return redirect('products')  # Redirect to the cart page

def remove_from_cart(request, product_id):
    """ Function to remove item from cart """
    # Retrieve the cart from the session, or initialize it as an empty list if it doesn't exist
    cart = request.session.get('cart', [])
    # Check if the product_id is in the cart
    if product_id in cart:
        # Remove the product_id from the cart
        cart.remove(product_id)

        # Save the updated cart back into the session
        request.session['cart'] = cart
        # Display a success message
        messages.success(request, "Item removed from cart.")
    else:
        # Display an error message if the item wasn't found in the cart
        messages.error(request, "Item not found in cart.")

    # Redirect to the cart page
    return redirect('products')

@login_required
def checkout(request):
    """ checkout page function """
    cart = request.session.get('cart', [])
    cart_items = Product.objects.filter(id__in=cart)

    # Calculate total price
    total_price = sum(
        Decimal(item.price) for item in cart_items).quantize(
            Decimal('0.00'), rounding=ROUND_DOWN)

    # Define tax and admin fee
    tax_rate = Decimal('0.10')  # Tax rate as Decimal
    admin_fee = Decimal('5.00')  # Admin fee as Decimal

    tax_amount = (
        total_price * tax_rate).quantize(
        Decimal('0.00'), rounding=ROUND_DOWN)  # Calculate tax
    final_total = (
        total_price + tax_amount + admin_fee).quantize(
            Decimal('0.00'), rounding=ROUND_DOWN)  # Final total

    return render(request, 'pets/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'tax_amount': tax_amount,
        'admin_fee': admin_fee,
        'final_total': final_total
    })

def contact_view(request):
    """Handle user contact form submissions"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = form.cleaned_data.get('email', settings.DEFAULT_FROM_EMAIL)
            send_mail(subject, message, from_email, [settings.DEFAULT_FROM_EMAIL])
            messages.success(
                request, "Your message has been sent successfully!")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

@login_required
def payment_page(request):
    """ payment page function """
    cart = request.session.get('cart', [])
    cart_items = Product.objects.filter(id__in=cart)

    # Calculate total price
    total_price = sum(
        Decimal(item.price) for item in cart_items).quantize(
            Decimal('0.00'), rounding=ROUND_DOWN)

    # Define tax and admin fee
    tax_rate = Decimal('0.10')  # Tax rate as Decimal
    admin_fee = Decimal('5.00')  # Admin fee as Decimal

    tax_amount = (total_price * tax_rate).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
    final_total = (
        total_price + tax_amount + admin_fee).quantize(
            Decimal('0.00'), rounding=ROUND_DOWN)  # Final total

    # Sending the payment notification to the admin
    message = (
    f"A payment has been made for {', '.join([item.name for item in cart_items])}. "
    f"Total earnings: ${final_total}."
    )

    send_sms(settings.ADMIN_PHONE_NUMBER, message)

    return render(request, 'pets/payment_page.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'tax_amount': tax_amount,
        'admin_fee': admin_fee,
        'final_total': final_total
    })
def adoption_page(request):
    """ A page to display pets for adoption """
    # List of pet data with Imgur image URLs
    pets = [
        {
            'name': 'Fluffy',
            'image': 'https://i.imgur.com/QHJVnNf.jpg',
            'description': 'A playful and friendly dog looking for a home.',
        },
        {
            'name': 'Rex',
            'image': 'https://i.imgur.com/n4153Cb.jpg',  # Replace with actual Imgur URL
            'description': 'An energetic dog that loves to play fetch.',
        },
        {
            'name': 'Bella',
            'image': 'https://i.imgur.com/heWnUlp.jpg',  # Replace with actual Imgur URL
            'description': 'A calm and loving dog that enjoys cuddles.',
        },
        {
            'name': 'Max',
            'image': 'https://i.imgur.com/e0mGyVb.jpg',  # Replace with actual Imgur URL
            'description': 'A loyal dog that loves long walks.',
        },
        {
            'name': 'Charlie',
            'image': 'https://i.imgur.com/MQj7R55.jpg',  # Replace with actual Imgur URL
            'description': 'A small and curious puppy looking for a family.',
        },
        {
            'name': 'Luna',
            'image': 'https://i.imgur.com/4EzFmkk.jpg',  # Replace with actual Imgur URL
            'description': 'A beautiful dog with a gentle personality.',
        },
        {
            'name': 'Oliver',
            'image': 'https://i.imgur.com/cOwc995.jpg',  # Replace with actual Imgur URL
            'description': 'A young and active dog ready for a new home.',
        },
        {
            'name': 'Tipsy',
            'image': 'https://i.imgur.com/3YIVKQD.jpg',  # Replace with actual Imgur URL
            'description': 'A sweet and playful dog looking for love.',
        },
        {
            'name': 'Blue',
            'image': 'https://i.imgur.com/xcDCoJW.jpg',  # Replace with actual Imgur URL
            'description': 'A playful and friendly dog looking for a home.',
        },
        {
            'name': 'Coco',
            'image': 'https://i.imgur.com/2aoEgNx.jpg',  # Replace with actual Imgur URL
            'description': 'A loyal dog that loves long walks.',
        }
    ]

    return render(request, 'pets/adoption_page.html', {'pets': pets})

def adopt_pet(request):
    """ Function to send message through telegram API """
    if request.method == 'POST':
        data = json.loads(request.body)
        pet_name = data.get('pet_name')
        pet_image_url = data.get('pet_image_url')

        # Send message to Telegram
        send_adoption_message(pet_name, pet_image_url)
        return JsonResponse({'message':f'Successfully adopted {pet_name}!Notified admin.'})

    return JsonResponse({'message': 'Invalid request method.'}, status=400)
