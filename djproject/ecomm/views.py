
from math import prod
from tkinter.messagebox import NO
from traceback import print_tb
from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import redirect, render
from sympy import Product,


from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
from .models import register_info, product, Category


def index(request):

    x = make_password('1234')
    print(x)

    print(check_password(
        '1234', 'pbkdf2_sha256$216000$Nw26i6wEpIRo$q00jvZ+9sLuwTmOwWVa8ahPFI/YMEZBe7bcyExKSECg='))

    # try:
    #     if request.session['email']:
    #         c = request.session['email']
    #         username = register_info.objects.all()
    #     else:
    #         return render(request, 'home.html', {'c': c})
    # except:
    #     return render(request, 'home.html')
    # path = upload_image.objects.all()
    products = None
    # request.session.clear()
    if request.method == "POST":
        product_id = request.POST.get('cartid')
        remove = request.POST.get('minus')
        cartid = request.session.get('cart')
        if cartid:
            quantity = cartid.get(product_id)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cartid.pop(product_id)
                    else:
                        cartid[product_id] = quantity - 1
                else:
                    cartid[product_id] = quantity + 1

            else:
                cartid[product_id] = 1

        else:
            cartid = {}
            cartid[product_id] = 1
        request.session['cart'] = cartid
        print(request.session['cart'])
        return redirect('home')

    cat = Category.objects.all()
    cat_id = request.GET.get('category')
    print(cat_id)

    if cat_id:
        products = product.objects.filter(category_id=cat_id)
    else:
        products = product.objects.all()
    context = {
        'products': products,
        'cat': cat
    }
    # print(request.session.get('customer_email'))
    return render(request, 'home.html', context)


def contact(request):

    fetch_img = product.objects.all()

    return render(request, 'contact.html', {'fetch_img': fetch_img})


def save(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        gender = request.POST.get('gender')

        # fetch_info = register_info.objects.get(email=email)
        # if(fetch_info == email):

        save_info = register_info(firstname=fname, lastname=lname,
                                  mobile=mobile, password=password, gender=gender, email=email)
        save_info.save()

        return redirect('home')


def login(request):
    error_msg = None
    if request.method == "POST":
        emails = request.POST.get('email')
        print(emails)
        try:
            fetch_email = register_info.objects.get(email=emails)
            print(fetch_email)
            request.session['email'] = emails
            return redirect('home')
        except:
            error_msg = "invalid email"
            return render(request, 'contact.html', {'error_msg': error_msg})

        # c = register_info.getemail(emails)
        # print(c)
        # password = request.POST.get('password')

        # try:
        #
        #     print(fetch_info)
        #     # return fetch_info
        # except:
        #     return False
        # if fetch_info == emails:
        #     print("hhhhh")
        #     return HttpResponse("fetch_info")
        # else:
        #     return HttpResponse("byr")
        # # context = {
        # #     'fetch_info': fetch_info
        # # }

        return render(request, 'home.html')


def register(request):
    if request.method == "POST":
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        mobile = request.POST.get('mobile')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        password = request.POST.get('password')

        store_data = register_info(firstname=fname, lastname=lname,
                                   mobile=mobile, gender=gender, email=email, password=make_password(password))

        store_data.save()
        # request.session['email'] = email
        return redirect('home')


def login_info(request):
    error_msg = None

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            fetch_email = register_info.objects.get(email=email)
            if (fetch_email.email == email):
                flag = check_password(password, fetch_email.password)
                if flag:
                    request.session['email'] = fetch_email.email
                    request.session['firstname'] = fetch_email.firstname
                    return redirect('home')
                else:
                    error_msg = "Please Enter valid password"
                    return render(request, 'home.html', {'error_msg': error_msg})

        except:
            error_msg = "Please Enter valid  Email"
            return render(request, 'home.html', {'error_msg': error_msg})

        return HttpResponse(fetch_email.email, fetch_email.password)


def logout(request):
    request.session.clear()
    return redirect('home')



    
    


     



