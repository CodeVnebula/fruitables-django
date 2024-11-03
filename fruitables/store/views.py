from functools import cache
from django.shortcuts import render
from .models import Category, Product, Tag
from django.db.models import Count
from order.forms import AddToCartForm
from django.db.models import Subquery
from django.views.generic import ListView, DetailView
from .forms import SearchForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@method_decorator(cache_page(600), name='dispatch')
class ShopView(ListView):
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 9  
    
    def post(self, request, *args, **kwargs):
        add_to_cart(request)
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        print("GET request", request.GET)
        category_slug = self.request.GET.getlist('category_slug')[0] if self.request.GET.getlist('category_slug') else None
        sorting_option = self.request.GET.get('productlist', 'nothing')
        price_range_filter = self.request.GET.get('rangeInput')
        additional_tag_filter = self.request.GET.get('tags', '')
        print("Category slug:", category_slug)
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            categories = category.get_all_children().annotate(products_count=Count('products'))
            categories = categories | Category.objects.filter(id=category.id)
            products = Product.objects.filter(category__in=categories, is_available=True).prefetch_related('category', 'tag')
            categories = categories[1:]
        else:
            categories = Category.objects.get_categories_with_children()
            products = Product.objects.filter(is_available=True).prefetch_related('category', 'tag')

        products_copy = products

        if price_range_filter and price_range_filter.isdigit():
            products_copy = products_copy.filter(price__lte=price_range_filter)

        if additional_tag_filter and additional_tag_filter != "":
            products_copy = products_copy.filter(tag__id=int(additional_tag_filter))

        sorting_options = {
            'def': 'default',
            'price_asc': 'ascending',
            'price_desc': 'descending',
        }
        if sorting_option == sorting_options['price_asc']:
            products_copy = products_copy.order_by('price')
        elif sorting_option == sorting_options['price_desc']:
            products_copy = products_copy.order_by('-price')

        search_query = self.request.GET.get('q', '')
        if search_query:
            products_copy = products_copy.filter(name__icontains=search_query)

        self.search_query = search_query
        self.category = category if category_slug else None
        self.categories = categories[1:] if category_slug else categories
        self.sorting_option = sorting_option
        self.price_range_filter = price_range_filter
        self.additional_tag_filter = additional_tag_filter

        paginator = Paginator(products_copy, self.paginate_by)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        get_context = {
            'products': page_obj,
            'search_query': search_query,
            'category': category if category_slug else None,
            'categories': categories,
            'sorting_option': sorting_option,
            'range_input': price_range_filter,
            'tags' : Tag.objects.all(),
            'selected_tag': additional_tag_filter,
            'page_obj': page_obj  
        }
        
        return render(request, self.template_name, self.get_context_data(get_context))

    def get_context_data(self, kwargs):
        context = kwargs

        page_obj = context['products'] 
        total_pages = page_obj.paginator.num_pages
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

        context.update({
            'current_page': 'Shop' if not context['category'] else context['category'].name,
            'form': SearchForm(self.request.GET or None),
            'page_numbers': page_numbers,
        })
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_related/product-details.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'

    def post(self, request, *args, **kwargs):
        add_to_cart(request)
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        product = self.get_object()

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

        rating = product.stars / product.reviews_amount if product.reviews_amount > 0 else 0
        rating = int(rating) if rating - int(rating) < 0.5 else int(rating) + 1
        filled_stars = '<i class="fa fa-star text-secondary"></i>' * rating
        empty_stars = '<i class="fa fa-star"></i>' * (5 - rating)
        star_html = filled_stars + empty_stars

        context.update({
            'current_page': product.name,
            'related_products': related_products,
            'categories': related_categories,
            'star_html': star_html,
            'product_count': related_products.count(),
        })
        
        return context
    

def add_to_cart(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please sign in to add items to your cart.")
        return None

    if request.method == 'POST':
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
    
    