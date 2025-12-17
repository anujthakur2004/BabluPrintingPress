from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.db.models import Q

def subcategory_list(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        parent__isnull=True,
        is_active=True
    )

    subcategories = category.children.filter(is_active=True)
    
    # Get products directly in this category
    direct_products = Product.objects.filter(
        category=category,
        is_active=True
    ).prefetch_related("images")

    # 🔹 CASE 1: Category has subcategories
    if subcategories.exists():
        return render(request, "catalog/subcategory_list.html", {
            "category": category,
            "subcategories": subcategories,
            "direct_products": direct_products,
        })

    # 🔹 CASE 2: Category has NO subcategories → show products directly
    sort_options = [
        ('popular', 'Popular'),
        ('newest', 'Newest'),
        ('price_low', 'Price: Low to High'),
        ('price_high', 'Price: High to Low'),
    ]
    
    return render(request, "product_list.html", {
        "subcategory": category,
        "products": direct_products,
        "sort_options": sort_options,
    })



def product_list(request, category_slug, subcategory_slug):
    subcategory = get_object_or_404(
        Category,
        slug=subcategory_slug,
        parent__slug=category_slug
    )

    products = Product.objects.filter(
        category=subcategory,
        is_active=True
    ).prefetch_related("images")

    # Apply price filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if min_price:
        try:
            products = products.filter(starting_price__gte=float(min_price))
        except (ValueError, TypeError):
            pass
    
    if max_price:
        try:
            products = products.filter(starting_price__lte=float(max_price))
        except (ValueError, TypeError):
            pass

    # Apply sorting
    sort_by = request.GET.get('sort', 'popular')
    if sort_by == 'price_low':
        products = products.order_by('starting_price')
    elif sort_by == 'price_high':
        products = products.order_by('-starting_price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:
        # popular - default order
        products = products.order_by('-created_at')

    sort_options = [
        ('popular', 'Popular'),
        ('newest', 'Newest'),
        ('price_low', 'Price: Low to High'),
        ('price_high', 'Price: High to Low'),
    ]

    return render(request, "product_list.html", {
        "subcategory": subcategory,
        "products": products,
        "sort_options": sort_options,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    return render(request, "product_detail.html", {
        "product": product,
    })

def business_essentials(request):
    # Find parent category by name or slug containing "business"
    parent = Category.objects.filter(
        parent__isnull=True,
        is_active=True
    ).filter(
        Q(slug__icontains='business') | Q(name__icontains='business')
    ).first()
    
    if parent:
        business_categories = parent.children.filter(is_active=True).prefetch_related('products__images')
    else:
        # No parent found - show empty list
        business_categories = []

    return render(request, "business_essentials.html", {
        "business_categories": business_categories,
    })
