from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Item, Category
from django.core.exceptions import ObjectDoesNotExist


# Display all categories
def category(request, foo):
    # Replace hyphens with spaces
    foo = foo.replace('-', ' ')
    try:
        # Look up the category
        category = Category.objects.get(name__iexact=foo)
        items = Item.objects.filter(category=category)
        return render(request, 'category.html', {'items': items, 'category': category})
    except ObjectDoesNotExist:
        messages.error(request, "Category doesn't exist")
        return redirect('home')


# Display details of a single item
def item(request, pk):
    item = Item.objects.get(id=pk)
    return render(request, 'item.html', {'item': item})

# Display all items
def home(request):
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})

# Display the About page
def about(request):
    return render(request, 'about.html', {})

# User login view
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful.")
            return redirect('home')
        else:
            messages.error(request, "Login unsuccessful. Please try again.")
            return redirect('login')
    
    return render(request, 'login.html', {})

# User logout view
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

# User registration view
def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect('home')
        else:
            messages.error(request, "Registration unsuccessful. Please try again.")
            return redirect('register')
        
    return render(request, 'register.html', {'form': form})
