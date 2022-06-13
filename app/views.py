from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from requests import request
from .models import Ticket_types, addevent,Payment
from .forms import addeventForm
from django.views import View
from django.views.generic import TemplateView,View,DetailView
import stripe
from django.conf import settings
from django.core.paginator import Paginator 
from django.contrib.auth.decorators import login_required



 # Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY 

# class MytemplateView(TemplateView):
#     template_name = 'app/index.html'
#     def get_context_data(self,**kwargs):
#         context = super(MytemplateView, self).get_context_data(**kwargs)
def MytemplateView(request):
    event_list = addevent.objects.all()

    #pagination
    p = Paginator(addevent.objects.all(),5)
    page = request.GET.get('page')
    events = p.get_page(page)   
    # context['all_events'] = addevent.objects.all()
    context={
        'all_events': addevent.objects.all(),
        'events' : events
    }
    return render(request,"app/index.html",context)



#logout view
class LogoutView(View):
    def get(self,request):
        messages.info(request,"You Logged out")
        logout(request)
        
        return HttpResponseRedirect('/')



def detailedview(request,pk):
    event_details=addevent.objects.filter(id=pk)
    print(event_details)
    context={
        'event_details':event_details
    }
    return render(request,"app/addevent_detail.html",context)




#event view
@login_required
def event(request):
    if request.method == "POST":
        form = addeventForm(request.POST,request.FILES)
        if form.is_valid():
            # event_name=form.cleaned_data.get('event_name')
            form.save()
            return redirect('/')
        else:
            messages.error(request,"Enter the correct event")
            return render(request,"app/addevent.html",context={"addeventForm":form})
    else:
        form=addeventForm()
        return render(request,"app/addevent.html",context={"addeventForm":form})


# user login

def user_login(request):
        if request.method == "POST":
            form = AuthenticationForm(request,data=request.POST)
            if form.is_valid():
                username=form.cleaned_data.get('username')
                password=form.cleaned_data.get('password')
                user=authenticate(username=username,password=password)
                print(user)
                if user is not None:
                    messages.info(request,"Login Successfull")
                    login(request,user)
                    return redirect("event")
                # else:
                #     messages.error(request,"Invalid login")
                #     return render(request,"app/login.html",context={"login_form":form})
                
            else:
                    messages.error(request,"Invalid Credentials")
                    return render(request,"app/login.html",context={"login_form":form})
        else:
            form=AuthenticationForm()
            return render(request,"app/login.html",context={"login_form":form})
    # except Exception as e:
    #     print(e)
    #     form=AuthenticationForm()
    #     return render(request,"app/login.html",context={"login_form":form})



class CheckPaymentView(TemplateView):
    print("payment view")
    template_name = "app/silver.html"
    def get_context_data(self, **kwargs):
        print("inside get method")
        # product = Payment.objects.get(Ticket="Gold")
        prices = Payment.objects.filter(Ticket="Gold")
        context = super(CheckPaymentView, self).get_context_data(**kwargs)
        context.update({
            # "product": product,
            "prices": prices
        })  
        return context


class Successview(TemplateView):
    template_name = "app/success.html"


class CancelView(TemplateView):
    template_name = "app/cancel.html"


YOUR_DOMAIN = "http://127.0.0.1:8000"


class CreateCheckoutSessionView(View):
    print("checkoutview functn")
    def post(self, request, *args, **kwargs):
        print("inside post")
        price = Payment.objects.get(id=self.kwargs["pk"])
        print(price)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price':price.stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
        )
        return redirect(checkout_session.url)

    #! /usr/bin/env python3.6
# def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    # return 1400


# def create_payment(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.data)
#             # Create a PaymentIntent with the order amount and currency
#             intent = stripe.PaymentIntent.create(
#                 amount=calculate_order_amount(data['items']),
#                 currency='eur',
#                 automatic_payment_methods={
#                     'enabled': True,
#                 },
#             )
#             return jsonify({
#                 'clientSecret': intent['client_secret']
#             })
#         except Exception as e:
#             return jsonify(error=str(e)), 403
