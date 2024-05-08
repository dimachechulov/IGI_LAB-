from django import template
from django.contrib.auth.models import Group

from ..models import User
from ..utils import get_all_employees

register = template.Library()

@register.simple_tag(name='get_category_in_list')
def get_category_in_list(categories, category):
    return categories[category.name]


@register.simple_tag(name='is_agency_realty')
def is_agency_realty(realty):
    return realty.owner in get_all_employees()


@register.simple_tag(name='is_employee')
def is_employee(user):
    return user in get_all_employees()

@register.simple_tag(name='get_price_discount')
def get_price_discount(price, discount):
    return price * (1- discount / 100)
