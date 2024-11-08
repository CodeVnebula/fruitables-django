from django.core.management.base import BaseCommand
from django.db.models import Count
from store.models import Product

class Command(BaseCommand):
    help = 'Returns the top popular products based on cart item count'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit', 
            type=int, 
            default=5, 
            help='Number of top products to display (default: 5)'
        )
    
    def handle(self, *args, **options):
        limit = options['limit']
        
        top_products = (
            Product.objects.annotate(user_count=Count('cartitem'))
            .order_by('-user_count')[:limit]
        )

        if top_products:
            self.stdout.write(self.style.SUCCESS(f"Top {limit} products in the store:"))
            for product in top_products:
                self.stdout.write(self.style.SUCCESS(f"{product.name} - added to {product.user_count} users' carts"))
        else:
            self.stdout.write(self.style.ERROR("No products found in carts."))
            