import random
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.db.models import Count, Sum, Prefetch, Q, Case, When, BooleanField, F
from django.shortcuts import get_object_or_404

from order.models import Cart, CartItem
from . import models

def cart_view(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all() 
        total_quantity = 0
        for _ in cart_items:
            total_quantity += 1
    else:
        cart_items = []
        total_quantity = 0

    return total_quantity, cart_items


def _get_category_info(category):
    category_info = {
        'name': category.name,
        'slug': category.slug,
        'subcategories': []
    }

    subcategories = category.children.all()

    for subcategory in subcategories:
        subcategory_info = {
            'name': subcategory.name,
            'slug': subcategory.slug,
            'products': [{
                'id': product.id,
                'name': product.name, 
                'price': product.price,
                'description': product.description,
                'slug': product.slug,
                'image': product.image.url if product.image else '',
                'is_available': product.is_available
            } for product in subcategory.products.all()]
        }
        category_info['subcategories'].append(subcategory_info)

    return category_info


def home(request):
    if request.method == 'GET':
        items_in_cart = cart_view(request)[0]
        
        categories = models.Category.objects.filter(parent=None).prefetch_related(
            'children__products'
        ).annotate(
            is_available_product=Case(
                When(
                    children__products__weight_available__lte=F('children__products__min_weight') * 100,
                    then=False
                ),
                default=True,
                output_field=BooleanField()
            )
        ).annotate(
            subcategory_product_count=Count('children__products', filter=Q(children__products__is_available=True, is_available_product=True)) 
        ).filter(
            subcategory_product_count__gt=0
        )

        total_products = categories.aggregate(
            total_products=Sum('subcategory_product_count')
        )['total_products'] or 0  

        if categories.exists():
            selected_categories = random.sample(list(categories), k=min(2, categories.count()))
        else:
            selected_categories = []

        categories_data = [_get_category_info(category) for category in selected_categories]

        random_category_data = random.choice(categories_data) if categories_data else None
        random_category_name = random_category_data['name'] if random_category_data else None
        first_is_beverages = False
        if random_category_name and random_category_name == 'Beverages':
            first_is_beverages = True
            
        subcategories = random_category_data['subcategories'] if random_category_data else []
        products = [product for subcat in subcategories for product in subcat['products'] if product['is_available']] if subcategories else []

        categories_data_copy = categories_data.copy()
        if random_category_data in categories_data_copy:
            categories_data_copy.remove(random_category_data)

        second_random_category_data = random.choice(categories_data_copy) if categories_data_copy else None
        second_random_category_name = second_random_category_data['name'] if second_random_category_data else None
        
        second_is_beverages = False
        if second_random_category_name and second_random_category_name == 'Beverages':
            second_is_beverages = True
        
        second_subcategories = second_random_category_data['subcategories'] if second_random_category_data else []
        products2 = [product for subcat in second_subcategories for product in subcat['products'] if product['is_available']] if second_subcategories else []

        all_categories = list(categories.values('name', 'slug')) if categories.exists() else []
        
        context = {
            'items_in_cart': items_in_cart,
            'random_category_name': random_category_name,
            'subcategories': subcategories,
            'products': products,
            'categories_data': categories_data,
            'second_random_category_name': second_random_category_name,
            'second_subcategories': second_subcategories,
            'products2': products2,
            'products_in_store': total_products,
            'products2_length': len(products2),
            'all_categories': all_categories,
            'first_is_beverages' : first_is_beverages,
            'second_is_beverages': second_is_beverages,
        }

        return render(request, 'index.html', context)
    

def shop(request):
    if request.method == 'GET':
        items_in_cart = cart_view(request)[0]
        
        children_categories = models.Category.objects.filter(
            parent__isnull=False
        ).select_related('parent').prefetch_related(
            Prefetch('products', queryset=models.Product.objects.filter(is_available=True))
        )

        top_level_categories = models.Category.objects.filter(parent=None).prefetch_related(
            Prefetch('children__products', queryset=models.Product.objects.filter(is_available=True))
        ).annotate(products_count=Count('children__products')).filter(products_count__gt=0)
        
        products_by_category = []
        for category in children_categories:
            parent_name = category.parent.name if category.parent else category.name
            
            for product in category.products.all(): 
                products_by_category.append({
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'description': product.description,
                    'slug': product.slug,
                    'image': product.image.url,
                    'category': parent_name,
                })
            
        paginator = Paginator(products_by_category, 9)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        total_pages = paginator.num_pages
        current_page = page_obj.number
        page_range = 10
        half_range = page_range // 2

        start_page = max(1, current_page - half_range)
        end_page = min(total_pages, current_page + half_range)

        if end_page - start_page < page_range:
            if start_page == 1:
                end_page = min(total_pages, start_page + page_range - 1)
            else:
                start_page = max(1, end_page - page_range + 1)

        page_numbers = list(range(start_page, end_page + 1))

        categories = [{
            'name': category.name,
            'slug': category.slug,
            'products_count': category.products_count
        } for category in top_level_categories]

        context = {
            'items_in_cart': items_in_cart,
            'products': page_obj,
            'page_obj': page_obj,
            'page_numbers': page_numbers, 
            'categories': categories,
        }

        return render(request, 'shop.html', context)


def product_details(request, product_slug):
    if request.method == 'GET':
        items_in_cart = cart_view(request)[0]
        
        product = get_object_or_404(models.Product.objects.prefetch_related(
            'category'
        ).prefetch_related('reviews'), slug=product_slug)

        product_category = product.category.first().name if product.category.exists() else 'Uncategorized or Unknown'
        
        rating = product.stars / product.stars_count if product.stars_count > 0 else 0
        rating = int(rating) if rating - int(rating) < 0.5 else int(rating) + 1
        filled_stars = '<i class="fa fa-star text-secondary"></i>' * rating
        empty_stars = '<i class="fa fa-star"></i>' * (5 - rating)
        star_html = filled_stars + empty_stars
        
        product_details = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'detailed_description': product.detailed_description,
            'pack_weight': product.pack_weight,
            'min_weight': product.min_weight,
            'country_of_origin': product.country_of_origin,
            'quality': product.quality,
            'health_check': product.health_check,
            'image': product.image.url,
            'rating': star_html,
            'category': product_category,
            'reviews': [{
                'name': review.name,
                'rating': review.rating,
                'comment': review.comment
            } for review in product.reviews.all()]
        }

        top_level_categories = models.Category.objects.filter(parent=None).annotate(
            products_count=Count('products')
        ).filter(products_count__gt=0)
        
        categories = []
        for category in top_level_categories:
            categories.append({
                'name': category.name,
                'slug': category.slug,
                'products_count': category.products_count
            })

        related_products = models.Product.objects.filter(
            category__name=product_category
        ).exclude(slug=product_slug)
        
        related_products_list = []
        for related_product in related_products:
            related_products_list.append({
                'id': related_product.id,
                'name': related_product.name,
                'price': related_product.price,
                'description': related_product.description,
                'slug': related_product.slug,
                'image': related_product.image.url,
                'category': product_category
            })

        context = {
            'items_in_cart': items_in_cart,
            'product_details': product_details,
            'categories': categories,
            'related_products': related_products_list, 
            'related_products_length': len(related_products_list)
        }    
        
        return render(request, 'product_details.html', context)


def category_products(request, category_slug):
    items_in_cart = cart_view(request)[0]
    
    selected_category = get_object_or_404(models.Category, slug=category_slug)

    subcategories = models.Category.objects.filter(parent=selected_category)

    products = models.Product.objects.filter(
        category__in=[selected_category] + list(subcategories),
        is_available=True
    )

    top_level_categories = models.Category.objects.filter(
        parent=None
    ).prefetch_related(
        Prefetch('children__products', queryset=models.Product.objects.filter(is_available=True))
    ).exclude(slug=category_slug).annotate(
        products_count=Count('children__products', filter=Q(children__products__is_available=True))
    ).filter(products_count__gt=0)

    products_by_category = [{
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'description': product.description,
        'slug': product.slug,
        'image': product.image.url,
    } for product in products]

    paginator = Paginator(products_by_category, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total_pages = paginator.num_pages
    current_page = page_obj.number
    page_range = 10
    half_range = page_range // 2
    start_page = max(1, current_page - half_range)
    end_page = min(total_pages, current_page + half_range)

    if end_page - start_page < page_range:
        if start_page == 1:
            end_page = min(total_pages, start_page + page_range - 1)
        else:
            start_page = max(1, end_page - page_range + 1)

    page_numbers = list(range(start_page, end_page + 1))

    categories = [{
        'name': category.name,
        'slug': category.slug,
        'products_count': category.products_count
    } for category in top_level_categories]

    context = {
        'items_in_cart': items_in_cart,
        'products': page_obj,  
        'page_obj': page_obj,
        'page_numbers': page_numbers,
        'categories': categories,
        'selected_category_name': selected_category.name,
    }

    return render(request, 'category_products.html', context)



def import_products_from_json(request):
    import json
    from django.shortcuts import render
    from .models import Category, Product
    from django.utils.text import slugify
    
    path = r'C:\Users\chkhi\OneDrive\Desktop\fruitables-django\fruitables\static\full_product_data.json'
    with open(path, 'r') as file:
        data = json.load(file)
    
    for product_data in data:
        category_name = product_data['category']
        subcategory_name = product_data['subcategory']

        category, created = Category.objects.get_or_create(name=category_name, parent=None)

        subcategory, created = Category.objects.get_or_create(name=subcategory_name, parent=category)

        product = Product(
            name=product_data['name'],
            price=product_data['price'],
            description=product_data['description'],
            pack_weight=product_data['weight_available'],
            min_weight=product_data['weight_available'], 
            country_of_origin=product_data['country_of_origin'],
            quality=product_data['quality'],
            image=product_data['image'],
            stars=product_data['stars'],
            stars_count=product_data['stars_count'],
            weight_available=product_data['weight_available']
        )
        
        product.save() 
        
        product.category.add(subcategory)

    return render(request, 'import_success.html')


def update_all_products(request):
    from .models import Product
    import random
    import os
    from django.conf import settings
    from django.core.files import File
    products = Product.objects.all()
    detailed_descriptions = [
        "This product is crafted with the finest materials to ensure top-notch quality and longevity. Ideal for those seeking superior performance and elegance.",
        "Engineered for excellence, this item combines functionality with modern design, making it a must-have in your collection.",
        "An exceptional blend of style and comfort, perfect for everyday use. Experience premium quality at an affordable price.",
        "Made from sustainably sourced ingredients, this product is designed to offer the best experience while being eco-friendly.",
        "This premium product offers unparalleled performance, designed to meet the demands of the most discerning users.",
        "An innovative solution for modern living, crafted to provide convenience and sophistication in one package.",
        "Created with the user in mind, this product ensures ease of use and maximum efficiency, perfect for any occasion.",
        "A top-tier choice for those who value quality and durability. Built to last and designed to impress.",
        "This product stands out for its remarkable versatility and attention to detail. Crafted for those who settle for nothing less than the best.",
        "Combining cutting-edge technology and classic craftsmanship, this item is perfect for enhancing your daily life.",
        "This product is meticulously engineered to provide optimal results, with a focus on both aesthetics and practicality.",
        "Designed to offer unmatched comfort and style, this product is ideal for those who appreciate high-end craftsmanship.",
        "A perfect harmony of innovation and tradition, making this product a standout choice for both functionality and elegance.",
        "Built to deliver exceptional performance, this item is a game-changer in its category, providing value beyond expectations.",
        "Handcrafted with precision, this product reflects an unwavering commitment to quality and attention to detail.",
        "An eco-friendly, high-performance product designed to meet your daily needs while minimizing environmental impact.",
        "Combining form and function, this product offers a sleek design without compromising on performance or durability.",
        "This product is a versatile addition to any home or office, offering both convenience and aesthetic appeal.",
        "With its innovative design and premium materials, this product is the perfect blend of luxury and functionality.",
        "Designed to exceed expectations, this product delivers top-tier results for those who demand the best in every aspect of their lives."
    ]
    product_qualities = [
        "Excellent",
        "Premium",
        "High Quality",
        "Superior",
        "Top-notch",
        "Eco-friendly",
        "Sustainable",
        "Organic",
        "Handcrafted",
        "Artisanal",
        "Durable",
        "Innovative",
        "Affordable",
        "Luxury",
        "Exceptional"
    ]
    countries_of_origin = [
        "USA",
        "Canada",
        "Germany",
        "France",
        "Italy",
        "Spain",
        "Japan",
        "China",
        "India",
        "Australia",
        "Brazil",
        "Mexico",
        "South Africa",
        "New Zealand",
        "United Kingdom",
        "Netherlands",
        "Switzerland",
        "Argentina",
        "Thailand",
        "Vietnam"
    ]
    health_check_list = [
        "Gluten-Free",
        "Low Sugar",
        "High Protein",
        "Low Fat",
        "Vegan",
        "Organic Certified",
        "Non-GMO",
        "Keto Friendly",
        "Paleo Approved",
        "Heart Healthy",
        "Dairy-Free",
        "No Artificial Additives",
        "Rich in Fiber",
        "Low Sodium",
        "Sugar-Free",
        "All Natural",
        "Rich in Antioxidants",
        "Immune Boosting",
        "Plant-Based",
        "No Preservatives"
    ]

    tags = models.Tag.objects.all()
    for product in products:
        random_tags = random.sample(list(tags), k=random.randint(1, min(3, len(tags))))
        product.tag.set(random_tags)
        # product.detailed_description = random.choice(detailed_descriptions)
        # product.weight_available = random.randint(750, 1000)
        # product.pack_weight = random.choice([0.5, 1])
        # product.min_weight = product.pack_weight/5 if product.pack_weight == 1 else product.pack_weight/2
        # product.country_of_origin = random.choice(countries_of_origin)
        # product.quality = random.choice(product_qualities)
        # product.health_check = random.choice(health_check_list)
        # random_image_number = random.randint(1, 6)
    
        # image_path = os.path.join(settings.MEDIA_ROOT, 'product_images', f'fruite-item-{random_image_number}.jpg')
        
        # if os.path.exists(image_path):
        #     with open(image_path, 'rb') as img_file:
        #         product.image.save(f'product_images/fruite-item-{random_image_number}.jpg', File(img_file))  
        #     product.save()
        # else:
        #     print(f"Image file not found: {image_path}")
        # product.stars = random.randint(product.stars_count*3 ,product.stars_count*5)
        product.save()
        
def header_search(request):
    
#     query = request.GET.get('q')
    
#     # If there's a search query, redirect to the shop page with the search query
#     if query:
#         return redirect(f"{reverse('shop')}?q={query}")
    
#     # If no query, just redirect to the shop page without any filter
#     return redirect(reverse('shop'))
    pass


def add_to_cart(request, product_id, weight=None):
    if request.method == 'POST':
        if product_id:
            product = get_object_or_404(models.Product, id=product_id)
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            if weight is None:
                weight = request.POST.get('weight', product.pack_weight)
            print(weight)
            try:
                from decimal import Decimal
                weight = Decimal(weight)
            except ValueError:
                weight = product.pack_weight
            
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'pack_weight': weight})
            if not created:
                cart_item.pack_weight += weight
                cart_item.save()
            
            product.weight_available -= float(weight)
            product.save()

            return redirect(request.META.get('HTTP_REFERER', 'home')) 
        return redirect('home')
