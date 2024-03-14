from django import template
from anotas.models import Category

register = template.Library()

@register.inclusion_tag('anotas/categories.html')
def get_category_list():
    return {'categories': Category.objects.all()}