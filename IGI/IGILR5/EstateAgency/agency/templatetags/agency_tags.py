from django import template

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
