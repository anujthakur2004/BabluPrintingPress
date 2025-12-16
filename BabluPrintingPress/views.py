from django.shortcuts import render


def home(request):
    return render(request, 'home.html')

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
