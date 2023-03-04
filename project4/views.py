from django.shortcuts import redirect, render
from app4.models import slider, banner_area, Main_Category, Product, Category,Color,Brand
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Min
from django.contrib.auth.decorators import login_required
from cart.cart import Cart





def base(request):
    return render(request, 'main/base2.html')


def index(request):
    sliders = slider.objects.all().order_by('-id')[0:3]
    banners = banner_area.objects.all().order_by('-id')[0:3]

    main_category = Main_Category.objects.all()
    product = Product.objects.filter(section__name = "Top Deal Of The Day")


    context = {
        'sliders' : sliders,
        'banners' : banners,
        'main_category' : main_category,
        'product' : product,
    }
    return render(request, 'main/index.html' ,context)

def product_detail(request,slug):
    product = Product.objects.filter(slug = slug)
    if product.exists():
        product = Product.objects.get(slug = slug)
    else:
        return redirect('404')

    context = {
        'product' : product,
    }


    return render(request, 'product/product_detail.html',context)


def error_404(request):
    return render(request, 'product/error.html')


def my_account(request):
    return render(request, 'account/my_account.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')


        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already exists')
            return redirect('login')


        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email-Id is already exists')
            return redirect('login')
       

        user = User(
            username = username,
            email = email,
            
        )
        user.set_password(password)
        user.save()
        return redirect('login')
       
    # return render(request, 'account/my_account.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username = username,password = password)
        if user is not None:

            # login(request,user)
            return redirect('index')
        else:
            messages.error(request, 'Email and password are invalid')
            return redirect('login')


@login_required(login_url='/accounts/login/') 
def my_profile(request):
    return render(request, 'profile/my_profile.html')


    
def profile_update(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        user = User.objects.get(id = user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request, 'Profile are successfully Updated')
        return redirect(my_profile)

    # return redirect(my_profile)
  
def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')

def userask(request):
    return render(request, 'main/userask.html')

def whishlist(request):
    return render(request, 'main/whishlist.html')


def product(request):
    category = Category.objects.all()
    product = Product.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()

    min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))
    ColorId = request.GET.get('colorId')
    
    FilterPrice = request.GET.get('FilterPrice')
    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        product = Product.objects.filter(price__lte = Int_FilterPrice)

    elif ColorId:
        product = Product.objects.filter(color=ColorId)
    else:
        product = Product.objects.all()



    context = {
        'category' : category,
        'product' : product,
        'min_price' : min_price,
        'max_price' : max_price,
        'FilterPrice' : FilterPrice,
        'color' : color,
        'brand': brand,
    }
    
    return render(request, 'product/product.html',context)


def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')

    product_num = request.GET.getList(product_num)
    brand = request.GET.getList('brand[]')

    allProducts = Product.objects.all().order_by('-id').distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(Categories__id__in=categories).distinct()

    if len(product_num) > 0:
        allProducts = allProducts.all().order_by('-id')[0:1]

    if len(brands) > 0:
        allProducts = allProducts.filter(Brand__id__in=brands).distinct()

    
    t = render_to_string('ajax/product.html', {'product': allProducts})

    return JsonResponse({'data': t})





@login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    return render(request, 'cart/cart.html')


def checkout(request):
    return render(request, 'cart/checkout.html')
