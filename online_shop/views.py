# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from forms import customer_data_form, product_data, product_edit
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from .models import CustomerProfile, customer_category as Customer_Cat, UserAccountActivation, Group_ProductCategory_Relationship, product_category, Products, Order, OrderItems, product_discount
from pinchi_online_shop import settings
from email.mime.multipart import MIMEMultipart
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import random
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from datetime import datetime
from .serializers import ProductSerializer, OrderSerializer
import json

# Create your views here.
def customer_signup_form(request):
    if request.user.is_authenticated:
        return redirect(index)
    if request.method == 'POST':
        data_form = customer_data_form(request.POST)
        if data_form.is_valid():
            email = data_form.cleaned_data.get('email')
            password = data_form.cleaned_data.get('password')
            first_name = data_form.cleaned_data.get('first_name')
            last_name = data_form.cleaned_data.get('last_name')
            phone_no = data_form.cleaned_data.get('phone_no')

            if not User.objects.filter(username=email):
                user_obj = User.objects.create_user(email, email, password, last_name=last_name, first_name=first_name)
                user_obj.is_active = 0
                user_obj.save()

                customer_category = Customer_Cat.objects.filter(start_order_point=0)
                if customer_category:
                    cat_obj = Customer_Cat.objects.get(start_order_point=0)
                else:
                    cat_obj = None

                profile_obj = CustomerProfile()
                profile_obj.user = user_obj
                profile_obj.phone_no = phone_no
                profile_obj.customer_category = cat_obj
                profile_obj.save()

                random_string = random.randint(1000000000000, 9999999999999)

                accactivate_obj = UserAccountActivation()
                accactivate_obj.user = user_obj
                accactivate_obj.random_string = random_string
                accactivate_obj.is_activate = False
                accactivate_obj.save()

                # send email
                subject = "Welcome To Pinchi Inc Online Shop"
                message = "Dear "
                email_from = settings.EMAIL_HOST_USER
                email_to = user_obj.email

                host = request.META['HTTP_HOST']
                link = "http://" + str(host) + "/activate/?id=" + str(random_string)

                html_content = render_to_string('email/activate_email.html', {"link": link, "user_obj": user_obj})

                msg = EmailMultiAlternatives(subject, message, email_from, [email_to,], cc=[])
                msg.attach_alternative(html_content, "text/html")
                related = MIMEMultipart("related")
                # msg.attach(related)
                msg.mixed_subtype = "related"

                msg.send(fail_silently=False)

            return render(request, 'registration/customer_signup.html',
                          {'success_msg': "You will receive an activation email to complete the Registration Process."})
        else:
            return render(request, 'registration/customer_signup.html', {'form': data_form, 'first_name': request.POST.get('first_name', ''),
                                                                         'last_name': request.POST.get('last_name',''), 'email': request.POST.get('email',''),
                                                                         'phone_no': request.POST.get('phone_no', '')})
    return render(request, 'registration/customer_signup.html')

def index(request):
    success_msg = None
    form = None
    fail_msg = None
    next = None

    all_products = Products.objects.all()
    all_products_serializer = ProductSerializer(all_products, many=True)

    try:
        all_orders = Order.objects.filter(user_id=request.user)
    except:
        all_orders = Order.objects.all()
    all_order_serializer = OrderSerializer(all_orders, many=True)

    if request.method == "POST":
        if request.user.is_authenticated:
            if(request.POST.get("source_call") == "product_creation"):
                data_form = product_data(request.POST)
                if data_form.is_valid():
                    data_form.save()
                    success_msg = "Product is created successfully."
                else:
                    form = data_form

            elif(request.POST.get("source_call") == "product_update"):
                product_obj = Products.objects.get(id=request.POST.get("product_id"))
                other_product_obj = Products.objects.filter(name=request.POST.get('name')).exclude(id=product_obj.id)
                if not other_product_obj:
                    data_form = product_edit(request.POST, instance=product_obj)
                    if data_form.is_valid():
                        data_form.save()
                        success_msg = "Product is updated successfully."
                    else:
                        form = data_form
                else:
                    fail_msg = "Product Name already exists."

            elif (request.POST.get("source_call") == "product_delete"):
                try:
                    product_obj = Products.objects.get(id=request.POST.get("product_id"))
                    product_obj.delete()
                    success_msg = "Product is deleted successfully."
                except:
                    fail_msg = "Cannot delete product."

    if request.method == "GET":
        if request.user.is_authenticated:
            next = request.GET.get('next', '')
    try:
        profile = CustomerProfile.objects.filter(user=request.user)
        assigned_department = False
        product_cat = None
        if profile:
            profile_obj = CustomerProfile.objects.get(user=request.user)
            if profile_obj.department:

                obj = Group_ProductCategory_Relationship.objects.get(department=profile_obj.department)
                if obj:
                    assigned_department = True
                    product_cat = product_category.objects.get(id=obj.product_category.id)

                    products = Products.objects.filter(product_category=obj.product_category.id)
                    serializer = ProductSerializer(products, many=True)
                    return render(request, 'shopping_card/index.html', {'assigned_department': assigned_department,
                                                                        'product_cat': product_cat,
                                                                        "success_msg": success_msg, "form": form,
                                                                        "fail_msg": fail_msg,
                                                                        'product_list': serializer.data, 'all_product': all_products_serializer.data, 'next': next, 'all_order': all_order_serializer.data})

        return render(request, 'shopping_card/index.html', {'assigned_department': assigned_department,
                                                            'product_cat': product_cat, "success_msg": success_msg, "form": form, "fail_msg": fail_msg,
                                                            'all_product': all_products_serializer.data, 'next': next, 'all_order': all_order_serializer.data})
    except:
        return render(request, 'shopping_card/index.html', {'all_product': all_products_serializer.data, 'next': next, 'all_order': all_order_serializer.data})

def login_view(request):
    if request.method == 'POST':
        try:
            user = authenticate(username=request.POST['email'], password=request.POST['password'])
            if user is not None:
                login(request, user)
        except:
            user = ''

        if user:
            return redirect(index)
        else:
            return render(request, 'registration/customer_signin.html', {'error_msg': 'Please fill email and password correctly.'})
    else:
        return render(request, 'registration/customer_signin.html')

def logout_view(request):
    logout(request)

def activate_account(request):
    if request.method == 'GET':
        if request.GET.get('id', ''):
            try:
                activate_obj = UserAccountActivation.objects.filter(random_string=request.GET.get('id'))
                if activate_obj:
                    activate_obj = UserAccountActivation.objects.get(random_string=request.GET.get('id'))

                    if activate_obj.is_activate:
                        return redirect(login_view)

                    activate_obj.user.is_active = True
                    activate_obj.user.save()

                    activate_obj.is_activate = True
                    activate_obj.activate_date = datetime.utcnow()
                    activate_obj.save()

                    return render(request, 'email/activation_success.html')
                else:
                    return HttpResponseNotFound("Page not found")

            except:
                return HttpResponseNotFound("Page not found")
        else:
            return HttpResponseNotFound("Page not found")

def check_item_discounts(customer_cat, product_category):
    return product_discount.objects.get(product_category=product_category, customer_category=customer_cat).discount_percent if product_discount.objects.filter(product_category=product_category, customer_category=customer_cat) else 0

def order_submit(request):
    if request.method == 'POST':
        data = dict()
        print(request.POST)
        items = json.loads(request.POST.get('items'))
        if len(items) > 0:
            order_no = "ORDER_"+datetime.strftime(datetime.utcnow(),"%Y%m%d%M%S")
            order_obj = Order()
            order_obj.user_id = request.user
            order_obj.order_date = datetime.utcnow()
            order_obj.order_no = order_no
            order_obj.order_status = "Draft"
            order_obj.save()

            customer_cat = None
            #check the user category
            profile = CustomerProfile.objects.filter(user=request.user)
            if profile:
                customer_cat = profile[0].customer_category

            total_amount = 0.0
            for item in items:
                product_obj= Products.objects.get(id=int(item.get('id')))
                if customer_cat:
                    discount = check_item_discounts(customer_cat, product_obj.product_category)
                    product_cost = (product_obj.original_price - (float(discount)/100) * product_obj.original_price) * int(item.get('count'))
                else:
                    discount = 0
                    product_cost = product_obj.original_price * int(item.get('count'))
                total_amount += product_cost

                order_item_obj = OrderItems()
                order_item_obj.order = order_obj
                order_item_obj.item_name = product_obj.name
                order_item_obj.item_price = product_obj.original_price
                order_item_obj.cost = product_cost
                order_item_obj.qty = int(item.get('count'))
                order_item_obj.discount_percent = discount
                order_item_obj.save()

            order_obj.total_amount = total_amount
            order_obj.save()


            data['success'] = 1
        else:
            data['success'] = 0
        return JsonResponse(data)
    else:
        return HttpResponseNotFound("Page not found")

def order_detail(request):
    data = dict()
    if request.method == 'GET' and request.user.is_authenticated:

        print(request.GET)
        order_id = int(request.GET.get('id'))
        order_obj = Order.objects.get(id=order_id)
        order_data = OrderSerializer(order_obj).data

        order_items = "<table class='table table-hover text-center'>" \
                      + "<thead class='text-uppercase'>"\
                      + "<tr>"\
                      + "<th scope='col'>Product Name</th>"       \
                      + "<th>Qty</th>"\
                      + "<th scope='col'>Original Price</th>"\
                      + "<th scope='col'>Discount %</th>"\
                      + "<th scope='col'>Cost</th>"\
                      + "</tr>"\
                      + "</thead><tbody>"\


        order_item_objs = OrderItems.objects.filter(order=order_obj)
        total_amount = 0.0
        for item_obj in order_item_objs:
            # product_obj = Products.objects.get(id=item_obj.item)
            total_amount += item_obj.cost

            order_items += "<tr>" \
                           + "<th class='td_class'>" + item_obj.item_name + "</th>" \
                           + "<th class='td_class'>" + str(item_obj.qty) + "</th>"\
                           + "<th class='td_class'>" + str(item_obj.item_price) + "</th>"\
                           + "<th class='td_class'>" + str(item_obj.discount_percent) + "</th>"\
                           + "<th class='td_class'>" + str(item_obj.cost) + "</th>" + "</tr>"

        order_items += "</tbody>" \
                        + "<tfoot class='text-uppercase'>"\
                        + "<tr>"\
                        + "<th scope='col'></th>"       \
                        + "<th></th>"\
                        + "<th scope='col'></th>"\
                        + "<th scope='col'>Total Price:</th>"\
                        + "<th scope='col td_class'>"+ str(total_amount) +"</th>"\
                        + "</tr>"\
                        + "</tfoot></table>"



        data['detail'] = {'order_ref': order_data.get('order_no'),
                          'order_by': request.user.first_name,
                          'order_date':  order_data.get('order_datetime'),
                          'order_items': order_items
                          }
        data['success'] = 1
        return JsonResponse(data)
    else:

        if request.POST.get('source_call', '') == "delete":
            order_id = request.POST.get('order_id')
            order_obj = Order.objects.get(id=int(order_id))
            order_obj.delete()
        elif request.POST.get('source_call', '') == "order_checkout":
            order_id = request.POST.get('order_id')
            contact_no = request.POST.get('contact_no')
            shipping_address = request.POST.get('shipping_address')
            if not contact_no:
                data['success'] = 0
                data['contact_error_msg'] = "This field is required."
                data['address_error_msg'] = ""
                return JsonResponse(data)
            if not shipping_address:
                data['success'] = 0
                data['address_error_msg'] = "This field is required."
                data['contact_error_msg'] = ""
                return JsonResponse(data)

            if contact_no:
                if len(contact_no) > 15:
                    data['success'] = 0
                    data['contact_error_msg'] = "Contact no is invalid."
                    data['address_error_msg'] = ""
                    return JsonResponse(data)
                if not str(contact_no).isdigit():
                    data['success'] = 0
                    data['contact_error_msg'] = "Contact no is invalid."
                    data['address_error_msg'] = ""
                    return JsonResponse(data)

            order_obj = Order.objects.get(id=int(order_id))
            order_obj.contact_no = contact_no
            order_obj.shipping_address = request.POST.get('shipping_address')
            order_obj.order_status = "Checkout"
            order_obj.save()

            customer_cat = None
            # check the user category
            profile = CustomerProfile.objects.filter(user=request.user)
            if profile:
                customer_cat = profile[0].customer_category

            # count the customer's orders
            orders = Order.objects.filter(user_id=request.user, order_status="Checkout")
            order_count = len(orders)

            customer_categories = Customer_Cat.objects.all()
            new_category = None
            for cat_obj in customer_categories:
                if (not cat_obj.end_order_point) and order_count >= cat_obj.start_order_point:
                    new_category = cat_obj
                elif order_count <= cat_obj.end_order_point and order_count >= cat_obj.start_order_point:
                    new_category = cat_obj

            if new_category and new_category != customer_cat:
                if profile:
                    profile[0].customer_category = new_category
                    profile[0].save()
                else:
                    profile_obj = CustomerProfile()
                    profile_obj.user = request.user
                    profile_obj.customer_category = new_category
                    profile_obj.save()

        data['success'] = 1
        return JsonResponse(data)

def user_detail(request):
    data = dict()
    if request.method == 'GET' and request.user.is_authenticated:
        print(request.GET)
        customer_cat = None
        phone_no = None
        # check the user category
        profile = CustomerProfile.objects.filter(user=request.user)
        if profile:
            customer_cat = profile[0].customer_category.category_name
            phone_no = profile[0].phone_no

        data['detail'] = {'customer_cat': customer_cat,
                          'username': request.user.username,
                          'email':  request.user.email,
                          'phone_no': phone_no,
                          'first_name': request.user.first_name,
                          'last_name': request.user.last_name
                          }
        data['success'] = 1
        return JsonResponse(data)
    else:
        return HttpResponseNotFound("Page not found")

