from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AccountInfoForm, UpdatePasswordForm, ProfileForm, RatingForm
from .models import Item, Category, UserProfile, Rating
from django.contrib.auth.models import User
from django.db.models import Q
import json
from django.http import JsonResponse
from cart.cart import Cart
from payment.models import ShippingAddress
from payment.forms import ShippingForm
from django.db.models import Avg




# Display details of a single item
def item(request, pk):
    item = get_object_or_404(Item, id=pk)
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = RatingForm(request.POST)
            if form.is_valid():
                rating = form.cleaned_data['rating']
                Rating.objects.create(item=item, user=request.user, rating=rating)
                messages.success(request, "Thank you for your rating!")
                return redirect('store:item', pk=pk)
        else:
            messages.error(request, "You must be logged in to rate an item.")
            return redirect('store:login')  # Redirect to login page if user is not authenticated
    else:
        form = RatingForm()

    average_rating = item.get_average_rating()
    
    return render(request, 'store/item.html', {
        'item': item,
        'average_rating': average_rating,
        'rating_form': form,
    })

# Display all items
def home(request):
    items = Item.objects.all()
    for item in items:
        item.average_rating = item.get_average_rating()
    return render(request, 'store/home.html', {'items': items})

# Display the About page
def about(request):
    return render(request, 'store/about.html', {})

# Display all items in a category
def category(request, foo):
    foo = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name__iexact=foo)
        items = Item.objects.filter(category=category)
        return render(request, 'store/category.html', {'items': items, 'category': category})
    except Category.DoesNotExist:
        messages.error(request, "Category doesn't exist")
        return redirect('store:home')

# Display category summary page
def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'store/category_summary.html', {'categories': categories})

# User login view
def login_user(request):
    if request.method == "POST":
        # Retrieve username and password from POST request
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in
            login(request, user)
            
            # Deal with saving items in the cart
            user_profile = UserProfile.objects.get(user=request.user)
            saved_cart = user_profile.cart
            if saved_cart:
                # Load saved cart from user profile
                cart_json = json.loads(saved_cart)
                cart = Cart(request)
                
                # Add items from saved cart to the current session cart
                for key, value in cart_json.items():
                    cart.database_add(item=key, quantity=value)
            
            # Add success message and redirect to home
            messages.success(request, "Login successful.")
            return redirect('store:home')
        else:
            # Add error message and redirect to login page
            messages.error(request, "Invalid username or password.")
            return redirect('store:login')
    
    # Render the login page if the request method is not POST
    return render(request, 'store/login.html', {})

# User logout view
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('store:home')

# User registration view
def register_user(request):
    if request.method == "POST":
        registration_form = SignUpForm(request.POST)
        if registration_form.is_valid():
            user = registration_form.save()
            login(request, user)
            messages.success(request, "Registration successful... Please complete your profile info")
            return redirect('store:account')
        else:
            for error in list(registration_form.errors.values()):
                messages.error(request, error)
            return redirect('store:register')
    else:
        registration_form = SignUpForm()
    
    return render(request, 'store/register.html', {'registration_form': registration_form})

# Account info view
def accountinfo(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            current_user = User.objects.get(id=request.user.id)
            accountinfo_form = AccountInfoForm(request.POST or None, instance=current_user)
            if accountinfo_form.is_valid():
                accountinfo_form.save()
                messages.success(request, "Account information updated successfully")
                return redirect('store:home')
        else:
            accountinfo_form = AccountInfoForm(instance=request.user)
        return render(request, "store/accountinfo.html", {'accountinfo_form': accountinfo_form})
    else:
        for error in list(accountinfo_form.errors.values()):
            messages.error(request, error)
        return redirect('store:home')

#View to manage use profile, account info and shipping address
def account(request):
    if request.user.is_authenticated:
        current_user_profile = UserProfile.objects.get(user__id=request.user.id)
        shipping_user, created = ShippingAddress.objects.get_or_create(user_id=request.user.id)
        
        
        profile_form = ProfileForm(request.POST or None, instance=current_user_profile)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        accountinfo_form = AccountInfoForm(request.POST or None, instance=request.user)
        
        # Handle form submissions
        if request.method == 'POST':
            if 'save_profile' in request.POST:
                if profile_form.is_valid():
                    profile_form.save()
                    messages.success(request, "Your profile information is updated successfully.")
                    return redirect('store:account')

            if 'save_shipping' in request.POST:
                if shipping_form.is_valid():
                    shipping_form.save()
                    messages.success(request, "Your shipping address is updated successfully.")
                    return redirect('store:account')

            if 'save_accountinfo' in request.POST:
                if accountinfo_form.is_valid():
                    accountinfo_form.save()
                    messages.success(request, "Your account information is updated successfully.")
                    return redirect('store:account')

        context = {
            'profile_form': profile_form,
            'shipping_form': shipping_form,
            'accountinfo_form': accountinfo_form,
        }
        
        return render(request, "store/account.html", context)
    else:
        messages.error(request, "You must be logged in")
        return redirect('store:login')
 
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
                return redirect('store:password_update')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect('store:password_update')
        else:
            form = UpdatePasswordForm(current_user)
            return render(request, "store/password_update.html", {'form': form})
    else:
        messages.success(request, "password updated successfully")
        return redirect('store:home')

# search view
def search(request):
    query = request.GET.get('searched')
    if query:
        results = Item.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
    else:
        results = Item.objects.none()
    return render(request, 'store/search.html', {'results': results, 'query': query})   


# rate item view
def rate_item(request, pk):
    if request.user.is_authenticated:
        item = get_object_or_404(Item, id=pk)
        rating = request.POST.get('rating')

        if rating:
            try:
                rating = int(rating)
                if 1 <= rating <= 5:
                    # Update or create the rating for the item
                    Rating.objects.update_or_create(
                        item=item,
                        user=request.user,
                        defaults={'rating': rating}
                    )
                    
                    # Calculate the average rating
                    average_rating = Rating.objects.filter(item=item).aggregate(Avg('rating'))['rating__avg']
                    
                    # Return the updated average rating and success status
                    return JsonResponse({'success': True, 'average_rating': average_rating})
                else:
                    # Rating out of bounds
                    return JsonResponse({'success': False, 'error': 'Rating must be between 1 and 5'}, status=400)
            except ValueError:
                # Handle the case where the rating is not an integer
                return JsonResponse({'success': False, 'error': 'Invalid rating value'}, status=400)
        
        return JsonResponse({'success': False, 'error': 'No rating provided'}, status=400)
    else:
        messages.error(request, "You must be logged in to rate items.")
        return redirect('store:login')
