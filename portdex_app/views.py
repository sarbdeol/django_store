from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
# from .models import Product, Category, Image
# from .forms import ProductForm
import requests
from django.utils.text import slugify


def main(request):
	return render(request, 'main.html')
def admin_page(request):
	return render(request, 'admin_product.html')
def index(request):
	try:
		# Fetch products from the API
		response = requests.get('https://walluk.s3.eu-north-1.amazonaws.com/themes/themes%26plugins.json')
		data = response.json()

		# Create a slug and set the first image for each product
		for product in data:
			product['slug'] = slugify(product['title'])
			product['sub_category'] = product.get('sub-category', 'N/A')
			product['tags'] = product.get('tags', [])
			product['first_image'] = product['images'][0] if product.get('images') and len(product['images']) > 0 else None

	except Exception as e:
		print(f"Error fetching data: {e}")
		data = []

	# Get category filter from query parameters
	category_filter = request.GET.get('category', None)

	# Filter products by category if a category is selected
	if category_filter:
		filtered_products = [product for product in data if product['category'] == category_filter]
	else:
		filtered_products = data

	# Get unique categories for filtering
	categories = list(set(item['category'] for item in data))

	return render(request, 'index.html', {'categories': categories, 'products': filtered_products, 'selected_category': category_filter})
# Product details
def product_page(request, slug):
	try:
		response = requests.get('https://walluk.s3.eu-north-1.amazonaws.com/themes/themes%26plugins.json')
		products = response.json()
		product = next((item for item in products if slugify(item['title']) == slug), None)
		
		# Set the first image
		if product:
			product['first_image'] = product['images'][0] if product.get('images') and len(product['images']) > 0 else None
	except Exception as e:
		print(f"Error fetching data: {e}")
		product = None

	return render(request, 'product.html', {'product': product})


# User Login View
def user_login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('admin_page')  # Replace 'main' with your homepage
		else:
			messages.error(request, 'Invalid credentials')
	return render(request, 'login.html')

# User Register View
def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Account created successfully!')
			return redirect('login')
	else:
		form = UserCreationForm()
	return render(request, 'register.html', {'form': form})
# User Logout
def user_logout(request):
	logout(request)
	return redirect('login')
