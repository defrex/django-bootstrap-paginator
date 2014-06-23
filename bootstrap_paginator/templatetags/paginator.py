
from django.utils.six.moves.urllib.parse import urlencode
from django import template
from django.conf import settings

try:
    from django_jinja import library
    lib = library.Library()

except ImportError:
    class LibraryStub(object):
        @staticmethod
        def global_function(func):
            return func
    lib = LibraryStub()


PAGINATOR_ADJACENT_PAGES = getattr(settings, 'PAGINATOR_ADJACENT_PAGES', 2)

register = template.Library()

@register.inclusion_tag('bootstrap_paginator/paginator.html', takes_context=True)
def paginator(context, page=None):
    """
    Based on: http://djangosnippets.org/snippets/2680/

    To be used in conjunction with the object_list generic view.

    Adds pagination context variables for use in displaying first, adjacent and
    last page links in addition to those created by the object_list generic
    view.
    """
    page = context.get('page_obj', page)
    paginator = page.paginator

    start_page = page.number - PAGINATOR_ADJACENT_PAGES
    if start_page <= PAGINATOR_ADJACENT_PAGES + 1:
        start_page = 1
    end_page = page.number + PAGINATOR_ADJACENT_PAGES + 1

    page_numbers = [
        n for n in range(start_page, end_page)
        if n >= 1 and n <= paginator.num_pages
    ]

    return {
        'page': page,
        'paginator': paginator,
        'page_numbers': page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': paginator.num_pages not in page_numbers,
        'request': context.get('request'),
    }


@register.simple_tag(takes_context=True)
def append_to_get(context, **kwargs):
    if 'request' in context:
        get = context['request'].GET.copy()
    else:
        get = {}
    get.update(kwargs)
    return '?{}'.format(urlencode(get))


@lib.global_function
def urlencode_plus(values, **plus):
    values = values.copy()
    values.update(plus)
    return '?{}'.format(urlencode(values))
