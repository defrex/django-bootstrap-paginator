
import urllib
from django import template

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
    adjacent_pages = 2

    page = context.get('page_obj', page)
    paginator = page.paginator

    startPage = page.number - adjacent_pages
    if startPage <= adjacent_pages + 1:
        startPage = 1
    endPage = page.number + adjacent_pages + 1

    page_numbers = [
        n for n in range(startPage, endPage)
        if n >= 1 and n <= paginator.num_pages
    ]

    return {
        'page': page,
        'paginator': paginator,
        'page_numbers': page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': paginator.num_pages not in page_numbers,
        'request': context['request'],
    }


@register.simple_tag(takes_context=True)
def append_to_get(context, **kwargs):
    get = context['request'].GET.copy()
    get.update(kwargs)
    return '?{1}'.format(urllib.urlencode(get))
