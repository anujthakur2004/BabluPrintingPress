from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage

def contact(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get("name"),
            phone=request.POST.get("phone"),
            email=request.POST.get("email"),
            message=request.POST.get("message"),
        )

        messages.success(
            request,
            "Thank you! Your message has been sent. We will contact you shortly."
        )

        return redirect("contact")

    return render(request, "contact.html")
