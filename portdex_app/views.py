from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Product, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from .forms import ProductForm
import requests
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
import json
@login_required
def user_profile(request):
    # Get the products created by the logged-in user
    products = Product.objects.filter(user=request.user)
    return render(request, 'profile.html', {'products': products})
@login_required
def add_product(request):
    if request.method == 'POST':
        print("Form submitted")
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")
            product = form.save(commit=False)
            selected_category = request.POST.get('category')
            custom_category = request.POST.get('custom_category')

            print(f"Selected Category: {selected_category}, Custom Category: {custom_category}")

            if selected_category == 'Other' and custom_category:
                print("Saving custom category")
                category, created = Category.objects.get_or_create(name=custom_category)
                product.category = category
            else:
                print("Saving selected category")
                product.category = Category.objects.get(name=selected_category)

            product.user = request.user
            product.save()
            print("Product saved")
            return redirect('user_profile')
        else:
            print("Form errors: ", form.errors)
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})

def main(request):
	return render(request, 'main2.html')
def contact(request):
	return render(request, 'contact.html')


# from .models import HeroSection, AwardInfo, AboutSection, Service, Project, Product

# def main(request):
#     hero_section = HeroSection.objects.first()  
#     awards = AwardInfo.objects.all()  
#     about_section = AboutSection.objects.first()  
#     services = Service.objects.all()  
#     projects = Project.objects.all()  
#     products = Product.objects.all()  # Fetch all products

#     context = {
#         'hero_section': hero_section,
#         'awards': awards,
#         'about_section': about_section,
#         'services': services,
#         'projects': projects,
#         'products': products,  # Pass products to the template
#     }
#     return render(request, 'main3.html', context)
    
def about(request):
	return render(request, 'about.html')
def service(request):
	return render(request, 'service.html')

def index(request):
    try:
        # Fetch products from the external API
        response = requests.get('https://walluk.s3.eu-north-1.amazonaws.com/themes/themes%26plugins.json')
        api_data = response.json()

        # Process API data: create slug and set the first image for each product
        for product in api_data:
            product['slug'] = slugify(product['title'])
            product['sub_category'] = product.get('sub-category', 'N/A')
            product['tags'] = product.get('tags', [])
            product['first_image'] = product['images'][0] if product.get('images') and len(product['images']) > 0 else None

    except Exception as e:
        print(f"Error fetching API data: {e}")
        api_data = []

    # Fetch user-created products and categories from the database
    user_products = Product.objects.all()
    user_categories = Category.objects.all()

    # Prepare user products in a similar format to API data
    user_data = [
        {
            'title': product.title,
            'slug': product.slug,
            'description': product.description,
            'category': product.category.name,
            'sub_category': getattr(product, 'sub_category', 'N/A'),
            'tags': product.tags,
            'first_image': product.image.url if product.image else None,
            'images': [img.image.url for img in product.images.all()] if hasattr(product, 'images') else []
        }
        for product in user_products
    ]

    # Combine both API and user-created data
    combined_products = api_data + user_data

    # Get category and subcategory filters from query parameters
    category_filter = request.GET.get('category', None)
    subcategory_filter = request.GET.get('subcategory', None)

    # Filter combined products by category and subcategory if selected
    if subcategory_filter:
        filtered_products = [product for product in combined_products if product['sub_category'] == subcategory_filter]
    elif category_filter:
        filtered_products = [product for product in combined_products if product['category'] == category_filter]
    else:
        filtered_products = combined_products

    # Combine categories and subcategories from both API and user-created categories
    api_categories = list(set(item['category'] for item in api_data))
    api_subcategories = list(set(item['sub_category'] for item in api_data))

    user_categories_list = list(set(cat.name for cat in user_categories))
    user_subcategories_list = list(set(prod.sub_category for prod in user_products))

    # Merge both API and user-created categories and subcategories
    combined_categories = list(set(api_categories + user_categories_list))
    combined_subcategories = list(set(api_subcategories + user_subcategories_list))

    # PAGINATION: Create a paginator object for 30 products per page
    paginator = Paginator(filtered_products, 30)  # Show 30 products per page

    # Get the current page number from the request
    page_number = request.GET.get('page')

    # Get the products for the current page
    page_products = paginator.get_page(page_number)

    return render(request, 'index.html', {
        'categories': combined_categories,
        'subcategories': combined_subcategories,
        'products': page_products,
        'selected_category': category_filter,
        'selected_subcategory': subcategory_filter
    })

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


def freelancer_list(request):
    # Get category filter from the request
    category_filter = request.GET.get('category', None)
    
    try:
        # Fetch data from the API
        response = requests.get('https://walluk.s3.eu-north-1.amazonaws.com/freelancers/freelancer_data.json')  # Replace <API_ENDPOINT> with the actual API URL
        freelancers = response.json()

        # Filter freelancers by category if a category is selected
        if category_filter:
            freelancers = [f for f in freelancers if f['category'] == category_filter]

    except Exception as e:
        freelancers = []

    # Paginate the freelancers (30 per page)
    paginator = Paginator(freelancers, 100)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # If the page is not an integer, deliver the first page.
        page_obj = paginator.get_page(1)
    except EmptyPage:
        # If the page is out of range (e.g., 9999), deliver the last page of results.
        page_obj = paginator.get_page(paginator.num_pages)

    # Get all unique categories for filtering
    categories = list(set(f['category'] for f in freelancers))

    return render(request, 'freelancers.html', {
        'page_obj': page_obj, 
        'categories': categories, 
        'selected_category': category_filter
    })


# User Login View
def user_login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('add_product')  # Replace 'main' with your homepage
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


JSON_URL = 'https://walluk.s3.amazonaws.com/gitrepos/finance_repo.json'

def finance_repos_view(request):
    # Fetch JSON data from the API
    finance_json_url = 'https://walluk.s3.amazonaws.com/gitrepos/finance_repo.json'
    education_json_url = 'https://walluk.s3.amazonaws.com/gitrepos/education_ai_repo.json'

    # Determine category from request
    selected_category = request.GET.get('category', 'finance')  # Default is 'finance'

    # Fetch the appropriate JSON data based on the selected category
    if selected_category == 'education':
        response = requests.get(education_json_url)
    else:
        response = requests.get(finance_json_url)

    repos_data = json.loads(response.text)

    # Optionally, filter by programming languages/types (if requested)
    selected_type = request.GET.get('type', None)
    if selected_type:
        repos_data = [repo for repo in repos_data if selected_type.lower() in [tag.lower() for tag in repo.get('topics', [])]]

    context = {
        'repos': repos_data,
        'selected_type': selected_type,
        'selected_category': selected_category
    }
    return render(request, 'finance_repos.html', context)