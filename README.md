# fruitables-django

current links for navigation:

1. shop page, with products list - http://127.0.0.1:8000/shop/
2. order page, wth products cart - http://127.0.0.1:8000/order/cart/
3. product detailed page - http://127.0.0.1:8000/shop/product/{product_slug}

other links are generated by what filter, search query or category user chooses.

#### Nice to read!

! product detailed page can be opened by clicking anywhere on product card in products listing page

! after selecting wanted weight of product, 'apply' button must be clicked so the new weight will be saved,

otherwise regulad prodct_pack weight will be added to cart, for cartitem pack_weight

! for now products related products are shown only if products direct category has no more than 1 product, 

in this case related products are searched in products parent category's parent category (a root category)


! over products cards, product's category can be seen, but that part is commented for now in html, due to

it using queries as much as product on one page is, in this case max queris added to queries total is 9, which

is maximum products count in one page, this doesnt work in related products section, there can be as much more 

queries as related products are found.
