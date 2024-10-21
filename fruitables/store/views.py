import random
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Count, Sum, Prefetch
from django.shortcuts import get_object_or_404
from . import models

def home(request):
    categories = models.Category.objects.filter(parent=None).prefetch_related(
        'products', 
        'children__products'
    ).annotate(
        products_count=Count('products')
    ).filter(products_count__gt=0)
    
    total_products = categories.aggregate(
        total_products=Sum('products_count')
    )['total_products']

    selected_categories = random.sample(list(categories), k=min(2, categories.count()))

    categories_data = []

    for category in selected_categories:
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
                    'name': product.name, 
                    'price': product.price,
                    'description': product.description,
                    'slug': product.slug,
                    'image': product.image.url
                } for product in subcategory.products.all()]
            }
            category_info['subcategories'].append(subcategory_info)

        categories_data.append(category_info)
    
    random_category = random.choice(categories_data)
    random_category_name = random_category['name']
    subcategories = random_category['subcategories']
    
    categories_data_copy = categories_data.copy()
    categories_data_copy.remove(random_category)
    
    if categories_data_copy:
        second_random_category = random.choice(categories_data_copy)
        second_random_category_name = second_random_category['name']
        second_subcategories = second_random_category['subcategories']
        products2 = [product for subcat in second_subcategories for product in subcat['products']]
    products = [product for subcat in subcategories for product in subcat['products']]

    all_categories = list(categories.values('name', 'slug'))
    
    context = {
        'random_category_name': random_category_name,
        'subcategories': subcategories,
        'products': products,
        'categories_data': categories_data,
        'second_random_category_name': second_random_category_name,
        'second_subcategories': second_subcategories,
        'products2': products2,
        'products_in_store' : total_products,
        'products2_length': len(products2),
        'all_categories': all_categories
    }

    return render(request, 'index.html', context)

def shop(request):
    price_range = None

    if request.method == 'POST' and 'price_range' in request.POST:
        price_range = request.POST.get('price_range')
        try:
            price_range = int(price_range)
        except (TypeError, ValueError):
            price_range = None  

    if price_range is not None and price_range > 0:
        filtered_products = models.Product.objects.filter(
            price__gte=price_range - 2,
            price__lte=price_range + 2
        )
    else:
        filtered_products = models.Product.objects.all()

    top_level_categories = models.Category.objects.filter(
        parent=None
    ).prefetch_related(
        Prefetch('products', queryset=filtered_products)
    ).annotate(products_count=Count('products')).filter(products_count__gt=0)

    products_by_category = []
    for category in top_level_categories:
        category_products = category.products.all()
        for product in category_products:
            products_by_category.append({
                'name': product.name,
                'price': product.price,
                'description': product.description,
                'slug': product.slug,
                'image': product.image.url,
                'category': category.name
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
        'products': page_obj,
        'page_obj': page_obj,
        'page_numbers': page_numbers, 
        'categories': categories,
    }

    return render(request, 'shop.html', context)

def product_details(request, product_slug):
    product = get_object_or_404(models.Product.objects.prefetch_related(
        'category'
    ).prefetch_related('reviews'), slug=product_slug)

    product_category = product.category.filter(parent=None).first().name
    
    rating = product.stars / product.stars_count if product.stars_count > 0 else 0
    rating = int(rating) if rating-int(rating) < 0.5 else int(rating) + 1
    filled_stars = '<i class="fa fa-star text-secondary"></i>' * rating
    empty_stars = '<i class="fa fa-star"></i>' * (5 - rating)
    star_html = filled_stars + empty_stars
    
    product_details = {
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
            'name': related_product.name,
            'price': related_product.price,
            'description': related_product.description,
            'slug': related_product.slug,
            'image': related_product.image.url,
            'category' : product_category
        })

    context = {
        'product_details': product_details,
        'categories': categories,
        'related_products': related_products_list, 
        'related_products_length': len(related_products_list)
    }    
    
    return render(request, 'product_details.html', context)

def category_products(request, category_slug):
    selected_category = models.Category.objects.get(slug=category_slug)

    products = models.Product.objects.filter(category=selected_category)

    top_level_categories = models.Category.objects.filter(
        parent=None
    ).exclude(slug=category_slug).annotate(
        products_count=Count('products')
    ).filter(products_count__gt=0)

    products_by_category = [{
        'name': product.name,
        'price': product.price,
        'description': product.description,
        'slug': product.slug,
        'image': product.image.url,
        'category': selected_category.name
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
        'products': page_obj,  
        'page_obj': page_obj,
        'page_numbers': page_numbers,
        'categories': categories, 
        'selected_category_name': selected_category.name,
    }

    return render(request, 'category_products.html', context)


