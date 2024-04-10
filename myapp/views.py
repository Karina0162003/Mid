import re
from datetime import datetime, timedelta, date
from django.http import Http404

from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.db import IntegrityError
import random
from django.db.models import QuerySet, Count, Sum
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template

otp_lst = []


# Create your views here.
# Create your views here.
def index(request):
    category_data = productcategory.objects.all()
    product_data = product.objects.all()
    cart_items = cart.objects.all()  # Fetch all cart items
    cart_count = cart_items.count()  # Count all cart items
    context = {
        "categories": category_data,
        "products": product_data,
        "cart_items": cart_items,  # Pass cart items to the context
        "cart_count": cart_count
    }
    return render(request, "index.html", context=context)


def about_us(request):
    return render(request, "about_us.html")


def contact(request):
    return render(request, "contact.html")


def ifo(request):
    return render(request, "ifo.html")


def info(request):
    return render(request, "info.html")


def blogs(request):
    return render(request, "blogs.html")


def blogs_details(request):
    return render(request, "blogs_details.html")


def sign_in(request):
    return render(request, "sign_in.html")


def otp(request):
    return render(request, 'otp.html')


def gen_otp():
    otp = 0
    num = random.randint(1000, 9999)
    timestamp = datetime.now()
    if num in otp_lst:
        otp_lst.append(num)
    else:
        otp = num
        otp_lst.append(otp)
    return otp, timestamp


def send_otp(request):
    otp, timestamp = gen_otp()
    request.session["otp"] = otp
    request.session["otp_timestamp"] = timestamp.timestamp()
    print("Your OTP number is :-", otp)
    email = request.session["useremail"]
    print(request.session["useremail"])
    subject = 'About Login for Revoultioninzing Agriculture'
    message = f"Hey, your login process is started on Revolutioninzing Agriculture and your OTP is: {otp}. Your OTP is valid for 5 minutes only."
    email_form = 'karinapatel615@gmail.com'
    cus = [email]
    send_mail(subject, message, email_form, cus)
    return redirect("otp")


def validate_otp(request):
    if request.method == "POST":
        if request.method == "POST":
            user_otp = int(request.POST.get("otp"))
            otp = int(request.session["otp"])
            email = request.session["useremail"]
            try:
                query = customer.objects.get(email=email)
            except:
                query = None

            timestamp = request.session.get("otp_timestamp", 0)
            current_timestamp = datetime.now().timestamp()
            if current_timestamp - timestamp <= 300:
                if otp == user_otp:
                    request.session["username"] = query.first_name
                    request.session["userid"] = query.id
                    request.session["useremail"] = query.email
                    request.session["userphone"] = query.contact
                    return redirect('index')
                # return render(request, "index.html")
                else:
                    messages.error(request, "OTP not matched")
                    return render(request, "otp.html")
            else:
                messages.error(request, "OTP has expired")
                return render(request, "otp.html")


def validate_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = customer.objects.get(email=email)
        except customer.DoesNotExist:
            messages.error(request, "When signing up, User Not Found")
            return redirect('sign_in')  # Redirect to sign-in page if user is not found

        # User found, proceed with sending OTP
        request.session["useremail"] = user.email
        # You may want to store additional user information in the session as needed
        # request.session["username"] = user.First_Name
        # request.session["phone"] = user.Contact

        # Send OTP
        send_otp(request)

        # Redirect to OTP verification page
        return render(request, "otp.html")

    # If request method is not POST, redirect to sign-in page
    return redirect('sign_in')


def logout(request):
    try:
        if request.session.is_empty():
            return render(request, "sign_in.html")
        else:
            try:
                user1 = request.session['userid']
                u1 = customer.objects.get(id=user1)
                del request.session['userid']
            except:
                u1 = None
        # return render(request, "login.html")
        return redirect("sign_in")
    except Exception as e:
        print(e)

    return redirect("loginView")


def sign_up(request):
    areadetails = area.objects.all()
    context = {

        'area': areadetails
    }
    return render(request, "sign_up.html", context)


def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        address = request.POST.get("address")

        if not first_name or first_name.isnumeric():
            messages.error(request, "First name is not valid")
            return render(request, "sign_up.html")

        if not last_name or last_name.isnumeric():
            messages.error(request, "Last name is not valid")
            return render(request, "sign_up.html")

        if len(contact) != 10 or not contact.isnumeric():
            messages.error(request, "Phone number is not valid")
            return render(request, "sign_up.html")

        if not contact.isnumeric():
            messages.error(request, "Phone number should only contain digits")
            return render(request, "sign_up.html")

        if address and not address.isnumeric():
            if any(char in ("#", "!", "@", "$", "%", "^", "&", "*", "~") for char in address):
                messages.error(request, "Address is not valid")
                return render(request, "sign_up.html")

        try:
            existing_user = customer.objects.get(email=email)
        except customer.DoesNotExist:
            existing_user = None

        if existing_user is not None:
            messages.error(request, "User with this email already exists. Please use a different email.")
            return redirect("sign_up")  # Redirect to "sign_up" to allow registration with a different email

        try:
            existing_contact = customer.objects.get(contact=contact)
        except customer.DoesNotExist:
            existing_contact = None

        if existing_contact is not None:
            messages.error(request, "User exists with that Contact number")
            return render(request, "sign_up.html")

        # Fix the indentation here
        new_user = customer(
            first_name=first_name,
            last_name=last_name,
            email=email,
            contact=contact,
            address=address,
        )
        new_user.save()

        messages.success(request, "You have successfully registered on Revolutionizing Agriculture")

        subject = 'About Registration for Revolutionizing Agriculture'
        message = f'Hi {first_name} {last_name}, you are successfully registered on Revolutionizing Agriculture'
        email_form = 'karinapatel615@gmail.com'
        cus = [email]
        send_mail(subject, message, email_form, cus)

        return render(request, "sign_in.html")
    else:
        messages.error(request, "Invalid request method")
        return render(request, "sign_up.html")


def dashboard(request):
    email = request.session["useremail"]
    try:
        query = customer.objects.get(email=email)
    except:
        query = None
    context = {
        'first_name': query.first_name,
        'last_name': query.last_name,
        'email': query.email,
        'contact': query.contact,
        'address': query.address,
    }
    return render(request, "dashboard.html", context)


def profile(request, id):
    # print(request.session["email"])
    email = request.session["useremail"]
    try:
        query = customer.objects.get(email=email)
    except:
        query = None
    context = {
        'first_name': query.first_name,
        'last_name': query.last_name,
        'email': query.email,
        'contact': query.contact,
        'address': query.address,
    }
    return render(request, "dashboard_info_edit.html", context)


def update(request, id):
    try:
        if request.session.is_empty():
            return render(request, "sign_in.html")
        else:
            try:
                if request.method == "POST":
                    fname = request.POST['fname']
                    lname = request.POST.get("lname")
                    email = request.POST.get("email")
                    phone = request.POST.get("contact")
                    add = request.POST.get("address")

                    try:
                        getcustomer = customer.objects.get(id=id)
                        getcustomer.first_name = fname
                        getcustomer.last_name = lname
                        getcustomer.email = email
                        getcustomer.contact = phone
                        getcustomer.address = add

                        getcustomer.save()
                        print("Hiii")
                        # return render(request, "index.html", context)
                        return redirect("index")
                    except:
                        print("Helloo")
                        messages.error(request, "your data is not updated please try again")
                        return render(request, "dashboard_info_edit.html")
                else:
                    print("elsee")
                    return render(request, "dashboard_info_edit.html")

            except:
                u1 = None
        print("Exceptt")
        return render(request, "dashboard_info_edit.html")
    except:
        pass
    return redirect('sign_in')


def cart_view(request):
    return render(request, "cart_view.html")


def checkout(request):
    return render(request, "checkout.html")


def dashboard_order(request):
    return render(request, "dashboard_order.html")


def dashboard_order_invoice(request):
    return render(request, "dashboard_order_invoice.html")


def productItems(request):
    return render(request, "productItems.html")


def products(request):
    return render(request, "products.html")


def product_details(request):
    return render(request, "product_details.html")


def subcategory(request, name):
    # Reconstruct the category name from URL parameter
    name_list = re.split('(?<=.)(?=[A-Z])', name)
    cat_name = " ".join(name_list)

    # Get all categories with the given name
    categories = productcategory.objects.filter(name=cat_name)

    # If no categories found, return 404
    if not categories:
        return render(request, 'subcategory.html')

    # Choose the first category or handle multiple categories as needed
    category = categories.first()

    # Fetch subcategories related to the category
    subcategory_data = productcategory.objects.filter(Subcategory=category).exclude(id=category.id)
    cart_count = cart.objects.count()

    if subcategory_data:
        context = {
            "subcategories": subcategory_data,
            "category": category,
            "cart_count": cart_count
        }
        return render(request, 'subcategory.html', context=context)
    else:
        # If no subcategories, fetch products related to the category
        food_data = product.objects.filter(Category=category)
        cart_count = cart.objects.count()
        context = {
            "category": category,
            "food_items": food_data,
            "cart_count": cart_count
        }
        return render(request, 'productItems.html', context=context)


def product_details(request, cat, name):
    global data, sub_3, sub_2
    name_list = re.split('(?<=.)(?=[A-Z])', name)
    print(name_list)
    food_name = name_list[0]
    if len(name_list) == 1:
        food_name = name_list[0]
    else:
        for name in name_list[1:]:
            food_name = food_name + " " + name

    print("name :", food_name)
    print(food_name)
    food_item_data = product.objects.get(name=food_name)
    print("cat is",food_item_data.Category)
    try:
        query2=productcategory.objects.get(name=food_item_data.Category)
        sub_2=query2.Subcategory
    except:
        query2=None
        sub_2=None
    try:
        query3=productcategory.objects.get(Subcategory=food_item_data.Category)
        sub_3 = query3.Subcategory

    except:
        query3=None
        sub_3=None
    print("query2 is ",sub_2)
    print("query3 is ",sub_3)
    if sub_2=="Rent Machinery" or sub_3=="Rent Machinery":
        data=False
        other_food_items_data = product.objects.filter(Category=food_item_data.Category).exclude(id=food_item_data.id)
        feedback_data = feedback1.objects.filter(product_name=food_item_data)
        print(feedback_data)
        cart_count = cart.objects.count()
        context = {
            "food_data": food_item_data,
            "other_food_items_data": other_food_items_data,
            "cart_count": cart_count,
            "feedback": feedback_data,
            "data": data

        }
        return render(request, "product_details.html", context=context)
    else:
        other_food_items_data = product.objects.filter(Category=food_item_data.Category).exclude(id=food_item_data.id)
        feedback_data = feedback1.objects.filter(product_name=food_item_data)
        print(feedback_data)
        data=True
        cart_count = cart.objects.count()
        context = {
            "food_data": food_item_data,
            "other_food_items_data": other_food_items_data,
            "cart_count": cart_count,
            "feedback" : feedback_data,
            "data":data

        }
        return render(request, "product_details.html", context=context)


def order_tracking(request):
    return render(request, "order_tracking.html")


def payment(request):
    return render(request, "payment.html")


def privacy_policy(request):
    return render(request, "privacy_policy.html")


def nested_cat(request):
    return render(request, "nested_cat.html")


def filterp(request, id):
    user = productcategory.objects.all()
    user2 = product.objects.filter(filter=id)
    userf = filter.objects.all()
    context = {
        'data1': user,
        'data2': user2,
        'dataf': userf
    }
    return render(request, "filterp.html", context)


def destroycart(request, id):
    # Get the cart entry with the given id
    query = cart.objects.get(id=id)

    # Delete the cart entry
    query.delete()

    # Redirect to the checkout page
    return redirect("checkout")


def cart_page(request):
    user_id = request.session.get('userid')
    if user_id:
        fetch_cart_data = cart.objects.filter(customer_name_id=user_id, product_status=1)
        cart_total = fetch_cart_data.aggregate(total_price=Sum('totalprice'))
        fetch_product_ids = fetch_cart_data.values_list('product_name_id', flat=True)
        fetch_product_data = product.objects.filter(id__in=fetch_product_ids)
        user_details = customer.objects.filter(id=user_id)
        cart_count = fetch_cart_data.count()
        context = {
            'cart': fetch_cart_data,
            'product': fetch_product_data,
            'user': user_details,
            'carttotal': cart_total['total_price'] if cart_total['total_price'] else 0,
            "cart_count": cart_count
        }
        return render(request, "cart_view.html", context)
    else:
        return redirect('sign_in')


def add_cart(request, id, qty):
    user_id = request.session.get('userid')
    if user_id:
        food_item = get_object_or_404(product, id=id)
        print("food item in cart is ",food_item)
        price = food_item.price
        try:
            query2 = productcategory.objects.get(name=food_item.Category)
            sub_2 = query2.Subcategory
            query4=productcategory.objects.get(name=sub_2)
        except:
            query2 = None
            sub_2 = None
            query4=None
        try:
            query3 = productcategory.objects.get(Subcategory=food_item.Category)
            sub_3 = query3.Subcategory

        except:
            query3 = None
            sub_3 = None
        print("query2 is ", sub_2)
        print("query3 is ", sub_3)
        print("query 4 is ",query4)
        try:
            if query4.name== "Rent Machinery":
                data=True
            else:
                data=False
        except:
            query4.name=""

        if query4.name=="Rent Machinery":

            foodid = product.objects.get(name=food_item)
            print("1")
            # print("food id is ", foodid.id)
            # query = rentmachinery.objects.filter(product_id=product(id=foodid.id))
            # print(query)
            booked_dates = rentmachinery.objects.filter(product_id=product(id=foodid.id))
            print(booked_dates)
            bdate_min = date.today().strftime('%Y-%m-%d')
            # Calculate maximum date (e.g., one year from today)
            bdate_max = (date.today() + timedelta(days=365)).strftime('%Y-%m-%d')
            print("1")
            query=rentmachinery.objects.filter(product_id=product(id=foodid.id))
            print(query)
            booked_dates = rentmachinery.objects.filter(product_id=product(id=foodid.id)).values_list('booked_date',flat=True)
            print(booked_dates)
            booked_days = [date.day for date in booked_dates]
            print("Booked days are", booked_days)

            context={
                'userid': user_id,
                'product_name': food_item,
                'price': food_item.price,
                'bdate_min': bdate_min,
                'bdate_max': bdate_max,
                # 'booked_dates': list(booked_dates)
            }
            return render(request,"booking_page.html",context)
        else:
            quantity = int(qty)
            total_price = price * quantity

            # Check if the requested quantity is valid
            if quantity <= 0:
                return HttpResponse("Invalid quantity")

            # Check if the requested quantity exceeds the available stock
            if quantity > food_item.ava_quantity:
                return HttpResponse("Requested quantity not available")

            try:
                cart_entry = cart.objects.get(product_name=food_item, customer_name=user_id, product_status=1)
                cart_entry.quantity += quantity
                cart_entry.totalprice += total_price
                cart_entry.save()
            except ObjectDoesNotExist:
                cart_entry = cart.objects.create(
                    product_name=food_item,
                    quantity=quantity,
                    product_status=1,
                    customer_name_id=user_id,
                    orderid=0,
                    totalprice=total_price
                )

            # Deduct the quantity from available stock
            food_item.ava_quantity -= quantity
            food_item.save()

            return redirect("cart_view")
    else:
        return redirect("sign_in")

def removeItem_cart(request, id):
    query = cart.objects.get(id=id)
    query.delete()
    return redirect("cart_view")


def destroy_cart(request, id):
    query = cart.objects.get(id=id)
    query.delete()
    return redirect("cart_view")


def search(request):
    if request.method == "POST":
        query = request.POST.get("search")
        if len(query) == 0:
            messages.error(request, "Please enter a product name to search")
            return redirect("search")
        elif len(query) > 30:
            user = productcategory.objects.all()
            context = {
                'data1': user
            }
            messages.error(request, "Your search query is too long!")
            return render(request, "search.html", context)
        else:
            user2 = product.objects.filter(name__icontains=query)
            user3 = product.objects.filter(description__icontains=query)
            user31 = product.objects.filter(
                Category__name__icontains=query)  # Use Category__name instead of category_name
            user4 = user2.union(user3, user31)
            user = productcategory.objects.all()
            context = {
                'data1': user,
                'data2': user4,
                'query': query
            }
            return render(request, "search.html", context)
    else:
        messages.error(request, "Please use the search form to submit a query")
        return redirect("search")


def checkout(request):
    global customer_id
    try:
        customer_id = request.session['userid']
        address_data = request.session['address']
    except KeyError:
        address_data = None

    area_name = area.objects.all()
    print(address_data)

    cart_items = cart.objects.count()
    user = request.session['userid']
    fee = 20
    carttotal = cart.objects.filter(customer_name=user, product_status=1).aggregate(Sum('totalprice'))[
        'totalprice__sum']
    carttotal = carttotal + fee if carttotal else fee  # Ensure carttotal is not None

    print(carttotal)

    if cart_items > 0:
        user_cart_items = cart.objects.filter(customer_name=user, product_status=1)
        print(user_cart_items)
        cart_count = cart.objects.count()
        context = {
            "cart_items": user_cart_items,
            "total_price": carttotal,
            "cart_count": cart_count,
            'packfees': fee,
            'address_data': address_data,
        }

        # Create a sales order instance with the calculated total amount
        sales_order = salesorder.objects.create(
            delivery_address=address_data,
            iscancel=False,
            totalamount=carttotal,  # Assign the calculated total amount here
            customer_name_id=customer_id,  # Assign customer_id directly
            order_status="Confirm",
            payment_status=False,  # Default payment status
            paymentmode="",  # Default payment mode
        )

        # Process the cart items and create corresponding sales order details
        for cart_item in user_cart_items:
            salesorder_detail.objects.create(
                salesorder_name=sales_order,
                product_name=cart_item.product_name,
                quantity=cart_item.quantity
            )

        return render(request, "checkout.html", context)

    return redirect("cart")


def placeorder(request):
    if request.method=="POST":
        # if request.POST.get('paypal'):
        reciver_name=request.POST.get("c_name")
        request.session['username']=reciver_name
        customer_id=request.session["userid"]
        reciver_phone=request.POST.get("c_phone")
        address=request.POST.get("c_address")
        print("address",address)
        if address is not None:
            # address_data=Address.objects.filter(id=address)
            # print("address data is",address_data)
            # area_pincode = address_data.first().Area_Pincode.Name
            # print("Area pincode is:", area_pincode)
            payment_type=request.POST.get("payment_type")
            if not reciver_name or not reciver_name.strip() or reciver_name.isdigit():  # Checking if name is empty or only whitespace
                messages.error(request,"Name is not valid")
                return redirect("checkout")
            # Validate phone
            if not reciver_phone or not reciver_phone.isdigit() or len(reciver_phone) != 10:
                messages.error(request,"Phone number must contain 10 digits")
                return redirect("checkout")
            fee = 20
            carttotal = cart.objects.filter(customer_name=customer_id, product_status=1).aggregate(Sum('totalprice'))[
                'totalprice__sum']
            carttotal = carttotal + fee
            print(carttotal)
            if payment_type=="Cash On Delivery":
                mode=False
            elif payment_type=="Card":
                print("88888888")
                print('paypal')
                print("88888888")

            else:
                mode=True
            orderquery = salesorder(iscancel=0, totalamount=carttotal,
                                    customer_name=customer(id=customer_id), payment_status=mode,
                                paymentmode=payment_type)

            orderquery.save()
            # print(orderquery)
            lastid = salesorder.objects.latest('id').pk
            print(lastid)
            sale_data=salesorder.objects.get(id=lastid)
            order_status=Order_Status(salesorder_id=salesorder(id=lastid),status=1)
            order_status.save()
            fetchcartdata = cart.objects.filter(customer_name=customer(id=customer_id))
            for ob in fetchcartdata:
                ob.product_status = 0
                ob.orderid = lastid
                ob.save()
                pid = ob.product_name
                quan = ob.quantity
                query = salesorder_detail(salesorder_name=salesorder(id=lastid), quantity=quan,
                                        product_name=pid)
                query.save()
            cart_count = cart.objects.count()
            print(cart_count)
            if(payment_type=="Cash On Delivery"):
                today = datetime.today()
                context={
                    'lastpid':lastid,
                    'datetime':sale_data,
                    "cart_count" : cart_count
                }
                fetchcartdata.delete()
                return render(request,"thanku.html",context)
        
    else:
        return redirect("cart_view")


def thanku(request):
    return render(request, 'thanku.html')


def dashboard_info_edit(request):
    return render(request,"dashboard_info_edit.html")

def orderhistory(request):
    try:
        user_id = request.session['userid']
        orders = salesorder.objects.filter(customer_name=user_id).order_by('-id')
        print(orders)
          # Corrected to print order_statuses
        cart_count = cart.objects.count()
        context = {
            'data': orders,
            'cart_count': cart_count
        }
       
        return render(request, "dashboard_order.html", context)
    except KeyError:
        # Handle KeyError if 'userid' is not found in session
        return render(request, "dashboard_order.html")


def orderdetails(request, id):

    try:

        global mode

        user1 = request.session['userid']
        print("1")
        sale_order = salesorder.objects.get(id=id)
        print("2")
        print(sale_order)
        print("4")
        fetchcartdata = salesorder_detail.objects.filter(salesorder_name=id)
        print("cart : " + str(fetchcartdata))
        print("5")
     
        fetchpid = salesorder_detail.objects.filter(salesorder_name=id).values('product_name')

        print(fetchpid)
        print("6")
        print(fetchpid)
        print(fetchcartdata)
        fetchproductdata = product.objects.filter(id__in=fetchpid)
        print("products: " + str(fetchproductdata))
       
        print("n")
        order_statuses = Order_Status.objects.filter(salesorder_id=id).order_by('id')
        print("nisu")

        cart_count = cart.objects.count()
        context = {
            'cart': fetchcartdata,
            'order_status': order_statuses,
            'product': fetchproductdata,
            'orderid': id,
            'cart_count': cart_count,
            'total_price': sale_order.totalamount,
           
        }
        return render(request, "order_details.html", context)
    except:
        u1 = None
    
    
def order_details(request):
    return render(request,"order_details.html")

def feedback(request):
    return render(request,"feedback.html")


def feedback(request, id, id2):
    customer_id = request.session.get("userid")
    print(customer_id)
    try:
        query = feedback1.objects.get(saleorder_name_id=id, customer_name_id=customer_id, product_name_id=id2)
        print(query)
    except feedback1.DoesNotExist:
        query = None
    print(query)
    if query is None:
        food_item = product.objects.get(id=id2)
        print(food_item.name)
        context = {
            'orderid': id,
            'prod': food_item.name,
            'prodid': id2
        }
    else:
        print(query.product_name)
        print(query.saleorder_name)
        print(query.customer_name)
        print(query.description)
        context = {
            'orderid': id,
            'prod': query.product_name,
            'prodid': id2,
            'description': query.description
        }
    return render(request, "feedback.html", context)

def send_feed(request, id, id2):
    customer_id = request.session["userid"]
    description = request.POST.get("feedback")
    try:
        # Check if feedback already exists for the specified sales order, customer, and product
        query = feedback1.objects.get(
            saleorder_name_id=id,
            customer_name_id=customer_id,
            product_name_id=id2
        )
    except feedback1.DoesNotExist:
        query = None

    if query is None:
        # If feedback doesn't exist, create a new instance of feedback1
        order_detail_id = id
        product_id = id2

        # Create a new instance of feedback1 with the provided details
        query = feedback1.objects.create(
            rating=1,  # Set default rating or update as necessary
            saleorder_name_id=order_detail_id,
            customer_name_id=customer_id,
            product_name_id=product_id,
            description=description
        )
        messages.success(request, "Thank you for giving feedback")
    else:
        # If feedback already exists, update the existing feedback's description
        query.description = description
        query.save()
        messages.success(request, "Feedback updated successfully")

    # Redirect to the order history page after processing feedback
    return redirect("orderhistory")


def invoice(request, id):
    try:
        user1 = request.session.get('userid')
    except KeyError:
        user1 = None
    
    if user1 is not None:
        user1 = request.session['userid']
        fetchcartdata = salesorder_detail.objects.filter(salesorder_name_id=id)
        sale_order = salesorder.objects.get(id=id)
        fetchpid = salesorder_detail.objects.filter(salesorder_name_id=id).values('product_name')
        fetchproductdata = product.objects.filter(id__in=fetchpid)
        order_statuses = Order_Status.objects.filter(salesorder_id=id).order_by('id')
        orders = salesorder.objects.filter(customer_name=user1).order_by('-id')
        cart_count = cart.objects.count()
        # fetchcartdata = salesorder_detail.objects.filter(salesorder_name_id=id)
        # print(id)
        # carttotal = cart.objects.filter(orderid=id).aggregate(Sum('totalprice'))
        # print(carttotal)
        today = datetime.today()
        # fetchpid = fetchcartdata.values_list('product_name', flat=True)
        # print(fetchpid)
        # print(fetchcartdata)
        s1 = salesorder.objects.get(id=id)
        # print(s1.totalamount)
        # ct = s1.totalamount
        da = s1.delivery_address
        dat = s1.date
        # fetchproductdata = product.objects.filter(id__in=fetchpid)
        # print(fetchproductdata)
        userdetails = customer.objects.filter(id=user1)
        user = productcategory.objects.all()
        context = {
            'cart': fetchcartdata,
            'product': fetchproductdata,
            'user': userdetails,
            'orderid': id,
            'daddress': da,
            'dat': dat,
            'dateq': today,
            'data1': user
        }
        temp = get_template('dashboard_order_invoice.html')
        html = temp.render(context)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error generating PDF")
    else:
        return redirect("sign_in")

def booking_page(request):
    food_item="Z N D T1000"
    foodid=product.objects.get(name=food_item)
    print("1")
    print("food id is ",foodid.id)
    query = rentmachinery.objects.filter(product_id=product(id=foodid.id))
    print(query)
    booked_dates = rentmachinery.objects.filter(product_id=product(id=foodid.id))
    print(booked_dates)
    return render(request,"booking_page.html")

def book_machinery(request):
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        foodid = product.objects.get(name=product_name)
        booked_dates = rentmachinery.objects.filter(product_id=product(id=foodid.id)).values_list('booked_date',                                                                      flat=True)
        print(booked_dates)
        booked_days = [date.day for date in booked_dates]
        print("Booked days are in ", booked_days)
        price = request.POST.get("price")
        userid = request.session.get('userid')
        bdate = request.POST.get("bdate")
        bdate_datetime = datetime.strptime(bdate, '%Y-%m-%d')

        # Extract the day number
        day_number = bdate_datetime.day
        print("the date number is : ",day_number)
        time_duration = "24Hours"

        # Create or get the product object
        for i in booked_days:
            if i==day_number:
                messages.error(request,"Machine already booked on this date. Please choose another date.")
                return render(request,"booking_page.html")
        product_obj, created = product.objects.get_or_create(name=product_name)
        # Create the rentmachinery object
        rent_obj = rentmachinery.objects.create(
            product_id=product_obj,
            customer_id=customer(id=userid),
            time_duration=time_duration,
            rent_amount=price,
            booked_date=bdate
        )
        messages.success(request, "Machine booked successfully!")
        return redirect("index") 
    
def bookmachinery(request):
    try:
        user_id = request.session.get('userid')  # Using get method to avoid KeyError
        if user_id:
            rented_machinery = rentmachinery.objects.filter(customer_id=user_id).order_by('-booked_date')
            print(rented_machinery)
            context = {
                'rented_machinery': rented_machinery,
                'user_id': user_id,  # Pass user ID to template
            }
            return render(request, "book_order.html", context)
        else:
            # Redirect user to login page or handle not logged-in scenario
            return render(request, "sign_in.html")  # Redirect to login page
    except Exception as e:
        # Log the exception or handle it appropriately
        print(e)
        return render(request, "book_order.html") 


def delete_order(request, id):
    try:
        sale_order = salesorder.objects.get(id=id)
        # sale_order.delete()
        sale_order.iscancel = True
        sale_order.save()
        messages.success(request, "Order deleted successfully.")
    except salesorder.DoesNotExist:
        messages.error(request, "Order does not exist.")
    return redirect("orderhistory")