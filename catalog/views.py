from django.shortcuts import render, get_object_or_404
from .models import Category, Product

from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def subcategory_list(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        parent__isnull=True,
        is_active=True
    )

    subcategories = category.children.filter(is_active=True)

    # 🔹 CASE 1: Category has subcategories
    if subcategories.exists():
        return render(request, "catalog/subcategory_list.html", {
            "category": category,
            "subcategories": subcategories,
        })

    # 🔹 CASE 2: Category has NO subcategories → show products directly
    products = Product.objects.filter(
        category=category,
        is_active=True
    ).prefetch_related("images")

    return render(request, "product_list.html", {
        "subcategory": category,
        "products": products,
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

    return render(request, "product_list.html", {
        "subcategory": subcategory,
        "products": products,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    return render(request, "product_detail.html", {
        "product": product,
    })
