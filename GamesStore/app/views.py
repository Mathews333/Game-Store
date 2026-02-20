from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import (
    gamedetails,
    Cart,
    Wishlist,
    UserProfile,
    Library
)

# ✅ Vector AI imports
from .vector_utils import (
    recommend_similar_games,
    recommend_for_user
)

from .vector_utils import semantic_search, generate_embeddings_for_all_games

# ==========================================================
# ADMIN
# ==========================================================

def adminlogin(request):
    if request.method == "POST":
        if request.POST.get("username") == "admin" and request.POST.get("password") == "admin123":
            return redirect("adminpage")
        messages.error(request, "Invalid admin credentials")

    return render(request, "adminlogin.html")


def adminpage(request):
    return render(request, "adminpage.html")


def manageproduct(request):
    return render(request, "manageproduct.html")


# ==========================================================
# ADMIN – PRODUCTS
# ==========================================================

def addproduct(request):

    if request.method == "POST":

        game = gamedetails.objects.create(
            category=request.POST.get("category"),
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            game_price=request.POST.get("game_price"),
            game_image=request.FILES.get("game_image"),
            game_logo=request.FILES.get("game_logo"),
            screenshot1=request.FILES.get("screenshot1"),
            screenshot2=request.FILES.get("screenshot2"),
            screenshot3=request.FILES.get("screenshot3"),
            screenshot4=request.FILES.get("screenshot4"),
            trailer=request.FILES.get("trailer"),
        )

        # ⚡ Regenerate embeddings for all games
        from .vector_utils import generate_embeddings_for_all_games
        generate_embeddings_for_all_games(gamedetails)

        return redirect("viewproduct")

    return render(request, "addproduct.html")


def viewproduct(request):
    products = gamedetails.objects.all()
    return render(request, "viewproduct.html", {"products": products})


def viewproductupdate(request, pk):
    product = get_object_or_404(gamedetails, pk=pk)

    if request.method == "POST":
        product.name = request.POST.get("name")
        product.category = request.POST.get("category")
        product.description = request.POST.get("description")
        product.game_price = request.POST.get("game_price")

        if request.FILES.get("game_image"):
            product.game_image = request.FILES.get("game_image")

        product.save()

        # ⚡ Regenerate embeddings
        from .vector_utils import generate_embeddings_for_all_games
        generate_embeddings_for_all_games(gamedetails)

        return redirect("viewproduct")

    return render(request, "updateview.html", {"product": product})


def viewproductdelet(request, pk):
    product = get_object_or_404(gamedetails, pk=pk)
    product.delete()

    from .vector_utils import generate_embeddings_for_all_games
    generate_embeddings_for_all_games(gamedetails)

    return redirect("viewproduct")


# ==========================================================
# USER AUTH
# ==========================================================

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

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully")
        return redirect("login")

    return render(request, "user/register.html")


from django.contrib import messages

def user_login(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )

        if user:
            auth_login(request, user)
            messages.success(request, "Welcome back 👋")
            return redirect("userpage")

        messages.error(request, "Invalid credentials")

    return render(request, "user/login.html")

# ==========================================================
# STORE (AI ENABLED)
# ==========================================================
from .vector_utils import semantic_search
from .models import gamedetails, Library
def userpage(request, category=None):

    query = request.GET.get("q", "")
    products = gamedetails.objects.all()

    # Category filter
    if category:
        products = products.filter(category=category)

    # 🔥 Semantic Search
    if query:
      products = semantic_search(query, gamedetails)
    if category:
        products = products.filter(category=category)

    # 🔥 Personalized AI Recommendations
    recommended = []
    if request.user.is_authenticated:
        recommended = recommend_for_user(
            request.user,
            gamedetails,
            Library
        )

    return render(request, "user/userpage.html", {
        "products": products,
        "recommended": recommended,
        "categories": gamedetails.CATEGORY_CHOICE,
        "active_category": category,
        "search_query": query,
    })

@login_required
def game_detail(request, id):

    game = get_object_or_404(gamedetails, id=id)

    # 🔥 Similar Games AI
    similar_games = recommend_similar_games(game, gamedetails)

    return render(request, "user/game_detail.html", {
        "game": game,
        "similar_games": similar_games,
    })


# ==========================================================
# CART
# ==========================================================

@login_required
def add_to_cart(request, game_id):
    game = get_object_or_404(gamedetails, id=game_id)
    Cart.objects.get_or_create(user=request.user, game=game)
    messages.success(request, f"{game.name} added to cart 🛒")
    return redirect("view_cart")

@login_required
def view_cart(request):
    items = Cart.objects.filter(user=request.user)
    return render(request, "user/cart.html", {"items": items})


@login_required
def remove_from_cart(request, game_id):
    Cart.objects.filter(user=request.user, game_id=game_id).delete()
    return redirect("view_cart")


# ==========================================================
# WISHLIST
# ==========================================================

@login_required
def add_to_wishlist(request, game_id):
    game = get_object_or_404(gamedetails, id=game_id)
    Wishlist.objects.get_or_create(user=request.user, game=game)
    return redirect("game_detail", id=game_id)


@login_required
def view_wishlist(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, "user/wishlist.html", {"items": items})


@login_required
def remove_from_wishlist(request, game_id):
    Wishlist.objects.filter(user=request.user, game_id=game_id).delete()
    return redirect("view_wishlist")


# ==========================================================
# CHECKOUT
# ==========================================================

@login_required
def checkout(request, game_id):

    game = get_object_or_404(gamedetails, id=game_id)

    if Library.objects.filter(user=request.user, game=game).exists():
        messages.info(request, "You already own this game.")
        return redirect("library")

    if request.method == "POST":
        Library.objects.create(user=request.user, game=game)
        Cart.objects.filter(user=request.user, game=game).delete()

        messages.success(request, "Purchase successful!")
        return redirect("library")

    return render(request, "user/checkout.html", {"game": game})


# ==========================================================
# LIBRARY
# ==========================================================

@login_required
def library(request):
    games = Library.objects.filter(user=request.user)
    return render(request, "user/library.html", {"games": games})


# ==========================================================
# PROFILE
# ==========================================================

@login_required
def user_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    games_owned = Library.objects.filter(user=request.user).count()
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    cart_count = Cart.objects.filter(user=request.user).count()

    return render(request, "user/profile.html", {
        "profile": profile,
        "games_owned": games_owned,
        "wishlist_count": wishlist_count,
        "cart_count": cart_count,
    })

@login_required
def buy_now(request, game_id):
    return redirect("checkout", game_id=game_id)