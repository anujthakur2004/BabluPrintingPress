from django.shortcuts import render
from catalog.models import Product, Category


def home(request):
    def get_category(slug):
        return Category.objects.filter(slug=slug, is_active=True).first()

    # ================= NEW ARRIVALS =================
    new_products = (
        Product.objects.filter(is_active=True)
        .prefetch_related("images", "videos", "category")
        .order_by("-created_at")[:12]
    )

    # ================= VIDEO INVITATIONS =================
    video_category = get_category("video-invitations") or get_category("video-invitation-cards")
    video_invites = (
        Product.objects.filter(category=video_category, is_active=True)
        .prefetch_related("images", "videos")
        if video_category
        else []
    )

    # ================= WEDDING CARDS BY PRICE =================
    wedding_category = get_category("wedding-cards")

    wedding_10_20 = Product.objects.filter(
        category=wedding_category,
        starting_price__gte=10,
        starting_price__lte=20,
        is_active=True,
    ).prefetch_related("images") if wedding_category else []

    wedding_20_30 = Product.objects.filter(
        category=wedding_category,
        starting_price__gte=20,
        starting_price__lte=30,
        is_active=True,
    ).prefetch_related("images") if wedding_category else []

    wedding_30_40 = Product.objects.filter(
        category=wedding_category,
        starting_price__gte=30,
        starting_price__lte=40,
        is_active=True,
    ).prefetch_related("images") if wedding_category else []

    # ================= BUSINESS ESSENTIALS (PRODUCTS) =================
    business_category = get_category("buisness-essentials")
    business_products = []
    
    if business_category:
        # Get all subcategories under Business Essentials
        business_subcats = business_category.children.filter(is_active=True)
        # Get products from those subcategories
        business_products = Product.objects.filter(
            category__in=business_subcats,
            is_active=True
        ).prefetch_related("images", "videos")[:8]

    context = {
        "new_products": new_products,
        "video_invites": video_invites,
        "wedding_10_20": wedding_10_20,
        "wedding_20_30": wedding_20_30,
        "wedding_30_40": wedding_30_40,
        "business_products": business_products,  
    }

    return render(request, "home.html", context)


def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def refund_policy(request):
    return render(request, 'refund_policy.html')

def shipping_policy(request):
    return render(request, 'shipping_policy.html')

def visit_us(request):
    return render(request, 'visit_us.html')

def our_story(request):
    return render(request, 'our_story.html')
