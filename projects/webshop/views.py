from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.db import IntegrityError
from django.core.mail import send_mail
from django.utils.text import slugify


from .models.user import User
from .models.category import Category
from .models.product import Product
from .cart import Cart


#-----------------------------HOME AND CATEGORY LIST-----------------------------#

def homepage(request: HttpRequest, category_slug=None):
    error = request.session.get("error", None)
    if error is not None:
        del request.session["error"]

    success = request.session.get("success", None)
    if success is not None:
        del request.session["success"]

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {"error": error, "success": success,  "category": category,
               "products": products, "categories": categories}
    return render(request, "webshop/homepage.html", context)


def product_detail(request, slug, id, category_slug=None):
    product = get_object_or_404(Product, slug=slug, id=id, available=True)

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {"product": product, "categories": categories}
    return render(request, "webshop/product/product_detail.html", context)


def product_all(request, category_slug=None):
    error = request.session.get("error", None)
    if error is not None:
        del request.session["error"]

    success = request.session.get("success", None)
    if success is not None:
        del request.session["success"]

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {"error": error, "success": success,  "category": category,
               "products": products, "categories": categories}
    return render(request, "webshop/product/products.html", context)


def product_by_user(request: HttpRequest, id: int, category_slug=None):
    user = get_object_or_404(User.objects, id=id)
    product_by_user = Product.objects.filter(user=user)

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {"product_by_user": product_by_user, "categories": categories}
    return render(request, "webshop/product/product_by_user.html", context)


#-----------------------------PRODUCT ADD, UPDATE AND DELETE-----------------------------#


def product_add(request: HttpRequest):
    if request.method == "GET":
        user = request.session.get("user")
        if user is not None:
            category_list = Category.objects.all()
            context = {"categories": category_list}
            return render(request, "webshop/product/product_add.html", context)
        else:
            request.session["error"] = "Ne možete da dodate proizvod dok ne napravite nalog."
            return redirect("webshop:home")
    if request.method == "POST":
        new_product = Product()
        new_product.category = Category.objects.get(
            name=request.POST["category"])
        new_product.user = User.objects.get(id=request.session["user"]["id"])
        new_product.name = request.POST["p_name"]
        new_product.image = request.FILES["img"]
        new_product.description = request.POST["description"]
        new_product.price = request.POST["price"]
        new_product.slug = slugify(new_product.name)
        new_product.save()
        return redirect("webshop:product_detail", slug=new_product.slug, id=new_product.id)


def product_update(request: HttpRequest, id: int, slug: str):
    product_by_id = Product.objects.get(id=id, slug=slug)
    if request.method == "GET":
        category_list = Category.objects.all()
        context = {"product": product_by_id, "categories": category_list}
        return render(request, "webshop/product/product_update.html", context)
    if request.method == "POST":
        product_by_id.category = Category.objects.get(
            name=str(request.POST["e_category"]))
        product_by_id.name = request.POST["e_name"]
        old_image = request.POST["old_img"]
        if "e_img" in request.FILES:
            product_by_id.image = request.FILES["e_img"]
        else:
            product_by_id.image = old_image
        product_by_id.description = request.POST["e_description"]
        product_by_id.price = request.POST["e_price"]
        product_by_id.slug = slugify(product_by_id.name)
        product_by_id.save()
        return redirect("webshop:product_detail", slug=product_by_id.slug, id=product_by_id.id)


def product_delete(request: HttpRequest, product_id: int):
    selected_product = Product.objects.get(id=product_id)
    if selected_product.user.id != request.session["user"]["id"]:
        request.session["error"] = "Nije Vam dozvoljeno da obrišete ovaj proizvod."
        return redirect("webshop:home")

    selected_product.delete()
    request.session["success"] = "Uspešno ste obrisali proizvod."
    return redirect("webshop:home")


#-----------------------------CONTACT-----------------------------#

def contactpage(request: HttpRequest, category_slug=None):
    if request.method == "GET":
        error = request.session.get("error", None)
        if error is not None:
            del request.session["error"]
        success = request.session.get("success", None)
        if success is not None:
            del request.session["success"]

        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)

        context = {"error": error, "success": success,
                   "categories": categories}
        return render(request, "webshop/contactpage.html", context)

    if request.method == "POST":
        message_subject = request.POST["subject"]
        message_email = request.POST["ct_email"]
        message = request.POST["textarea"]
        send_mail(
            message_subject,
            message,
            message_email,
            ['nemanja.ilic0000@gmail.com']
        )

        request.session["success"] = "Uspešno poslata poruka."
        return redirect("webshop:home")


#-----------------------------USER REGISTER, LOGIN, LOGOUT-----------------------------#

def register(request: HttpRequest, category_slug=None):
    if request.method == "GET":
        error = request.session.get("error", None)
        if error is not None:
            del request.session["error"]
        success = request.session.get("success", None)
        if success is not None:
            del request.session["success"]

        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)

        context = {"error": error, "success": success,
                   "categories": categories}
        return render(request, "webshop/account/register.html", context)
    if request.method == "POST":
        new_user = User()
        new_user.first_name = request.POST["first_name"]
        new_user.last_name = request.POST['last_name']
        new_user.username = request.POST["username"]
        new_user.email = request.POST["email"]
        if request.POST["password"] == request.POST["password2"]:
            new_user.create_hashed_password(request.POST['password2'])
        else:
            request.session["error"] = "Lozinke nisu iste!"
            return redirect("webshop:register")
        try:
            new_user.save()
            request.session["user"] = new_user.to_dict()
            return redirect("webshop:home")
        except IntegrityError:
            request.session["error"] = f"Korisnik sa korisničkim imenom {request.POST['username']} već postoji."
            return redirect("webshop:register")


def login(request: HttpRequest, category_slug=None):
    if request.method == "GET":
        error = request.session.get("error", None)
        if error is not None:
            del request.session["error"]
        success = request.session.get("success", None)
        if success is not None:
            del request.session["success"]

        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)

        context = {"error": error, "success": success,
                   "categories": categories}
        if "user" in request.session:
            return redirect("webshop:home")
        else:
            return render(request, "webshop/account/login.html", context)
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.POST["login_username"])
            if user.verify_password(request.POST["login_password"]):
                request.session["user"] = user.to_dict()
                request.session["success"] = "Uspešno ste se prijavili."
                return redirect("webshop:home")
        except:

            request.session["error"] = "Korisničko ime ili lozinka nisu tačne."
            return redirect("webshop:login")


def logout(request: HttpRequest):
    user = request.session.get("user", None)
    if user is not None:
        request.session["success"] = "Uspešno ste se odjavili."
        del request.session["user"]
    return redirect("webshop:home")


#-----------------------------USER VIEW, UPDATE AND DELETE PROFILE-----------------------------#

def view_profile(request: HttpRequest, id: int, category_slug=None):
    try:
        error = request.session.get('error', None)
        if error is not None:
            del request.session['error']

        success = request.session.get('success', None)
        if success is not None:
            del request.session['success']

        user = User.objects.get(pk=id)
        product_by_user = Product.objects.filter(user=user)

        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)

        context = {"user": user, "error": error,
                   "success": success, "categories": categories, "product_by_user":product_by_user}
        return render(request, "webshop/account/profile.html", context)
    except:
        request.session["error"] = f"Ne postoji korisnik sa ID: '{id}'."
        return redirect("webshop:home")


def edit_profile(request: HttpRequest, id: int, category_slug=None):
    if request.session["user"]["id"] != id:
        request.session["error"] = "Ne možete ažurirati ovaj profil."
        return redirect("webshop:view_profile", id=id)
    try:
        selected_user = User.objects.get(id=id)
        if request.method == "POST":
            selected_user.first_name = request.POST["e_first_name"]
            selected_user.last_name = request.POST["e_last_name"]
            selected_user.username = request.POST["e_username"]
            selected_user.email = request.POST["e_email"]
            selected_user.save()
            request.session["user"] = selected_user.to_dict()
            request.session["success"] = "Uspešno ste ažurirali Vaš profil."
        success = request.session.get("success", None)
        if success is not None:
            del request.session["success"]

        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)

        context = {"user": selected_user,
                   "success": success, "categories": categories}
        return render(request, "webshop/account/edit_profile.html", context)
    except:
        request.session["error"] = f"Ne postoji korisnik sa ID '{id}'."
        return redirect("webshop:home")


def delete_profile(request: HttpRequest, id: int):
    if request.session["user"]["id"] == id:
        delete_user = get_object_or_404(User, id=id)
        delete_user.delete()
        request.session["success"] = f"Korisnik sa ID: {id} je uspešno obrisan."
        user = request.session.get("user", None)
        if user is not None:
            del request.session["user"]
        return redirect("webshop:home")
    else:
        request.session["error"] = "Nije dozvoljeno obrisati ovaj profil."
        return redirect("webshop:home")


#-----------------------------CART AND ORDERS-----------------------------#

def cart_add(request: HttpRequest, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect('webshop:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('webshop:cart_detail')


def cart_detail(request, category_slug=None):
    cart = Cart(request)

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'webshop/cart/cart_detail.html', {'cart': cart, "categories": categories})
