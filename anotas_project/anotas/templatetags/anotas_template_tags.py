from django import template
from anotas.models import Subject

register = template.Library()

@register.inclusion_tag('anotas/subjects.html')
def get_category_list():
    return {'categories': Subject.objects.all()}