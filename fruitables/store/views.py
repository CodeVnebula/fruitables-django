from django.shortcuts import redirect, render
from .models import Category, Product, Tag
from django.db.models import Count, Prefetch
from django.core.paginator import Paginator
from .forms import SearchForm
from order.forms import AddToCartForm
from django.db.models import Subquery, OuterRef

def shop_view(request, category_slug=None, product_slug=None):
    if request.method == 'POST':
        add_to_cart(request)

    items_in_cart = 0
    if request.user.is_authenticated:
        items_in_cart = request.user.cart.total_items_in_cart()
    
    sorting_option = request.GET.get('productlist', 'nothing')
    form = SearchForm(request.GET or None)
    search_query = ''
    
    sorting_options = {
        'def': 'default',
        'price_asc': 'ascending',
        'price_desc': 'descending',
    }
    
    category = None
    products = None
    
    if category_slug:
        category = Category.objects.get(slug=category_slug)
        categories = category.get_all_children().annotate(products_count=Count('products'))
        
        categories = categories | Category.objects.filter(id=category.id)
        products = Product.objects.filter(category__in=categories, is_available=True)
        categories = categories[1:]
    
    else:
        categories = Category.objects.get_categories_with_children()
        products = Product.objects.filter(is_available=True)
    
    products_copy = products.prefetch_related('category', 'tag')
    
    price_range_filter = request.GET.get('rangeInput')
    if price_range_filter and int(price_range_filter) > 0:
        products_copy = products_copy.filter(price__lte=price_range_filter)
        
    additional_tag_filter = request.GET.get('tags', '')
    if additional_tag_filter and additional_tag_filter != "":
        products_copy = products_copy.filter(tag__id=int(additional_tag_filter))

    if sorting_option == sorting_options['price_asc']:
        products_copy = products_copy.order_by('price')  
    elif sorting_option == sorting_options['price_desc']:
        products_copy = products_copy.order_by('-price')
        
    if form.is_valid():
        search_query = form.cleaned_data['q']
        products_copy = products_copy.filter(name__icontains=search_query)
    
    paginator = Paginator(products_copy, 9)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total_pages = paginator.num_pages
    current_page = page_obj.number
    page_range = 9
    half_range = page_range // 2
    start_page = max(1, current_page - half_range)
    end_page = min(total_pages, current_page + half_range)

    if end_page - start_page < page_range:
        if start_page == 1:
            end_page = min(total_pages, start_page + page_range - 1)
        else:
            start_page = max(1, end_page - page_range + 1)

    page_numbers = list(range(start_page, end_page + 1))

    return render(request, 'shop.html', {
        'current_page' : 'Shop' if not category else category.name,
        'items_in_cart': items_in_cart,
        'search_query' : search_query,
        'form': form,
        'category' : category,
        'categories': categories,
        'products': page_obj,
        'page_obj': page_obj,
        'page_numbers': page_numbers,
        'sorting_option': sorting_option,
        'range_input': price_range_filter,
        'tags' : Tag.objects.all(),
        'selected_tag': additional_tag_filter
        })



def product_view(request, product_slug=None):
    if request.method == 'POST':
        add_to_cart(request)
    
    items_in_cart = 0
    if request.user.is_authenticated:
        items_in_cart = request.user.cart.total_items_in_cart()
        
    if product_slug:
        product = Product.objects.prefetch_related('category').get(slug=product_slug)
        
        related_products = Product.objects.filter(
            category__in=product.category.all()
        ).exclude(id=product.id)
        
        if not related_products.exists():
            parent_category_ids = product.category.filter(
                parent__isnull=False
            ).values_list('parent_id', flat=True)
            
            related_products = Product.objects.filter(
                category__parent__in=Subquery(parent_category_ids)
            ).prefetch_related('category').exclude(id=product.id).distinct()
        
        related_categories = Category.objects.filter(
            parent__id__in=product.category.filter(parent__isnull=False).values_list('parent__id', flat=True)
        ).annotate(products_count=Count('products')).distinct()
        
        rating = product.stars / product.stars_count if product.stars_count > 0 else 0
        rating = int(rating) if rating - int(rating) < 0.5 else int(rating) + 1
        filled_stars = '<i class="fa fa-star text-secondary"></i>' * rating
        empty_stars = '<i class="fa fa-star"></i>' * (5 - rating)
        star_html = filled_stars + empty_stars
        
    context = {
        'current_page' : product.name,
        'items_in_cart': items_in_cart,
        'product' : product,
        'related_products': related_products,
        'categories' : related_categories,
        'star_html': star_html,
        'product_count' : related_products.count()
    }
    
    return render(request, 'product_related/product-details.html', context)

def add_to_cart(request):
    if request.method == 'POST':
        print("\n\n\naaaaaaaaaaaaa--------------------------------------\n\n", request.POST)
        data = {
            'cart': request.user.cart.id,
            'product': int(request.POST.getlist('product_id')[0]),
            'pack_weight': float(request.POST.getlist('pack_weight')[0]),
        }
        
        form = AddToCartForm(data)
        if form.is_valid():
            print("Form is valid, cart item updated or created.")
            form.save()  
        else:
            print("Form errors:", form.errors)
    
    