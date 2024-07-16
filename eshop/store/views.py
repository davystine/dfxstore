from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AccountInfoForm, UpdatePasswordForm, ProfileForm
from .models import Item, Category, UserProfile
from django.contrib.auth.models import User


# Display details of a single item
def item(request, pk):
    item = get_object_or_404(Item, id=pk)
    return render(request, 'item.html', {'item': item})

# Display all items
def home(request):
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})

# Display the About page
def about(request):
    return render(request, 'about.html', {})

# Display all items in a category
def category(request, foo):
    foo = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name__iexact=foo)
        items = Item.objects.filter(category=category)
        return render(request, 'category.html', {'items': items, 'category': category})
    except Category.DoesNotExist:
        messages.error(request, "Category doesn't exist")
        return redirect('home')

# Display category summary page
def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories})

# User login view
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    
    return render(request, 'login.html', {})

# User logout view
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

# User registration view
def register_user(request):
    if request.method == "POST":
        registration_form = SignUpForm(request.POST)
        if registration_form.is_valid():
            user = registration_form.save()
            login(request, user)
            messages.success(request, "Registration successful... Please complete your profile info")
            return redirect('profile')
        else:
            for error in list(registration_form.errors.values()):
                messages.error(request, error)
            return redirect('register')
    else:
        registration_form = SignUpForm()
    
    return render(request, 'register.html', {'registration_form': registration_form})

# Account info view
def accountinfo(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            current_user = User.objects.get(id=request.user.id)
            accountinfo_form = AccountInfoForm(request.POST or None, instance=current_user)
            if accountinfo_form.is_valid():
                accountinfo_form.save()
                messages.success(request, "Account information updated successfully")
                return redirect('home')
        else:
            accountinfo_form = AccountInfoForm(instance=request.user)
        return render(request, "accountinfo.html", {'accountinfo_form': accountinfo_form})
    else:
        for error in list(accountinfo_form.errors.values()):
            messages.error(request, error)
        return redirect('home')

# Update User profile view 
def profile(request):
    if request.user.is_authenticated:
        current_user = UserProfile.objects.get(user__id=request.user.id)
        if request.method == 'POST':
            profile_form = ProfileForm(request.POST, instance=current_user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('home')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            profile_form = ProfileForm(instance=current_user)
        
        return render(request, 'profile.html', {'profile_form': profile_form})
    else:
        return redirect('login') 

# update account password view     
def password_update(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == "POST":
            form = UpdatePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "password updated successfully")
                login(request, current_user)
                return redirect('password_update')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect('password_update')
        else:
            form = UpdatePasswordForm(current_user)
            return render(request, "password_update.html", {'form': form})
    else:
        messages.success(request, "password updated successfully")
        return redirect('home')

# search view
def search(request):
    query = request.GET.get('searched')
    if query:
        results = Item.objects.filter(name__icontains=query)
    else:
        results = Item.objects.none()
    return render(request, 'search.html', {'results': results, 'query': query})
