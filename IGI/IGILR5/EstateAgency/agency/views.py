import datetime
import os
import statistics

import django
import requests
import stripe
from django.contrib.auth.models import Group
from django.db.models import Q, Count
from django.template.context_processors import csrf
from django.template.defaultfilters import slugify
from django.template.response import TemplateResponse

from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.test import Client
from requests import get as get_request
from dateutil.relativedelta import relativedelta
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, UpdateView
import logging
from .forms import LoginUserForm, RegisterUserForm, AddRealtyForm, AdminAddRealtyForm, AdminUpdateRealtyForm, \
    UpdateRealtyForm, UpdateUserForm, ReviewForm
from .models import *
from .utils import get_ip_adress, get_info_user_by_ip, get_all_employees, get_all_clients, filter_sort_realties
from django.conf import settings
from django.contrib import messages
from django.db import connection
import matplotlib.pyplot as plt

main_logger = logging.getLogger('main')
def main(request):
    last_article = Article.objects.latest('created_at')
    context = {
        'last_article': last_article
    }
    return TemplateResponse(request, 'agency/main.html', context=context)


def users_realty(request):
    category = Category.objects.all()
    all_employees = get_all_employees()
    realties = Realty.objects.select_related('address').filter(~Q(owner__in=all_employees), landlord__isnull=True)
    realties = filter_sort_realties(request, realties)
    if request.user.is_authenticated:
        realties = realties.filter(~Q(owner=request.user))

    context = {
        'Agency' : False,
        'realties': realties,
        'cats': category,
    }
    return TemplateResponse(request, 'agency/realties.html', context)

def agency_realty(request):
    category = Category.objects.all()
    all_employees = get_all_employees()
    realties = Realty.objects.select_related('address').filter(landlord__isnull=True,  owner__in=all_employees)
    realties = filter_sort_realties(request, realties)
    if request.user.is_authenticated:
        realties = realties.filter(~Q(owner=request.user))

    context = {
        'Agency': True,
        'realties': realties,
        'cats': category,
    }
    return TemplateResponse(request, 'agency/realties.html', context)


def user_category_realties(request, category_slug):
    cat = Category.objects.get(slug=category_slug)
    category = Category.objects.all()
    info_user = get_info_user_by_ip(get_ip_adress(request))
    if 'city' in info_user:
        user_city = info_user['city']
    else:
        main_logger.error(f"Don't get ip of user: {request.user}")
        user_city = None
    all_employees = get_all_employees()
    realties = Realty.objects.select_related('address').filter(~Q(owner__in=all_employees), landlord__isnull=True,cat=cat)
    if request.user.is_authenticated:
        realties = realties.filter(~Q(owner=request.user))
    realties = filter_sort_realties(request, realties)
    realties_city_user = realties.filter(address__city=user_city)

    context = {
        'Agency': False,
        'cats':category,
        'cat_selected': cat,
        'realties': realties,
        'realtys_city_user': realties_city_user
    }
    return TemplateResponse(request, 'agency/category.html', context)


def agency_category_realties(request, category_slug):
    cat = Category.objects.get(slug=category_slug)
    category = Category.objects.all()
    info_user = get_info_user_by_ip(get_ip_adress(request))
    if 'city' in info_user:
        user_city = info_user['city']
    else:
        main_logger.error(f"Don't get ip of user: {request.user}")
        user_city = None
    all_employees = get_all_employees()
    realties = Realty.objects.select_related('address').filter(landlord__isnull=True, cat=cat,  owner__in=all_employees)
    if request.user.is_authenticated:
        realties = realties.filter(~Q(owner=request.user))
    realties = filter_sort_realties(request, realties)
    realtys_city_user = realties.filter(address__city=user_city)
    context = {
        'Agency' : True,
        'cats':category,
        'cat_selected': cat,
        'realties': realties,
        'realtys_city_user': realtys_city_user
    }
    return TemplateResponse(request, 'agency/category.html', context)

def realty(request, realty_slug):
    try:
        realty = Realty.objects.select_related('address').get(slug=realty_slug)
        reviews = realty.comments.all()
    except Realty.DoesNotExist as ex:
        main_logger.error(f"Don't find realty(realty slug: {realty_slug})")
        messages.add_message(request, messages.ERROR, f"Don't find realty(realty slug: {realty_slug})")
        return redirect('main')
    form = ReviewForm(request.POST or None)
    if form.is_valid() and not request.user.is_authenticated:
        messages.info(request, 'You must log in to your account to leave a review.')
        return redirect('login')

    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.realty = realty
        comment.rating = form.cleaned_data['rating']
        comment.save()
        messages.success(request, 'Your comment was added.')
        return redirect('realty', realty_slug=realty_slug)


    context = {
        'realty': realty,
        'form': form,
        'comments' : reviews

    }
    return TemplateResponse(request, 'agency/realty.html', context)


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'agency/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = {"title": "Login"}
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        main_logger.info(f"auth user: {self.request.user.username}")
        return reverse_lazy('main')

    def form_invalid(self, form):
        main_logger.debug(f'Invalid data in LoginForm, errors: {form.errors}')
        return super().form_invalid(form)



class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'agency/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            c_def = {"title": "Create Employee"}
        else:
            c_def = {"title": "Register"}
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        if self.request.user.is_superuser:
            employee_group = Group.objects.get(name='Employee')
            user.groups.add(employee_group)
            user.save()
            messages.add_message(self.request, messages.SUCCESS, f"You success create employee: {user.username}")
            main_logger.info(f"Register employee: {user.username}")
        else:
            login(self.request, user)
            main_logger.info(f"Register user: {self.request.user.username}")
        return redirect('main')

    def form_invalid(self, form):
        main_logger.debug(f'Invalid data in RegisterForm, errors: {form.errors}')
        return super().form_invalid(form)

def logout_user(request):
    main_logger.debug(f"logout user: {request.user.username}")
    logout(request)
    return redirect('main')



def owner_realties(request):
    if not request.user.is_authenticated:
        return redirect('main')
    realtys = Realty.objects.select_related('address').select_related('address').filter(owner=request.user)
    owner_buying_realties = realtys.filter(is_sold=True)
    owner_not_buying_realties = realtys.filter(is_sold=False)
    category = Category.objects.all()
    context = {
        'owner_buying_realties': owner_buying_realties,
        'owner_not_buying_realties' : owner_not_buying_realties,
        'cats': category,
    }
    if request.user not in get_all_employees():
        buying_realties = Realty.objects.filter(landlord=request.user, is_sold=True)
        must_pay_realties = Realty.objects.filter(landlord=request.user, is_sold=False)
        context['buying_realties'] =  buying_realties
        context['must_pay_realties'] = must_pay_realties

    context.update(csrf(request))
    return TemplateResponse(request, 'agency/owner_realty.html', context)

def query(request):

    querys_to = Query.objects.filter(owner=request.user)
    category = Category.objects.all()
    context = {
        'querys_to' : querys_to,
        'cats': category
    }
    if request.user not in get_all_employees():
        querys_from = Query.objects.filter(landlord=request.user)
        context['querys_from'] = querys_from
    return TemplateResponse(request, 'agency/query.html', context)


def create_query(request, realty_slug):
    if request.user.is_authenticated:
        try:
            realty = Realty.objects.get(slug=realty_slug)
        except Realty.DoesNotExist as ex:
            main_logger.error(f"Don't find realty(realty slug: {realty_slug})")
            main_logger.error(f"Type error {type(ex)})")
            messages.add_message(request, messages.ERROR, f"Don't find realty(realty slug: {realty_slug})")
            return redirect('main')
        try:
            query = Query.objects.create(owner=realty.owner, landlord=request.user, realty=realty)
            main_logger.info(f"Create new query, Owner: {query.owner.username}, landlord: {query.landlord.username}, Realty: {realty.name}")
        except Exception as ex:
            main_logger.error(f"Can't create query with realty: {realty}, landlord: {request.user}")
            messages.add_message(request, messages.ERROR, "You Can't create query, try again..")
            return redirect('main')
        return redirect("query")
    else:
        return redirect('login')

def accept_query(request, query_id):
    query = Query.objects.get(id=query_id)
    realty = query.realty

    main_logger.info(f"Accept query, Owner: {query.owner.username}, landlord: {query.landlord.username}, Realty: {realty.name}")

    landlord_email = query.landlord.email
    owner_email = query.landlord.email

    info_realty = f"Info about realty:\nRealty name: {query.realty.name}\nRealty description: {query.realty.description}\nRealty price: {query.realty.price}\n"
    message_to_landlord = "You query to buy accepted\n"
    message_to_landlord += info_realty
    message_to_landlord+="Info about owner:\n"
    message_to_landlord+=f"Owner name: {query.owner.username}"
    message_to_landlord+=f"Owner phone number: {query.owner.phone_number}"
    message_to_landlord+=f"Owner gmail: {owner_email}"
    message_to_owner = "You accepted query to buy\n"
    message_to_owner += info_realty
    message_to_owner += "Info about landlord:\n"
    message_to_owner += f"Landlord name: {query.landlord.username}"
    message_to_owner += f"Landlord phone number: {query.landlord.phone_number}"
    message_to_owner += f"Landlord gmail: {landlord_email}"
    try:
        send_mail(
            "Accept query to buy",
            message_to_landlord,
            "store13313@gmail.com",
            [landlord_email],
            fail_silently=False,
        )
    except Exception as ex:
        main_logger.error(f"Don't send message to email: {landlord_email}")
    try:
        send_mail(
            "Accept query to buy",
            message_to_owner,
            "store13313@gmail.com",
            [owner_email],
            fail_silently=False,
        )
    except Exception as ex:
        main_logger.error(f"Don't send message to email: {owner_email}")


    if request.user not in get_all_employees():
        discount = -1
        promocode = request.GET.get('promocode')
        try:
            promo = PromoCode.objects.get(code=promocode)
            discount = promo.discount
            request.session['discount'] = discount
            messages.add_message(request, messages.SUCCESS, f"We find this promocode, you have discount {discount}")
        except PromoCode.DoesNotExist:
            if promocode is not None:
                messages.add_message(request, messages.SUCCESS, f"We don't find promocode {promocode}")
                main_logger.error(f"Don't find promocode with code {promocode}")
            if 'discount' in request.session:
                request.session.pop('discount')

        context = {
            'realty': realty,
            'landlord': query.landlord
        }
        if discount != -1:
            context['discount'] = discount
        return TemplateResponse(request, 'agency/pay_accept_query.html', context)
    else:
        realty.landlord = query.landlord
        realty.save()
        main_logger.info(f"Employee: {realty.owner} accept query of landlord {query.landlord}")
        Query.objects.filter(realty=realty).delete()
        return redirect("query")



def success(request, realty_slug, landlord_id):
    try:
        realty = Realty.objects.get(slug=realty_slug)
    except Realty.DoesNotExist as ex:
        main_logger.error(f"Don't find realty(realty slug: {realty_slug})")
        messages.add_message(request, messages.ERROR, f"Don't find realty(realty slug: {realty_slug})")
        return redirect('main')
    try:
        landlord = User.objects.get(id=landlord_id)
    except User.DoesNotExist as ex:
        main_logger.error(f"Don't find user with id: {realty_slug})")
        messages.add_message(request, messages.ERROR, f"Don't find you id, try again")
        return redirect('main')
    querys = Query.objects.filter(realty=realty)
    realty.landlord = landlord
    realty.is_sold = True
    realty.save()
    if realty.owner not in get_all_employees():
        price = realty.price //100
        main_logger.info(
            f"Buy accept query, Owner: {realty.owner.username}, landlord: {realty.landlord.username}, Realty: {realty.name}")
        landlord_email = realty.landlord.email
        owner_email = realty.owner.email
        info_realty = f"Info about realty:\nRealty name: {realty.name}\nRealty description: {realty.description}\nRealty price: {realty.price}\n"


        message_to_owner = "You bought accept to query to buy\n"
        message_to_owner += info_realty
        message_to_owner += "Info about landlord:\n"
        message_to_owner += f"Landlord name: {realty.landlord.username}\n"
        message_to_owner += f"Landlord phone number: {realty.landlord.phone_number}\n"
        message_to_owner += f"Landlord gmail: {landlord_email}\n"
        try:
            send_mail(
                "Accept query to buy",
                message_to_owner,
                "store13313@gmail.com",
                [owner_email],
                fail_silently=False,
            )
        except Exception as ex:
            main_logger.error(f"Don't send message to email: {owner_email}")

        all_emails = []
        message_refusal = "You query to arent realty rejected\n"
        message_refusal += info_realty
        for q in querys:
            if q.landlord != landlord:
                all_emails.append(q.landlord.email)


            try:
                query = Query.objects.get(id=q.id).delete()
            except Query.DoesNotExist as ex:
                main_logger.error(f"Don't find query with id: {q.id})")
                messages.add_message(request, messages.ERROR, f"Some errors, try again")
                return redirect('main')
        if all_emails:
            try:
                send_mail(
                    "Reject query to arent",
                    message_refusal,
                    "store13313@gmail.com",
                    all_emails,
                    fail_silently=False,
                )
            except Exception as ex:
                main_logger.error(f"Don't send message to emails: {all_emails}")

    else:
        landlord_email = landlord.email
        owner_email = settings.EMAIL_HOST_USER
        message_to_landlord = "You query to arent accepted\n"
        info_realty = f"Info about realty:\nRealty name: {realty.name}\nRealty description: {realty.description}\nRealty price: {realty.price}\n"
        message_to_landlord += info_realty
        message_to_landlord += "Owner: agency realty\n"
        message_to_landlord += "To get access to you realty, go to our agency, address: Minsk, Filimonova 12A"
        message_to_agency = "Person buy realty\n"
        message_to_agency += info_realty
        message_to_agency += "Info about landlord:\n"
        message_to_agency += f"Landlord name: {landlord.username}\n"
        message_to_agency += f"Landlord phone number: {landlord.phone_number}\n"
        message_to_agency += f"Landlord gmail: {landlord_email}\n"
        message_to_agency += f"Landlord gmail: {landlord_email}\n"
        try:
            send_mail(
                "Buy realty",
                message_to_landlord,
                "store13313@gmail.com",
                [landlord_email],
                fail_silently=False,
            )
        except Exception as ex:
            main_logger.error(f"Don't send message to emails: {landlord_email}")

        try:
            send_mail(
                "Buy realty",
                message_to_agency,
                "store13313@gmail.com",
                [owner_email],
                fail_silently=False,
            )
        except Exception as ex:

            main_logger.error(f"Don't send message to emails: {landlord_email}")
        price = realty.price
        messages.success(request, "Success: You buy realty. Check you gmail")

    discount = request.session.get('discount', None)
    if discount:
        request.session.pop('discount')
        price = int(price * (1 - discount / 100))
    Transaction.objects.create(realty=realty, price=price)
    realty.rented_at = django.utils.timezone.now()
    realty.save()
    return redirect('main')



class AddRealtyView(CreateView):
    template_name = 'agency/add_realty.html'

    def get_form_class(self):
        if self.request.user.is_superuser:
            return AdminAddRealtyForm
        else:
            return AddRealtyForm


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = {"title": "Realty"}
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        name = form.cleaned_data['name']
        description= form.cleaned_data['description']
        price= form.cleaned_data['price']
        category= form.cleaned_data['category']
        photo = form.cleaned_data['photo']
        city  = form.cleaned_data['city']
        state = form.cleaned_data['state']
        address = form.cleaned_data['address']
        main_logger.info(f"Create new realty, name: {name}")
        if self.request.user.is_superuser:
            employee_username = form.cleaned_data['employee']
            owner = User.objects.get(username=employee_username)
        else:
            owner = self.request.user
        try:
            addres = Address.objects.filter(city=city, state=state, address=address)
            if addres:
                new_address = addres[0]
            else:
                new_address = Address.objects.create(city=city, state=state, address=address)
            if Realty.objects.filter(slug=slugify(name)):
                form.add_error(None, "The name must be unique")
                return self.form_invalid(form)
            Realty.objects.create(name=name, description=description, price=price, cat=category, owner=owner,
                                  photo=photo, address=new_address, slug=slugify(name))
        except:
            messages.add_message(self.request, messages.ERROR, "Some error")
            main_logger.critical(f"Can't create realty with slug {realty}")
            return self.form_invalid(form)
        return redirect('main')

    def form_invalid(self, form):
        main_logger.debug(f"Invalid data in form of create realty, errors {form.errors}")
        return super().form_invalid(form)


class UpdateRealtyView(UpdateView):
    template_name = 'agency/add_realty.html'
    model = Realty
    extra_context = {
        'title': 'Редактирование недвижимости',
    }
    def get_form_class(self):
        if self.request.user.is_superuser:
            return AdminUpdateRealtyForm
        else:
            return UpdateRealtyForm

    def form_valid(self, form):
        name = form.cleaned_data['name']
        description = form.cleaned_data['description']
        price = form.cleaned_data['price']
        category = form.cleaned_data['category']
        photo = form.cleaned_data['photo']
        city = form.cleaned_data['city']
        state = form.cleaned_data['state']
        address = form.cleaned_data['address']
        if self.request.user.is_superuser:
            employee_username = form.cleaned_data['employee']
            owner = User.objects.get(username=employee_username)
        else:
            owner = self.request.user
        try:
            addres = Address.objects.filter(city=city, state=state, address=address)
            if addres:
                new_address = addres[0]
            else:
                new_address = Address.objects.create(city=city, state=state, address=address)
            same_name_realties = Realty.objects.filter(name=name)
            if  same_name_realties and same_name_realties[0] != self.object:
                form.add_error(None, "The name must be unique")
                return self.form_invalid(form)

            self.object.name = name
            self.object.description = description
            self.object.price = price
            self.object.cat = category
            self.object.owner = owner
            self.object.photo = photo
            self.object.address = new_address
            self.object.discount = False
            self.object.price_discount = price
            self.object.slug = slugify(name)
            self.object.save()

        except Exception as ex:
            form.add_error(None, "Some error...")
            main_logger.error(f"Can't update realty, type ex: {type(ex)} {ex.args}")
            return self.form_invalid(form)
        return HttpResponseRedirect(self.object.get_absolute_url())

    def form_invalid(self, form):
        main_logger.debug(f"Invalid data in form of update realty, errors {form.errors}")
        return super().form_invalid(form)
    def get_success_url(self):
        return self.object.get_absolute_url()


def delete_realty(request, realty_slug):
    try:
        realty = Realty.objects.get(slug=realty_slug)
    except Realty.DoesNotExist as ex:
        main_logger.error(f"Don't find realty(realty slug: {realty_slug})")
        messages.add_message(request, messages.ERROR, f"Don't find realty(realty slug: {realty_slug})")
        return redirect('main')

    main_logger.info(f"Delete realty, Owner: {realty.owner.username}, name: {realty.name}")
    realty.delete()
    if request.user.is_superuser:
        return redirect('all_realties')
    else:
        return redirect('owner_realties')

def delete_query(request, query_id):

    try:
        query = Query.objects.get(id=query_id)
    except Query.DoesNotExist as ex:
        main_logger.error(f"Don't find query with id  {query_id})")
        messages.add_message(request, messages.ERROR, f"Don't find quer with id {query_id})")
        return redirect('main')
    main_logger.info(f"Delete query, Owner: {query.owner.username}, name: {query.realty.name}")
    query.delete()
    return redirect('query')





def admin_info(request):
    if request.user.is_superuser:
        all_transactions = Transaction.objects.select_related('realty').select_related('realty__cat').select_related('realty__owner').select_related('realty__landlord').all().order_by('realty__name')

        realties_prices = {}
        prices = []
        for transaction in all_transactions:
            realties_prices[transaction.realty] = transaction.price
            prices.append(transaction.price)
        all_category = Category.objects.all()
        if prices:
            average = statistics.mean(prices)
            mode = statistics.mode(prices)
            mediana = statistics.median(prices)
        else:
            average = 0
            mode = 0
            mediana = 0
        employee_group = Group.objects.get(name='Employee')
        dates = [relativedelta(datetime.date.today(), user.date).years for user in User.objects.prefetch_related('groups').filter(is_superuser=False) if employee_group not in user.groups.all() ]
        if dates:
            average_date = statistics.mean(dates)
            mediana_date = statistics.median(dates)
        else:
            average_date = 0
            mediana_date = 0

        categories ={}
        categories_price = {}
        for category in all_category:
            categories[category.name] = 0
            categories_price[category.name] = 0

        for rented_realty, user_paid in realties_prices.items():
            categories[rented_realty.cat.name]+=1
            categories_price[rented_realty.cat.name] += user_paid
        most_popular_category = max(categories, key=categories.get)
        most_beneficial_category = max(categories_price, key=categories.get)


        end_date = django.utils.timezone.now()
        start_date = end_date+ datetime.timedelta(days=-30)
        dates = []
        category_hist = []

        for transaction in all_transactions:
            date = transaction.realty.rented_at
            if date and date <= end_date and date >= start_date:
                dates.append(date)
            category_hist.append(transaction.realty.cat.name)
        category_hist.sort()
        dates.sort()
        dates = [date.strftime("%d-%m") for date in dates]



        plt.clf()
        plt.hist(dates, bins=31)
        plt.xlabel('Dates')
        plt.ylabel('Count of Rented Realty')
        plt.title(f'Count of Rented Realty from {start_date.strftime("%B %d, %y")}, to {end_date.strftime("%B %d, %y")}')
        if not os.path.isdir(settings.MEDIA_ROOT+'/graphics'):
            os.makedirs(settings.MEDIA_ROOT+'/graphics')

        plt.savefig(settings.MEDIA_ROOT+'/graphics/seil_realties_by_dates.png')
        plt.clf()
        plt.hist(category_hist, bins=len(categories))
        plt.xlabel('Category')
        plt.ylabel('Count of Rented Realty')
        plt.title(
            f'Count of Rented Realty by category')
        plt.savefig(settings.MEDIA_ROOT + '/graphics/seil_realties_by_cat.png')

        context = {
            'realties_prices': realties_prices,
            'prices': prices,
            'average':average,
            'mode':mode,
            'mediana': mediana,
            'average_date': average_date,
            'mediana_date': mediana_date,
            'all_category': all_category,
            'categories':categories,
            'categories_price':categories_price,
            'most_popular_category':most_popular_category,
            'most_beneficial_category':most_beneficial_category,
            'graphic1': settings.MEDIA_URL+'graphics/seil_realties_by_dates.png',
            'graphic2': settings.MEDIA_URL+'graphics/seil_realties_by_cat.png',
        }
        return TemplateResponse(request, 'agency/owner/admin_info.html', context)
    else:
        return redirect('main')




def profile_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist as ex:
        main_logger.error(f"Don't find user with id {user_id})")
        messages.add_message(request, messages.ERROR, f"Somer errors, try again")
        return redirect('main')
    realtys = Realty.objects.select_related('address').filter(owner=user)
    context={
        'user': user,
        'realtys':realtys
    }
    return TemplateResponse(request, 'agency/profile_user.html', context)

class UpdateUserView(UpdateView):
    template_name = 'agency/update_user.html'
    model = User
    extra_context = {
        'title': 'Редактирование персональный данных',
    }
    def get_form_class(self):
        return UpdateUserForm


    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.object.get_absolute_url())

    def form_invalid(self, form):
        main_logger.debug(f"Invalid data in Update user form, errors {form.errors}")
        return super().form_invalid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()

def buy_realty(request, realty_slug):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        realty = Realty.objects.get(slug=realty_slug)
    except User.DoesNotExist as ex:
        main_logger.error(f"Don't find realty with slug {realty_slug})")
        messages.add_message(request, messages.ERROR, f"Don't find realty with slug {realty_slug})")
        return redirect('main')
    landlord = request.user
    discount = -1
    promocode = request.GET.get('promocode')
    try:
        promo = PromoCode.objects.get(code=promocode)
        discount= promo.discount
        request.session['discount'] = discount
        messages.add_message(request, messages.SUCCESS, f"We find this promocode, you have discount {discount}")
    except PromoCode.DoesNotExist:
        if promocode is not None:
            messages.add_message(request, messages.SUCCESS, f"We don't find promocode {promocode}")
            main_logger.error(f"Don't find promocode with code {promocode}")
        if 'discount' in request.session:
            request.session.pop('discount')


    context = {
        'realty': realty,
        'landlord': landlord,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
    }
    if discount != -1:
        context['discount'] = discount
    context.update(csrf(request))
    return TemplateResponse(request, 'agency/buy_realty.html', context)



stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        realty_slug= self.kwargs["realty_slug"]
        landlord_id = self.kwargs["landlord_id"]
        realty = Realty.objects.get(slug=realty_slug)
        discount = self.request.session.get('discount', None)
        if realty.owner not in get_all_employees():
            price = realty.price #convert dollars to cent, and /100
        else:
            price = realty.price * 100
        if discount:
            price = int(price * (1-discount/100))
        YOUR_DOMAIN = "http://localhost:8000"
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': price,
                            'product_data': {
                                'name': realty.name,
                            },
                        },
                        'quantity': 1,
                    },
                ],
                metadata={
                    "product_id": realty.id
                },
                mode='payment',
                success_url=YOUR_DOMAIN + reverse('success', kwargs={'realty_slug': realty.slug, 'landlord_id': landlord_id}),
                cancel_url=YOUR_DOMAIN + '/cancel/',
            )
            return redirect(checkout_session.url, code=303)
        except Exception as ex:
            main_logger.critical(f"Can't create checkout session with price: {price}")
            messages.add_message(request, messages.ERROR, "Can't create checkout session")
            return redirect('main')





def cancel(request):
    messages.debug(request, "You cancel stripe view..")
    return redirect('main')

def all_realties(request):
    if request.user.is_superuser:

        employees = get_all_employees()
        realties = Realty.objects.select_related('address').all()
        realties = filter_sort_realties(request, realties)
        sold_realties = realties.filter(is_sold=True)
        not_sold_realties = realties.filter(is_sold=False)
        context = {
            'sold_realties': sold_realties,
            'not_sold_realties': not_sold_realties,
            'employees' : employees,
        }
        return TemplateResponse(request, 'agency/owner/all_realties.html', context=context)
    else:
        return redirect('main')

def view_all_employees(request):
    if request.user.is_superuser:
        all_employees = get_all_employees()
        all_realties = Realty.objects.select_related('address').select_related('owner').select_related('landlord').all()
        employee_realties = { employee : [] for employee in all_employees}
        for realty in all_realties:
            if realty.owner in all_employees:
                employee_realties[realty.owner].append(realty)
        context = {
            'all_employees' : all_employees,
            'employee_realties' : employee_realties
        }
        return TemplateResponse(request, 'agency/owner/all_employees.html', context=context)
    else:
        return redirect('main')

def delete_employee(request, user_id):
    if request.user.is_superuser:
        try:
            user = User.objects.get(id=user_id).delete()
        except User.DoesNotExist:
            main_logger.error(f"Don't find user with id {user_id}")
            messages.add_message(request, messages.SUCCESS, f"You don't find you..")
            return redirect('main')
        except django.db.models.deletion.ProtectedError:
            messages.add_message(request, messages.ERROR, f"First of all delete all realties, before deleted Employee")
        else:
            if user in get_all_employees():
                messages.add_message(request, messages.SUCCESS, f"You success delete employee")
            else:
                messages.add_message(request, messages.SUCCESS, f"You success delete client")
    return redirect('main')

def view_all_clients(request):
    if request.user.is_superuser:
        all_clients = get_all_clients()
        all_realties = Realty.objects.select_related('address').select_related('owner').select_related('landlord').all()
        client_realties = {client: {'buying_realty': [], 'exposed_realty': []} for client in all_clients}
        for realty in all_realties:
            if realty.owner in all_clients:
                client_realties[realty.owner]['exposed_realty'].append(realty)

            if realty.landlord in all_clients and realty.is_sold:
                client_realties[realty.landlord]['buying_realty'].append(realty)
        context = {
            'all_clients': all_clients,
            'client_realties': client_realties
        }
        return TemplateResponse(request, 'agency/owner/all_clients.html', context=context)
    else:
        return redirect('main')


def employee_clients(request, employee_id):

    if request.user in get_all_employees():
        try:
            selected_employee = User.objects.get(id=employee_id)
        except User.DoesNotExist:
            main_logger.error(f"Don't find employee with id {employee_id}")
            messages.add_message(request, messages.SUCCESS, f"You don't find you..")
            return redirect('main')
        all_clients = get_all_clients()
        all_realties = Realty.objects.select_related('address').select_related('owner').select_related('landlord').all()
        client_realties = {client: {'buying_realty': [], 'send_query_realty': []} for client in all_clients}
        for realty in all_realties:
            if realty.owner == selected_employee:
                query_by_realty = Query.objects.select_related('realty').select_related('landlord').filter(realty=realty)
                for query in query_by_realty:
                    client_realties[query.landlord]['send_query_realty'].append(realty)
                if realty.landlord in all_clients and realty.is_sold:
                    client_realties[realty.landlord]['buying_realty'].append(realty)
        client_realties = {client: client_realties[client] for client in all_clients if client_realties[client]['buying_realty'] or client_realties[client]['send_query_realty']}
        context = {
            'all_clients': all_clients,
            'client_realties': client_realties
        }
        return TemplateResponse(request, 'agency/employee_clients.html', context=context)
    else:
        return redirect('main')


def view_info_company(request):
    info = InformationCompany.objects.first()
    privacy = PrivacyPolicy.objects.first()
    context = {
        'info': info,
        'privacy': privacy
    }
    return TemplateResponse(request, 'agency/InfoCompany.html', context=context)

def view_news(request):
    all_article = Article.objects.select_related('publisher').all()
    context = {
        'all_article': all_article,
    }
    return TemplateResponse(request, 'agency/articlies.html', context=context)


def view_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    context = {
        'article': article,
    }
    return TemplateResponse(request, 'agency/article.html', context=context)


def view_FAQ(request):
    all_questions = Question.objects.all().order_by('-created_at')
    context = {
        'all_questions': all_questions,
    }
    return TemplateResponse(request, 'agency/FAQ.html', context=context)

def view_vacancies(request):
    all_vacancies = Vacancy.objects.all().order_by('-created_at')
    context = {
        'all_vacancies': all_vacancies,
    }
    return TemplateResponse(request, 'agency/vacancies.html', context=context)










