from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Product
from .forms import *


def index(request):
    if request.method == 'POST':
        category = request.POST.get("category")
        return render(request, "hack_app/index.html", {
            "products": Product.objects.filter(category=category)
        })
    else:    
        return render(request, "hack_app/index.html", {
            "products": Product.objects.all()
        })


def log_in(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "hack_app/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "hack_app/login.html")


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "hack_app/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "hack_app/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "hack_app/register.html")

def profile(request, pk):
    return render(request, "hack_app/profile.html", {
        "products": Product.objects.filter(user=User.objects.get(pk=pk))
    })

def profile_create(request, pk):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            f = Product(user=User.objects.get(pk=pk),
                        title=form.cleaned_data["title"],
                        description=form.cleaned_data["description"],
                        price=form.cleaned_data["price"],
                        image=form.cleaned_data["image"],
                        category=form.cleaned_data["category"])
            f.save()
            return HttpResponseRedirect(reverse('profile', kwargs={'pk': pk}))
        else:
            return render(request, "hack_app/errors.html", {
                "errors": [form.errors, form.non_field_errors]
            })
    else:
        return render(request, "hack_app/profile-create.html", {
            "form": ProductForm()
        })

def profile_edit(request, pk, prpk):
    if request.method == 'POST':
        f = Product.objects.get(pk=prpk)
        f.title = request.POST["title"]
        f.description = request.POST["description"]
        f.price = request.POST["price"]
        f.category = request.POST["category"]

        f.save()
        return HttpResponseRedirect(reverse('profile', kwargs={'pk': pk}))
    else:
        return render(request, "hack_app/profile-edit.html", {
            "product": Product.objects.get(pk=prpk),
            "form": ProductForm()
        })
    