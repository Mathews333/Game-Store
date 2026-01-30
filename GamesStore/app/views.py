from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import gamedetails, Cart, Wishlist, UserProfile



# =========================
# ADMIN AUTH & PAGES
# =========================

def adminlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'admin' and password == 'admin123':
            return redirect('adminpage')

        messages.error(request, "Invalid admin credentials")

    return render(request, 'adminlogin.html')


def adminpage(request):
    return render(request, 'adminpage.html')


def manageproduct(request):
    return render(request, 'manageproduct.html')


# =========================
# ADMIN – ADD PRODUCT
# =========================

def addproduct(request):
    if request.method == 'POST':
        gamedetails.objects.create(
            name=request.POST.get('name'),
            category=request.POST.get('category'),
            description=request.POST.get('description'),
            game_price=request.POST.get('game_price'),

            game_image=request.FILES.get('game_image'),
            game_logo=request.FILES.get('game_logo'),

            screenshot1=request.FILES.get('screenshot1'),
            screenshot2=request.FILES.get('screenshot2'),
            screenshot3=request.FILES.get('screenshot3'),
            screenshot4=request.FILES.get('screenshot4'),

            trailer=request.FILES.get('trailer'),
        )
        messages.success(request, "Game added successfully")
        return redirect('viewproduct')

    return render(request, 'addproduct.html')


# =========================
# ADMIN – VIEW / UPDATE / DELETE PRODUCTS
# =========================

def viewproduct(request):
    products = gamedetails.objects.all()
    return render(request, 'viewproduct.html', {'products': products})


def viewproductupdate(request, pk):
    product = get_object_or_404(gamedetails, pk=pk)

    if request.method == 'POST':
        product.name = request.POST['name']
        product.category = request.POST['category']
        product.description = request.POST['description']
        product.game_price = request.POST['game_price']

        if request.FILES.get('game_image'):
            product.game_image = request.FILES['game_image']

        if request.FILES.get('game_logo'):
            product.game_logo = request.FILES['game_logo']

        if request.FILES.get('screenshot1'):
            product.screenshot1 = request.FILES['screenshot1']

        if request.FILES.get('screenshot2'):
            product.screenshot2 = request.FILES['screenshot2']

        if request.FILES.get('screenshot3'):
            product.screenshot3 = request.FILES['screenshot3']

        if request.FILES.get('screenshot4'):
            product.screenshot4 = request.FILES['screenshot4']

        if request.FILES.get('trailer'):
            product.trailer = request.FILES['trailer']

        product.save()
        return redirect('viewproduct')

    return render(request, 'updateview.html', {'product': product})



def viewproductdelet(request, pk):
    product = get_object_or_404(gamedetails, pk=pk)
    product.delete()
    messages.success(request, "Game deleted successfully")
    return redirect('viewproduct')


# =========================
# USER AUTH
# =========================

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")

    return render(request, "user/register.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            auth_login(request, user)
            messages.success(request, "Login successful")
            return redirect("userpage")

        messages.error(request, "Invalid username or password")
        return redirect("login")

    return render(request, "user/login.html")


# =========================
# USER STORE & GAME PAGES
# =========================

def userpage(request):
    products = gamedetails.objects.all()
    return render(request, 'user/userpage.html', {'products': products})


def view_game(request):
    games = gamedetails.objects.all()
    return render(request, 'user/view_game.html', {'games': games})


def game_detail(request, id):
    game = get_object_or_404(gamedetails, id=id)
    return render(request, 'user/game_detail.html', {'game': game})


# =========================
# CART & WISHLIST
# =========================

@login_required
def add_to_cart(request, game_id):
    game = get_object_or_404(gamedetails, id=game_id)

    Cart.objects.get_or_create(
        user=request.user,
        game=game
    )

    return redirect('game_detail', id=game_id)

@login_required
def remove_from_cart(request, game_id):
    Cart.objects.filter(
        user=request.user,
        game_id=game_id
    ).delete()

    return redirect('view_cart')



@login_required
def add_to_wishlist(request, game_id):
    game = get_object_or_404(gamedetails, id=game_id)

    Wishlist.objects.get_or_create(
        user=request.user,
        game=game
    )

    messages.success(request, "Added to wishlist")
    return redirect('game_detail', id=game_id)


@login_required
def view_cart(request):
    items = Cart.objects.filter(user=request.user)
    return render(request, 'user/cart.html', {'items': items})


@login_required
def view_wishlist(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'user/wishlist.html', {'items': items})

@login_required
def add_to_wishlist(request, game_id):
    game = get_object_or_404(gamedetails, id=game_id)

    Wishlist.objects.get_or_create(
        user=request.user,
        game=game
    )

    return redirect('game_detail', id=game_id)

@login_required
def view_wishlist(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'user/wishlist.html', {'items': items})


@login_required
def remove_from_wishlist(request, game_id):
    Wishlist.objects.filter(
        user=request.user,
        game_id=game_id
    ).delete()

    return redirect('view_wishlist')


@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'user/profile.html', {'profile': profile})

