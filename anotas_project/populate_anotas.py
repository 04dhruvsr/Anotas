import os
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE','anotas_project.settings')

import django
django.setup()
from anotas.models import Category, Page
def populate():
    users = ["michel", "alvaro", "juan",]
    users = create_users()
    for user in users:
        pass
        


def populate():
    python_pages = [
        {'title': 'Official Python Tutorial',
        'url':'http://docs.python.org/3/tutorial/'},
        {'title':'How to Think like a Computer Scientist',
        'url':'http://www.greenteapress.com/thinkpython/'},
        {'title':'Learn Python in 10 Minutes',
        'url':'http://www.korokithakis.net/tutorials/python/'} ]

    django_pages = [
        {'title':'Official Django Tutorial',
        'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/'},
        {'title':'Django Rocks',
        'url':'http://www.djangorocks.com/'},
        {'title':'How to Tango with Django',
        'url':'http://www.tangowithdjango.com/'} ]

    other_pages = [
        {'title':'Bottle',
        'url':'http://bottlepy.org/docs/dev/'},
        {'title':'Flask',
        'url':'http://flask.pocoo.org'} ]

    cats = {'Python': {'pages': python_pages, 'views': 128, 'likes': 64,},
            'Django': {'pages': django_pages, 'views': 64, 'likes': 32,},
            'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16,} }


    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data)
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'],views=view_number)
            view_number += 10

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, name_data):
    c = Category.objects.get_or_create(name=name, views=name_data['views'], likes=name_data['likes'])[0]
    c.save()
    return c

if __name__ == '__main__':
    print('Starting Anotas population script...')
    populate()